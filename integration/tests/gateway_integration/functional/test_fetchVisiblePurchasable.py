import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities, RequestBuilder, PurchaseUtil

"""
    See fetchProducts, and fetchProductList tests for the visible = true, purchasable = true test case
"""

@pytest.allure.feature('functional')
@pytest.allure.story('visible field')
class TestFetchVisiblePurchasable(object):

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

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_fail_when_vis_is_false_and_purch_is_true_vc(self, config):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_VISIBLE_FALSE_PURCHASABLE_TRUE_VC.CODE],
            config.store.wgid,
            config.data.TEST_VISIBLE_FALSE_PURCHASABLE_TRUE_VC.COUNTRY,
            config.data.TEST_VISIBLE_FALSE_PURCHASABLE_TRUE_VC.LANGUAGE
        )
        fetch_response.expect_failure(result_code='NO_PRODUCTS')

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_vis_is_true_and_purch_is_false_vc(self, config):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_VISIBLE_TRUE_PURCHASEABLE_FALSE_VC.CODE],
            config.store.wgid,
            config.data.TEST_VISIBLE_TRUE_PURCHASEABLE_FALSE_VC.COUNTRY,
            config.data.TEST_VISIBLE_TRUE_PURCHASEABLE_FALSE_VC.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('virtual_price'))
        assert_that(prod_response.content['price']['virtual_price'], has_length(1))
        cost = prod_response.content['price']['virtual_price'][0]

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_VISIBLE_TRUE_PURCHASEABLE_FALSE_VC.VIRTUAL_CURRENCY.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to(str(config.data.TEST_VISIBLE_TRUE_PURCHASEABLE_FALSE_VC.VIRTUAL_CURRENCY.AMOUNT))
        )

        assert_that(prod_response.content, has_key('entitlements'))
        assert_that(prod_response.content['entitlements'], has_length(1))
        entitlement = prod_response.content['entitlements'][0]

        assert_that(entitlement, has_key('code'))
        assert_that(entitlement['code'],
                    equal_to(config.data.TEST_VISIBLE_TRUE_PURCHASEABLE_FALSE_VC.ENTITLEMENTS.CODE))
        assert_that(entitlement, has_key('amount'))
        assert_that(
            entitlement['amount'],
            equal_to(config.data.TEST_VISIBLE_TRUE_PURCHASEABLE_FALSE_VC.ENTITLEMENTS.AMOUNT)
        )

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_fail_when_vis_is_false_and_purch_is_false_vc(self, config):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_VISIBLE_FALSE_PURCHASEABLE_FALSE_VC.CODE],
            config.store.wgid,
            config.data.TEST_VISIBLE_FALSE_PURCHASEABLE_FALSE_VC.COUNTRY,
            config.data.TEST_VISIBLE_FALSE_PURCHASEABLE_FALSE_VC.LANGUAGE
        )
        fetch_response.expect_failure(result_code='NO_PRODUCTS')

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_fail_when_vis_is_false_and_purch_is_true_vc(self, config):
        config.log.info('Fetch Product List should not contain the invisible product')

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_VISIBLE_FALSE_PURCHASABLE_TRUE_VC.STOREFRONT,
            config.store.wgid,
            config.data.TEST_VISIBLE_FALSE_PURCHASABLE_TRUE_VC.COUNTRY,
            config.data.TEST_VISIBLE_FALSE_PURCHASABLE_TRUE_VC.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri_list = fetch_response.content['body']['uriList']

        prod = next(
            (
                prod for prod in PurchaseUtil.get_product_infos(uri_list)
                if prod['product_code'] == config.data.TEST_VISIBLE_FALSE_PURCHASABLE_TRUE_VC.CODE
            ),
            None
        )
        assert_that(prod, none())

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_vis_is_true_and_purch_is_false_vc(self, config):
        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_VISIBLE_TRUE_PURCHASEABLE_FALSE_VC.STOREFRONT,
            config.store.wgid,
            config.data.TEST_VISIBLE_TRUE_PURCHASEABLE_FALSE_VC.COUNTRY,
            config.data.TEST_VISIBLE_TRUE_PURCHASEABLE_FALSE_VC.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri_list = fetch_response.content['body']['uriList']

        prod = next(
            (
                prod for prod in PurchaseUtil.get_product_infos(uri_list)
                if prod['product_code'] == config.data.TEST_VISIBLE_TRUE_PURCHASEABLE_FALSE_VC.CODE
            ),
            None
        )

        assert_that(prod, has_key('price'))
        assert_that(prod['price'], has_key('virtual_price'))
        assert_that(prod['price']['virtual_price'], has_length(1))
        cost = prod['price']['virtual_price'][0]

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_VISIBLE_TRUE_PURCHASEABLE_FALSE_VC.VIRTUAL_CURRENCY.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to(str(config.data.TEST_VISIBLE_TRUE_PURCHASEABLE_FALSE_VC.VIRTUAL_CURRENCY.AMOUNT))
        )

        assert_that(prod, has_key('entitlements'))
        assert_that(prod['entitlements'], has_length(1))
        entitlement = prod['entitlements'][0]

        assert_that(entitlement, has_key('code'))
        assert_that(entitlement['code'],
                    equal_to(config.data.TEST_VISIBLE_TRUE_PURCHASEABLE_FALSE_VC.ENTITLEMENTS.CODE))
        assert_that(entitlement, has_key('amount'))
        assert_that(
            entitlement['amount'],
            equal_to(config.data.TEST_VISIBLE_TRUE_PURCHASEABLE_FALSE_VC.ENTITLEMENTS.AMOUNT)
        )

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_fail_when_vis_is_false_and_purch_is_false_vc(self, config):
        config.log.info('Fetch Product List should not contain the invisible product')

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_VISIBLE_FALSE_PURCHASEABLE_FALSE_VC.STOREFRONT,
            config.store.wgid,
            config.data.TEST_VISIBLE_FALSE_PURCHASEABLE_FALSE_VC.COUNTRY,
            config.data.TEST_VISIBLE_FALSE_PURCHASEABLE_FALSE_VC.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri_list = fetch_response.content['body']['uriList']

        prod = next(
            (
                prod for prod in PurchaseUtil.get_product_infos(uri_list)
                if prod['product_code'] == config.data.TEST_VISIBLE_FALSE_PURCHASEABLE_FALSE_VC.CODE
            ),
            None
        )
        assert_that(prod, none())

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_fail_when_vis_is_false_and_purch_is_true_rm(self, config):
        config.log.info('Fetch Product List should not contain the invisible product')

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_VISIBLE_FALSE_PURCHASABLE_TRUE_RM.CODE],
            config.store.wgid,
            config.data.TEST_VISIBLE_FALSE_PURCHASABLE_TRUE_RM.COUNTRY,
            config.data.TEST_VISIBLE_FALSE_PURCHASABLE_TRUE_RM.LANGUAGE
        )
        fetch_response.expect_failure(result_code='NO_PRODUCTS')

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_vis_is_true_and_purch_is_false_rm(self, config):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_VISIBLE_TRUE_PURCHASEABLE_FALSE_RM.CODE],
            config.store.wgid,
            config.data.TEST_VISIBLE_TRUE_PURCHASEABLE_FALSE_RM.COUNTRY,
            config.data.TEST_VISIBLE_TRUE_PURCHASEABLE_FALSE_RM.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_VISIBLE_TRUE_PURCHASEABLE_FALSE_RM.REAL_MONEY.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to(config.data.TEST_VISIBLE_TRUE_PURCHASEABLE_FALSE_RM.REAL_MONEY.AMOUNT)
        )

        assert_that(prod_response.content, has_key('entitlements'))
        assert_that(prod_response.content['entitlements'], has_length(1))
        entitlement = prod_response.content['entitlements'][0]

        assert_that(entitlement, has_key('code'))
        assert_that(entitlement['code'],
                    equal_to(config.data.TEST_VISIBLE_TRUE_PURCHASEABLE_FALSE_RM.ENTITLEMENTS.CODE))
        assert_that(entitlement, has_key('amount'))
        assert_that(
            entitlement['amount'],
            equal_to(config.data.TEST_VISIBLE_TRUE_PURCHASEABLE_FALSE_RM.ENTITLEMENTS.AMOUNT)
        )

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_fail_when_vis_is_false_and_purch_is_false_rm(self, config):
        config.log.info('Fetch Product List should not contain the invisible product')

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_VISIBLE_FALSE_PURCHASEABLE_FALSE_RM.CODE],
            config.store.wgid,
            config.data.TEST_VISIBLE_FALSE_PURCHASEABLE_FALSE_RM.COUNTRY,
            config.data.TEST_VISIBLE_FALSE_PURCHASEABLE_FALSE_RM.LANGUAGE
        )
        fetch_response.expect_failure(result_code='NO_PRODUCTS')

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_fail_when_vis_is_false_and_purch_is_true_rm(self, config):
        config.log.info('Fetch Product List should not contain the invisible product')

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_VISIBLE_FALSE_PURCHASABLE_TRUE_RM.STOREFRONT,
            config.store.wgid,
            config.data.TEST_VISIBLE_FALSE_PURCHASABLE_TRUE_RM.COUNTRY,
            config.data.TEST_VISIBLE_FALSE_PURCHASABLE_TRUE_RM.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri_list = fetch_response.content['body']['uriList']

        prod = next(
            (
                prod for prod in PurchaseUtil.get_product_infos(uri_list)
                if prod['product_code'] == config.data.TEST_VISIBLE_FALSE_PURCHASABLE_TRUE_RM.CODE
            ),
            None
        )
        assert_that(prod, none())

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_vis_is_true_and_purch_is_false_rm(self, config):
        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_VISIBLE_TRUE_PURCHASEABLE_FALSE_RM.STOREFRONT,
            config.store.wgid,
            config.data.TEST_VISIBLE_TRUE_PURCHASEABLE_FALSE_RM.COUNTRY,
            config.data.TEST_VISIBLE_TRUE_PURCHASEABLE_FALSE_RM.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri_list = fetch_response.content['body']['uriList']

        prod = next(
            (
                prod for prod in PurchaseUtil.get_product_infos(uri_list)
                if prod['product_code'] == config.data.TEST_VISIBLE_TRUE_PURCHASEABLE_FALSE_RM.CODE
            ),
            None
        )

        assert_that(prod, has_key('price'))
        assert_that(prod['price'], has_key('real_price'))
        cost = prod['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_VISIBLE_TRUE_PURCHASEABLE_FALSE_RM.REAL_MONEY.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to(config.data.TEST_VISIBLE_TRUE_PURCHASEABLE_FALSE_RM.REAL_MONEY.AMOUNT)
        )

        assert_that(prod, has_key('entitlements'))
        assert_that(prod['entitlements'], has_length(1))
        entitlement = prod['entitlements'][0]

        assert_that(entitlement, has_key('code'))
        assert_that(entitlement['code'],
                    equal_to(config.data.TEST_VISIBLE_TRUE_PURCHASEABLE_FALSE_RM.ENTITLEMENTS.CODE))
        assert_that(entitlement, has_key('amount'))
        assert_that(
            entitlement['amount'],
            equal_to(config.data.TEST_VISIBLE_TRUE_PURCHASEABLE_FALSE_RM.ENTITLEMENTS.AMOUNT)
        )

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_fail_when_vis_is_false_and_purch_is_false_rm(self, config):
        config.log.info('Fetch Product List should not contain the invisible product')

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_VISIBLE_FALSE_PURCHASEABLE_FALSE_RM.STOREFRONT,
            config.store.wgid,
            config.data.TEST_VISIBLE_FALSE_PURCHASEABLE_FALSE_RM.COUNTRY,
            config.data.TEST_VISIBLE_FALSE_PURCHASEABLE_FALSE_RM.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri_list = fetch_response.content['body']['uriList']

        prod = next(
            (
                prod for prod in PurchaseUtil.get_product_infos(uri_list)
                if prod['product_code'] == config.data.TEST_VISIBLE_FALSE_PURCHASEABLE_FALSE_RM.CODE
            ),
            None
        )
        assert_that(prod, none())

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_fail_when_store_has_no_visible_products(self, config):
        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_VISIBLE_FALSE_PURCHASABLE_TRUE_VC.NOT_VISIBLE_STORE,
            config.store.wgid,
            config.data.TEST_VISIBLE_FALSE_PURCHASABLE_TRUE_VC.COUNTRY,
            config.data.TEST_VISIBLE_FALSE_PURCHASABLE_TRUE_VC.LANGUAGE
        )
        fetch_response.expect_failure(result_code='NO_PRODUCTS')
