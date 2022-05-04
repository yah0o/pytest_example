import uuid

import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities, PurchaseUtil, WaitOn, ReturnValue, InventoryUtilities
from integration.main.request import RequestBuilder
from integration.main.services import LegacyProductItem, CurrencyItem


@pytest.mark.skip_for_regions('trie')
# ORDO errors
@pytest.allure.feature('functional')
@pytest.allure.story('promotion vc purchase product')
class TestPromotionVCPurchaseProduct(object):

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

        config.store.profile_id = account_created.content['id']
        config.store.wgid = account_created.content['id']

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(config.store.wgid)
        delete_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_should_succeed_when_all_products_in_storefront_have_pct_pro_promo(self, config):
        grant_test_currency_for_prod_1_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                config.data.TEST_PROMO_PCT_PRO_VC.VIRTUAL_CURRENCY.AMOUNT
            )]
        )
        grant_test_currency_for_prod_1_response.assert_is_success()

        fetch_prod_1_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PROMO_PCT_PRO_VC.PRODUCT1.CODE],
            config.store.profile_id,
            config.data.TEST_PROMO_PCT_PRO_VC.COUNTRY,
            config.data.TEST_PROMO_PCT_PRO_VC.LANGUAGE,
            config.data.TEST_PROMO_PCT_PRO_VC.STOREFRONT
        )
        fetch_prod_1_response.assert_is_success()
        assert_that(fetch_prod_1_response.content['body']['uriList'], has_length(1))
        prod_1_uri = fetch_prod_1_response.content['body']['uriList'][0]

        prod_1_response = RequestBuilder(prod_1_uri).get()
        prod_1_response.assert_is_success()

        assert_that(prod_1_response.content, has_key('price'))
        assert_that(prod_1_response.content['price'], has_key('virtual_price'))
        assert_that(prod_1_response.content['price']['virtual_price'], has_length(1))

        prod_1_price = prod_1_response.content['price']['virtual_price'][0]
        assert_that(
            prod_1_price['code'],
            equal_to(config.data.TEST_PROMO_PCT_PRO_VC.VIRTUAL_CURRENCY.CODE)
        )
        assert_that(
            prod_1_price['amount'],
            equal_to(str(config.data.TEST_PROMO_PCT_PRO_VC.VIRTUAL_CURRENCY.AMOUNT))
        )

        purchase_prod_1_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PROMO_PCT_PRO_VC.PRODUCT1.CODE,
            config.data.TEST_PROMO_PCT_PRO_VC.AMOUNT,
            [
                CurrencyItem(
                    prod_1_price['code'],
                    int(prod_1_price['amount'])
                )
            ],
            storefront=config.data.TEST_PROMO_PCT_PRO_VC.STOREFRONT
        )
        purchase_prod_1_response.assert_is_success()

        prod_1_currency_waiter = WaitOn(lambda: InventoryUtilities.inventory_empty(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            check_currencies=True,
            check_entitlements=False
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_1_currency_waiter.wait('Currencies was not empty\n{}'.format(
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        prod_1_entitlement_waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={},
            to_check_entitlements={
                config.data.TEST_PROMO_PCT_PRO_VC.PRODUCT1.ENTITLEMENT: config.data.TEST_PROMO_PCT_PRO_VC.AMOUNT
            }
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)

        prod_1_entitlement_waiter.wait('Did not get {} {}\n{}'.format(
            config.data.TEST_PROMO_PCT_PRO_VC.PRODUCT1.ENTITLEMENT,
            config.data.TEST_PROMO_PCT_PRO_VC.AMOUNT,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        grant_test_currency_for_prod_2_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                config.data.TEST_PROMO_PCT_PRO_VC.VIRTUAL_CURRENCY.AMOUNT
            )]
        )
        grant_test_currency_for_prod_2_response.assert_is_success()

        fetch_prod_2_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PROMO_PCT_PRO_VC.PRODUCT2.CODE],
            config.store.profile_id,
            config.data.TEST_PROMO_PCT_PRO_VC.COUNTRY,
            config.data.TEST_PROMO_PCT_PRO_VC.LANGUAGE,
            config.data.TEST_PROMO_PCT_PRO_VC.STOREFRONT
        )
        fetch_prod_2_response.assert_is_success()
        assert_that(fetch_prod_2_response.content['body']['uriList'], has_length(1))
        prod_2_uri = fetch_prod_2_response.content['body']['uriList'][0]

        prod_2_response = RequestBuilder(prod_2_uri).get()
        prod_2_response.assert_is_success()

        assert_that(prod_2_response.content, has_key('price'))
        assert_that(prod_2_response.content['price'], has_key('virtual_price'))
        assert_that(prod_2_response.content['price'], has_length(1))
        product_2_price = prod_2_response.content['price']['virtual_price'][0]

        assert_that(product_2_price['code'], equal_to(config.data.TEST_PROMO_PCT_PRO_VC.VIRTUAL_CURRENCY.CODE))
        assert_that(
            product_2_price['amount'],
            equal_to(str(config.data.TEST_PROMO_PCT_PRO_VC.VIRTUAL_CURRENCY.AMOUNT))
        )

        purchase_prod_2_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PROMO_PCT_PRO_VC.PRODUCT2.CODE,
            config.data.TEST_PROMO_PCT_PRO_VC.AMOUNT,
            [
                CurrencyItem(
                    product_2_price['code'],
                    int(product_2_price['amount'])
                )
            ],
            storefront=config.data.TEST_PROMO_PCT_PRO_VC.STOREFRONT
        )
        purchase_prod_2_response.assert_is_success()

        prod_2_currency_waiter = WaitOn(lambda: InventoryUtilities.inventory_empty(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            check_currencies=True,
            check_entitlements=False
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_2_currency_waiter.wait('Currencies was not empty\n{}'.format(
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        prod_2_entitlement_waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={},
            to_check_entitlements={
                config.data.TEST_PROMO_PCT_PRO_VC.PRODUCT2.ENTITLEMENT: config.data.TEST_PROMO_PCT_PRO_VC.AMOUNT
            }
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)

        prod_2_entitlement_waiter.wait('Did not get {} {}\n{}'.format(
            config.data.TEST_PROMO_PCT_PRO_VC.PRODUCT2.ENTITLEMENT,
            config.data.TEST_PROMO_PCT_PRO_VC.AMOUNT,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_should_succeed_when_all_products_in_storefront_have_fixed_promo(self, config):
        grant_test_currency_for_prod_1_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                config.data.TEST_PROMO_FIXED_VC.VIRTUAL_CURRENCY.AMOUNT
            )]
        )
        grant_test_currency_for_prod_1_response.assert_is_success()

        fetch_prod_1_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PROMO_FIXED_VC.PRODUCT1.CODE],
            config.store.profile_id,
            config.data.TEST_PROMO_FIXED_VC.COUNTRY,
            config.data.TEST_PROMO_FIXED_VC.LANGUAGE,
            storefront=config.data.TEST_PROMO_FIXED_VC.STOREFRONT
        )
        fetch_prod_1_response.assert_is_success()
        assert_that(fetch_prod_1_response.content['body']['uriList'], has_length(1))
        prod_1_uri = fetch_prod_1_response.content['body']['uriList'][0]

        prod_1_response = RequestBuilder(prod_1_uri).get()
        prod_1_response.assert_is_success()
        assert_that(prod_1_response.content, has_key('price'))
        assert_that(prod_1_response.content['price'], has_key('virtual_price'))

        assert_that(prod_1_response.content['price']['virtual_price'], has_length(1))
        prod_1_test_currency_price = prod_1_response.content['price']['virtual_price'][0]
        assert_that(
            prod_1_test_currency_price['amount'],
            equal_to(str(config.data.TEST_PROMO_FIXED_VC.VIRTUAL_CURRENCY.AMOUNT))
        )

        purchase_prod_1_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PROMO_FIXED_VC.PRODUCT1.CODE,
            config.data.TEST_PROMO_FIXED_VC.AMOUNT,
            [
                CurrencyItem(
                    prod_1_test_currency_price['code'],
                    int(prod_1_test_currency_price['amount'])
                )
            ],
            storefront=config.data.TEST_PROMO_FIXED_VC.STOREFRONT
        )
        purchase_prod_1_response.assert_is_success()

        prod_1_currency_waiter = WaitOn(lambda: InventoryUtilities.inventory_empty(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            check_currencies=True,
            check_entitlements=False
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_1_currency_waiter.wait('Currencies was not empty\n{}'.format(
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        prod_1_entitlement_waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={},
            to_check_entitlements={
                config.data.TEST_PROMO_FIXED_VC.PRODUCT1.ENTITLEMENT: config.data.TEST_PROMO_FIXED_VC.AMOUNT
            }
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)

        prod_1_entitlement_waiter.wait('Did not get {} {}\n{}'.format(
            config.data.TEST_PROMO_FIXED_VC.PRODUCT1.ENTITLEMENT,
            config.data.TEST_PROMO_FIXED_VC.AMOUNT,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        grant_test_currency_for_prod_2_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                config.data.TEST_PROMO_FIXED_VC.VIRTUAL_CURRENCY.AMOUNT
            )]
        )
        grant_test_currency_for_prod_2_response.assert_is_success()

        fetch_prod_2_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PROMO_FIXED_VC.PRODUCT2.CODE],
            config.store.profile_id,
            config.data.TEST_PROMO_FIXED_VC.COUNTRY,
            config.data.TEST_PROMO_FIXED_VC.LANGUAGE,
            storefront=config.data.TEST_PROMO_FIXED_VC.STOREFRONT
        )
        fetch_prod_2_response.assert_is_success()
        assert_that(fetch_prod_2_response.content['body']['uriList'], has_length(1))
        prod_2_uri = fetch_prod_2_response.content['body']['uriList'][0]

        prod_2_response = RequestBuilder(prod_2_uri).get()
        prod_2_response.assert_is_success()
        assert_that(prod_2_response.content, has_key('price'))
        assert_that(prod_2_response.content['price'], has_key('virtual_price'))
        assert_that(prod_2_response.content['price']['virtual_price'], has_length(1))

        prod_2_price = prod_2_response.content['price']['virtual_price'][0]
        assert_that(prod_2_price['amount'], equal_to(str(config.data.TEST_PROMO_FIXED_VC.VIRTUAL_CURRENCY.AMOUNT)))

        purchase_prod_2_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PROMO_FIXED_VC.PRODUCT2.CODE,
            config.data.TEST_PROMO_FIXED_VC.AMOUNT,
            [
                CurrencyItem(
                    prod_2_price['code'],
                    int(prod_2_price['amount'])
                )
            ],
            storefront=config.data.TEST_PROMO_FIXED_VC.STOREFRONT
        )
        purchase_prod_2_response.assert_is_success()

        prod_2_currency_waiter = WaitOn(lambda: InventoryUtilities.inventory_empty(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            check_currencies=True,
            check_entitlements=False
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_2_currency_waiter.wait('Currencies was not empty\n{}'.format(
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        prod_2_entitlement_waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={},
            to_check_entitlements={
                config.data.TEST_PROMO_FIXED_VC.PRODUCT2.ENTITLEMENT: config.data.TEST_PROMO_FIXED_VC.AMOUNT
            }
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)

        prod_2_entitlement_waiter.wait('Did not get {} {}\n{}'.format(
            config.data.TEST_PROMO_FIXED_VC.PRODUCT2.ENTITLEMENT,
            config.data.TEST_PROMO_FIXED_VC.AMOUNT,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

    @pytest.mark.skip(reason='WGPTCOM-1311')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_should_succeed_when_all_products_in_storefront_have_abs_promo(self, config):
        grant_test_currency_for_prod_1_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                config.data.TEST_PROMO_ABS_VC.VIRTUAL_CURRENCY.AMOUNT
            )]
        )
        grant_test_currency_for_prod_1_response.assert_is_success()

        fetch_prod_1_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PROMO_ABS_VC.PRODUCT1.CODE],
            config.store.profile_id,
            config.data.TEST_PROMO_ABS_VC.COUNTRY,
            config.data.TEST_PROMO_ABS_VC.LANGUAGE,
            storefront=config.data.TEST_PROMO_ABS_VC.STOREFRONT
        )
        fetch_prod_1_response.assert_is_success()
        assert_that(fetch_prod_1_response.content['body']['uriList'], has_length(1))
        prod_1_uri = fetch_prod_1_response.content['body']['uriList'][0]

        prod_1_response = RequestBuilder(prod_1_uri).get()
        prod_1_response.assert_is_success()
        assert_that(prod_1_response.content, has_key('price'))
        assert_that(prod_1_response.content['price'], has_key('virtual_price'))

        assert_that(prod_1_response.content['price']['virtual_price'], has_length(1))
        prod_1_test_currency_price = prod_1_response.content['price']['virtual_price'][0]
        assert_that(
            prod_1_test_currency_price['amount'],
            equal_to(str(config.data.TEST_PROMO_ABS_VC.VIRTUAL_CURRENCY.AMOUNT))
        )

        purchase_prod_1_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PROMO_ABS_VC.PRODUCT1.CODE,
            config.data.TEST_PROMO_ABS_VC.AMOUNT,
            [
                CurrencyItem(
                    prod_1_test_currency_price['code'],
                    int(prod_1_test_currency_price['amount'])
                )
            ],
            storefront=config.data.TEST_PROMO_ABS_VC.STOREFRONT
        )
        purchase_prod_1_response.assert_is_success()

        prod_1_currency_waiter = WaitOn(lambda: InventoryUtilities.inventory_empty(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            check_currencies=True,
            check_entitlements=False
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_1_currency_waiter.wait('Currencies was not empty\n{}'.format(
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        prod_1_entitlement_waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={},
            to_check_entitlements={
                config.data.TEST_PROMO_ABS_VC.PRODUCT1.ENTITLEMENT: config.data.TEST_PROMO_ABS_VC.AMOUNT
            }
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_1_entitlement_waiter.wait('Did not get {} {}\n{}'.format(
            config.data.TEST_PROMO_ABS_VC.PRODUCT1.ENTITLEMENT,
            config.data.TEST_PROMO_ABS_VC.AMOUNT,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        grant_test_currency_for_prod_2_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                config.data.TEST_PROMO_ABS_VC.VIRTUAL_CURRENCY.AMOUNT
            )]
        )
        grant_test_currency_for_prod_2_response.assert_is_success()

        fetch_prod_2_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PROMO_ABS_VC.PRODUCT2.CODE],
            config.store.profile_id,
            config.data.TEST_PROMO_ABS_VC.COUNTRY,
            config.data.TEST_PROMO_ABS_VC.LANGUAGE,
            storefront=config.data.TEST_PROMO_ABS_VC.STOREFRONT
        )
        fetch_prod_2_response.assert_is_success()
        assert_that(fetch_prod_2_response.content['body']['uriList'], has_length(1))
        prod_2_uri = fetch_prod_2_response.content['body']['uriList'][0]

        prod_2_response = RequestBuilder(prod_2_uri).get()
        prod_2_response.assert_is_success()
        assert_that(prod_2_response.content, has_key('price'))
        assert_that(prod_2_response.content['price'], has_key('virtual_price'))
        assert_that(prod_2_response.content['price']['virtual_price'], has_length(1))

        prod_2_price = prod_2_response.content['price']['virtual_price'][0]
        assert_that(prod_2_price['amount'], equal_to(str(config.data.TEST_PROMO_ABS_VC.VIRTUAL_CURRENCY.AMOUNT)))

        purchase_prod_2_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PROMO_ABS_VC.PRODUCT2.CODE,
            config.data.TEST_PROMO_ABS_VC.AMOUNT,
            [
                CurrencyItem(
                    prod_2_price['code'],
                    int(prod_2_price['amount'])
                )
            ],
            storefront=config.data.TEST_PROMO_ABS_VC.STOREFRONT
        )
        purchase_prod_2_response.assert_is_success()

        prod_2_currency_waiter = WaitOn(lambda: InventoryUtilities.inventory_empty(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            check_currencies=True,
            check_entitlements=False
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_2_currency_waiter.wait('Currencies was not empty\n{}'.format(
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        prod_2_entitlement_waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={},
            to_check_entitlements={
                config.data.TEST_PROMO_ABS_VC.PRODUCT2.ENTITLEMENT: config.data.TEST_PROMO_ABS_VC.AMOUNT
            }
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_2_entitlement_waiter.wait('Did not get {} {}\n{}'.format(
            config.data.TEST_PROMO_ABS_VC.PRODUCT2.ENTITLEMENT,
            config.data.TEST_PROMO_ABS_VC.AMOUNT,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_should_succeed_when_one_product_in_storefront_have_pct_pro_promo(self, config):
        grant_test_currency_for_prod_1_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                config.data.TEST_SINGLE_PROD_PROMO_PCT_PRO_VC.PRODUCT1.VIRTUAL_CURRENCY.AMOUNT
            )]
        )
        grant_test_currency_for_prod_1_response.assert_is_success()

        fetch_prod_1_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_SINGLE_PROD_PROMO_PCT_PRO_VC.PRODUCT1.CODE],
            config.store.profile_id,
            config.data.TEST_SINGLE_PROD_PROMO_PCT_PRO_VC.COUNTRY,
            config.data.TEST_SINGLE_PROD_PROMO_PCT_PRO_VC.LANGUAGE,
            storefront=config.data.TEST_SINGLE_PROD_PROMO_PCT_PRO_VC.STOREFRONT
        )
        fetch_prod_1_response.assert_is_success()
        assert_that(fetch_prod_1_response.content['body']['uriList'], has_length(1))
        prod_1_uri = fetch_prod_1_response.content['body']['uriList'][0]

        prod_1_response = RequestBuilder(prod_1_uri).get()
        prod_1_response.assert_is_success()
        assert_that(prod_1_response.content, has_key('price'))
        assert_that(prod_1_response.content['price'], has_key('virtual_price'))
        assert_that(prod_1_response.content['price']['virtual_price'], has_length(1))

        prod_1_price = prod_1_response.content['price']['virtual_price'][0]
        assert_that(
            prod_1_price['code'],
            equal_to(config.data.TEST_SINGLE_PROD_PROMO_PCT_PRO_VC.PRODUCT1.VIRTUAL_CURRENCY.CODE)
        )
        assert_that(
            prod_1_price['amount'],
            equal_to(str(config.data.TEST_SINGLE_PROD_PROMO_PCT_PRO_VC.PRODUCT1.VIRTUAL_CURRENCY.AMOUNT))
        )

        purchase_prod_1_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_SINGLE_PROD_PROMO_PCT_PRO_VC.PRODUCT1.CODE,
            config.data.TEST_SINGLE_PROD_PROMO_PCT_PRO_VC.AMOUNT,
            [
                CurrencyItem(
                    prod_1_price['code'],
                    int(prod_1_price['amount'])
                )
            ],
            storefront=config.data.TEST_SINGLE_PROD_PROMO_PCT_PRO_VC.STOREFRONT
        )
        purchase_prod_1_response.assert_is_success()

        prod_1_currency_waiter = WaitOn(lambda: InventoryUtilities.inventory_empty(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            check_currencies=True,
            check_entitlements=False
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_1_currency_waiter.wait('Currencies was not empty\n{}'.format(
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        prod_1_inventory_waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={},
            to_check_entitlements={
                config.data.TEST_SINGLE_PROD_PROMO_PCT_PRO_VC.PRODUCT1.ENTITLEMENT:
                    config.data.TEST_SINGLE_PROD_PROMO_PCT_PRO_VC.AMOUNT
            }
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_1_inventory_waiter.wait('Did not get {} {}\n{}'.format(
            config.data.TEST_SINGLE_PROD_PROMO_PCT_PRO_VC.PRODUCT1.ENTITLEMENT,
            config.data.TEST_SINGLE_PROD_PROMO_PCT_PRO_VC.AMOUNT,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        grant_test_currency_for_prod_2_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                config.data.TEST_SINGLE_PROD_PROMO_PCT_PRO_VC.PRODUCT2.VIRTUAL_CURRENCY.AMOUNT
            )]
        )
        grant_test_currency_for_prod_2_response.assert_is_success()

        fetch_prod_2_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_SINGLE_PROD_PROMO_PCT_PRO_VC.PRODUCT2.CODE],
            config.store.profile_id,
            config.data.TEST_SINGLE_PROD_PROMO_PCT_PRO_VC.COUNTRY,
            config.data.TEST_SINGLE_PROD_PROMO_PCT_PRO_VC.LANGUAGE,
            storefront=config.data.TEST_SINGLE_PROD_PROMO_PCT_PRO_VC.STOREFRONT
        )
        fetch_prod_2_response.assert_is_success()
        assert_that(fetch_prod_2_response.content['body']['uriList'], has_length(1))
        prod_2_uri = fetch_prod_2_response.content['body']['uriList'][0]

        prod_2_response = RequestBuilder(prod_2_uri).get()
        prod_2_response.assert_is_success()
        assert_that(prod_2_response.content, has_key('price'))
        assert_that(prod_2_response.content['price'], has_key('virtual_price'))
        assert_that(prod_2_response.content['price']['virtual_price'], has_length(1))

        prod_2_price = prod_2_response.content['price']['virtual_price'][0]
        assert_that(
            prod_2_price['code'],
            equal_to(config.data.TEST_SINGLE_PROD_PROMO_PCT_PRO_VC.PRODUCT2.VIRTUAL_CURRENCY.CODE)
        )
        assert_that(
            prod_2_price['amount'],
            equal_to(str(config.data.TEST_SINGLE_PROD_PROMO_PCT_PRO_VC.PRODUCT2.VIRTUAL_CURRENCY.AMOUNT))
        )

        purchase_prod_2_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_SINGLE_PROD_PROMO_PCT_PRO_VC.PRODUCT2.CODE,
            config.data.TEST_SINGLE_PROD_PROMO_PCT_PRO_VC.AMOUNT,
            [
                CurrencyItem(
                    prod_2_price['code'],
                    int(prod_2_price['amount'])
                )
            ],
            storefront=config.data.TEST_SINGLE_PROD_PROMO_PCT_PRO_VC.STOREFRONT
        )
        purchase_prod_2_response.assert_is_success()

        prod_2_currency_waiter = WaitOn(lambda: InventoryUtilities.inventory_empty(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            check_currencies=True,
            check_entitlements=False
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_2_currency_waiter.wait('Currencies was not empty\n{}'.format(
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        prod_2_entitlement_waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={},
            to_check_entitlements={
                config.data.TEST_SINGLE_PROD_PROMO_PCT_PRO_VC.PRODUCT2.ENTITLEMENT:
                    config.data.TEST_SINGLE_PROD_PROMO_PCT_PRO_VC.AMOUNT
            }
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_2_entitlement_waiter.wait('Did not get {} {}\n{}'.format(
            config.data.TEST_SINGLE_PROD_PROMO_PCT_PRO_VC.PRODUCT2.ENTITLEMENT,
            config.data.TEST_SINGLE_PROD_PROMO_PCT_PRO_VC.AMOUNT,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_should_succeed_when_one_product_in_storefront_have_fixed_promo(self, config):
        grant_test_currency_for_prod_1_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                config.data.TEST_SINGLE_PROD_PROMO_FIXED_VC.PRODUCT1.VIRTUAL_CURRENCY.AMOUNT
            )]
        )
        grant_test_currency_for_prod_1_response.assert_is_success()

        fetch_prod_1_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_SINGLE_PROD_PROMO_FIXED_VC.PRODUCT1.CODE],
            config.store.profile_id,
            config.data.TEST_SINGLE_PROD_PROMO_FIXED_VC.COUNTRY,
            config.data.TEST_SINGLE_PROD_PROMO_FIXED_VC.LANGUAGE,
            storefront=config.data.TEST_SINGLE_PROD_PROMO_FIXED_VC.STOREFRONT
        )
        fetch_prod_1_response.assert_is_success()
        assert_that(fetch_prod_1_response.content['body']['uriList'], has_length(1))
        prod_1_uri = fetch_prod_1_response.content['body']['uriList'][0]

        prod_1_response = RequestBuilder(prod_1_uri).get()
        prod_1_response.assert_is_success()
        assert_that(prod_1_response.content, has_key('price'))
        assert_that(prod_1_response.content['price'], has_key('virtual_price'))
        assert_that(prod_1_response.content['price']['virtual_price'], has_length(1))

        prod_1_price = prod_1_response.content['price']['virtual_price'][0]
        assert_that(
            prod_1_price['code'],
            equal_to(config.data.TEST_SINGLE_PROD_PROMO_FIXED_VC.PRODUCT1.VIRTUAL_CURRENCY.CODE)
        )
        assert_that(
            prod_1_price['amount'],
            equal_to(str(config.data.TEST_SINGLE_PROD_PROMO_FIXED_VC.PRODUCT1.VIRTUAL_CURRENCY.AMOUNT))
        )

        purchase_prod_1_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_SINGLE_PROD_PROMO_FIXED_VC.PRODUCT1.CODE,
            config.data.TEST_SINGLE_PROD_PROMO_FIXED_VC.AMOUNT,
            [
                CurrencyItem(
                    prod_1_price['code'],
                    int(prod_1_price['amount'])
                )
            ],
            storefront=config.data.TEST_SINGLE_PROD_PROMO_FIXED_VC.STOREFRONT
        )
        purchase_prod_1_response.assert_is_success()

        prod_1_currency_waiter = WaitOn(lambda: InventoryUtilities.inventory_empty(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            check_currencies=True,
            check_entitlements=False
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_1_currency_waiter.wait('Currencies was not empty\n{}'.format(
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        prod_1_entitlement_waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={},
            to_check_entitlements={
                config.data.TEST_SINGLE_PROD_PROMO_FIXED_VC.PRODUCT1.ENTITLEMENT:
                    config.data.TEST_SINGLE_PROD_PROMO_FIXED_VC.AMOUNT
            }
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_1_entitlement_waiter.wait('Did not get {} {}\n{}'.format(
            config.data.TEST_SINGLE_PROD_PROMO_FIXED_VC.PRODUCT1.ENTITLEMENT,
            config.data.TEST_SINGLE_PROD_PROMO_FIXED_VC.AMOUNT,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        grant_test_currency_for_prod_2_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                config.data.TEST_SINGLE_PROD_PROMO_FIXED_VC.PRODUCT2.VIRTUAL_CURRENCY.AMOUNT
            )]
        )
        grant_test_currency_for_prod_2_response.assert_is_success()

        fetch_prod_2_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_SINGLE_PROD_PROMO_FIXED_VC.PRODUCT2.CODE],
            config.store.profile_id,
            config.data.TEST_SINGLE_PROD_PROMO_FIXED_VC.COUNTRY,
            config.data.TEST_SINGLE_PROD_PROMO_FIXED_VC.LANGUAGE,
            storefront=config.data.TEST_SINGLE_PROD_PROMO_FIXED_VC.STOREFRONT
        )
        fetch_prod_2_response.assert_is_success()
        assert_that(fetch_prod_2_response.content['body']['uriList'], has_length(1))
        prod_2_uri = fetch_prod_2_response.content['body']['uriList'][0]

        prod_2_response = RequestBuilder(prod_2_uri).get()
        prod_2_response.assert_is_success()
        assert_that(prod_2_response.content, has_key('price'))
        assert_that(prod_2_response.content['price'], has_key('virtual_price'))
        assert_that(prod_2_response.content['price']['virtual_price'], has_length(1))

        prod_2_price = prod_2_response.content['price']['virtual_price'][0]
        assert_that(
            prod_2_price['code'],
            equal_to(config.data.TEST_SINGLE_PROD_PROMO_FIXED_VC.PRODUCT2.VIRTUAL_CURRENCY.CODE)
        )
        assert_that(
            prod_2_price['amount'],
            equal_to(str(config.data.TEST_SINGLE_PROD_PROMO_FIXED_VC.PRODUCT2.VIRTUAL_CURRENCY.AMOUNT))
        )

        purchase_prod_2_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_SINGLE_PROD_PROMO_FIXED_VC.PRODUCT2.CODE,
            config.data.TEST_SINGLE_PROD_PROMO_FIXED_VC.AMOUNT,
            [
                CurrencyItem(
                    prod_2_price['code'],
                    int(prod_2_price['amount'])
                )
            ],
            storefront=config.data.TEST_SINGLE_PROD_PROMO_FIXED_VC.STOREFRONT
        )
        purchase_prod_2_response.assert_is_success()

        prod_2_currency_waiter = WaitOn(lambda: InventoryUtilities.inventory_empty(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            check_currencies=True,
            check_entitlements=False
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_2_currency_waiter.wait('Currencies was not empty\n{}'.format(
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        prod_2_entitlement_waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={},
            to_check_entitlements={
                config.data.TEST_SINGLE_PROD_PROMO_FIXED_VC.PRODUCT2.ENTITLEMENT:
                    config.data.TEST_SINGLE_PROD_PROMO_FIXED_VC.AMOUNT
            }
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_2_entitlement_waiter.wait('Did not get {} {}\n{}'.format(
            config.data.TEST_SINGLE_PROD_PROMO_FIXED_VC.PRODUCT2.ENTITLEMENT,
            config.data.TEST_SINGLE_PROD_PROMO_FIXED_VC.AMOUNT,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.xfail(reason='FREYA-917')
    def test_purchase_product_should_succeed_when_no_store_ref_in_pct_pro_promo(self, config):
        grant_test_currency_for_prod_1_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.VIRTUAL_CURRENCY.AMOUNT
            )]
        )
        grant_test_currency_for_prod_1_response.assert_is_success()

        fetch_product_list_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.STOREFRONT,
            config.store.profile_id,
            config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.COUNTRY,
            config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.LANGUAGE
        )
        fetch_product_list_response.assert_is_success()

        assert_that(fetch_product_list_response.content['body']['uriList'], has_length(3))
        uri_list = fetch_product_list_response.content['body']['uriList']

        prod_1_response = next(
            (
                prod_content for prod_content in PurchaseUtil.get_product_infos(uri_list)
                if prod_content['product_code'] == config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.PRODUCT1.CODE
            ),
            None
        )

        assert_that(prod_1_response, not_none())
        assert_that(prod_1_response, has_key('price'))
        assert_that(prod_1_response['price'], has_key('virtual_price'))
        assert_that(prod_1_response['price']['virtual_price'], has_length(1))

        prod_1_price = prod_1_response['price']['virtual_price'][0]
        assert_that(
            prod_1_price['code'],
            equal_to(config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.VIRTUAL_CURRENCY.CODE)
        )
        assert_that(
            prod_1_price['amount'],
            equal_to(str(config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.VIRTUAL_CURRENCY.AMOUNT))
        )

        purchase_prod_1_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.PRODUCT1.CODE,
            config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.AMOUNT,
            [CurrencyItem(
                prod_1_price['code'],
                int(prod_1_price['amount'])
            )],
            storefront=config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.STOREFRONT
        )
        purchase_prod_1_response.assert_is_success()

        prod_1_currency_waiter = WaitOn(lambda: InventoryUtilities.inventory_empty(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            check_currencies=True,
            check_entitlements=False
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_1_currency_waiter.wait('Currencies was not empty\n{}'.format(
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        prod_1_entitlement_waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={},
            to_check_entitlements={
                config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.PRODUCT1.ENTITLEMENT:
                    config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.AMOUNT
            }
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_1_entitlement_waiter.wait('Did not get {} {}\n{}'.format(
            config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.PRODUCT1.ENTITLEMENT,
            config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.AMOUNT,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        grant_test_currency_for_prod_2_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.VIRTUAL_CURRENCY.AMOUNT
            )]
        )
        grant_test_currency_for_prod_2_response.assert_is_success()

        prod_2_response = next(
            (
                prod_content for prod_content in PurchaseUtil.get_product_infos(uri_list)
                if prod_content['product_code'] == config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.PRODUCT2.CODE
            ),
            None
        )

        assert_that(prod_2_response, not_none())
        assert_that(prod_2_response, has_key('price'))
        assert_that(prod_2_response['price'], has_key('virtual_price'))
        assert_that(prod_2_response['price']['virtual_price'], has_length(1))

        prod_2_price = prod_2_response['price']['virtual_price'][0]
        assert_that(
            prod_2_price['code'],
            equal_to(config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.VIRTUAL_CURRENCY.CODE)
        )
        assert_that(
            prod_2_price['amount'],
            equal_to(str(config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.VIRTUAL_CURRENCY.AMOUNT))
        )

        purchase_prod_2_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.PRODUCT2.CODE,
            config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.AMOUNT,
            [CurrencyItem(
                prod_2_price['code'],
                int(prod_2_price['amount'])
            )],
            storefront=config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.STOREFRONT
        )
        purchase_prod_2_response.assert_is_success()

        prod_2_currency_waiter = WaitOn(lambda: InventoryUtilities.inventory_empty(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            check_currencies=True,
            check_entitlements=False
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_2_currency_waiter.wait('Currencies was not empty\n{}'.format(
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        prod_2_entitlement_waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={},
            to_check_entitlements={
                config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.PRODUCT2.ENTITLEMENT:
                    config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.AMOUNT
            }
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_2_entitlement_waiter.wait('Did not get {} {}\n{}'.format(
            config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.PRODUCT2.ENTITLEMENT,
            config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.AMOUNT,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        grant_test_currency_for_prod_3_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.PRODUCT3.VIRTUAL_CURRENCY.AMOUNT
            )]
        )
        grant_test_currency_for_prod_3_response.assert_is_success()

        prod_3_response = next(
            (
                prod_content for prod_content in PurchaseUtil.get_product_infos(uri_list)
                if prod_content['product_code'] == config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.PRODUCT3.CODE
            ),
            None
        )

        assert_that(prod_3_response, not_none())
        assert_that(prod_3_response, has_key('price'))
        assert_that(prod_3_response['price'], has_key('virtual_price'))
        assert_that(prod_3_response['price']['virtual_price'], has_length(1))

        prod_3_price = prod_3_response['price']['virtual_price'][0]
        assert_that(
            prod_3_price['code'],
            equal_to(config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.PRODUCT3.VIRTUAL_CURRENCY.CODE)
        )
        assert_that(
            prod_3_price['amount'],
            equal_to(str(config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.PRODUCT3.VIRTUAL_CURRENCY.AMOUNT))
        )

        purchase_prod_3_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.PRODUCT3.CODE,
            config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.AMOUNT,
            [CurrencyItem(
                prod_3_price['code'],
                int(prod_3_price['amount'])
            )],
            storefront=config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.STOREFRONT
        )
        purchase_prod_3_response.assert_is_success()
        prod_3_currency_waiter = WaitOn(lambda: InventoryUtilities.inventory_empty(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            check_currencies=True,
            check_entitlements=False
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_3_currency_waiter.wait('Currencies was not empty\n{}'.format(
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        prod_3_entitlement_waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={},
            to_check_entitlements={
                config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.PRODUCT3.ENTITLEMENT:
                    config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.AMOUNT
            }
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_3_entitlement_waiter.wait('Did not get {} {}\n{}'.format(
            config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.PRODUCT3.ENTITLEMENT,
            config.data.TEST_NO_STORE_REF_PROMO_PCT_PRO_VC.AMOUNT,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.xfail(reason='FREYA-917')
    def test_purchase_product_should_succeed_when_no_store_ref_in_fixed_promo(self, config):
        grant_test_currency_for_prod_1_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.VIRTUAL_CURRENCY.AMOUNT
            )]
        )
        grant_test_currency_for_prod_1_response.assert_is_success()

        fetch_product_list_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.STOREFRONT,
            config.store.profile_id,
            config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.COUNTRY,
            config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.LANGUAGE
        )
        fetch_product_list_response.assert_is_success()

        assert_that(fetch_product_list_response.content['body']['uriList'], has_length(3))
        uri_list = fetch_product_list_response.content['body']['uriList']

        prod_1_response = next(
            (
                prod_content for prod_content in PurchaseUtil.get_product_infos(uri_list)
                if prod_content['product_code'] == config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.PRODUCT1.CODE
            ),
            None
        )

        assert_that(prod_1_response, not_none())
        assert_that(prod_1_response, has_key('price'))
        assert_that(prod_1_response['price'], has_key('virtual_price'))
        assert_that(prod_1_response['price']['virtual_price'], has_length(1))

        prod_1_price = prod_1_response['price']['virtual_price'][0]
        assert_that(
            prod_1_price['code'],
            equal_to(config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.VIRTUAL_CURRENCY.CODE)
        )
        assert_that(
            prod_1_price['amount'],
            equal_to(str(config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.VIRTUAL_CURRENCY.AMOUNT))
        )

        purchase_prod_1_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.PRODUCT1.CODE,
            config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.AMOUNT,
            [CurrencyItem(
                prod_1_price['code'],
                int(prod_1_price['amount'])
            )],
            storefront=config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.STOREFRONT
        )
        purchase_prod_1_response.assert_is_success()

        prod_1_currency_waiter = WaitOn(lambda: InventoryUtilities.inventory_empty(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            check_currencies=True,
            check_entitlements=False
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_1_currency_waiter.wait('Currencies was not empty\n{}'.format(
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        prod_1_entitlement_waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={},
            to_check_entitlements={
                config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.PRODUCT1.ENTITLEMENT:
                    config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.AMOUNT
            }
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_1_entitlement_waiter.wait('Did not get {} {}\n{}'.format(
            config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.PRODUCT1.ENTITLEMENT,
            config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.AMOUNT,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        grant_test_currency_for_prod_2_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.VIRTUAL_CURRENCY.AMOUNT
            )]
        )
        grant_test_currency_for_prod_2_response.assert_is_success()

        prod_2_response = next(
            (
                prod_content for prod_content in PurchaseUtil.get_product_infos(uri_list)
                if prod_content['product_code'] == config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.PRODUCT2.CODE
            ),
            None
        )

        assert_that(prod_2_response, not_none())
        assert_that(prod_2_response, has_key('price'))
        assert_that(prod_2_response['price'], has_key('virtual_price'))
        assert_that(prod_2_response['price']['virtual_price'], has_length(1))

        prod_2_price = prod_2_response['price']['virtual_price'][0]
        assert_that(
            prod_2_price['code'],
            equal_to(config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.VIRTUAL_CURRENCY.CODE)
        )
        assert_that(
            prod_2_price['amount'],
            equal_to(str(config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.VIRTUAL_CURRENCY.AMOUNT))
        )

        purchase_prod_2_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.PRODUCT2.CODE,
            config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.AMOUNT,
            [CurrencyItem(
                prod_2_price['code'],
                int(prod_2_price['amount'])
            )],
            storefront=config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.STOREFRONT
        )
        purchase_prod_2_response.assert_is_success()

        prod_2_currency_waiter = WaitOn(lambda: InventoryUtilities.inventory_empty(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            check_currencies=True,
            check_entitlements=False
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_2_currency_waiter.wait('Currencies was not empty\n{}'.format(
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        prod_2_entitlement_waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={},
            to_check_entitlements={
                config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.PRODUCT2.ENTITLEMENT:
                    config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.AMOUNT
            }
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_2_entitlement_waiter.wait('Did not get {} {}\n{}'.format(
            config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.PRODUCT2.ENTITLEMENT,
            config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.AMOUNT,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        grant_test_currency_for_prod_3_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.PRODUCT3.VIRTUAL_CURRENCY.AMOUNT
            )]
        )
        grant_test_currency_for_prod_3_response.assert_is_success()

        prod_3_response = next(
            (
                prod_content for prod_content in PurchaseUtil.get_product_infos(uri_list)
                if prod_content['product_code'] == config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.PRODUCT3.CODE
            ),
            None
        )

        assert_that(prod_3_response, not_none())
        assert_that(prod_3_response, has_key('price'))
        assert_that(prod_3_response['price'], has_key('virtual_price'))
        assert_that(prod_3_response['price']['virtual_price'], has_length(1))

        prod_3_price = prod_3_response['price']['virtual_price'][0]
        assert_that(
            prod_3_price['code'],
            equal_to(config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.PRODUCT3.VIRTUAL_CURRENCY.CODE)
        )
        assert_that(
            prod_3_price['amount'],
            equal_to(str(config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.PRODUCT3.VIRTUAL_CURRENCY.AMOUNT))
        )

        purchase_prod_3_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.PRODUCT3.CODE,
            config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.AMOUNT,
            [CurrencyItem(
                prod_3_price['code'],
                int(prod_3_price['amount'])
            )],
            storefront=config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.STOREFRONT
        )
        purchase_prod_3_response.assert_is_success()

        prod_3_currency_waiter = WaitOn(lambda: InventoryUtilities.inventory_empty(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            check_currencies=True,
            check_entitlements=False
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_3_currency_waiter.wait('Currencies was not empty\n{}'.format(
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        prod_3_entitlement_waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={},
            to_check_entitlements={
                config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.PRODUCT3.ENTITLEMENT:
                    config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.AMOUNT
            }
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_3_entitlement_waiter.wait('Did not get {} {}\n{}'.format(
            config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.PRODUCT3.ENTITLEMENT,
            config.data.TEST_NO_STORE_REF_PROMO_FIXED_VC.AMOUNT,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.xfail(reason='FREYA-917')
    def test_purchase_product_should_succeed_when_no_store_ref_in_abs_promo(self, config):
        grant_test_currency_for_prod_1_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.VIRTUAL_CURRENCY.AMOUNT
            )]
        )
        grant_test_currency_for_prod_1_response.assert_is_success()

        fetch_product_list_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.STOREFRONT,
            config.store.profile_id,
            config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.COUNTRY,
            config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.LANGUAGE
        )
        fetch_product_list_response.assert_is_success()

        assert_that(fetch_product_list_response.content['body']['uriList'], has_length(3))
        uri_list = fetch_product_list_response.content['body']['uriList']

        prod_1_response = next(
            (
                prod_content for prod_content in PurchaseUtil.get_product_infos(uri_list)
                if prod_content['product_code'] == config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.PRODUCT1.CODE
            ),
            None
        )

        assert_that(prod_1_response, not_none())
        assert_that(prod_1_response, has_key('price'))
        assert_that(prod_1_response['price'], has_key('virtual_price'))
        assert_that(prod_1_response['price']['virtual_price'], has_length(1))

        prod_1_price = prod_1_response['price']['virtual_price'][0]
        assert_that(
            prod_1_price['code'],
            equal_to(config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.VIRTUAL_CURRENCY.CODE)
        )
        assert_that(
            prod_1_price['amount'],
            equal_to(str(config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.VIRTUAL_CURRENCY.AMOUNT))
        )

        purchase_prod_1_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.PRODUCT1.CODE,
            config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.AMOUNT,
            [CurrencyItem(
                prod_1_price['code'],
                int(prod_1_price['amount'])
            )],
            storefront=config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.STOREFRONT
        )
        purchase_prod_1_response.assert_is_success()

        prod_1_currency_waiter = WaitOn(lambda: InventoryUtilities.inventory_empty(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            check_currencies=True,
            check_entitlements=False
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_1_currency_waiter.wait('Currencies was not empty\n{}'.format(
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        prod_1_entitlement_waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={},
            to_check_entitlements={
                config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.PRODUCT1.ENTITLEMENT:
                    config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.AMOUNT
            }
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_1_entitlement_waiter.wait('Did not get {} {}\n{}'.format(
            config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.PRODUCT1.ENTITLEMENT,
            config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.AMOUNT,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        grant_test_currency_for_prod_2_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.VIRTUAL_CURRENCY.AMOUNT
            )]
        )
        grant_test_currency_for_prod_2_response.assert_is_success()

        prod_2_response = next(
            (
                prod_content for prod_content in PurchaseUtil.get_product_infos(uri_list)
                if prod_content['product_code'] == config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.PRODUCT2.CODE
            ),
            None
        )

        assert_that(prod_2_response, not_none())
        assert_that(prod_2_response, has_key('price'))
        assert_that(prod_2_response['price'], has_key('virtual_price'))
        assert_that(prod_2_response['price']['virtual_price'], has_length(1))

        prod_2_price = prod_2_response['price']['virtual_price'][0]
        assert_that(
            prod_2_price['code'],
            equal_to(config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.VIRTUAL_CURRENCY.CODE)
        )
        assert_that(
            prod_2_price['amount'],
            equal_to(str(config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.VIRTUAL_CURRENCY.AMOUNT))
        )

        purchase_prod_2_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.PRODUCT2.CODE,
            config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.AMOUNT,
            [CurrencyItem(
                prod_2_price['code'],
                int(prod_2_price['amount'])
            )],
            storefront=config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.STOREFRONT
        )
        purchase_prod_2_response.assert_is_success()

        prod_2_currency_waiter = WaitOn(lambda: InventoryUtilities.inventory_empty(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            check_currencies=True,
            check_entitlements=False
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_2_currency_waiter.wait('Currencies was not empty\n{}'.format(
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        prod_2_entitlement_waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={},
            to_check_entitlements={
                config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.PRODUCT2.ENTITLEMENT:
                    config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.AMOUNT
            }
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_2_entitlement_waiter.wait('Did not get {} {}\n{}'.format(
            config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.PRODUCT2.ENTITLEMENT,
            config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.AMOUNT,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        grant_test_currency_for_prod_3_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.PRODUCT3.VIRTUAL_CURRENCY.AMOUNT
            )]
        )
        grant_test_currency_for_prod_3_response.assert_is_success()

        prod_3_response = next(
            (
                prod_content for prod_content in PurchaseUtil.get_product_infos(uri_list)
                if prod_content['product_code'] == config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.PRODUCT3.CODE
            ),
            None
        )

        assert_that(prod_3_response, not_none())
        assert_that(prod_3_response, has_key('price'))
        assert_that(prod_3_response['price'], has_key('virtual_price'))
        assert_that(prod_3_response['price']['virtual_price'], has_length(1))

        prod_3_price = prod_3_response['price']['virtual_price'][0]
        assert_that(
            prod_3_price['code'],
            equal_to(config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.PRODUCT3.VIRTUAL_CURRENCY.CODE)
        )
        assert_that(
            prod_3_price['amount'],
            equal_to(str(config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.PRODUCT3.VIRTUAL_CURRENCY.AMOUNT))
        )

        purchase_prod_3_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.PRODUCT3.CODE,
            config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.AMOUNT,
            [CurrencyItem(
                prod_3_price['code'],
                int(prod_3_price['amount'])
            )],
            storefront=config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.STOREFRONT
        )
        purchase_prod_3_response.assert_is_success()
        prod_3_currency_waiter = WaitOn(lambda: InventoryUtilities.inventory_empty(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            check_currencies=True,
            check_entitlements=False
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_3_currency_waiter.wait('Currencies was not empty\n{}'.format(
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        prod_3_entitlement_waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={},
            to_check_entitlements={
                config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.PRODUCT3.ENTITLEMENT:
                    config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.AMOUNT
            }
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        prod_3_entitlement_waiter.wait('Did not get {} {}\n{}'.format(
            config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.PRODUCT3.ENTITLEMENT,
            config.data.TEST_NO_STORE_REF_PROMO_ABS_VC.AMOUNT,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_should_succeed_when_prod_in_two_stores_have_pct_pro_promo_in_one_store(self, config):
        grant_test_currency_for_store_1_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                config.data.TEST_PROD_IN_TWO_STORES_PROMO_PCT_PRO_VC.STOREFRONT1.VIRTUAL_CURRENCY.AMOUNT
            )]
        )
        grant_test_currency_for_store_1_response.assert_is_success()

        fetch_prod_from_store_1_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PROD_IN_TWO_STORES_PROMO_PCT_PRO_VC.PRODUCT],
            config.store.profile_id,
            config.data.TEST_PROD_IN_TWO_STORES_PROMO_PCT_PRO_VC.COUNTRY,
            config.data.TEST_PROD_IN_TWO_STORES_PROMO_PCT_PRO_VC.LANGUAGE,
            config.data.TEST_PROD_IN_TWO_STORES_PROMO_PCT_PRO_VC.STOREFRONT1.CODE
        )
        fetch_prod_from_store_1_response.assert_is_success()
        assert_that(fetch_prod_from_store_1_response.content['body']['uriList'], has_length(1))
        store_1_prod_uri = fetch_prod_from_store_1_response.content['body']['uriList'][0]

        store_1_prod_response = RequestBuilder(store_1_prod_uri).get()
        store_1_prod_response.assert_is_success()

        assert_that(store_1_prod_response.content, has_key('price'))
        assert_that(store_1_prod_response.content['price'], has_key('virtual_price'))
        assert_that(store_1_prod_response.content['price']['virtual_price'], has_length(1))

        store_1_prod_price = store_1_prod_response.content['price']['virtual_price'][0]
        assert_that(
            store_1_prod_price['code'],
            equal_to(config.data.TEST_PROD_IN_TWO_STORES_PROMO_PCT_PRO_VC.STOREFRONT1.VIRTUAL_CURRENCY.CODE)
        )
        assert_that(
            store_1_prod_price['amount'],
            equal_to(str(config.data.TEST_PROD_IN_TWO_STORES_PROMO_PCT_PRO_VC.STOREFRONT1.VIRTUAL_CURRENCY.AMOUNT))
        )

        purchase_store_1_prod_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PROD_IN_TWO_STORES_PROMO_PCT_PRO_VC.PRODUCT,
            config.data.TEST_PROD_IN_TWO_STORES_PROMO_PCT_PRO_VC.AMOUNT,
            [
                CurrencyItem(
                    store_1_prod_price['code'],
                    int(store_1_prod_price['amount'])
                )
            ],
            storefront=config.data.TEST_PROD_IN_TWO_STORES_PROMO_PCT_PRO_VC.STOREFRONT1.CODE
        )
        purchase_store_1_prod_response.assert_is_success()

        store_1_currency_waiter = WaitOn(lambda: InventoryUtilities.inventory_empty(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            check_currencies=True,
            check_entitlements=False
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        store_1_currency_waiter.wait('Currencies was not empty\n{}'.format(
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        store_1_entitlement_waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={},
            to_check_entitlements={
                config.data.TEST_PROD_IN_TWO_STORES_PROMO_PCT_PRO_VC.ENTITLEMENT: 1
            }
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        store_1_entitlement_waiter.wait('Did not get {} {}\n{}'.format(
            config.data.TEST_PROD_IN_TWO_STORES_PROMO_PCT_PRO_VC.ENTITLEMENT,
            1,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        grant_test_currency_for_store_2_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                config.data.TEST_PROD_IN_TWO_STORES_PROMO_PCT_PRO_VC.STOREFRONT2.VIRTUAL_CURRENCY.AMOUNT
            )]
        )
        grant_test_currency_for_store_2_response.assert_is_success()

        fetch_prod_from_store_2_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PROD_IN_TWO_STORES_PROMO_PCT_PRO_VC.PRODUCT],
            config.store.profile_id,
            config.data.TEST_PROD_IN_TWO_STORES_PROMO_PCT_PRO_VC.COUNTRY,
            config.data.TEST_PROD_IN_TWO_STORES_PROMO_PCT_PRO_VC.LANGUAGE,
            config.data.TEST_PROD_IN_TWO_STORES_PROMO_PCT_PRO_VC.STOREFRONT2.CODE
        )
        fetch_prod_from_store_2_response.assert_is_success()
        assert_that(fetch_prod_from_store_2_response.content['body']['uriList'], has_length(1))
        store_2_prod_uri = fetch_prod_from_store_2_response.content['body']['uriList'][0]

        store_2_prod_response = RequestBuilder(store_2_prod_uri).get()
        store_2_prod_response.assert_is_success()

        assert_that(store_2_prod_response.content, has_key('price'))
        assert_that(store_2_prod_response.content['price'], has_key('virtual_price'))
        assert_that(store_2_prod_response.content['price']['virtual_price'], has_length(1))

        store_2_prod_price = store_2_prod_response.content['price']['virtual_price'][0]
        assert_that(
            store_2_prod_price['code'],
            equal_to(config.data.TEST_PROD_IN_TWO_STORES_PROMO_PCT_PRO_VC.STOREFRONT2.VIRTUAL_CURRENCY.CODE)
        )
        assert_that(
            store_2_prod_price['amount'],
            equal_to(str(config.data.TEST_PROD_IN_TWO_STORES_PROMO_PCT_PRO_VC.STOREFRONT2.VIRTUAL_CURRENCY.AMOUNT))
        )

        purchase_store_2_prod_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PROD_IN_TWO_STORES_PROMO_PCT_PRO_VC.PRODUCT,
            config.data.TEST_PROD_IN_TWO_STORES_PROMO_PCT_PRO_VC.AMOUNT,
            [
                CurrencyItem(
                    store_2_prod_price['code'],
                    int(store_2_prod_price['amount'])
                )
            ],
            storefront=config.data.TEST_PROD_IN_TWO_STORES_PROMO_PCT_PRO_VC.STOREFRONT2.CODE
        )
        purchase_store_2_prod_response.assert_is_success()

        store_2_currency_waiter = WaitOn(lambda: InventoryUtilities.inventory_empty(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            check_currencies=True,
            check_entitlements=False
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        store_2_currency_waiter.wait('Currencies was not empty\n{}'.format(
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        store_2_entitlement_waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={},
            to_check_entitlements={
                config.data.TEST_PROD_IN_TWO_STORES_PROMO_PCT_PRO_VC.ENTITLEMENT: 2
            }
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        store_2_entitlement_waiter.wait('Did not get {} {}\n{}'.format(
            config.data.TEST_PROD_IN_TWO_STORES_PROMO_PCT_PRO_VC.ENTITLEMENT,
            2,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_should_succeed_when_prod_in_two_stores_have_fixed_promo_in_one_store(self, config):
        grant_test_currency_for_store_1_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                config.data.TEST_PROD_IN_TWO_STORES_PROMO_FIXED_VC.STOREFRONT1.VIRTUAL_CURRENCY.AMOUNT
            )]
        )
        grant_test_currency_for_store_1_response.assert_is_success()

        fetch_prod_from_store_1_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PROD_IN_TWO_STORES_PROMO_FIXED_VC.PRODUCT],
            config.store.profile_id,
            config.data.TEST_PROD_IN_TWO_STORES_PROMO_FIXED_VC.COUNTRY,
            config.data.TEST_PROD_IN_TWO_STORES_PROMO_FIXED_VC.LANGUAGE,
            config.data.TEST_PROD_IN_TWO_STORES_PROMO_FIXED_VC.STOREFRONT1.CODE
        )
        fetch_prod_from_store_1_response.assert_is_success()
        assert_that(fetch_prod_from_store_1_response.content['body']['uriList'], has_length(1))
        store_1_prod_uri = fetch_prod_from_store_1_response.content['body']['uriList'][0]

        store_1_prod_response = RequestBuilder(store_1_prod_uri).get()
        store_1_prod_response.assert_is_success()

        assert_that(store_1_prod_response.content, has_key('price'))
        assert_that(store_1_prod_response.content['price'], has_key('virtual_price'))
        assert_that(store_1_prod_response.content['price']['virtual_price'], has_length(1))

        store_1_prod_price = store_1_prod_response.content['price']['virtual_price'][0]
        assert_that(
            store_1_prod_price['code'],
            equal_to(config.data.TEST_PROD_IN_TWO_STORES_PROMO_FIXED_VC.STOREFRONT1.VIRTUAL_CURRENCY.CODE)
        )
        assert_that(
            store_1_prod_price['amount'],
            equal_to(str(config.data.TEST_PROD_IN_TWO_STORES_PROMO_FIXED_VC.STOREFRONT1.VIRTUAL_CURRENCY.AMOUNT))
        )

        purchase_store_1_prod_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PROD_IN_TWO_STORES_PROMO_FIXED_VC.PRODUCT,
            config.data.TEST_PROD_IN_TWO_STORES_PROMO_FIXED_VC.AMOUNT,
            [
                CurrencyItem(
                    store_1_prod_price['code'],
                    int(store_1_prod_price['amount'])
                )
            ],
            storefront=config.data.TEST_PROD_IN_TWO_STORES_PROMO_FIXED_VC.STOREFRONT1.CODE
        )
        purchase_store_1_prod_response.assert_is_success()

        store_1_currency_waiter = WaitOn(lambda: InventoryUtilities.inventory_empty(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            check_currencies=True,
            check_entitlements=False
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        store_1_currency_waiter.wait('Currencies was not empty\n{}'.format(
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        store_1_entitlement_waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={},
            to_check_entitlements={
                config.data.TEST_PROD_IN_TWO_STORES_PROMO_FIXED_VC.ENTITLEMENT: 1
            }
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        store_1_entitlement_waiter.wait('Did not get {} {}\n{}'.format(
            config.data.TEST_PROD_IN_TWO_STORES_PROMO_FIXED_VC.ENTITLEMENT,
            1,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        grant_test_currency_for_store_2_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                config.data.TEST_PROD_IN_TWO_STORES_PROMO_FIXED_VC.STOREFRONT2.VIRTUAL_CURRENCY.AMOUNT
            )]
        )
        grant_test_currency_for_store_2_response.assert_is_success()

        fetch_prod_from_store_2_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PROD_IN_TWO_STORES_PROMO_FIXED_VC.PRODUCT],
            config.store.profile_id,
            config.data.TEST_PROD_IN_TWO_STORES_PROMO_FIXED_VC.COUNTRY,
            config.data.TEST_PROD_IN_TWO_STORES_PROMO_FIXED_VC.LANGUAGE,
            config.data.TEST_PROD_IN_TWO_STORES_PROMO_FIXED_VC.STOREFRONT2.CODE
        )
        fetch_prod_from_store_2_response.assert_is_success()
        assert_that(fetch_prod_from_store_2_response.content['body']['uriList'], has_length(1))
        store_2_prod_uri = fetch_prod_from_store_2_response.content['body']['uriList'][0]

        store_2_prod_response = RequestBuilder(store_2_prod_uri).get()
        store_2_prod_response.assert_is_success()

        assert_that(store_2_prod_response.content, has_key('price'))
        assert_that(store_2_prod_response.content['price'], has_key('virtual_price'))
        assert_that(store_2_prod_response.content['price']['virtual_price'], has_length(1))

        store_2_prod_price = store_2_prod_response.content['price']['virtual_price'][0]
        assert_that(
            store_2_prod_price['code'],
            equal_to(config.data.TEST_PROD_IN_TWO_STORES_PROMO_FIXED_VC.STOREFRONT2.VIRTUAL_CURRENCY.CODE)
        )
        assert_that(
            store_2_prod_price['amount'],
            equal_to(str(config.data.TEST_PROD_IN_TWO_STORES_PROMO_FIXED_VC.STOREFRONT2.VIRTUAL_CURRENCY.AMOUNT))
        )

        purchase_store_2_prod_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PROD_IN_TWO_STORES_PROMO_FIXED_VC.PRODUCT,
            config.data.TEST_PROD_IN_TWO_STORES_PROMO_FIXED_VC.AMOUNT,
            [
                CurrencyItem(
                    store_2_prod_price['code'],
                    int(store_2_prod_price['amount'])
                )
            ],
            storefront=config.data.TEST_PROD_IN_TWO_STORES_PROMO_FIXED_VC.STOREFRONT2.CODE
        )
        purchase_store_2_prod_response.assert_is_success()

        store_2_currency_waiter = WaitOn(lambda: InventoryUtilities.inventory_empty(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            check_currencies=True,
            check_entitlements=False
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        store_2_currency_waiter.wait('Currencies was not empty\n{}'.format(
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        store_2_entitlement_waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={},
            to_check_entitlements={
                config.data.TEST_PROD_IN_TWO_STORES_PROMO_FIXED_VC.ENTITLEMENT: 2
            }
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        store_2_entitlement_waiter.wait('Did not get {} {}\n{}'.format(
            config.data.TEST_PROD_IN_TWO_STORES_PROMO_FIXED_VC.ENTITLEMENT,
            2,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))
