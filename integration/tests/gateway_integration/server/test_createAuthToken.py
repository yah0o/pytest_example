import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities
from integration.main.request import RequestConstants, ResponseMessage


class TestCreateAuthToken(object):

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

        config.store.wgid = account_created.content['id']

        login_response = config.freya.auth_gateway.login_with_email(account.login, account.password)
        login_response.assert_is_success()

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(config.store.wgid)
        delete_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('create auth token')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_create_auth_token_should_succeed_when_account_create_auth_token(self, config, content_type):
        create_response = config.freya.server_gateway.create_auth_token(config.store.wgid,
                                                                        config.data.TARGET_APPLICATION,
                                                                        content_type=content_type)
        create_response.assert_is_success()
        assert_that(create_response.content['body'], has_key('auth_token'))
        assert_that(create_response.content['body'], has_key('wgid'))
        assert_that(str(create_response.content['body']['wgid']), equal_to(str(config.store.wgid)))

    @pytest.allure.feature('server')
    @pytest.allure.story('create auth token')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_profile_id', [-1, 0, .50, '', None])
    def test_create_auth_token_should_fail_when_profile_id_is_invalid(self, config, invalid_profile_id):
        create_response = config.freya.server_gateway.create_auth_token(invalid_profile_id,
                                                                        config.data.TARGET_APPLICATION, '127.0.0.1')

        create_response.expect_failure(result_code=ResponseMessage.INVALID_PROFILE_ID,
                                       result_message='Profile ID must be > 0',
                                       code=200)
        assert_that(create_response.content['body'], has_key('wgid'))
        assert_that(create_response.content['body']['wgid'], equal_to('0'))

    @pytest.allure.feature('server')
    @pytest.allure.story('create auth token')
    @pytest.allure.severity(severity_level.MINOR)
    def test_create_auth_token_should_fail_when_profile_id_is_string(self, config):
        create_response = config.freya.server_gateway.create_auth_token('bad_profile_id',
                                                                        config.data.TARGET_APPLICATION)
        create_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                       result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.feature('server')
    @pytest.allure.story('create auth token')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_target_application', [0, '', None,
                                                            'ixtmcT2ZeSbFauhinGHJyhyGuCIZuy7phYmDAxtGBxPjQ2Cu85jEEtS3mwSAU6RGl7jr4aKhbJgAhf1HCVHW5JYdBRBvpWZLDaad'])
    def test_create_auth_token_should_fail_when_target_application_is_invalid(self, config, invalid_target_application):
        create_response = config.freya.server_gateway.create_auth_token(config.store.wgid, invalid_target_application)
        create_response.expect_failure(result_code='CLIENT_ERROR_409')
