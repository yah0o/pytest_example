import uuid

import pytest
from allure import severity_level
from hamcrest import *
from integration.main.helpers import AccountUtilities, InventoryUtilities, PurchaseUtil, RequestBuilder, ReturnValue, \
    WaitOn
from integration.main.services import CurrencyItem, LegacyProductItem


@pytest.allure.feature('functional')
@pytest.allure.story('future promo activation')
class TestFuturePromoActivation(object):

    @pytest.fixture(autouse=True)
    def setup(self, config):
        ###
        # Test setup

        config.store.account = AccountUtilities.create_account(attrs='user_stated_country=ZZ')

        account_created = config.spa.http.create_account(config.store.account.__dict__)
        account_created.assert_is_success()
        update_account = config.spa.http.update(account_created.content['id'],
                                                game=config.environment['test_title_pgn'])
        update_account.assert_is_success()

        config.store.wgid = account_created.content['id']

        ###
        # Runs test
        yield

        ###
        # Test cleanup
        delete_response = config.spa.http.delete_account(config.store.wgid)
        delete_response.assert_is_success()

    @pytest.mark.skip_for_regions('trie')
    # ORDO error
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_promo_is_not_yet_activated(self, config):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_FUTURE_ACTIVATED_PROMO.CODE],
            config.store.wgid,
            config.data.TEST_FUTURE_ACTIVATED_PROMO.COUNTRY,
            config.data.TEST_FUTURE_ACTIVATED_PROMO.LANGUAGE,
            storefront=config.data.TEST_FUTURE_ACTIVATED_PROMO.STOREFRONT
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        url = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(url).get()
        product_response.assert_is_success()

        product_info = product_response.content

        assert_that(product_info, has_key('product_code'))
        assert_that(product_info['product_code'], equal_to(config.data.TEST_FUTURE_ACTIVATED_PROMO.CODE))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_promo_is_not_yet_activated(self, config):
        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_FUTURE_ACTIVATED_PROMO.STOREFRONT,
            config.store.wgid,
            config.data.TEST_FUTURE_ACTIVATED_PROMO.COUNTRY,
            config.data.TEST_FUTURE_ACTIVATED_PROMO.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri_list = fetch_response.content['body']['uriList']

        product = next(
            (
                product for product in PurchaseUtil.get_product_infos(uri_list)
                if product['product_code'] == config.data.TEST_FUTURE_ACTIVATED_PROMO.CODE
            ),
            None
        )
        assert_that(product, not_none())

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_should_succeed_when_promo_is_not_yet_activated(self, config):
        config.log.info('Grant {} {} to purchase {}'.format(
            config.data.TEST_FUTURE_ACTIVATED_PROMO.VIRTUAL_CURRENCY.AMOUNT,
            config.data.TEST_FUTURE_ACTIVATED_PROMO.VIRTUAL_CURRENCY.CODE,
            config.data.TEST_FUTURE_ACTIVATED_PROMO.CODE
        ))

        grant_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.wgid,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                config.data.TEST_FUTURE_ACTIVATED_PROMO.VIRTUAL_CURRENCY.AMOUNT
            )]
        )
        grant_response.assert_is_success()

        config.log.info('Purchase {}'.format(config.data.TEST_FUTURE_ACTIVATED_PROMO.CODE))
        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.wgid,
            config.store.wgid,
            config.data.TEST_FUTURE_ACTIVATED_PROMO.CODE,
            config.data.TEST_FUTURE_ACTIVATED_PROMO.AMOUNT,
            [CurrencyItem(
                config.data.TEST_FUTURE_ACTIVATED_PROMO.VIRTUAL_CURRENCY.CODE,
                str(config.data.TEST_FUTURE_ACTIVATED_PROMO.VIRTUAL_CURRENCY.AMOUNT)
            )],
            storefront=config.data.TEST_FUTURE_ACTIVATED_PROMO.STOREFRONT
        )
        purchase_response.assert_is_success()

        config.log.info('Check if inventory has {} from {}'.format(
            config.data.TEST_FUTURE_ACTIVATED_PROMO.ENTITLEMENTS.CODE,
            config.data.TEST_FUTURE_ACTIVATED_PROMO.CODE
        ))
        waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.wgid,
            to_check_currencies={},
            to_check_entitlements={
                config.data.TEST_FUTURE_ACTIVATED_PROMO.ENTITLEMENTS.CODE:
                    config.data.TEST_FUTURE_ACTIVATED_PROMO.ENTITLEMENTS.AMOUNT
            }
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        waiter.wait('Did not get {} {}\n{}'.format(
            config.data.TEST_FUTURE_ACTIVATED_PROMO.ENTITLEMENTS.AMOUNT,
            config.data.TEST_FUTURE_ACTIVATED_PROMO.ENTITLEMENTS.CODE,
            config.freya.server_gateway.get_full_inventory(config.store.wgid).details
        ))
