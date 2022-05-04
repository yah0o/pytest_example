import uuid

import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities, PurchaseUtil
from integration.main.request import RequestBuilder
from integration.main.services import CurrencyItem, LegacyProductItem, PurchaseProductItem


@pytest.allure.feature('functional')
@pytest.allure.story('grant product uses cache')
class TestPurchaseAccountCountryCache(object):
    """
    Our services have a cache that is used to map a wgid to a country associated with that account.
    The country associated with the account is specified when creating the account in SPA via Tools.

    The user's country is cached whenever any of the following calls are made in GAPI and a valid wgid(>0) is specified:
        /fetchProducts
        /fetchProductList
        /fetchProductsCrossTitle
        /grantProduct
        /purchaseProductWithMoney
        Auth's /loginWithEmail

    Furthermore /grant and /purchase will still attempt to contact SPA if the user country cached is 'ZZ' or 'UNDEFINED'

    Tests below ensure that the cache is working properly for /purchase and /grant.
    """

    @pytest.fixture(autouse=True)
    def setup(self, config):
        ###
        # Test setup
        # account from US
        config.store.us_account = AccountUtilities.create_account(attrs='user_stated_country=US')

        account_created = config.spa.http.create_account(config.store.us_account.__dict__)
        account_created.assert_is_success()
        update_account = config.spa.http.update(account_created.content['id'],
                                                game=config.environment['test_title_pgn'])
        update_account.assert_is_success()

        config.store.us_profile_id = account_created.content['id']
        config.store.us_wgid = account_created.content['id']

        # account from ZZ
        config.store.zz_account = AccountUtilities.create_account(
            attrs='user_stated_country={}'.format(config.data.TEST_COUNTRY_CACHE.UNKNOWN_COUNTRY))

        account_created = config.spa.http.create_account(config.store.zz_account.__dict__)
        account_created.assert_is_success()
        update_account = config.spa.http.update(account_created.content['id'],
                                                game=config.environment['test_title_pgn'])
        update_account.assert_is_success()

        config.store.zz_profile_id = account_created.content['id']
        config.store.zz_wgid = account_created.content['id']

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        us_delete_response = config.spa.http.delete_account(config.store.us_wgid)
        us_delete_response.assert_is_success()

        zz_delete_response = config.spa.http.delete_account(config.store.zz_wgid)
        zz_delete_response.assert_is_success()

    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.xfail(reason='Not available in wgie and above', raises=AssertionError)
    def test_grant_product_cache_works(self, config):
        """
        A user's country gets cached as part of a /grantProduct call.
        If that cached country is unknown ('ZZ' or 'UNDEFINED'), then the cache will be skipped and country will
        be pulled from SPA instead.
        However, if country is known, then that will be used in favor of what is stored in SPA.
        """
        # check that the grant request fails as expected when both api call- and account-country are unknown
        # this will also cache 'ZZ' under zz_profile_id in Redis
        zz_grant_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_COUNTRY_CACHE.UNKNOWN_COUNTRY,
            config.data.TEST_PRODUCT.LANGUAGE,
            config.store.zz_profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT.PRODUCT_CODE, config.data.TEST_PRODUCT.AMOUNT)],
        )
        zz_grant_response.expect_failure(result_code='COUNTRY_NOT_DEFINED')

        # via SPA, change ZZ-account country to US
        spa_response = config.spa.http.update_account(config.store.zz_profile_id, 'user_stated_country',
                                                      config.data.TEST_COUNTRY_CACHE.ALLOWED_COUNTRY)
        spa_response.assert_is_success()

        assert_that(config.data.TEST_COUNTRY_CACHE.ALLOWED_COUNTRY,
                    spa_response.content['attrs']['user_stated_country'])

        # because 'ZZ' is cached, the backend will query SPA directly and use 'US' for the flow -- grant will succeed.
        us_changed_grant_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_COUNTRY_CACHE.UNKNOWN_COUNTRY,
            config.data.TEST_PRODUCT.LANGUAGE,
            config.store.zz_profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT.PRODUCT_CODE, config.data.TEST_PRODUCT.AMOUNT)],
        )
        us_changed_grant_response.assert_is_success()

        # now change SPA country back to ZZ
        spa_response = config.spa.http.update_account(config.store.zz_profile_id, 'user_stated_country', 'ZZ')
        spa_response.assert_is_success()

        assert_that('ZZ', equal_to(spa_response.content['attrs']['user_stated_country']))

        # because 'US' is still cached and is a known country, the backend will not query SPA
        # hence 'ZZ' will not be used and grant will still succeed.
        zz_changed_grant_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_COUNTRY_CACHE.UNKNOWN_COUNTRY,
            config.data.TEST_PRODUCT.LANGUAGE,
            config.store.zz_profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT.PRODUCT_CODE, config.data.TEST_PRODUCT.AMOUNT)],
        )
        zz_changed_grant_response.assert_is_success()

    @pytest.allure.severity(severity_level.NORMAL)
    def test_purchase_product_cache_works(self, config):
        """
        A user's country gets cached as part of a /purchaseProductWithMoney call.
        If that cached country is unknown ('ZZ' or 'UNDEFINED'), then the cache will be skipped and country will be
        pulled from SPA instead.
        However, if cached country is known, then that will be used in favor of what is stored in SPA.
        """
        # fetch product id
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_MONEY.PRODUCT_CODE],
            config.store.us_profile_id,
            config.data.TEST_MONEY.COUNTRY,
            config.data.TEST_COUNTRY_CACHE.UNKNOWN_COUNTRY
        )
        fetch_response.assert_is_success()

        uri = fetch_response.content['body']['uriList'][0]
        product_response = RequestBuilder(uri).get()
        product_data = product_response.content
        product_id = product_data["product_id"]
        assert_that(product_id, not_none())

        cost = product_data['price']['real_price']

        # check that the purchase request fails as expected when both api call- and account-country are unknown
        # this will also cache 'ZZ' under zz_profile_id in Redis

        zz_purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_COUNTRY_CACHE.UNKNOWN_COUNTRY,
            config.data.TEST_MONEY.LANGUAGE,
            config.store.zz_profile_id,
            config.store.zz_account.email,
            config.store.zz_profile_id,
            [PurchaseProductItem(product_id, 1, [])],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_MONEY.STOREFRONT,
            client_payment_method_id=product_response.content['client_payment_methods'][0]
        )
        zz_purchase_response.expect_failure(result_code='COUNTRY_NOT_DEFINED')

        # via SPA, change ZZ-account country to US
        spa_response = config.spa.http.update_account(config.store.zz_profile_id, 'user_stated_country',
                                                      config.data.TEST_COUNTRY_CACHE.ALLOWED_COUNTRY)
        spa_response.assert_is_success()

        assert_that(config.data.TEST_COUNTRY_CACHE.ALLOWED_COUNTRY,
                    spa_response.content['attrs']['user_stated_country'])

        # because 'ZZ' is cached, the backend will query SPA directly and use 'US' for the flow -- grant will succeed.
        us_changed_purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            'ZZ',
            config.data.TEST_MONEY.LANGUAGE,
            config.store.zz_profile_id,
            config.store.zz_account.email,
            config.store.zz_profile_id,
            [PurchaseProductItem(product_id, 1, [])],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_MONEY.STOREFRONT,
            client_payment_method_id=product_response.content['client_payment_methods'][0]
        )
        us_changed_purchase_response.assert_is_success()

        # now change SPA country back to ZZ
        spa_response = config.spa.http.update_account(config.store.zz_profile_id, 'user_stated_country',
                                                      config.data.TEST_COUNTRY_CACHE.UNKNOWN_COUNTRY)
        spa_response.assert_is_success()

        assert_that(config.data.TEST_COUNTRY_CACHE.UNKNOWN_COUNTRY,
                    equal_to(spa_response.content['attrs']['user_stated_country']))

        # Old behavior: because 'US' is still cached and is a known country, the backend will not query SPA
        # hence 'ZZ' will not be used and grant will still succeed.
        # New behavior: https://jira.wargaming.net/browse/FREYA-999 'US' is not cached and 'ZZ' pass to req
        zz_changed_purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_COUNTRY_CACHE.UNKNOWN_COUNTRY,
            config.data.TEST_MONEY.LANGUAGE,
            config.store.zz_profile_id,
            config.store.zz_account.email,
            config.store.zz_profile_id,
            [PurchaseProductItem(product_id, 1, [])],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_MONEY.STOREFRONT,
            client_payment_method_id=product_response.content['client_payment_methods'][0]
        )
        zz_changed_purchase_response.expect_failure(result_code='COUNTRY_NOT_DEFINED')
