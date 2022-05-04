import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities
from integration.main.request import RequestConstants


class TestcreateRememberMeToken(object):

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

        config.store.profile_id = account_created.content['id']

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(config.store.profile_id)
        delete_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('create remember me token')
    @pytest.allure.severity(severity_level.BLOCKER)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_create_remember_me_token(self, config, content_type):
        create_response = config.freya.server_gateway.create_remember_me_token(config.store.account.email,
                                                                               config.store.account.password,
                                                                               client_ip='127.0.0.1',
                                                                               content_type=content_type)
        create_response.assert_is_success()

        assert_that(create_response.content['body'], has_key('remember_me'))

    @pytest.allure.feature('server')
    @pytest.allure.story('create remember me token')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_email', ['bad_email', None, 656, ''])
    def test_create_remember_me_token_invalid_email(self, config, invalid_email):
        create_response = config.freya.server_gateway.create_remember_me_token(invalid_email,
                                                                               config.store.account.password,
                                                                               client_ip='127.0.0.1')
        create_response.expect_failure(result_code='CLIENT_ERROR_409')

    @pytest.allure.feature('server')
    @pytest.allure.story('create remember me token')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_password', ['bad_password', None, 656, ''])
    def test_create_remember_me_token_invalid_password(self, config, invalid_password):
        create_response = config.freya.server_gateway.create_remember_me_token(config.store.account.email,
                                                                               invalid_password, client_ip='127.0.0.1')
        create_response.expect_failure(result_code='CLIENT_ERROR_409')

    @pytest.allure.feature('server')
    @pytest.allure.story('create remember me token')
    @pytest.allure.severity(severity_level.NORMAL)
    def test_login_generating_a_remember_me_token(self, config):

        login_response = config.freya.auth_gateway.login_with_email(config.store.account.email,
                                                                    config.store.account.password,
                                                                    create_remember_me=True)
        login_response.assert_is_success()

        assert_that(login_response.content['body']['nickname'], not_none(),
                    'loginWithEmail did not return nickname field.')
        assert_that(login_response.content['body']['remember_me'], not_none(),
                    'loginWithEmail did not return remember_me field.')

    @pytest.allure.feature('server')
    @pytest.allure.story('create remember me token')
    @pytest.allure.severity(severity_level.MINOR)
    def test_create_remember_me_token_fail_when_banned(self, config):
        create_response = config.freya.server_gateway.create_remember_me_token('freya666@wargaming.net', 'freya666',
                                                                               client_ip='127.0.0.1',
                                                                               content_type=RequestConstants.ContentTypes.MSG_PACK)
        create_response.expect_failure(result_code='CLIENT_ERROR_409', code=200)

    @pytest.allure.feature('server')
    @pytest.allure.story('create remember me token')
    @pytest.allure.severity(severity_level.MINOR)
    def test_login_failure_with_bad_email(self, config):

        login_response = config.freya.auth_gateway.login_with_email('not_an_email', 'password', fingerprint='fingerprint',
                                                                    create_remember_me=False, client_ip='127.0.0.1')
        login_response.expect_failure(result_code='CLIENT_ERROR_409', code=200)

    @pytest.allure.feature('server')
    @pytest.allure.story('create remember me token')
    @pytest.allure.severity(severity_level.NORMAL)
    def test_login_handoff_from_email_to_remember_me(self, config):
        fingerprint = config.data.FINGERPRINT
        login_response = config.freya.auth_gateway.login_with_email(config.store.account.email,
                                                                    config.store.account.password,
                                                                    fingerprint=fingerprint,
                                                                    create_remember_me=True,
                                                                    client_ip='127.0.0.1',
                                                                    auth_token_target_application=False)
        login_response.assert_is_success()
        assert_that(login_response.content['body']['remember_me'], not_none(),
                    'loginWithEmail did not return remember_me field.')

        current_remember_me = login_response.content['body']['remember_me']

        login_response = config.freya.auth_gateway.login_with_remember_me(login_response.content['body']['remember_me'],
                                                                          config.environment['region'],
                                                                          fingerprint=fingerprint, client_ip='127.0.0.1',
                                                                          auth_token_target_application=None)
        login_response.assert_is_success()
        assert_that(login_response.content['body'], has_key('client_session'))
        assert_that(current_remember_me, not_(login_response.content['body']['remember_me']))

    @pytest.allure.feature('server')
    @pytest.allure.story('create remember me token')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('client_language', ['en', 'ru', '', 1, None])
    def test_create_remember_me_token_wit_client_language(self, config, client_language):
        create_response = config.freya.server_gateway.create_remember_me_token(config.store.account.email,
                                                                               config.store.account.password,
                                                                               client_ip='127.0.0.1',
                                                                               client_language=client_language)
        create_response.assert_is_success()

        assert_that(create_response.content['body'], has_key('remember_me'))
