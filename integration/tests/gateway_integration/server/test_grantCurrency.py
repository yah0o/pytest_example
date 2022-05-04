import uuid

import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities, WaitOn, ReturnValue, InventoryUtilities
from integration.main.request import RequestConstants, ResponseMessage
from integration.main.session import Parameters


class TestGrantCurrency(object):

    @pytest.fixture(autouse=True)
    def setup(self, config):
        ###
        # Test setup
        config.store.account = AccountUtilities.create_account()
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
    @pytest.allure.story('grant currency')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    @pytest.mark.parametrize('quantity', [1, 2147483647, Parameters.RandomInt(2, 2147483646)])
    def test_grant_currency_should_grant_test_currency_to_account_with_profile_id(self, config, content_type, quantity):
        quantity = Parameters.evaluate(quantity)

        config.log.info('granting {} amount of {}'.format(quantity, config.data.TEST_CURRENCY.CURRENCY_CODE))
        grant_response = config.freya.server_gateway.grant_currency(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.data.TEST_CURRENCY.CURRENCY_CODE,
            str(quantity),
            content_type=content_type)
        grant_response.assert_is_success()

        assert_that(grant_response.content['body'], has_key('transaction_id'))
        assert_that(grant_response.content['body'], has_key('currency'))
        assert_that(grant_response.content['body']['currency']['code'],
                    equal_to(config.data.TEST_CURRENCY.CURRENCY_CODE))
        assert_that(grant_response.content['body']['currency']['amount'], equal_to(str(quantity)))

        inventory_waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={config.data.TEST_CURRENCY.CURRENCY_CODE: quantity},
            to_check_entitlements={}
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)
        inventory_waiter.wait('Did not get {} {} in inventory\n{}'.format(
            config.data.TEST_CURRENCY.CURRENCY_CODE,
            quantity,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

    @pytest.allure.feature('server')
    @pytest.allure.story('grant currency')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('quantity', [-1, 0, 2147483648, 'bad_number', None, ''])
    def test_grant_currency_should_fail_when_amount_is_invalid(self, config, quantity):
        config.log.info('granting {} amount of {}'.format(quantity, config.data.TEST_CURRENCY.CURRENCY_CODE))

        invalid_grant_response = config.freya.server_gateway.grant_currency(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.data.TEST_CURRENCY.CURRENCY_CODE,
            str(quantity)
        )
        invalid_grant_response.expect_failure(result_code=ResponseMessage.INVALID_AMOUNT)

    @pytest.allure.feature('server')
    @pytest.allure.story('grant currency')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_currency_code', [-1, 0, 2147483648, 'invalid_currency_code'])
    def test_grant_currency_should_fail_when_currency_code_is_invalid(self, config, invalid_currency_code):
        grant_response = config.freya.server_gateway.grant_currency(
            str(uuid.uuid4()),
            config.store.profile_id,
            invalid_currency_code,
            config.data.TEST_CURRENCY.AMOUNT
        )
        grant_response.expect_failure(result_code=ResponseMessage.UNKNOWN_CURRENCY_CODE, code=200)

    @pytest.allure.feature('server')
    @pytest.allure.story('grant currency')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('empty_currency_code', [None, ''])
    def test_grant_currency_should_fail_when_currency_code_is_empty(self, config, empty_currency_code):
        invalid_grant_response = config.freya.server_gateway.grant_currency(
            str(uuid.uuid4()),
            config.store.profile_id,
            empty_currency_code,
            config.data.TEST_CURRENCY.AMOUNT
        )
        invalid_grant_response.expect_failure(result_code=ResponseMessage.INVALID_CURRENCY_CODE)

    @pytest.allure.feature('server')
    @pytest.allure.story('grant currency')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_profile_id', [-1, 0, .50, '', None])
    def test_grant_currency_should_fail_when_profile_id_is_invalid(self, config, invalid_profile_id):
        grant_response = config.freya.server_gateway.grant_currency(
            str(uuid.uuid4()),
            invalid_profile_id,
            config.data.TEST_CURRENCY.CURRENCY_CODE,
            config.data.TEST_CURRENCY.AMOUNT
        )
        grant_response.expect_failure(result_code=ResponseMessage.INVALID_PROFILE_ID, code=200)

    @pytest.allure.feature('server')
    @pytest.allure.story('grant currency')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_transaction_id', [
        '00000000-0000-0000-0000-00000000000000',
        '00000000-0000-0000-0000-0000000000',
        '00000000-0000-XXXX-0000-000000000000',
        'bad_order_id',
        0,
        -1
    ])
    def test_grant_currency_should_fail_when_transaction_id_is_invalid(self, config, invalid_transaction_id):
        grant_response = config.freya.server_gateway.grant_currency(
            invalid_transaction_id,
            config.store.profile_id,
            config.data.TEST_CURRENCY.CURRENCY_CODE,
            config.data.TEST_CURRENCY.AMOUNT
        )
        grant_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                      result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.feature('server')
    @pytest.allure.story('grant currency')
    @pytest.allure.severity(severity_level.NORMAL)
    def test_grant_currency_should_fail_when_using_a_duplicate_transaction_id(self, config):
        tx_id = uuid.uuid4()
        grant_response = config.freya.server_gateway.grant_currency(
            str(tx_id),
            config.store.profile_id,
            config.data.TEST_CURRENCY.CURRENCY_CODE,
            config.data.TEST_CURRENCY.AMOUNT
        )
        grant_response.assert_is_success()

        update_response = config.freya.server_gateway.grant_currency(
            str(tx_id),
            config.store.profile_id,
            config.data.TEST_CURRENCY.CURRENCY_CODE,
            config.data.TEST_CURRENCY.AMOUNT
        )
        update_response.assert_is_success()
        assert_that(
            update_response.content['body'],
            has_entries({
                'result_code': equal_to('ALREADY_PROCESSED'),
                'result_message': equal_to('Transaction already processed')
            })
        )
