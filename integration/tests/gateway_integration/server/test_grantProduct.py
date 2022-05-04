import uuid

import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities, WaitOn, ReturnValue, InventoryUtilities
from integration.main.request import RequestConstants, ResponseMessage
from integration.main.services import LegacyProductItem
from integration.main.session import Parameters


class TestGrantProduct(object):

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

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(config.store.wgid)
        delete_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('grant product')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_grant_product_should_succeed_grant_product_with_test_currency(self, config, content_type):
        grant_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT.COUNTRY,
            config.data.TEST_PRODUCT.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT.PRODUCT_CODE, config.data.TEST_PRODUCT.AMOUNT)],
            payer_current_ip='127.0.0.1',
            content_type=content_type
        )
        grant_response.assert_is_success()
        assert_that(grant_response.content['body'], has_key('required_action'))
        assert_that(grant_response.content['body']['required_action'], has_key('action_code'))

    @pytest.allure.feature('server')
    @pytest.allure.story('grant product')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('quantity', [30, Parameters.RandomInt(2, 29)])
    def test_grant_product_should_succeed_when_grant_unmergeable_product_with_test_currency(self, config, quantity):
        quantity = Parameters.evaluate(quantity)

        config.log.info("granting {} unmergeable products".format(quantity))

        inventory_response = config.freya.server_gateway.get_full_inventory(config.store.profile_id)
        inventory_response.assert_is_success()
        inventory = inventory_response.content['body']['profile']
        assert_that(inventory['currencies'], is_(empty()))

        grant_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT.COUNTRY,
            config.data.TEST_PRODUCT.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT.PRODUCT_CODE, quantity)]
        )
        grant_response.assert_is_success()

        expected_after_currency = quantity * config.data.TEST_PRODUCT.CURRENCIES.AMOUNT
        inventory_waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={config.data.TEST_PRODUCT.CURRENCIES.CODE: expected_after_currency},
            to_check_entitlements={},
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        inventory_waiter.wait('Inventory was not granted {} {}\n{}'.format(
            config.data.TEST_PRODUCT.CURRENCIES.CODE, expected_after_currency,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

    @pytest.mark.xfail(reason='FREYA-290')
    @pytest.allure.feature('server')
    @pytest.allure.story('grant product')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    @pytest.mark.parametrize('quantity', [1, 2147483647, Parameters.RandomInt(2, 2147483646)])
    def test_grant_product_should_succeed_when_grant_mergeable_product_with_test_currency(self, config, quantity,
                                                                                          content_type):
        quantity = Parameters.evaluate(quantity)

        config.log.info("granting {} mergeable products".format(quantity))

        inventory_response = config.freya.server_gateway.get_full_inventory(config.store.profile_id)
        inventory_response.assert_is_success()
        inventory = inventory_response.content['body']['profile']
        assert_that(inventory['currencies'], is_(empty()))

        config.log.info(config.store.profile_id)
        grant_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_MERGEABLE.COUNTRY,
            config.data.TEST_PRODUCT_MERGEABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT_MERGEABLE.PRODUCT_CODE, quantity)],
            content_type=content_type
        )
        grant_response.assert_is_success()

        expected_after_currency = quantity * config.data.TEST_PRODUCT_MERGEABLE.TEST_CURRENCY_GRANTED_PER_AMOUNT
        inventory_waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={'test_currency': expected_after_currency},
            to_check_entitlements={},
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        inventory_waiter.wait('Inventory was not granted {} {}\n{}'.format(
            'test_currency',
            expected_after_currency,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

    @pytest.allure.feature('server')
    @pytest.allure.story('grant product')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('quantity', [1, 2147483647, Parameters.RandomInt(2, 2147483646)])
    def test_grant_product_should_succeed_when_grant_product_with_entitlement(self, config, quantity):
        quantity = Parameters.evaluate(quantity)

        grant_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_ENTITLEMENT.COUNTRY,
            config.data.TEST_PRODUCT_ENTITLEMENT.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT_ENTITLEMENT.CODE, quantity)],
            content_type=RequestConstants.ContentTypes.JSON
        )
        grant_response.assert_is_success()

        inventory_response = config.freya.server_gateway.get_full_inventory(config.store.profile_id)
        inventory_response.assert_is_success()
        inventory = inventory_response.content['body']['profile']

        entitlement = next((entitlement for entitlement in inventory['entitlements'] if
                            entitlement['code'] == config.data.TEST_PRODUCT_ENTITLEMENT.ENTITLEMENTS.CODE), None)
        assert_that(entitlement, not_none())
        assert_that(entitlement['amount'], equal_to(quantity))

    @pytest.mark.xfail(reason='FREYA-290')
    @pytest.allure.feature('server')
    @pytest.allure.story('grant product')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('quantity', [1, 2147483647, Parameters.RandomInt(2, 2147483646)])
    def test_grant_product_should_succeed_when_grant_product_with_entitlement_and_test_currency(self, config, quantity):
        quantity = Parameters.evaluate(quantity)

        inventory_response = config.freya.server_gateway.get_full_inventory(config.store.profile_id)
        inventory_response.assert_is_success()
        inventory = inventory_response.content['body']['profile']

        assert_that(inventory['entitlements'], is_(empty()))
        assert_that(inventory['currencies'], is_(empty()))

        grant_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_FULL.COUNTRY,
            config.data.TEST_PRODUCT_FULL.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT_FULL.CODE, quantity)]
        )
        grant_response.assert_is_success()

        waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            {config.data.TEST_PRODUCT_FULL.CURRENCIES.CODE: config.data.TEST_PRODUCT_FULL.CURRENCIES.AMOUNT * quantity},
            {config.data.TEST_PRODUCT_FULL.ENTITLEMENTS.CODE: quantity}
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        waiter.wait('Inventory did not return expected entitlement and currencies\n{}'.format(
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

    @pytest.mark.skip_for_regions('wgs11')
    @pytest.allure.feature('server')
    @pytest.allure.story('grant product')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('quantity', [1, 2147483647, Parameters.RandomInt(2, 2147483646)])
    def test_grant_product_should_succeed_when_product_have_multi_currencies(self, config, quantity):
        quantity = Parameters.evaluate(quantity)

        grant_product_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES.COUNTRY,
            config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES.CODE,
                quantity
            )]
        )
        grant_product_response.assert_is_success()

        waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={
                config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES.CURRENCY1: quantity,
                config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES.CURRENCY2: quantity
            },
            to_check_entitlements={}
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        waiter.wait('Did not get {} amount of {} and {}\n{}'.format(
            quantity,
            config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES.CURRENCY1,
            config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES.CURRENCY2,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

    @pytest.mark.skip_for_regions('trie')
    @pytest.allure.feature('server')
    @pytest.allure.story('grant product')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('quantity', [1, 2147483647, Parameters.RandomInt(2, 2147483646)])
    def test_grant_product_should_succeed_when_product_have_multi_entitlements(self, config, quantity):
        quantity = Parameters.evaluate(quantity)

        grant_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_MULTIPLE_ENTITLEMENTS.COUNTRY,
            config.data.TEST_PRODUCT_MULTIPLE_ENTITLEMENTS.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_MULTIPLE_ENTITLEMENTS.CODE,
                quantity
            )]
        )
        grant_response.assert_is_success()

        waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={},
            to_check_entitlements={
                config.data.TEST_PRODUCT_MULTIPLE_ENTITLEMENTS.ENTITLEMENT1: quantity,
                config.data.TEST_PRODUCT_MULTIPLE_ENTITLEMENTS.ENTITLEMENT2: quantity
            }
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        waiter.wait('Did not get {} amount of {} and {}\n{}'.format(
            quantity,
            config.data.TEST_PRODUCT_MULTIPLE_ENTITLEMENTS.ENTITLEMENT1,
            config.data.TEST_PRODUCT_MULTIPLE_ENTITLEMENTS.ENTITLEMENT2,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

    @pytest.mark.skip_for_regions('wgs11')
    @pytest.allure.feature('server')
    @pytest.allure.story('grant product')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('quantity', [1, 2147483647, Parameters.RandomInt(2, 2147483646)])
    def test_grant_product_should_succeed_when_product_have_multi_curr_and_entitle(self, config, quantity):
        quantity = Parameters.evaluate(quantity)

        grant_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES_AND_ENTITLEMENTS.COUNTRY,
            config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES_AND_ENTITLEMENTS.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES_AND_ENTITLEMENTS.CODE,
                quantity
            )]
        )
        grant_response.assert_is_success()

        waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={
                config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES_AND_ENTITLEMENTS.CURRENCY1: quantity,
                config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES_AND_ENTITLEMENTS.CURRENCY2: quantity
            },
            to_check_entitlements={
                config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES_AND_ENTITLEMENTS.ENTITLEMENT1: quantity,
                config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES_AND_ENTITLEMENTS.ENTITLEMENT2: quantity
            }
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        waiter.wait('Did not get {} {} or {} and {} {} or {}\n{}'.format(
            quantity,
            config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES_AND_ENTITLEMENTS.CURRENCY1,
            config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES_AND_ENTITLEMENTS.CURRENCY2,
            quantity,
            config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES_AND_ENTITLEMENTS.ENTITLEMENT1,
            config.data.TEST_PRODUCT_MULTIPLE_CURRENCIES_AND_ENTITLEMENTS.ENTITLEMENT2,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

    @pytest.allure.feature('server')
    @pytest.allure.story('grant product')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_product_code', ['', None])
    def test_grant_product_should_fail_when_product_is_invalid(self, config, invalid_product_code):
        grant_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT.COUNTRY,
            config.data.TEST_PRODUCT.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(invalid_product_code, config.data.TEST_PRODUCT.AMOUNT)]
        )
        grant_response.expect_failure(result_code=ResponseMessage.UNKNOWN_PRODUCT)

    @pytest.allure.feature('server')
    @pytest.allure.story('grant product')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_product_code', [-1, 0, 'bad_product_code'])
    def test_grant_product_should_fail_when_product_not_found(self, config, invalid_product_code):
        grant_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT.COUNTRY,
            config.data.TEST_PRODUCT.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(invalid_product_code, config.data.TEST_PRODUCT.AMOUNT)]
        )
        grant_response.expect_failure(result_code=ResponseMessage.PRODUCT_NOT_FOUND)

    @pytest.allure.feature('server')
    @pytest.allure.story('grant product')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('quantity', [-1, 0, '', None])
    def test_grant_product_should_fail_when_quantity_is_invalid(self, config, quantity):
        grant_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT.COUNTRY,
            config.data.TEST_PRODUCT.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT.PRODUCT_CODE, quantity)]
        )
        grant_response.expect_failure(result_code=ResponseMessage.INVALID_AMOUNT)

    @pytest.allure.feature('server')
    @pytest.allure.story('grant product')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.allure.issue('PLAT-2516')
    @pytest.mark.parametrize('invalid_quantity', [2147483648, 'invalid_quantity'])
    def test_grant_product_should_fail_when_quantity_is_out_of_range_or_string(self, config, invalid_quantity):
        config.log.info("granting {} products".format(invalid_quantity))

        grant_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT.COUNTRY,
            config.data.TEST_PRODUCT.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT.PRODUCT_CODE, invalid_quantity)]
        )
        grant_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                      result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.feature('server')
    @pytest.allure.story('grant product')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('null_country', [None, 'ZZ'])
    def test_grant_product_should_fail_when_country_is_none(self, config, null_country):
        grant_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            null_country,
            config.data.TEST_PRODUCT.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT.PRODUCT_CODE, config.data.TEST_PRODUCT.AMOUNT)]
        )
        grant_response.expect_failure(result_code=ResponseMessage.COUNTRY_NOT_DEFINED)

    @pytest.allure.feature('server')
    @pytest.allure.story('grant product')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_country', [-1, 0, '', 'invalid_country'])
    def test_grant_product_should_fail_when_country_is_invalid(self, config, invalid_country):
        grant_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            invalid_country,
            config.data.TEST_PRODUCT.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT.PRODUCT_CODE, config.data.TEST_PRODUCT.AMOUNT)]
        )
        grant_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                      result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.feature('server')
    @pytest.allure.story('grant product')
    @pytest.allure.severity(severity_level.MINOR)
    def test_grant_product_should_fail_when_language_is_none(self, config):
        grant_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT.COUNTRY,
            None,  # language param is left out
            config.store.profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT.PRODUCT_CODE, config.data.TEST_PRODUCT.AMOUNT)]
        )
        grant_response.expect_failure(result_code=ResponseMessage.LANGUAGE_NOT_DEFINED)

    @pytest.allure.feature('server')
    @pytest.allure.story('grant product')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_language', [-1, 0, 'test'])
    def test_grant_product_should_succeed_when_invalid_language_has_five_or_less_characters(self, config,
                                                                                            invalid_language):
        grant_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT.COUNTRY,
            invalid_language,
            config.store.profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT.PRODUCT_CODE, config.data.TEST_PRODUCT.AMOUNT)]
        )
        grant_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('grant product')
    @pytest.allure.severity(severity_level.MINOR)
    def test_grant_product_should_fail_when_language_is_more_than_five_characters(self, config):
        grant_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT.COUNTRY,
            'invalid_language',
            config.store.profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT.PRODUCT_CODE, config.data.TEST_PRODUCT.AMOUNT)]
        )
        grant_response.expect_failure(result_code=ResponseMessage.ORDER_PROCESSING_ERROR)

    @pytest.allure.feature('server')
    @pytest.allure.story('grant product')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_profile_id', [-1, 0, .50, '', None])
    def test_grant_product_should_fail_when_profile_id_is_invalid(self, config, invalid_profile_id):
        grant_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT.COUNTRY,
            config.data.TEST_PRODUCT.LANGUAGE,
            invalid_profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT.PRODUCT_CODE, config.data.TEST_PRODUCT.AMOUNT)]
        )
        grant_response.expect_failure(result_code=ResponseMessage.INVALID_WGID)

    @pytest.allure.feature('server')
    @pytest.allure.story('grant product')
    @pytest.allure.severity(severity_level.MINOR)
    def test_grant_product_should_fail_when_profile_id_is_string(self, config):
        grant_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT.COUNTRY,
            config.data.TEST_PRODUCT.LANGUAGE,
            'bad_profile_id',
            [LegacyProductItem(config.data.TEST_PRODUCT.PRODUCT_CODE, config.data.TEST_PRODUCT.AMOUNT)]
        )
        grant_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                      result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.feature('server')
    @pytest.allure.story('grant product')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_transaction_id', [
        '00000000-0000-0000-0000-00000000000000',
        '00000000-0000-0000-0000-0000000000',
        '00000000-0000-XXXX-0000-000000000000',
        'bad_transaction_id',
        0,
        -1
    ])
    def test_grant_product_should_fail_when_transaction_id_is_invalid(self, config, invalid_transaction_id):
        grant_response = config.freya.server_gateway.grant_product(
            invalid_transaction_id,
            config.data.TEST_PRODUCT.COUNTRY,
            config.data.TEST_PRODUCT.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT.PRODUCT_CODE, config.data.TEST_PRODUCT.AMOUNT)]
        )
        grant_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                      result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)
