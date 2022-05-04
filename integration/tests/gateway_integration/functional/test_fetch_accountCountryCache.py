import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities


@pytest.allure.feature('functional')
@pytest.allure.story('fetch products uses cache')
class TestFetchAccountCountryCache(object):
    """
    Our services have a cache that is used to map a wgid to a country associated with that account.
    The country associated with the account is specified when creating the account in SPA via Tools.

    The user's country is cached whenever any of the following calls are made in GAPI and a valid wgid (>0) is specified:
        /fetchProducts
        /fetchProductList
        /fetchProductsCrossTitle
        /grantProduct
        /purchaseProductWithMoney
        Auth's /loginWithEmail

    Tests below ensure that the cache is working properly for /fetchProducts and /fetchProductList.
    """

    ALLOWED_COUNTRY = 'FR'

    @pytest.fixture(autouse=True)
    def setup(self, config):
        ###
        # Test setup
        config.store.us_account = AccountUtilities.create_account(attrs='user_stated_country=US')

        account_created = config.spa.http.create_account(config.store.us_account.__dict__)
        account_created.assert_is_success()
        update_account = config.spa.http.update(account_created.content['id'],
                                                game=config.environment['test_title_pgn'])
        update_account.assert_is_success()

        config.store.us_profile_id = account_created.content['id']
        us_wgid = account_created.content['id']

        # account from FR
        config.store.fr_account = AccountUtilities.create_account(
            attrs='user_stated_country={}'.format(TestFetchAccountCountryCache.ALLOWED_COUNTRY))

        account_created = config.spa.http.create_account(config.store.fr_account.__dict__)
        account_created.assert_is_success()
        update_account = config.spa.http.update(account_created.content['id'],
                                                game=config.environment['test_title_pgn'])
        update_account.assert_is_success()

        config.store.fr_profile_id = account_created.content['id']
        fr_wgid = account_created.content['id']

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        us_delete_response = config.spa.http.delete_account(us_wgid)
        us_delete_response.assert_is_success()

        fr_delete_response = config.spa.http.delete_account(fr_wgid)
        fr_delete_response.assert_is_success()

    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.xfail(reason='Not available in wgie and above', raises=AssertionError)
    def test_fetch_products_cache_works(self, config):
        """
        Use case: once a user's country gets cached as part of a /fetchProducts call, the backend will use that cached country for subsequent calls as well.
        This means that changing the user's country via SPA after the first call will not affect outcome of subsequent calls.
        """

        # benchmark -- attempt to fetch using the FR profile -- product will be visible
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT_COUNTRY_RESTRICTED.PRODUCT_CODE],
            config.store.fr_profile_id,
            TestFetchAccountCountryCache.ALLOWED_COUNTRY,
            config.data.TEST_PRODUCT_COUNTRY_RESTRICTED.LANGUAGE
        )
        fetch_response.assert_is_success()

        # attempt to fetch using the US profile -- product will not be visible
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT_COUNTRY_RESTRICTED.PRODUCT_CODE],
            config.store.us_profile_id,
            TestFetchAccountCountryCache.ALLOWED_COUNTRY,
            config.data.TEST_PRODUCT_COUNTRY_RESTRICTED.LANGUAGE
        )
        fetch_response.expect_failure(result_code='NO_PRODUCTS')

        # via SPA, change US user's country to FR
        spa_response = config.spa.http.update_account(config.store.us_profile_id, 'user_stated_country',
                                                      TestFetchAccountCountryCache.ALLOWED_COUNTRY)
        spa_response.assert_is_success()

        # ensure that SPA has required country on record now
        assert_that(TestFetchAccountCountryCache.ALLOWED_COUNTRY, spa_response.content['attrs']['user_stated_country'])

        # product is restricted in US
        # SPA knows that the US account is now in FR, but the local cache thinks they're still in US
        # so making the call on behalf of the US account will still fail
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT_COUNTRY_RESTRICTED.PRODUCT_CODE],
            config.store.us_profile_id,
            TestFetchAccountCountryCache.ALLOWED_COUNTRY,
            config.data.TEST_PRODUCT_COUNTRY_RESTRICTED.LANGUAGE
        )
        fetch_response.expect_failure(result_code='NO_PRODUCTS')

    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.xfail(reason='Not available in wgie and above', raises=AssertionError)
    def test_fetch_product_list_cache_works(self, config):
        """
        Use case: once a user's country gets cached as part of a /fetchProductList call, the backend will use that cached country for subsequent calls as well.
        This means that changing the user's country via SPA after the first call will not affect outcome of subsequent calls.
        """

        # benchmark -- attempt to fetch list using the FR profile -- all products will be visible
        fr_product_list_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_STORE_COUNTRY_RESTRICTED.STOREFRONT,
            config.store.fr_profile_id,
            TestFetchAccountCountryCache.ALLOWED_COUNTRY,
            config.data.TEST_STORE_COUNTRY_RESTRICTED.LANGUAGE
        )
        fr_product_list_response.assert_is_success()
        assert_that(fr_product_list_response.content['body']['uriList'], has_length(3))

        # attempt to fetch using the US profile -- only the two products will be visible
        us_product_list_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_STORE_COUNTRY_RESTRICTED.STOREFRONT,
            config.store.us_profile_id,
            TestFetchAccountCountryCache.ALLOWED_COUNTRY,
            config.data.TEST_STORE_COUNTRY_RESTRICTED.LANGUAGE
        )
        us_product_list_response.assert_is_success()
        assert_that(us_product_list_response.content['body']['uriList'], has_length(2))

        # via SPA, change US user's country to FR
        spa_response = config.spa.http.update_account(config.store.us_profile_id, 'user_stated_country',
                                                      TestFetchAccountCountryCache.ALLOWED_COUNTRY)
        spa_response.assert_is_success()

        # ensure that SPA has required country on record now
        assert_that(TestFetchAccountCountryCache.ALLOWED_COUNTRY, spa_response.content['attrs']['user_stated_country'])

        # one of the products is restricted in US
        # SPA knows that the US account is now in FR, but the local cache thinks they're still in US
        # so making the call on behalf of the US account will still show only two products
        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_STORE_COUNTRY_RESTRICTED.STOREFRONT,
            config.store.us_profile_id,
            TestFetchAccountCountryCache.ALLOWED_COUNTRY,
            config.data.TEST_PRODUCT_COUNTRY_RESTRICTED.LANGUAGE
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body']['uriList'], has_length(2))
