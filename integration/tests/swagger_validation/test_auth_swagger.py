import pytest

from integration.main.helpers import AccountUtilities
from integration.schemas import Schemas


@pytest.allure.feature('swagger')
@pytest.allure.story('auth')
class TestAuthSwagger(object):

    @pytest.fixture(autouse=True)
    def setup(self, config):
        ###
        # Test setup
        login_response = config.freya.tools_gateway.login.auth_adfs_login(config.admin.username, config.admin.password)
        login_response.assert_is_success()

        config.store.account = AccountUtilities.create_account()
        account_response = config.freya.tools_gateway.player.new(
            config.store.account.email,
            config.store.account.name,
            config.store.account.password,
            config.data.TEST_TITLE,
            config.environment['region']
        )
        account_response.assert_is_success()
        config.store.wgid = account_response.content['id']

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here

    def test_login_with_auth_token(self, config):
        profile_response = config.freya.tools_gateway.player.create_title_profile(config.store.wgid,
                                                                                  config.data.TEST_TITLE,
                                                                                  config.environment['region'])
        profile_response.assert_is_success()
        profile_id = profile_response.content['profile_id']

        create_response = config.freya.server_gateway.create_auth_token(
            profile_id,
            config.environment['test_title_pgn']
        )
        create_response.assert_is_success()
        token = create_response.content['body']['auth_token']

        login_response = config.freya.auth_gateway.login_with_auth_token(
            token,
            config.store.wgid,
            auth_token_target_application=config.environment['test_title_pgn']
        )
        login_response.assert_is_success()
        Schemas.swagger_validate(login_response, '/api/v1/loginWithAuthToken')

    def test_login_with_email(self, config):

        login_response = config.freya.auth_gateway.login_with_email(config.store.account.email,
                                                                    config.store.account.password)
        login_response.assert_is_success()
        Schemas.swagger_validate(login_response, '/api/v1/loginWithEmail')

    def test_login_with_remember_me(self, config):

        create_response = config.freya.server_gateway.create_remember_me_token(config.store.account.email,
                                                                            config.store.account.password)
        create_response.assert_is_success()

        remember_me = create_response.content['body']['remember_me']

        login_response = config.freya.auth_gateway.login_with_remember_me(remember_me, config.environment['region'])
        login_response.assert_is_success()
        Schemas.swagger_validate(login_response, '/api/v1/loginWithRememberMe')
