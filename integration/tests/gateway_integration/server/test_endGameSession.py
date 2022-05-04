import pytest
from allure import severity_level

from integration.main.helpers import AccountUtilities
from integration.main.request import RequestConstants, ResponseMessage


class TestEndGameSession(object):

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

        login_response = config.freya.auth_gateway.login_with_email(account.email, account.password)
        login_response.assert_is_success()

        create_response = config.freya.server_gateway.account_created(config.store.profile_id, 'OK')
        create_response.assert_is_success()

        config.freya.server_gateway.begin_game_session(config.store.profile_id)

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(config.store.profile_id)
        delete_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('end game session')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_end_game_session(self, config, content_type):
        end_session_response = config.freya.server_gateway.end_game_session(config.store.profile_id,
                                                                            content_type=content_type)
        end_session_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('end game session')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_profile_id', [-1, 0, .50, '', None])
    def test_end_game_session_invalid_profile_id(self, config, invalid_profile_id):
        end_session_response = config.freya.server_gateway.end_game_session(invalid_profile_id)
        end_session_response.expect_failure(result_code=ResponseMessage.INVALID_PROFILE_ID)

    @pytest.allure.feature('server')
    @pytest.allure.story('end game session')
    @pytest.allure.severity(severity_level.MINOR)
    def test_end_game_session_bad_profile_id(self, config):
        end_session_response = config.freya.server_gateway.end_game_session('bad_profile_id')
        end_session_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                            result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.feature('server')
    @pytest.allure.story('end game session')
    @pytest.allure.severity(severity_level.NORMAL)
    def test_end_game_session_with_client_ip_should_succeed(self, config):
        end_session_response = config.freya.server_gateway.end_game_session(config.store.profile_id,
                                                                            client_ip='192.0.2.1')
        end_session_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('end game session')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('client_language', ['en', 'ru', '', 1, None])
    def test_end_game_session_with_client_language_should_succeed(self, config, client_language):
        end_session_response = config.freya.server_gateway.end_game_session(config.store.profile_id,
                                                                            client_language=client_language)
        end_session_response.assert_is_success()
