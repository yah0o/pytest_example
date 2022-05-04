import time
import uuid

import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities
from integration.main.helpers.utils import random_transaction_id
from integration.main.request import RequestConstants, ResponseMessage
from integration.main.services import LegacyProductItem


@pytest.mark.skip_for_regions('trie')
class TestReverseEntitlement(object):

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

        # need the active catalog and this call gets the working which may not be active!
        title_version_response = config.cats.service.active_catalogs(title_code=config.environment['integration_title'])
        title_version_response.assert_is_success()

        config.store.active_catalog = str(title_version_response.content[0]['catalog_code'])
        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(config.store.wgid)
        delete_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('reverse entitlement')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_reverse_entitlement_should_succeed_when_granting_entitlement(self, config, content_type):
        grant_entitlement_response = config.freya.server_gateway.grant_entitlement(
            config.store.profile_id,
            config.data.TEST_ENTITLEMENT.ENTITLEMENT_CODE,
            config.data.TEST_ENTITLEMENT.AMOUNT,
            tx_id=random_transaction_id()
        )
        grant_entitlement_response.assert_is_success()
        transaction_id = grant_entitlement_response.content['body']['transaction_id']
        assert_that(transaction_id, is_not(None))

        reverse_response = config.freya.server_gateway.reverse_entitlement(config.store.wgid, transaction_id,
                                                                           str(uuid.uuid4()), content_type=content_type)
        reverse_response.assert_is_success()
        assert_that(reverse_response.content['body']['had_shortages'], equal_to(False))

    @pytest.allure.feature('server')
    @pytest.allure.story('reverse entitlement')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_reverse_entitlement_should_succeed_when_have_shortages(self, config, content_type):
        grant_response = config.freya.server_gateway.grant_entitlement(
            config.store.profile_id,
            config.data.TEST_ENTITLEMENT.ENTITLEMENT_CODE,
            config.data.TEST_ENTITLEMENT.AMOUNT,
            tx_id=random_transaction_id()
        )
        grant_response.assert_is_success()
        transaction_id = grant_response.content['body']['transaction_id']
        assert_that(transaction_id, is_not(None))

        consume_response = config.freya.server_gateway.consume_entitlement(
            config.store.profile_id,
            config.data.TEST_ENTITLEMENT.ENTITLEMENT_CODE,
            config.data.TEST_ENTITLEMENT.AMOUNT,
            tx_id=random_transaction_id()
        )
        consume_response.assert_is_success()

        reverse_response = config.freya.server_gateway.reverse_entitlement(
            config.store.wgid,
            transaction_id,
            str(uuid.uuid4()),
            content_type=content_type
        )
        reverse_response.assert_is_success()
        assert_that(reverse_response.content['body']['had_shortages'], equal_to(True))
        assert_that(reverse_response.content['body']['shortages'],
                    contains(config.data.TEST_ENTITLEMENT.ENTITLEMENT_CODE))
        assert_that(
            reverse_response.content['body']['shortages'][config.data.TEST_ENTITLEMENT.ENTITLEMENT_CODE],
            equal_to(config.data.TEST_ENTITLEMENT.AMOUNT))

    @pytest.allure.feature('server')
    @pytest.allure.story('reverse entitlement')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_reverse_entitlement_should_succeed_when_transaction_in_pending_state(self, config, content_type):
        # will create a transaction in PENDING state
        grant_response = config.freya.inventory_service.v3.grant(
            '{0}.players'.format(config.environment['integration_title']),
            config.store.wgid,
            config.store.profile_id,
            str(uuid.uuid4()),
            config.data.TEST_ENTITLEMENT.ENTITLEMENT_CODE,
            config.environment['integration_title'],
            config.store.active_catalog,
            config.data.TEST_ENTITLEMENT.AMOUNT
        )
        grant_response.assert_is_success()
        transaction_id = grant_response.content['transaction_id']
        assert_that(transaction_id, is_not(None))

        reverse_response = config.freya.server_gateway.reverse_entitlement(config.store.wgid, transaction_id,
                                                                           str(uuid.uuid4()), content_type=content_type)
        reverse_response.assert_is_success()
        assert_that(reverse_response.content['body']['had_shortages'], equal_to(False))

    @pytest.allure.feature('server')
    @pytest.allure.story('reverse entitlement')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_reverse_entitlement_should_succeed_when_transaction_in_canceled_state(self, config, content_type):
        grant_response = config.freya.inventory_service.v3.grant(
            '{0}.players'.format(config.environment['integration_title']),
            config.store.wgid,
            config.store.profile_id,
            str(uuid.uuid4()),
            config.data.TEST_ENTITLEMENT.ENTITLEMENT_CODE,
            config.environment['integration_title'],
            config.store.active_catalog,
            config.data.TEST_ENTITLEMENT.AMOUNT
        )
        grant_response.assert_is_success()
        transaction_id = grant_response.content['transaction_id']
        assert_that(transaction_id, is_not(None))

        cancel_response = config.freya.inventory_service.v3.cancel(
            '{0}.players'.format(config.environment['integration_title']),
            config.store.wgid,
            transaction_id
        )
        cancel_response.assert_is_success()

        reverse_response = config.freya.server_gateway.reverse_entitlement(config.store.wgid, transaction_id,
                                                                           str(uuid.uuid4()), content_type=content_type)
        reverse_response.assert_is_success()
        assert_that(reverse_response.content['body']['had_shortages'], equal_to(False))

    @pytest.allure.feature('server')
    @pytest.allure.story('reverse entitlement')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_reverse_entitlement_should_succeed_when_transaction_in_rollback_state(self, config, content_type):
        grant_response = config.freya.inventory_service.v3.grant(
            '{0}.players'.format(config.environment['integration_title']),
            config.store.wgid,
            config.store.profile_id,
            str(uuid.uuid4()),
            config.data.TEST_ENTITLEMENT.ENTITLEMENT_CODE,
            config.environment['integration_title'],
            config.store.active_catalog,
            config.data.TEST_ENTITLEMENT.AMOUNT
        )
        grant_response.assert_is_success()
        transaction_id = grant_response.content['transaction_id']
        assert_that(transaction_id, is_not(None))

        rollback_response = config.freya.inventory_service.v3.rollback(
            '{0}.players'.format(config.environment['integration_title']),
            config.store.wgid,
            config.store.profile_id,
            transaction_id
        )
        rollback_response.assert_is_success()

        reverse_response = config.freya.server_gateway.reverse_entitlement(config.store.wgid, transaction_id,
                                                                           str(uuid.uuid4()), content_type=content_type)
        reverse_response.assert_is_success()
        assert_that(reverse_response.content['body']['had_shortages'], equal_to(False))

    @pytest.allure.feature('server')
    @pytest.allure.story('reverse entitlement')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_profile_id', [-1, 0, .50, '', None])
    def test_reverse_entitlement_should_fail_when_profile_id_is_invalid(self, config, invalid_profile_id):
        grant_product_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_ENTITLEMENT.COUNTRY,
            config.data.TEST_PRODUCT_ENTITLEMENT.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT_ENTITLEMENT.CODE, config.data.TEST_PRODUCT_ENTITLEMENT.AMOUNT)]
        )
        grant_product_response.assert_is_success()
        transaction_id = grant_product_response.content['body']['transaction_id']
        assert_that(transaction_id, is_not(None))

        reverse_response = config.freya.server_gateway.reverse_entitlement(invalid_profile_id, transaction_id,
                                                                           str(uuid.uuid4()))
        reverse_response.expect_failure(result_code=ResponseMessage.INVALID_PROFILE_ID)

    @pytest.allure.feature('server')
    @pytest.allure.story('reverse entitlement')
    @pytest.allure.severity(severity_level.MINOR)
    def test_reverse_entitlement_should_fail_when_profile_id_is_string(self, config):
        grant_product_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_ENTITLEMENT.COUNTRY,
            config.data.TEST_PRODUCT_ENTITLEMENT.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT_ENTITLEMENT.CODE, config.data.TEST_PRODUCT_ENTITLEMENT.AMOUNT)]
        )
        grant_product_response.assert_is_success()
        transaction_id = grant_product_response.content['body']['transaction_id']
        assert_that(transaction_id, is_not(None))

        reverse_response = config.freya.server_gateway.reverse_entitlement(
            'bad_profile_id',
            transaction_id,
            str(uuid.uuid4())
        )
        reverse_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                        result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.feature('server')
    @pytest.allure.story('reverse entitlement')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_transaction_id', [
        '00000000-0000-0000-0000-00000000000000',
        '00000000-0000-0000-0000-0000000000',
        '00000000-0000-XXXX-0000-000000000000',
        'bad_order_id',
        0,
        -1
    ])
    def test_reverse_entitlement_should_fail_when_transaction_id_is_invalid(self, config, invalid_transaction_id):
        reverse_response = config.freya.server_gateway.reverse_entitlement(
            config.store.wgid,
            invalid_transaction_id,
            str(uuid.uuid4())
        )
        reverse_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                        result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)
