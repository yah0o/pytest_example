import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities
from integration.main.request import RequestConstants
from integration.main.request.constants import ResponseMessage


class TestGetFullInventory(object):

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
    @pytest.allure.story('full inventory')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_get_full_inventory_should_succeed_only_for_profile_id(self, config, content_type):
        # FREYA-782 (now getFullInventory gets data only for profile id)
        inventory_response = config.freya.server_gateway.get_full_inventory(
            config.store.profile_id,
            content_type=content_type
        )
        inventory_response.assert_is_success()
        assert_that(inventory_response.content['body'], has_key('profile'))

        profile = inventory_response.content['body']['profile']
        assert_that(str(profile['profile_id']), equal_to(str(config.store.profile_id)))
        assert_that(profile, has_key('children'))
        assert_that(profile['children'], has_length(0))

    @pytest.allure.feature('server')
    @pytest.allure.story('full inventory')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_profile_id', [-1, 0, .50, None, ''])
    def test_get_full_inventory_should_fail_when_profile_id_is_invalid(self, config, invalid_profile_id):
        inventory_response = config.freya.server_gateway.get_full_inventory(invalid_profile_id)
        inventory_response.expect_failure(result_code=ResponseMessage.INVALID_PROFILE_ID)

    @pytest.allure.feature('server')
    @pytest.allure.story('full inventory')
    @pytest.allure.severity(severity_level.MINOR)
    def test_get_full_inventory_should_fail_when_profile_is_string(self, config):
        inventory_response = config.freya.server_gateway.get_full_inventory('bad_profile')
        inventory_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                          result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)
