import uuid

import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities
from integration.main.helpers.utils import random_transaction_id
from integration.main.request import RequestConstants, ResponseMessage
from integration.main.session import Parameters


class TestGrantEntitlement(object):

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
    @pytest.allure.story('grant entitlement')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    @pytest.mark.parametrize('quantity', [1, 2147483647, Parameters.RandomInt(2, 2147483646)])
    def test_grant_entitlement_will_grant_entitlement_to_profile(self, config, content_type, quantity):
        quantity = Parameters.evaluate(quantity)

        grant_response = config.freya.server_gateway.grant_entitlement(
            config.store.profile_id,
            config.data.TEST_ENTITLEMENT.ENTITLEMENT_CODE,
            quantity,
            tx_id=random_transaction_id(),
            content_type=content_type)
        grant_response.assert_is_success()

        assert_that(grant_response.content['body'], has_key('entitlement'))
        assert_that(grant_response.content['body']['entitlement']['amount'], equal_to(quantity))

        inventory_response = config.freya.server_gateway.get_full_inventory(config.store.profile_id)
        inventory_response.assert_is_success()
        inventory = inventory_response.content['body']['profile']

        entitlement = next((entitlement for entitlement in inventory['entitlements']
                            if entitlement['code'] == config.data.TEST_ENTITLEMENT.ENTITLEMENT_CODE), None)
        assert_that(entitlement, not_none())
        assert_that(entitlement['amount'], equal_to(quantity))
        assert_that(entitlement['code'], equal_to(config.data.TEST_ENTITLEMENT.ENTITLEMENT_CODE))

    @pytest.allure.feature('server')
    @pytest.allure.story('grant entitlement')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.skip(reason='DEPOT-793')
    @pytest.mark.parametrize('invalid_amount', [-1, 0, .50, '', None])
    def test_grant_entitlement_should_fail_when_amount_is_invalid(self, config, invalid_amount):
        grant_response = config.freya.server_gateway.grant_entitlement(config.store.profile_id,
                                                                       config.data.TEST_ENTITLEMENT.ENTITLEMENT_CODE,
                                                                       invalid_amount,
                                                                       tx_id=random_transaction_id()
                                                                       )
        grant_response.expect_failure(result_code=ResponseMessage.INVALID_AMOUNT)

    @pytest.allure.feature('server')
    @pytest.allure.story('grant entitlement')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('faulty_amount', [2147483648, 'string_amount'])
    def test_grant_entitlement_should_fail_when_amount_is_string_or_out_of_range(self, config, faulty_amount):
        grant_response = config.freya.server_gateway.grant_entitlement(config.store.profile_id,
                                                                       config.data.TEST_ENTITLEMENT.ENTITLEMENT_CODE,
                                                                       faulty_amount,
                                                                       tx_id=random_transaction_id()
                                                                       )
        grant_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                      result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.feature('server')
    @pytest.allure.story('grant entitlement')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_profile_id', [-1, 0, .50, '', None])
    def test_grant_entitlement_should_fail_when_profile_id_is_invalid(self, config, invalid_profile_id):
        grant_response = config.freya.server_gateway.grant_entitlement(invalid_profile_id,
                                                                       config.data.TEST_ENTITLEMENT.ENTITLEMENT_CODE,
                                                                       config.data.TEST_ENTITLEMENT.AMOUNT,
                                                                       tx_id=random_transaction_id()
                                                                       )
        grant_response.expect_failure(result_code=ResponseMessage.INVALID_PROFILE_ID)

    @pytest.allure.feature('server')
    @pytest.allure.story('grant entitlement')
    @pytest.allure.severity(severity_level.MINOR)
    def test_grant_entitlement_should_fail_when_profile_id_is_string(self, config):
        grant_response = config.freya.server_gateway.grant_entitlement('invalid_profile_id',
                                                                       config.data.TEST_ENTITLEMENT.ENTITLEMENT_CODE,
                                                                       config.data.TEST_ENTITLEMENT.AMOUNT,
                                                                       tx_id=random_transaction_id()
                                                                       )
        grant_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                      result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.feature('server')
    @pytest.allure.story('grant entitlement')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_entitlement_code', ['', None])
    def test_grant_entitlement_should_fail_when_entitlement_code_is_empty_or_none(self, config,
                                                                                  invalid_entitlement_code):
        grant_response = config.freya.server_gateway.grant_entitlement(config.store.profile_id,
                                                                       invalid_entitlement_code,
                                                                       config.data.TEST_ENTITLEMENT.AMOUNT,
                                                                       tx_id=random_transaction_id()
                                                                       )
        # Depot handler should be used for error
        grant_response.expect_failure(result_code=ResponseMessage.COMMON_VALIDATION_ERROR)

    @pytest.allure.feature('server')
    @pytest.allure.story('grant entitlement')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('bad_entitlement_code', [-1, 0, 'invalid_entitlement_code'])
    def test_grant_entitlement_should_fail_when_entitlement_code_is_invalid(self, config, bad_entitlement_code):
        grant_response = config.freya.server_gateway.grant_entitlement(config.store.profile_id, bad_entitlement_code,
                                                                       config.data.TEST_ENTITLEMENT.AMOUNT,
                                                                       tx_id=random_transaction_id())
        grant_response.expect_failure(result_code=ResponseMessage.ENTITLEMENT_NOT_FOUND)

    @pytest.allure.feature('server')
    @pytest.allure.story('grant entitlement')
    @pytest.allure.severity(severity_level.NORMAL)
    def test_grant_entitlement_should_fail_when_transaction_id_is_reused(self, config):
        """
        The bug in question is as follows:
            granting 1 entitlement to id #5 and then 1 entitlement to id #6 using the same transaction_id
            between both requests will result in id #6 now having 2 entitlements.
            This is because in the database, the transaction_id was not unique and previous
            query versions would look for only a transaction_id instead of including root_id as well.
        """

        config.log.info('generate a transaction_id to be reused, and grant an entitlement to account #1')
        transaction_id = str(uuid.uuid4())
        grant_response1 = config.freya.server_gateway.grant_entitlement(
            config.store.profile_id,
            config.data.TEST_ENTITLEMENT.ENTITLEMENT_CODE,
            config.data.TEST_ENTITLEMENT.AMOUNT,
            tx_id=transaction_id
        )
        grant_response1.assert_is_success()

        config.log.info('create a second account, and grant it an entitlement using the same transaction_id')
        account_two_info = AccountUtilities.create_account()
        account_created = config.spa.http.create_account(account_two_info.__dict__)
        account_created.assert_is_success()
        update_account = config.spa.http.update(account_created.content['id'],
                                                game=config.environment['test_title_pgn'])
        update_account.assert_is_success()
        profile_two_id = account_created.content['id']

        grant_response2 = config.freya.server_gateway.grant_entitlement(
            profile_two_id,
            config.data.TEST_ENTITLEMENT.ENTITLEMENT_CODE,
            config.data.TEST_ENTITLEMENT.AMOUNT,
            tx_id=transaction_id
        )
        grant_response2.assert_is_success()

        config.log.info(
            'fetch inventory of the second account, and ensure that it does not contain any extra entitlements')
        inventory_response = config.freya.server_gateway.get_full_inventory(profile_two_id)
        inventory_response.assert_is_success()
        inventory = inventory_response.content['body']['profile']

        entitlement = next((entitlement for entitlement in inventory['entitlements'] if
                            entitlement['code'] == config.data.TEST_ENTITLEMENT.ENTITLEMENT_CODE), None)
        assert_that(entitlement['amount'], equal_to(config.data.TEST_ENTITLEMENT.AMOUNT))
