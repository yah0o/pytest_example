import uuid

import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities, InventoryUtilities, ReturnValue, WaitOn
from integration.main.request.constants import RequestConstants
from integration.main.request.constants import ResponseMessage
from integration.main.services import CurrencyItem, LegacyProductItem
from integration.main.session import Parameters


@pytest.mark.skip_for_regions('trie')
class TestPurchaseProduct(object):

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
        config.store.profile_id = account_created.content['id']

        inventory_response = config.freya.server_gateway.get_full_inventory(config.store.profile_id)
        inventory_response.assert_is_success()
        all_entitlements = InventoryUtilities.get_all_entitlements(inventory_response.content['body']['profile'])
        assert_that(sum(entitlement['amount'] for entitlement in all_entitlements), equal_to(0))

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(config.store.wgid)
        delete_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_purchase_product_should_succeed_when_product_is_free(self, config, content_type):
        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PURCHASE.FREE.PRODUCT_CODE,
            1,
            [],
            payer_current_ip='127.0.0.1',
            content_type=content_type,
            storefront=config.data.TEST_PURCHASE.FREE.STOREFRONT
        )
        purchase_response.assert_is_success()

        inventory_response = config.freya.server_gateway.get_full_inventory(config.store.profile_id)
        inventory_response.assert_is_success()
        all_entitlements = InventoryUtilities.get_all_entitlements(inventory_response.content['body']['profile'])
        entitlements_count_after = sum(entitlement['amount'] for entitlement in all_entitlements)

        assert_that(
            entitlements_count_after,
            equal_to(1),
            'profile {0} expected {1} but actual {2}'.format(
                config.store.profile_id,
                1,
                entitlements_count_after
            )
        )

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    @pytest.mark.parametrize('quantity', [2147483647, Parameters.RandomInt(2, 2147483646)])
    def test_purchase_product_should_fail_when_fixed_price_product_quantity_is_free(self, config, content_type,
                                                                                    quantity):
        quantity = Parameters.evaluate(quantity)
        product = config.data.TEST_PURCHASE.FREE.PRODUCT_CODE
        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PURCHASE.FREE.PRODUCT_CODE,
            quantity,
            [],
            payer_current_ip='127.0.0.1',
            content_type=content_type,
            storefront=config.data.TEST_PURCHASE.FREE.STOREFRONT
        )
        purchase_response.expect_failure(result_code=ResponseMessage.INVALID_PRODUCT_QUANTITY)

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_purchase_product_should_succeed_when_product_with_test_currency_is_purchased(self, config, content_type,
                                                                                          ):
        config.log.info('granting {} amount of {}'.format(
            config.data.TEST_PRODUCT.VIRTUAL_CURRENCY.AMOUNT * 1,
            config.data.TEST_PRODUCT.VIRTUAL_CURRENCY.CURRENCY_CODE
        ))
        grant_product_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                               config.data.TEST_PRODUCT.VIRTUAL_CURRENCY.AMOUNT * 1)]
        )
        grant_product_response.assert_is_success()

        tx_id = str(uuid.uuid4())
        purchase_response = config.freya.server_gateway.purchase_product(
            tx_id,
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PRODUCT.PRODUCT_CODE,
            1,
            [CurrencyItem(
                config.data.TEST_PRODUCT.VIRTUAL_CURRENCY.CURRENCY_CODE,
                str(config.data.TEST_PRODUCT.VIRTUAL_CURRENCY.AMOUNT * 1)
            )],
            content_type=content_type,
            storefront=config.data.TEST_PRODUCT.STOREFRONT
        )
        purchase_response.assert_is_success()

        inventory_response = config.freya.server_gateway.get_full_inventory(config.store.profile_id)
        inventory_response.assert_is_success()
        inventory = inventory_response.content['body']['profile']

        currency = next((c for c in inventory['currencies'] if c['code'] == config.data.TEST_PRODUCT.CURRENCIES.CODE),
                        None)
        assert_that(currency, not_none())
        assert_that(currency['amount'], equal_to(str(config.data.TEST_PRODUCT.CURRENCIES.AMOUNT * 1)))

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    @pytest.mark.parametrize('quantity', [2147483647, Parameters.RandomInt(2, 2147483646)])
    def test_purchase_product_should_fail_when_product_with_test_currency_quantity_is_purchased(self, config,
                                                                                                content_type,
                                                                                                quantity):
        quantity = Parameters.evaluate(quantity)

        config.log.info('granting {} amount of {}'.format(
            config.data.TEST_PRODUCT.VIRTUAL_CURRENCY.AMOUNT * quantity,
            config.data.TEST_PRODUCT.VIRTUAL_CURRENCY.CURRENCY_CODE
        ))
        grant_product_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                               config.data.TEST_PRODUCT.VIRTUAL_CURRENCY.AMOUNT * quantity)]
        )
        grant_product_response.assert_is_success()

        product = config.data.TEST_PRODUCT.PRODUCT_CODE
        tx_id = str(uuid.uuid4())
        purchase_response = config.freya.server_gateway.purchase_product(
            tx_id,
            config.store.profile_id,
            config.store.profile_id,
            product,
            quantity,
            [CurrencyItem(
                config.data.TEST_PRODUCT.VIRTUAL_CURRENCY.CURRENCY_CODE,
                str(config.data.TEST_PRODUCT.VIRTUAL_CURRENCY.AMOUNT * quantity)
            )],
            content_type=content_type,
            storefront=config.data.TEST_PRODUCT.STOREFRONT
        )
        purchase_response.expect_failure(result_code=ResponseMessage.INVALID_PRODUCT_QUANTITY)

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_purchase_product_should_succeed_when_product_with_entitlement_is_purchased(self, config, content_type):
        config.log.info('granting {} amount of {}'.format(
            config.data.TEST_PRODUCT_ENTITLEMENT.COST.AMOUNT * 1,
            config.data.TEST_PRODUCT_ENTITLEMENT.COST.CURRENCY_CODE
        ))
        grant_product_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                               config.data.TEST_PRODUCT_ENTITLEMENT.COST.AMOUNT * 1)]
        )
        grant_product_response.assert_is_success()

        tx_id = str(uuid.uuid4())
        purchase_response = config.freya.server_gateway.purchase_product(
            tx_id,
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PRODUCT_ENTITLEMENT.CODE,
            1,
            [CurrencyItem(
                config.data.TEST_PRODUCT_ENTITLEMENT.COST.CURRENCY_CODE,
                str(config.data.TEST_PRODUCT_ENTITLEMENT.COST.AMOUNT * 1)
            )],
            content_type=content_type,
            storefront=config.data.TEST_PRODUCT_ENTITLEMENT.STOREFRONT
        )
        purchase_response.assert_is_success()

        inventory_response = config.freya.server_gateway.get_full_inventory(config.store.profile_id)
        inventory_response.assert_is_success()
        inventory = inventory_response.content['body']['profile']

        entitlement = next((e for e in inventory['entitlements']
                            if e['code'] == config.data.TEST_PRODUCT_ENTITLEMENT.ENTITLEMENTS.CODE), None)
        assert_that(entitlement, not_none())
        assert_that(entitlement['amount'], equal_to(1))

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    @pytest.mark.parametrize('quantity', [1073741, Parameters.RandomInt(2, 1073740)])
    def test_purchase_product_should_fail_when_fixed_price_product_quantity_with_entitlement_is_purchased(self, config,
                                                                                                          content_type,
                                                                                                          quantity):
        quantity = Parameters.evaluate(quantity)

        config.log.info('granting {} amount of {}'.format(
            config.data.TEST_PRODUCT_ENTITLEMENT.COST.AMOUNT * quantity,
            config.data.TEST_PRODUCT_ENTITLEMENT.COST.CURRENCY_CODE
        ))
        grant_product_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                               config.data.TEST_PRODUCT_ENTITLEMENT.COST.AMOUNT * quantity)]
        )
        grant_product_response.assert_is_success()

        product = config.data.TEST_PRODUCT_ENTITLEMENT.CODE
        tx_id = str(uuid.uuid4())
        purchase_response = config.freya.server_gateway.purchase_product(
            tx_id,
            config.store.profile_id,
            config.store.profile_id,
            product,
            quantity,
            [CurrencyItem(
                config.data.TEST_PRODUCT_ENTITLEMENT.COST.CURRENCY_CODE,
                str(config.data.TEST_PRODUCT_ENTITLEMENT.COST.AMOUNT * quantity)
            )],
            content_type=content_type,
            storefront=config.data.TEST_PRODUCT_ENTITLEMENT.STOREFRONT
        )
        purchase_response.expect_failure(result_code=ResponseMessage.INVALID_PRODUCT_QUANTITY)

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_purchase_product_should_succeed_when_product_with_test_currency_and_entitlement_is_purchased(
            self, config, content_type):
        config.log.info('granting {} amount of {}'.format(
            config.data.TEST_PRODUCT_FULL.VIRTUAL_CURRENCY.AMOUNT * 1,
            config.data.TEST_PRODUCT_FULL.VIRTUAL_CURRENCY.CURRENCY_CODE
        ))
        grant_product_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                               config.data.TEST_PRODUCT_FULL.VIRTUAL_CURRENCY.AMOUNT * 1)]
        )
        grant_product_response.assert_is_success()

        tx_id = str(uuid.uuid4())
        purchase_response = config.freya.server_gateway.purchase_product(
            tx_id,
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PRODUCT_FULL.CODE,
            1,
            [CurrencyItem(
                config.data.TEST_PRODUCT_FULL.VIRTUAL_CURRENCY.CURRENCY_CODE,
                str(config.data.TEST_PRODUCT_FULL.VIRTUAL_CURRENCY.AMOUNT * 1)
            )],
            content_type=content_type,
            storefront=config.data.TEST_PRODUCT_FULL.STOREFRONT
        )

        purchase_response.assert_is_success()

        inventory_waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={
                config.data.TEST_PRODUCT_FULL.CURRENCIES.CODE:
                    config.data.TEST_PRODUCT_FULL.CURRENCIES.AMOUNT * 1
            },
            to_check_entitlements={
                config.data.TEST_PRODUCT_FULL.ENTITLEMENTS.CODE:
                    config.data.TEST_PRODUCT_FULL.ENTITLEMENTS.AMOUNT * 1
            }
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)

        inventory_waiter.wait('Did not get {} {} and {} {}.\n{}'.format(
            config.data.TEST_PRODUCT_FULL.CURRENCIES.AMOUNT * 1,
            config.data.TEST_PRODUCT_FULL.CURRENCIES.CODE,
            config.data.TEST_PRODUCT_FULL.ENTITLEMENTS.CODE,
            config.data.TEST_PRODUCT_FULL.ENTITLEMENTS.AMOUNT * 1,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    @pytest.mark.parametrize('quantity', [1073741, Parameters.RandomInt(2, 1073740)])
    def test_purchase_product_should_fail_when_fixed_price_product_quantity_with_test_currency_and_entitlement_is_purchased(
            self, config, content_type, quantity):
        quantity = Parameters.evaluate(quantity)

        config.log.info('granting {} amount of {}'.format(
            config.data.TEST_PRODUCT_FULL.VIRTUAL_CURRENCY.AMOUNT * quantity,
            config.data.TEST_PRODUCT_FULL.VIRTUAL_CURRENCY.CURRENCY_CODE
        ))
        grant_product_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                               config.data.TEST_PRODUCT_FULL.VIRTUAL_CURRENCY.AMOUNT * quantity)]
        )
        grant_product_response.assert_is_success()

        product = config.data.TEST_PRODUCT_FULL.CODE
        tx_id = str(uuid.uuid4())
        purchase_response = config.freya.server_gateway.purchase_product(
            tx_id,
            config.store.profile_id,
            config.store.profile_id,
            product,
            quantity,
            [CurrencyItem(
                config.data.TEST_PRODUCT_FULL.VIRTUAL_CURRENCY.CURRENCY_CODE,
                str(config.data.TEST_PRODUCT_FULL.VIRTUAL_CURRENCY.AMOUNT * quantity)
            )],
            content_type=content_type,
            storefront=config.data.TEST_PRODUCT_FULL.STOREFRONT
        )

        purchase_response.expect_failure(result_code=ResponseMessage.INVALID_PRODUCT_QUANTITY)

    @pytest.mark.skip_for_regions('wgs11')
    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_should_succeed_when_product_have_multi_currencies(self, config):
        grant_curr_prod_for_purchase_product = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                1
            )]
        )
        grant_curr_prod_for_purchase_product.assert_is_success()

        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES.CODE,
            1,
            [CurrencyItem(
                config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES.VIRTUAL_CURRENCY,
                str(1)
            )],
            storefront=config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES.STOREFRONT
        )
        purchase_response.assert_is_success()

        waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={
                config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES.CURRENCY1: 1,
                config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES.CURRENCY2: 1
            },
            to_check_entitlements={}
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        waiter.wait('Did not get {} amount of {} and {}\n{}'.format(
            1,
            config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES.CURRENCY1,
            config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES.CURRENCY2,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('quantity', [2147483647, Parameters.RandomInt(2, 2147483646)])
    def test_purchase_product_should_fail_when_fixed_price_product_quantity_have_multi_currencies(self, config,
                                                                                                  quantity):
        quantity = Parameters.evaluate(quantity)

        grant_curr_prod_for_purchase_product = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                quantity
            )]
        )
        grant_curr_prod_for_purchase_product.assert_is_success()
        product = config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES.CODE
        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            product,
            quantity,
            [CurrencyItem(
                config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES.VIRTUAL_CURRENCY,
                str(quantity)
            )],
            storefront=config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES.STOREFRONT
        )
        purchase_response.expect_failure(result_code=ResponseMessage.INVALID_PRODUCT_QUANTITY)

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_should_succeed_when_product_have_multi_entitlements(self, config):
        grant_curr_prod_for_purchase_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                1
            )]
        )
        grant_curr_prod_for_purchase_response.assert_is_success()

        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PRODUCT_MULTIPLE_ENTITLEMENTS.CODE,
            1,
            [CurrencyItem(
                config.data.TEST_PRODUCT_MULTIPLE_ENTITLEMENTS.VIRTUAL_CURRENCY,
                str(1)
            )],
            storefront=config.data.TEST_PRODUCT_MULTIPLE_ENTITLEMENTS.STOREFRONT
        )
        purchase_response.assert_is_success()

        waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={},
            to_check_entitlements={
                config.data.TEST_PRODUCT_MULTIPLE_ENTITLEMENTS.ENTITLEMENT1: 1,
                config.data.TEST_PRODUCT_MULTIPLE_ENTITLEMENTS.ENTITLEMENT2: 1
            }
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        waiter.wait('Did not get {} amount of {} and {}\n{}'.format(
            1,
            config.data.TEST_PRODUCT_MULTIPLE_ENTITLEMENTS.ENTITLEMENT1,
            config.data.TEST_PRODUCT_MULTIPLE_ENTITLEMENTS.ENTITLEMENT2,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('quantity', [2147483647, Parameters.RandomInt(2, 2147483646)])
    def test_purchase_product_should_fail_when_fixed_price_product_quantity_have_multi_entitlements(self, config,
                                                                                                    quantity):
        quantity = Parameters.evaluate(quantity)

        grant_curr_prod_for_purchase_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                quantity
            )]
        )
        grant_curr_prod_for_purchase_response.assert_is_success()
        product = config.data.TEST_PRODUCT_MULTIPLE_ENTITLEMENTS.CODE
        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            product,
            quantity,
            [CurrencyItem(
                config.data.TEST_PRODUCT_MULTIPLE_ENTITLEMENTS.VIRTUAL_CURRENCY,
                str(quantity)
            )],
            storefront=config.data.TEST_PRODUCT_MULTIPLE_ENTITLEMENTS.STOREFRONT
        )
        purchase_response.expect_failure(result_code=ResponseMessage.INVALID_PRODUCT_QUANTITY)

    @pytest.mark.skip_for_regions('wgs11')
    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_should_succeed_when_product_have_multi_curr_and_entitle(self, config):
        grant_curr_prod_for_purchase_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                1
            )]
        )
        grant_curr_prod_for_purchase_response.assert_is_success()

        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES_AND_ENTITLEMENTS.CODE,
            1,
            [CurrencyItem(
                config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES_AND_ENTITLEMENTS.VIRTUAL_CURRENCY,
                str(1)
            )],
            storefront=config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES_AND_ENTITLEMENTS.STOREFRONT
        )
        purchase_response.assert_is_success()

        waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={
                config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES_AND_ENTITLEMENTS.CURRENCY1: 1,
                config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES_AND_ENTITLEMENTS.CURRENCY2: 1
            },
            to_check_entitlements={
                config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES_AND_ENTITLEMENTS.ENTITLEMENT1: 1,
                config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES_AND_ENTITLEMENTS.ENTITLEMENT2: 1
            }
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        waiter.wait('Did not get {} {} or {} and {} {} or {}\n{}'.format(
            1,
            config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES_AND_ENTITLEMENTS.CURRENCY1,
            config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES_AND_ENTITLEMENTS.CURRENCY2,
            1,
            config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES_AND_ENTITLEMENTS.ENTITLEMENT1,
            config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES_AND_ENTITLEMENTS.ENTITLEMENT2,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('quantity', [2147483647, Parameters.RandomInt(2, 2147483646)])
    def test_purchase_product_should_fail_when_fixed_price_product_quantity_have_multi_curr_and_entitle(self, config,
                                                                                                        quantity):
        quantity = Parameters.evaluate(quantity)

        grant_curr_prod_for_purchase_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                quantity
            )]
        )
        grant_curr_prod_for_purchase_response.assert_is_success()

        product = config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES_AND_ENTITLEMENTS.CODE

        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            product,
            quantity,
            [CurrencyItem(
                config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES_AND_ENTITLEMENTS.VIRTUAL_CURRENCY,
                str(quantity)
            )],
            storefront=config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES_AND_ENTITLEMENTS.STOREFRONT
        )
        purchase_response.expect_failure(result_code=ResponseMessage.INVALID_PRODUCT_QUANTITY)

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product')
    @pytest.allure.severity(severity_level.MINOR)
    def test_purchase_product_full_should_fail_when_invalid_source_profile_id(self, config):
        config.log.info('granting {} amount of {}'.format(
            config.data.TEST_PRODUCT.VIRTUAL_CURRENCY.AMOUNT,
            config.data.TEST_PRODUCT.VIRTUAL_CURRENCY.CURRENCY_CODE))
        grant_product_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                               config.data.TEST_PRODUCT_FULL.VIRTUAL_CURRENCY.AMOUNT)]
        )
        grant_product_response.assert_is_success()

        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            -1,
            config.store.profile_id,
            config.data.TEST_PRODUCT_FULL.CODE,
            config.data.TEST_PRODUCT_FULL.AMOUNT,
            [CurrencyItem(config.data.TEST_PRODUCT_FULL.VIRTUAL_CURRENCY.CURRENCY_CODE,
                          config.data.TEST_PRODUCT_FULL.VIRTUAL_CURRENCY.AMOUNT)],
            storefront=config.data.TEST_PRODUCT_FULL.STOREFRONT
        )
        purchase_response.expect_failure(result_code=ResponseMessage.CLIENT_ERROR_404)

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product')
    @pytest.allure.severity(severity_level.MINOR)
    def test_purchase_product_test_currency_should_fail_when_purchase_twice_with_same_tx_id(self, config):
        config.log.info('granting {} amount of {}'.format(
            config.data.TEST_PRODUCT.VIRTUAL_CURRENCY.AMOUNT,
            config.data.TEST_PRODUCT.VIRTUAL_CURRENCY.CURRENCY_CODE
        ))
        grant_product_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                               config.data.TEST_PRODUCT_FULL.VIRTUAL_CURRENCY.AMOUNT)]
        )
        grant_product_response.assert_is_success()

        tx_id = str(uuid.uuid4())
        purchase_response = config.freya.server_gateway.purchase_product(
            tx_id,
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PRODUCT_FULL.CODE,
            config.data.TEST_PRODUCT_FULL.AMOUNT,
            [CurrencyItem(config.data.TEST_PRODUCT_FULL.VIRTUAL_CURRENCY.CURRENCY_CODE,
                          config.data.TEST_PRODUCT_FULL.VIRTUAL_CURRENCY.AMOUNT)],
            storefront=config.data.TEST_PRODUCT_FULL.STOREFRONT
        )
        purchase_response.assert_is_success()

        inventory_waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={
                config.data.TEST_PRODUCT.CURRENCIES.CODE: config.data.TEST_PRODUCT.CURRENCIES.AMOUNT
            },
            to_check_entitlements={}
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)

        inventory_waiter.wait('Did not get {} {}.\n{}'.format(
            config.data.TEST_PRODUCT_FULL.CURRENCIES.CODE,
            config.data.TEST_PRODUCT_FULL.CURRENCIES.AMOUNT,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        purchase_response = config.freya.server_gateway.purchase_product(
            tx_id,
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PRODUCT_FULL.CODE,
            config.data.TEST_PRODUCT_FULL.AMOUNT,
            [CurrencyItem(config.data.TEST_PRODUCT_FULL.VIRTUAL_CURRENCY.CURRENCY_CODE,
                          config.data.TEST_PRODUCT_FULL.VIRTUAL_CURRENCY.AMOUNT)],
            storefront=config.data.TEST_PRODUCT_FULL.STOREFRONT
        )
        purchase_response.assert_is_success()

        inventory_response = config.freya.server_gateway.get_full_inventory(config.store.profile_id)
        inventory_response.assert_is_success()

        inventory = inventory_response.content['body']['profile']

        second_currencies = next(
            (currency for currency in inventory['currencies'] if
             currency['code'] == config.data.TEST_PRODUCT_FULL.CURRENCIES.CODE),
            None)
        assert_that(second_currencies, not_none())
        assert_that(second_currencies['amount'], equal_to(str(config.data.TEST_PRODUCT_FULL.CURRENCIES.AMOUNT)))

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('currency_name', ['xp', 'test_currency'])
    def test_purchase_product_full_should_fail_when_expected_currency_is_invalid(self, config, currency_name):
        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PRODUCT.PRODUCT_CODE,
            config.data.TEST_PRODUCT.AMOUNT,
            [CurrencyItem(currency_name, 0)],
            storefront=config.data.TEST_PRODUCT.STOREFRONT
        )
        purchase_response.expect_failure(result_code=ResponseMessage.EXPECTED_PRICE_MISMATCH)

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product')
    @pytest.allure.severity(severity_level.MINOR)
    def test_purchase_large_product_should_fail_when_profile_does_not_contain_enough_currency(self, config):
        inventory_response = config.freya.server_gateway.get_full_inventory(config.store.profile_id)
        inventory_response.assert_is_success()
        inventory = inventory_response.content['body']['profile']

        assert_that(inventory['currencies'], has_length(0))

        data = config.data['TEST_PURCHASE']

        currencies = data['MULTIPLE_LARGE_COST']['CURRENCIES']
        insufficient_funds = [CurrencyItem(currency['CODE'], currency['AMOUNT']) for currency in currencies]

        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PURCHASE.MULTIPLE_LARGE_COST.PRODUCT_CODE,
            config.data.TEST_PURCHASE.MULTIPLE_LARGE_COST.AMOUNT,
            insufficient_funds,
            storefront=config.data.TEST_PURCHASE.MULTIPLE_LARGE_COST.STOREFRONT
        )
        purchase_response.expect_failure(result_code=ResponseMessage.INSUFFICIENT_FUNDS)

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product')
    @pytest.allure.severity(severity_level.MINOR)
    def test_purchase_product_test_currency_should_fail_when_source_profile_id_is_invalid(self, config):
        config.log.info('granting {} amount of {}'.format(
            config.data.TEST_PRODUCT.VIRTUAL_CURRENCY.AMOUNT,
            config.data.TEST_PRODUCT.VIRTUAL_CURRENCY.CURRENCY_CODE))
        grant_product_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                               config.data.TEST_PRODUCT_FULL.VIRTUAL_CURRENCY.AMOUNT)]
        )
        grant_product_response.assert_is_success()

        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            -1,
            config.store.profile_id,
            config.data.TEST_PRODUCT_FULL.CODE,
            config.data.TEST_PRODUCT_FULL.AMOUNT,
            [CurrencyItem(config.data.TEST_PRODUCT_FULL.VIRTUAL_CURRENCY.CURRENCY_CODE,
                          config.data.TEST_PRODUCT_FULL.VIRTUAL_CURRENCY.AMOUNT)],
            storefront=config.data.TEST_PRODUCT_FULL.STOREFRONT
        )
        purchase_response.expect_failure(result_code=ResponseMessage.CLIENT_ERROR_404)

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('empty_source_profile_id', ['', None])
    def test_purchase_full_product_should_fail_when_source_profile_id_is_empty(self, config, empty_source_profile_id):
        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            empty_source_profile_id,
            config.store.profile_id,
            config.data.TEST_PRODUCT_FULL.CODE,
            config.data.TEST_PRODUCT_FULL.AMOUNT,
            [],
            storefront=config.data.TEST_PRODUCT_FULL.STOREFRONT
        )
        purchase_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                         result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product')
    @pytest.allure.severity(severity_level.MINOR)
    def test_purchase_full_product_should_fail_when_source_profile_id_is_wrong_type(self, config):
        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            'invalid_source_profile_id',
            config.store.profile_id,
            config.data.TEST_PRODUCT_FULL.CODE,
            config.data.TEST_PRODUCT_FULL.AMOUNT,
            [],
            storefront=config.data.TEST_PRODUCT_FULL.STOREFRONT
        )
        purchase_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                         result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_destination_profile_id', [0, .50, '', None])
    def test_purchase_full_product_should_fail_when_destination_profile_id_is_invalid(self, config,
                                                                                      invalid_destination_profile_id):
        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            invalid_destination_profile_id,
            config.data.TEST_PRODUCT_FULL.CODE,
            config.data.TEST_PRODUCT_FULL.AMOUNT,
            [],
            storefront=config.data.TEST_PRODUCT_FULL.STOREFRONT
        )
        purchase_response.expect_failure(result_code=ResponseMessage.INVALID_PROFILE_ID)

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product')
    @pytest.allure.severity(severity_level.MINOR)
    def test_purchase_full_product_should_fail_when_destination_profile_id_is_wrong_type(self, config):
        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            'invalid_destination_profile_id',
            config.data.TEST_PRODUCT_FULL.CODE,
            config.data.TEST_PRODUCT_FULL.AMOUNT,
            [],
            storefront=config.data.TEST_PRODUCT_FULL.STOREFRONT
        )
        purchase_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                         result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_product_code', [-1, 0, .50, 'bad_product_code',
                                                      '3kIWAOOG8xWF28oJakAWblSflHoQ5EZpRA6f3oNXHFaueV8McSskVVbUe2zzhRIGI7Qx0vsEVnWPqmIbfgTnbncM7XqIduVU9OC1'])
    def test_purchase_full_product_should_fail_when_product_code_is_invalid(self, config, invalid_product_code):
        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            invalid_product_code,
            config.data.TEST_PRODUCT_FULL.AMOUNT,
            [],
            storefront=config.data.TEST_PRODUCT_FULL.STOREFRONT
        )
        purchase_response.expect_failure(result_code=ResponseMessage.PRODUCT_NOT_FOUND)

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('empty_product_code', ['', None])
    def test_purchase_full_product_should_fail_when_product_code_is_none_or_empty(self, config, empty_product_code):
        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            empty_product_code,
            config.data.TEST_PRODUCT_FULL.AMOUNT,
            [],
            storefront=config.data.TEST_PRODUCT_FULL.STOREFRONT
        )
        purchase_response.expect_failure(result_code=ResponseMessage.INVALID_PRODUCT_CODE)

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_amount', [-1, 0, .50, '', None])
    def test_purchase_full_product_should_fail_when_amount_is_invalid(self, config, invalid_amount):
        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PRODUCT_FULL.CODE,
            invalid_amount,
            [],
            storefront=config.data.TEST_PRODUCT_FULL.STOREFRONT
        )
        purchase_response.expect_failure(result_code=ResponseMessage.INVALID_PRODUCT_AMOUNT)

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product')
    @pytest.allure.severity(severity_level.MINOR)
    def test_purchase_full_product_should_fail_when_amount_is_wrong_type(self, config):
        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PRODUCT_FULL.CODE,
            'bad_amount',
            [],
            storefront=config.data.TEST_PRODUCT_FULL.STOREFRONT
        )
        purchase_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                         result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_transaction_id', [
        '00000000-0000-0000-0000-00000000000000',
        '00000000-0000-0000-0000-0000000000',
        '00000000-0000-XXXX-0000-000000000000',
        'bad_transaction_id',
        0,
        -1
    ])
    def test_purchase_full_product_should_fail_when_transaction_id_is_invalid(self, config, invalid_transaction_id):
        purchase_response = config.freya.server_gateway.purchase_product(
            invalid_transaction_id,
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PRODUCT_FULL.CODE,
            config.data.TEST_PRODUCT_FULL.AMOUNT,
            [],
            storefront=config.data.TEST_PRODUCT_FULL.STOREFRONT
        )
        purchase_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                         result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product')
    @pytest.allure.severity(severity_level.NORMAL)
    def test_purchase_full_product_should_fail_with_no_storefront_in_req(self, config):
        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PRODUCT_FULL.CODE,
            10,
            [],
            storefront=None
        )
        purchase_response.expect_failure(code=200, result_code=ResponseMessage.STOREFRONT_NOT_DEFINED)

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product')
    @pytest.allure.severity(severity_level.NORMAL)
    def test_purchase_product_should_fail_with_restricted_countries(self, config):
        #  PRODO-613
        # Should fail when country is restricted (e.g. BY is restricted in product)
        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PURCHASE_RESTRICTED.PRODUCT,
            1,
            [],
            country=config.data.TEST_PURCHASE_RESTRICTED.RESTRICTED_COUNTRY,
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_PURCHASE_RESTRICTED.STOREFRONT
        )
        purchase_response.expect_failure(result_code=ResponseMessage.PRODUCT_NOT_ALLOWED)

    @pytest.mark.skip(reason='PRODO-625')
    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product')
    @pytest.allure.severity(severity_level.NORMAL)
    def test_purchase_product_should_succeed_with_non_restricted_countries(self, config):
        # PRODO-613
        # Should pass when country is not restricted
        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PURCHASE_RESTRICTED.PRODUCT,
            1,
            [],
            country='RU',
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_PURCHASE_RESTRICTED.STOREFRONT
        )
        purchase_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('country', ['UNDEFINED', 'ZZ'])
    def test_purchase_product_should_fail_with_undefined_countries(self, config, country):
        #  PRODO-613
        # Should fail when country is undefined (e.g. 'UNDEFINED', 'ZZ' is undefined)
        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PURCHASE_RESTRICTED.PRODUCT,
            1,
            [],
            country=country,
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_PURCHASE_RESTRICTED.STOREFRONT
        )
        purchase_response.expect_failure(result_code=ResponseMessage.PRODUCT_NOT_ALLOWED)
