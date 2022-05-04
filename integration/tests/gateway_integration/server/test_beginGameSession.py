import pytest
from allure import severity_level

from integration.main.helpers import AccountUtilities
from integration.main.request import RequestConstants, ResponseMessage


class TestBeginGameSession(object):

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
        wgid = account_created.content['id']
        config.store.profile_id = account_created.content['id']

        account_response = config.freya.server_gateway.account_created(config.store.profile_id, 'OK')
        account_response.assert_is_success()

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(wgid)
        delete_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('begin game session')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_begin_game_session(self, config, content_type):
        session_response = config.freya.server_gateway.begin_game_session(config.store.profile_id,
                                                                          content_type=content_type)
        session_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('begin game session')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_profile_id', [-1, 0, .50, '', None])
    def test_begin_game_session_invalid_profile(self, config, invalid_profile_id):
        invalid_profile_session_response = config.freya.server_gateway.begin_game_session(invalid_profile_id)
        invalid_profile_session_response.expect_failure(result_code=ResponseMessage.INVALID_PROFILE_ID)

    @pytest.allure.feature('server')
    @pytest.allure.story('begin game session')
    @pytest.allure.severity(severity_level.MINOR)
    def test_begin_game_session_bad_profile(self, config):
        bad_profile_session_response = config.freya.server_gateway.begin_game_session('bad_id')
        bad_profile_session_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                                    result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.feature('server')
    @pytest.allure.story('begin game session')
    @pytest.allure.severity(severity_level.MINOR)
    def test_begin_game_session_with_client_ip_should_succeed(self, config):
        session_response = config.freya.server_gateway.begin_game_session(config.store.profile_id,
                                                                          client_ip='192.0.2.1')
        session_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('begin game session')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('client_language', ['en', 'ru', '', 1, None])
    def test_begin_game_session_with_client_language(self, config, client_language):
        session_response = config.freya.server_gateway.begin_game_session(config.store.profile_id,
                                                                          client_language=client_language)
        session_response.assert_is_success()
