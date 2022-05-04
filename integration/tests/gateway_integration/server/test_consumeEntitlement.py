import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities, uuid
from integration.main.helpers.utils import random_transaction_id
from integration.main.request import RequestConstants
from integration.main.request.constants import ResponseMessage
from integration.main.services import LegacyProductItem


class TestConsumeEntitlement(object):

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
            config.data.TEST_PRODUCT_ENTITLEMENT.COUNTRY,
            config.data.TEST_PRODUCT_ENTITLEMENT.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT_ENTITLEMENT.CODE,
                               config.data.TEST_PRODUCT_ENTITLEMENT.AMOUNT)]
        )
        grant_product_response.assert_is_success()

        inventory_response = config.freya.server_gateway.get_full_inventory(config.store.profile_id)
        inventory_response.assert_is_success()
        inventory = inventory_response.content['body']['profile']

        entitlement = next((entitlement for entitlement in inventory['entitlements'] if
                            entitlement['code'] == config.data.TEST_PRODUCT_ENTITLEMENT.ENTITLEMENTS.CODE), None)
        assert_that(entitlement, not_none())
        assert_that(entitlement['amount'],
                    equal_to(config.data.TEST_PRODUCT_ENTITLEMENT.ENTITLEMENTS.AMOUNT))

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(config.store.profile_id)
        delete_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('consume entitlement')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_consume_entitlement_should_succeed_when_entitlement_is_consumed(self, config, content_type):
        consume_response = config.freya.server_gateway.consume_entitlement(
            config.store.profile_id,
            config.data.TEST_PRODUCT_ENTITLEMENT.ENTITLEMENTS.CODE,
            config.data.TEST_PRODUCT_ENTITLEMENT.ENTITLEMENTS.AMOUNT,
            tx_id=random_transaction_id(),
            content_type=content_type)
        consume_response.assert_is_success()

        assert_that(consume_response.content['body'], has_key('entitlement'))
        assert_that(consume_response.content['body']['entitlement']['amount'], equal_to(0))

        inventory_response = config.freya.server_gateway.get_full_inventory(config.store.profile_id)
        inventory_response.assert_is_success()
        inventory = inventory_response.content['body']['profile']

        entitlement = next((entitlement for entitlement in inventory['entitlements'] if
                            entitlement['code'] == config.data.TEST_PRODUCT_ENTITLEMENT.ENTITLEMENTS.CODE), None)
        assert_that(entitlement, none())

    @pytest.mark.skip_for_regions('trie')
    @pytest.allure.feature('server')
    @pytest.allure.story('consume entitlement')
    @pytest.allure.severity(severity_level.MINOR)
    def test_consume_entitlement_should_fail_when_quantity_to_consume_is_more_than_amount_held_in_inventory(self,
                                                                                                            config):
        consume_response = config.freya.server_gateway.consume_entitlement(
            config.store.profile_id,
            config.data.TEST_PRODUCT_ENTITLEMENT.ENTITLEMENTS.CODE,
            config.data.TEST_PRODUCT_ENTITLEMENT.ENTITLEMENTS.AMOUNT + 1,
            tx_id=random_transaction_id()
        )
        # Depot handler should be used for error
        consume_response.expect_failure(result_code=ResponseMessage.ENTITLEMENT_ILLEGAL_STATE_ERROR)

    @pytest.mark.skip_for_regions('trie')
    @pytest.allure.feature('server')
    @pytest.allure.story('consume entitlement')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_profile_id', [-1, 0, .50, '', None])
    def test_consume_entitlement_should_fail_when_profile_id_is_invalid(self, config, invalid_profile_id):
        consume_response = config.freya.server_gateway.consume_entitlement(
            invalid_profile_id,
            config.data.TEST_PRODUCT_ENTITLEMENT.ENTITLEMENTS.CODE,
            config.data.TEST_PRODUCT_ENTITLEMENT.ENTITLEMENTS.AMOUNT,
            tx_id=random_transaction_id()
        )
        consume_response.expect_failure(result_code=ResponseMessage.INVALID_PROFILE_ID)

    @pytest.allure.feature('server')
    @pytest.allure.story('consume entitlement')
    @pytest.allure.severity(severity_level.MINOR)
    def test_consume_entitlement_should_fail_when_profile_id_is_string(self, config):
        consume_response = config.freya.server_gateway.consume_entitlement(
            'invalid_profile_id',
            config.data.TEST_PRODUCT_ENTITLEMENT.ENTITLEMENTS.CODE,
            config.data.TEST_PRODUCT_ENTITLEMENT.ENTITLEMENTS.AMOUNT,
            tx_id=random_transaction_id()
        )
        consume_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                        result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.feature('server')
    @pytest.allure.story('consume entitlement')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_entitlement_code', ['', None])
    def test_consume_entitlement_should_fail_when_entitlement_code_is_invalid(self, config, invalid_entitlement_code):
        consume_response = config.freya.server_gateway.consume_entitlement(
            config.store.profile_id,
            invalid_entitlement_code,
            config.data.TEST_PRODUCT_ENTITLEMENT.ENTITLEMENTS.AMOUNT,
            tx_id=random_transaction_id()
        )
        # Depot handler should be used for error
        consume_response.expect_failure(result_code=ResponseMessage.COMMON_VALIDATION_ERROR)

    @pytest.mark.skip_for_regions('trie')
    @pytest.allure.feature('server')
    @pytest.allure.story('consume entitlement')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('bad_entitlement_code', [
        'bad_entitlement_code',
        'SfUxojCbtW8Nk533gCPNzhSW79AkZp8y90ojWtZzhnxBnE9Mu5IIvjE6ArsZ3ElfeuXg98lTKdaO4nhuFkcR6VFrEued3eZ21Sdn',
        -1
    ])
    def test_consume_entitlement_should_fail_when_entitlement_code_is_bad(self, config, bad_entitlement_code):
        consume_response = config.freya.server_gateway.consume_entitlement(
            config.store.profile_id,
            bad_entitlement_code,
            config.data.TEST_PRODUCT_ENTITLEMENT.ENTITLEMENTS.AMOUNT,
            tx_id=random_transaction_id()
        )
        # Depot handler should be used for error
        consume_response.expect_failure(result_code=ResponseMessage.ENTITLEMENT_NOT_FOUND)

    @pytest.mark.skip(reason='DEPOT-793')
    @pytest.mark.skip_for_regions('trie')
    @pytest.allure.feature('server')
    @pytest.allure.story('consume entitlement')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_entitlement_amount', [-1, 0, '', None])
    def test_consume_entitlement_should_success_when_entitlement_amount_is_invalid(self, config,
                                                                                   invalid_entitlement_amount):
        consume_response = config.freya.server_gateway.consume_entitlement(
            config.store.profile_id,
            config.data.TEST_PRODUCT_ENTITLEMENT.ENTITLEMENTS.CODE,
            invalid_entitlement_amount,
            tx_id=random_transaction_id()
        )
        # Depot handler should be used for error
        # New flow - positive. No validation on amount param in contract.
        # Maybe contract will be redesigned w/ validation
        consume_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('consume entitlement')
    @pytest.allure.severity(severity_level.MINOR)
    def test_consume_entitlement_should_fail_when_entitlement_amount_is_string(self, config):
        consume_response = config.freya.server_gateway.consume_entitlement(
            config.store.profile_id,
            config.data.TEST_PRODUCT_ENTITLEMENT.ENTITLEMENTS.CODE,
            'bad_entitlement_amount',
            tx_id=random_transaction_id()
        )
        consume_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                        result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)
