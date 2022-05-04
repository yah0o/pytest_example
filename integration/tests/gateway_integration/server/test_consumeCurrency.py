import uuid

import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities, WaitOn, ReturnValue, InventoryUtilities
from integration.main.request import RequestConstants
from integration.main.request.constants import ResponseMessage
from integration.main.services import LegacyProductItem


class TestConsumeCurrency(object):

    @pytest.fixture(autouse=True)
    def setup(self, config):
        ###
        # Test setup
        account = AccountUtilities.create_account()
        account_created = config.spa.http.create_account(account.__dict__)
        account_created.assert_is_success()
        update_account = config.spa.http.update(account_created.content['id'],
                                                game=config.environment['test_title_pgn'])
        update_account.assert_is_success()

        config.store.profile_id = account_created.content['id']

        grant_product_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT.COUNTRY,
            config.data.TEST_PRODUCT.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT.PRODUCT_CODE,
                               config.data.TEST_PRODUCT.AMOUNT)]
        )
        grant_product_response.assert_is_success()

        waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={config.data.TEST_PRODUCT.CURRENCIES.CODE:
                                     config.data.TEST_PRODUCT.CURRENCIES.AMOUNT},
            to_check_entitlements={}
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        waiter.wait('Inventory was not granted {} {}\n{}'.format(
            config.data.TEST_PRODUCT.CURRENCIES.CODE,
            config.data.TEST_PRODUCT.CURRENCIES.AMOUNT,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(config.store.profile_id)
        delete_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('consume currency')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_consume_currency_should_succeed_when_currency_is_consumed(self, config, content_type):
        consume_response = config.freya.server_gateway.consume_currency(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.data.TEST_PRODUCT.CURRENCIES.CODE,
            str(config.data.TEST_PRODUCT.CURRENCIES.AMOUNT),
            content_type=content_type)
        consume_response.assert_is_success()

        assert_that(consume_response.content['body'], has_key('transaction_id'))
        assert_that(consume_response.content['body'], has_key('currency'))
        assert_that(consume_response.content['body']['currency']['amount'], equal_to(str(0)))
        assert_that(consume_response.content['body']['currency']['code'],
                    equal_to(config.data.TEST_PRODUCT.CURRENCIES.CODE))

        inventory_response = config.freya.server_gateway.get_full_inventory(
            config.store.profile_id)
        inventory_response.assert_is_success()
        inventory = inventory_response.content['body']['profile']

        currency = next((currency for currency in inventory['currencies'] if
                         currency['code'] == config.data.TEST_PRODUCT.CURRENCIES.CODE), None)

        assert_that(currency, none())

    @pytest.allure.feature('server')
    @pytest.allure.story('consume currency')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_profile_id', [-1, 0, .50, '', None])
    def test_consume_currency_should_fail_when_profile_id_is_invalid(self, config, invalid_profile_id):
        consume_response = config.freya.server_gateway.consume_currency(
            str(uuid.uuid4()),
            invalid_profile_id,
            config.data.TEST_PRODUCT.CURRENCIES.CODE,
            str(config.data.TEST_PRODUCT.CURRENCIES.AMOUNT))
        consume_response.expect_failure(result_code=ResponseMessage.INVALID_PROFILE_ID)

    @pytest.allure.feature('server')
    @pytest.allure.story('consume currency')
    @pytest.allure.severity(severity_level.MINOR)
    def test_consume_currency_should_fail_when_profile_id_is_string(self, config):
        consume_response = config.freya.server_gateway.consume_currency(
            str(uuid.uuid4()),
            'invalid_profile_id',
            config.data.TEST_PRODUCT.CURRENCIES.CODE,
            str(config.data.TEST_PRODUCT.CURRENCIES.AMOUNT))
        consume_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                        result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.mark.skip_for_regions('trie')
    @pytest.allure.feature('server')
    @pytest.allure.story('consume currency')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_currency_code', [
        0,
        'bad_currency_code',
        'HWid8viSdIYjiIXYNRcWLco3Xkqb3iq2CHhqulb3D7nJczwf1cD9DSq6l7RTxIwz17tEjLYc583aUfGhc6CRZRchvtQ0uZTaf1Dv'
    ])
    def test_consume_currency_should_fail_when_currency_code_is_invalid(self, config, invalid_currency_code):
        consume_response = config.freya.server_gateway.consume_currency(
            str(uuid.uuid4()),
            config.store.profile_id,
            invalid_currency_code,
            str(config.data.TEST_PRODUCT.CURRENCIES.AMOUNT))
        consume_response.expect_failure(result_code=ResponseMessage.UNKNOWN_CURRENCY_CODE)

    @pytest.allure.feature('server')
    @pytest.allure.story('consume currency')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('blank_currency_code', ['', None])
    @pytest.mark.xfail(
        reason='Error result codes changed; not yet available on all environments',
        raises=AssertionError
    )
    def test_consume_currency_should_fail_when_currency_code_is_empty_string_or_none(self, config, blank_currency_code):
        consume_response = config.freya.server_gateway.consume_currency(
            str(uuid.uuid4()),
            config.store.profile_id,
            blank_currency_code,
            str(config.data.TEST_PRODUCT.CURRENCIES.AMOUNT))
        consume_response.expect_failure(result_code=ResponseMessage.INVALID_CURRENCY_CODE)

    @pytest.mark.skip_for_regions('trie')
    @pytest.allure.feature('server')
    @pytest.allure.story('consume currency')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_amount', [
        '-1',
        0,
        .50,
        '',
        None,
        'bad_amount',
        'oO5r4BDwnVAEzWqv1QxcQDAA3dj3VXMefRgwvjemQHeQaMy2MO4De0RB5T9sPbzkZxBfoczs801M52w4nm3OcAnWeq9eJ2HEIr40'
    ])
    def test_consume_currency_should_fail_when_amount_is_invalid(self, config, invalid_amount):
        consume_response = config.freya.server_gateway.consume_currency(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.data.TEST_PRODUCT.CURRENCIES.CODE,
            invalid_amount)
        consume_response.expect_failure(result_code=ResponseMessage.INVALID_AMOUNT)

    @pytest.mark.skip_for_regions('trie')
    @pytest.allure.feature('server')
    @pytest.allure.story('consume currency')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_transaction_id', [
        '00000000-0000-0000-0000-00000000000000',
        '00000000-0000-0000-0000-0000000000',
        '00000000-0000-XXXX-0000-000000000000',
        'bad_transaction_id',
        0,
        -1
    ])
    def test_consume_currency_should_fail_when_transaction_id_is_invalid(self, config, invalid_transaction_id):
        consume_response = config.freya.server_gateway.consume_currency(
            invalid_transaction_id,
            config.store.profile_id,
            config.data.TEST_PRODUCT.CURRENCIES.CODE,
            str(config.data.TEST_PRODUCT.CURRENCIES.AMOUNT))
        consume_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                        result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.feature('server')
    @pytest.allure.story('consume currency')
    @pytest.allure.severity(severity_level.MINOR)
    def test_consume_currency_should_fail_when_transaction_id_is_none(self, config):
        consume_response = config.freya.server_gateway.consume_currency(
            None,
            config.store.profile_id,
            config.data.TEST_PRODUCT.CURRENCIES.CODE,
            str(config.data.TEST_PRODUCT.CURRENCIES.AMOUNT))
        consume_response.expect_failure(result_code=ResponseMessage.NULL_TRANSACTION_ID)

    @pytest.allure.feature('server')
    @pytest.allure.story('consume currency')
    @pytest.allure.severity(severity_level.NORMAL)
    def test_consume_currency_should_succeed_when_consume_twice_with_same_tx_id(self, config):
        tx_id = str(uuid.uuid4())
        consume_response = config.freya.server_gateway.consume_currency(
            tx_id,
            config.store.profile_id,
            config.data.TEST_PRODUCT.CURRENCIES.CODE,
            str(100))
        consume_response.assert_is_success()
        consume_response2 = config.freya.server_gateway.consume_currency(
            tx_id,
            config.store.profile_id,
            config.data.TEST_PRODUCT.CURRENCIES.CODE,
            str(100))
        consume_response2.assert_is_success()
        assert_that(consume_response2.content['body']['result_code'], equal_to('ALREADY_PROCESSED'))
