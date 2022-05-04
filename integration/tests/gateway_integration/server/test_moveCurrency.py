import uuid

import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities
from integration.main.request import RequestConstants
from integration.main.request.response import ResponseMessage
from integration.main.services import LegacyProductItem


class TestMoveCurrency(object):

    @pytest.fixture(autouse=True)
    def setup(self, config):
        ###
        # Test setup
        config.log.info('creating two accounts')
        config.log.info('creating account 1')
        config.store.account_one = AccountUtilities.create_account()
        account_one_created = config.spa.http.create_account(config.store.account_one.__dict__)
        account_one_created.assert_is_success()
        update_account = config.spa.http.update(account_one_created.content['id'],
                                                game=config.environment['test_title_pgn'])
        update_account.assert_is_success()
        config.store.account_one_wgid = account_one_created.content['id']
        config.store.profile_one_id = account_one_created.content['id']

        config.log.info('creating account 2')
        config.store.account_two = AccountUtilities.create_account()
        account_two_created = config.spa.http.create_account(config.store.account_two.__dict__)
        account_two_created.assert_is_success()
        update_account = config.spa.http.update(account_two_created.content['id'],
                                                game=config.environment['test_title_pgn'])
        update_account.assert_is_success()
        config.store.account_two_wgid = account_two_created.content['id']
        config.store.profile_two_id = account_two_created.content['id']

        grant_product_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT.COUNTRY,
            config.data.TEST_PRODUCT.LANGUAGE,
            config.store.profile_one_id,
            [LegacyProductItem(config.data.TEST_PRODUCT.PRODUCT_CODE,
                               config.data.TEST_PRODUCT.AMOUNT)]
        )
        grant_product_response.assert_is_success()

        inventory_response = config.freya.server_gateway.get_full_inventory(config.store.profile_one_id)
        inventory_response.assert_is_success()
        inventory = inventory_response.content['body']['profile']

        currency = next((currency for currency in inventory['currencies'] if
                         currency['code'] == config.data.TEST_PRODUCT.CURRENCIES.CODE), None)
        assert_that(currency, not_none())
        assert_that(currency['amount'], equal_to(str(config.data.TEST_PRODUCT.CURRENCIES.AMOUNT)))

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_one_response = config.spa.http.delete_account(config.store.account_one_wgid)
        delete_one_response.assert_is_success()

        delete_two_response = config.spa.http.delete_account(config.store.account_two_wgid)
        delete_two_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('move currency')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_move_currency_should_succeed_when_transferring_from_one_account_to_another(self, config, content_type):
        move_response = config.freya.server_gateway.move_currency(
            str(uuid.uuid4()),
            config.store.profile_one_id,
            config.store.profile_two_id,
            config.data.TEST_PRODUCT.CURRENCIES.CODE,
            str(config.data.TEST_PRODUCT.CURRENCIES.AMOUNT),
            content_type=content_type)
        move_response.assert_is_success()

        inventory_response = config.freya.server_gateway.get_full_inventory(config.store.profile_one_id)
        inventory_response.assert_is_success()
        inventory = inventory_response.content['body']['profile']

        currency = next((currency for currency in inventory['currencies'] if
                         currency['code'] == config.data.TEST_PRODUCT.CURRENCIES.CODE), None)
        assert_that(currency, none())

        inventory_response = config.freya.server_gateway.get_full_inventory(config.store.profile_two_id)
        inventory_response.assert_is_success()
        inventory = inventory_response.content['body']['profile']

        currency = next((currency for currency in inventory['currencies'] if
                         currency['code'] == config.data.TEST_PRODUCT.CURRENCIES.CODE), None)
        assert_that(currency, not_none())
        assert_that(currency['amount'], equal_to(str(config.data.TEST_PRODUCT.CURRENCIES.AMOUNT)))

    @pytest.allure.feature('server')
    @pytest.allure.story('move currency')
    @pytest.allure.severity(severity_level.MINOR)
    def test_move_currency_should_fail_when_transferring_to_same_account(self, config):
        move_response = config.freya.server_gateway.move_currency(
            str(uuid.uuid4()),
            config.store.profile_one_id,
            config.store.profile_one_id,
            config.data.TEST_PRODUCT.CURRENCIES.CODE,
            str(config.data.TEST_PRODUCT.CURRENCIES.AMOUNT))
        move_response.expect_failure(result_code='ERROR',
                                     result_message='source and destination profiles may not be the same')

    @pytest.allure.feature('server')
    @pytest.allure.story('move currency')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_profile_one_id, result_code', [(-1, ResponseMessage.INVALID_PROFILE_ID),
                                                                     (0, 'ERROR'),
                                                                     (.50, 'ERROR'),
                                                                     ('', 'ERROR'),
                                                                     (None, 'ERROR')])
    def test_move_currency_should_fail_when_source_profile_id_is_invalid(self, config,
                                                                         invalid_profile_one_id, result_code):
        move_response = config.freya.server_gateway.move_currency(
            str(uuid.uuid4()),
            invalid_profile_one_id,
            config.store.profile_two_id,
            config.data.TEST_PRODUCT.CURRENCIES.CODE,
            str(config.data.TEST_PRODUCT.CURRENCIES.AMOUNT))
        move_response.expect_failure(result_code=result_code)

    @pytest.allure.feature('server')
    @pytest.allure.story('move currency')
    @pytest.allure.severity(severity_level.MINOR)
    def test_move_currency_should_fail_when_source_profile_id_is_string(self, config):
        move_response = config.freya.server_gateway.move_currency(
            str(uuid.uuid4()),
            'invalid_profile_one_id',
            config.store.profile_two_id,
            config.data.TEST_PRODUCT.CURRENCIES.CODE,
            str(config.data.TEST_PRODUCT.CURRENCIES.AMOUNT))
        move_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                     result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.feature('server')
    @pytest.allure.story('move currency')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_profile_two_id, result_code', [(-1, ResponseMessage.INVALID_PROFILE_ID),
                                                                     (0, 'ERROR'),
                                                                     (.50, 'ERROR'),
                                                                     ('', 'ERROR'),
                                                                     (None, 'ERROR')])
    def test_move_currency_should_fail_when_destination_profile_id_is_invalid(self, config,
                                                                              invalid_profile_two_id, result_code):
        move_response = config.freya.server_gateway.move_currency(
            str(uuid.uuid4()),
            config.store.profile_two_id,
            invalid_profile_two_id,
            config.data.TEST_PRODUCT.CURRENCIES.CODE,
            str(config.data.TEST_PRODUCT.CURRENCIES.AMOUNT))
        move_response.expect_failure(result_code=result_code)

    @pytest.allure.feature('server')
    @pytest.allure.story('move currency')
    @pytest.allure.severity(severity_level.MINOR)
    def test_move_currency_should_fail_when_destination_profile_id_is_string(self, config):
        move_response = config.freya.server_gateway.move_currency(
            str(uuid.uuid4()),
            config.store.profile_two_id,
            'invalid_profile_two_id',
            config.data.TEST_PRODUCT.CURRENCIES.CODE,
            str(config.data.TEST_PRODUCT.CURRENCIES.AMOUNT))
        move_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                     result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.feature('server')
    @pytest.allure.story('move currency')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_currency_code', [-1, 0, 'invalid_currency_code'])
    def test_move_currency_should_fail_when_currency_code_is_invalid(self, config, invalid_currency_code):
        move_response = config.freya.server_gateway.move_currency(
            str(uuid.uuid4()),
            config.store.profile_one_id,
            config.store.profile_two_id,
            invalid_currency_code,
            str(config.data.TEST_PRODUCT.CURRENCIES.AMOUNT))
        move_response.expect_failure(result_code=ResponseMessage.UNKNOWN_CURRENCY_CODE)

    @pytest.allure.feature('server')
    @pytest.allure.story('move currency')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('bad_currency_code', ['', None])
    def test_move_currency_should_fail_when_currency_code_is_empty_string_or_none(self, config, bad_currency_code):
        move_response = config.freya.server_gateway.move_currency(
            str(uuid.uuid4()),
            config.store.profile_one_id,
            config.store.profile_two_id,
            bad_currency_code,
            str(config.data.TEST_PRODUCT.CURRENCIES.AMOUNT))
        move_response.expect_failure(result_code=ResponseMessage.INVALID_CURRENCY_CODE)

    @pytest.allure.feature('server')
    @pytest.allure.story('move currency')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_amount', [-1, 0])
    def test_move_currency_should_fail_when_amount_is_zero_or_negative(self, config, invalid_amount):
        move_response = config.freya.server_gateway.move_currency(
            str(uuid.uuid4()),
            config.store.profile_one_id,
            config.store.profile_two_id,
            config.data.TEST_PRODUCT.CURRENCIES.CODE,
            invalid_amount)
        move_response.expect_failure(result_code='ERROR')

    @pytest.allure.feature('server')
    @pytest.allure.story('move currency')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('bad_amount', [2147483648, 'invalid_amount', None, ''])
    def test_move_currency_should_fail_when_amount_is_invalid(self, config, bad_amount):
        move_response = config.freya.server_gateway.move_currency(
            str(uuid.uuid4()),
            config.store.profile_one_id,
            config.store.profile_two_id,
            config.data.TEST_PRODUCT.CURRENCIES.CODE,
            bad_amount)
        move_response.expect_failure(result_code=ResponseMessage.INVALID_CURRENCY_AMOUNT)

    @pytest.allure.feature('server')
    @pytest.allure.story('move currency')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_transaction_id', [
        '00000000-0000-0000-0000-00000000000000',
        '00000000-0000-0000-0000-0000000000',
        '00000000-0000-XXXX-0000-000000000000',
        'bad_transaction_id',
        0,
        -1
    ])
    def test_move_currency_should_fail_when_transaction_id_is_invalid(self, config, invalid_transaction_id):
        move_response = config.freya.server_gateway.move_currency(
            invalid_transaction_id,
            config.store.profile_one_id,
            config.store.profile_two_id,
            config.data.TEST_PRODUCT.CURRENCIES.CODE,
            str(config.data.TEST_PRODUCT.CURRENCIES.AMOUNT))
        move_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                     result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.feature('server')
    @pytest.allure.story('move currency')
    @pytest.allure.severity(severity_level.MINOR)
    def test_move_currency_should_fail_when_transaction_id_is_none(self, config):
        move_response = config.freya.server_gateway.move_currency(
            None,
            config.store.profile_one_id,
            config.store.profile_two_id,
            config.data.TEST_PRODUCT.CURRENCIES.CODE,
            str(config.data.TEST_PRODUCT.CURRENCIES.AMOUNT))
        move_response.expect_failure(result_code='ERROR', result_message='transaction Id must not be null')
