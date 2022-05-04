import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities
from integration.main.helpers.utils import random_transaction_id
from integration.main.request import RequestConstants, ResponseMessage


class TestCancelEntitlement(object):

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

        grant_response = config.freya.server_gateway.grant_entitlement(
            config.store.profile_id,
            config.data.TEST_ENTITLEMENT.ENTITLEMENT_CODE,
            1,
            tx_id=random_transaction_id()
        )
        grant_response.assert_is_success()
        config.store.transaction_id = grant_response.content['body']['transaction_id']

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(config.store.profile_id)
        delete_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('cancel entitlement')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_cancel_entitlement_should_succeed_when_grant_product(self, config, content_type):
        cancel_grant_product_response = config.freya.server_gateway.cancel_entitlement(
            config.store.profile_id,
            config.store.transaction_id,
            transaction_id=random_transaction_id(),
            content_type=content_type)
        cancel_grant_product_response.assert_is_success()

        inventory_response = config.freya.server_gateway.get_full_inventory(config.store.profile_id)
        inventory_response.assert_is_success()
        entitlements = inventory_response.content['body']['profile']['entitlements']
        assert_that(len(entitlements), equal_to(0))

    @pytest.allure.feature('server')
    @pytest.allure.story('cancel entitlement')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_profile_id', [-1, 0, .50, '', None])
    def test_cancel_entitlement_should_fail_when_profile_id_is_invalid(self, config, invalid_profile_id):
        cancel_grant_product_response = config.freya.server_gateway.cancel_entitlement(
            invalid_profile_id,
            config.store.transaction_id,
            transaction_id=random_transaction_id()
        )
        cancel_grant_product_response.expect_failure(result_code=ResponseMessage.INVALID_PROFILE_ID)

    @pytest.allure.feature('server')
    @pytest.allure.story('cancel entitlement')
    @pytest.allure.severity(severity_level.MINOR)
    def test_cancel_entitlement_should_fail_when_profile_id_is_string(self, config):
        cancel_grant_product_response = config.freya.server_gateway.cancel_entitlement(
            'invalid_profile_id',
            config.store.transaction_id,
            transaction_id=random_transaction_id()
        )
        cancel_grant_product_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                                     result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.feature('server')
    @pytest.allure.story('cancel entitlement')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_transaction_id', [
        '00000000-0000-0000-0000-00000000000000',
        '00000000-0000-0000-0000-0000000000',
        '00000000-0000-XXXX-0000-000000000000',
        'bad_transaction_id',
        0,
        -1
    ])
    def test_cancel_entitlement_should_fail_when_transaction_id_is_invalid(self, config, invalid_transaction_id):
        cancel_response = config.freya.server_gateway.cancel_entitlement(
            config.store.profile_id,
            invalid_transaction_id,
            transaction_id=random_transaction_id()
        )
        cancel_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                       result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)
