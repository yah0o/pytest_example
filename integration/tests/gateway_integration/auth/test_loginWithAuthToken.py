import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities
from integration.main.helpers.matchers import has_keys


class TestLoginWithAuthToken(object):

    @pytest.fixture(autouse=True)
    def setup(self, config):
        ###
        # Test setup

        config.store.account = AccountUtilities.create_account(attrs='user_stated_country=ZZ')

        account_created = config.spa.http.create_account(config.store.account.__dict__)
        account_created.assert_is_success()
        update_account = config.spa.http.update(account_created.content['id'],
                                                game=config.environment['test_title_pgn'])
        update_account.assert_is_success()

        config.store.wgid = account_created.content['id']
        profile_id = account_created.content['id']

        create_response = config.freya.server_gateway.create_auth_token(
            profile_id,
            config.environment['test_title_pgn']
        )
        create_response.assert_is_success()
        config.store.token = create_response.content['body']['auth_token']

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(config.store.wgid)
        delete_response.assert_is_success()

    @pytest.allure.feature('auth')
    @pytest.allure.story('auth token')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_login_with_auth_token_should_work_as_intended(self, config):
        login_response = config.freya.auth_gateway.login_with_auth_token(
            config.store.token,
            config.store.wgid,
            auth_token_target_application=config.environment['test_title_pgn']
        )
        login_response.assert_is_success()

        assert_that(login_response.content['body'], has_keys('remember_me', 'first_login', 'success', 'restrictions',
                                                             'auth_token', 'profile_id', 'activated', 'wgid',
                                                             'allowed', 'client_session', 'nickname',
                                                             'result_code', 'spa_session_id'))
        assert_that(int(login_response.content['body']['wgid']), equal_to(config.store.wgid))
        assert_that(int(login_response.content['body']['profile_id']), equal_to(config.store.wgid))
        assert_that(login_response.content['body']['first_login'], equal_to(True))
        assert_that(login_response.content['body']['allowed'], equal_to(True))
        assert_that(login_response.content['body']['restrictions'], empty())
        assert_that(login_response.content['body']['spa_session_id'], is_not(empty()))

    @pytest.allure.feature('auth')
    @pytest.allure.story('auth token')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_login_with_auth_token_should_not_allow_same_token_twice(self, config):
        login_response = config.freya.auth_gateway.login_with_auth_token(
            config.store.token,
            config.store.wgid,
            auth_token_target_application=config.environment['test_title_pgn']
        )
        login_response.assert_is_success()

        login_response = config.freya.auth_gateway.login_with_auth_token(
            config.store.token,
            config.store.wgid,
            auth_token_target_application=config.environment['test_title_pgn']
        )
        login_response.expect_failure(result_code='CLIENT_ERROR_409')

    @pytest.allure.feature('auth')
    @pytest.allure.story('auth token')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_login_with_auth_token_should_return_xmppcs_auth_key_when_xmppcs_is_requested_as_target_application(
            self,
            config
    ):
        login_response = config.freya.auth_gateway.login_with_auth_token(
            config.store.token,
            config.store.wgid,
            auth_token_target_application=config.data.TARGET_APPLICATION
        )
        login_response.assert_is_success()
        assert_that(login_response.content['body'], has_key('remember_me'))

        target_app_token = login_response.content['body']['remember_me']
        login_with_remember_me_response = config.freya.auth_gateway.login_with_remember_me(target_app_token,
                                                                                           config.environment['region'])
        login_with_remember_me_response.assert_is_success()

        # this is where we would check that the login_with_remember_me_response was for target_app_instead of our main
        # application, but there isn't any unique data from what I can tell that signifies this

    @pytest.allure.feature('auth')
    @pytest.allure.story('auth token')
    @pytest.allure.severity(severity_level.MINOR)
    def test_login_with_auth_token_should_not_succeed_with_bad_token(self, config):
        login_response = config.freya.auth_gateway.login_with_auth_token(
            '{0}1'.format(config.store.token),
            config.store.wgid
        )
        login_response.expect_failure(result_code='CLIENT_ERROR_409')

    @pytest.allure.feature('auth')
    @pytest.allure.story('auth token')
    @pytest.allure.severity(severity_level.MINOR)
    def test_login_with_auth_token_should_not_succeed_with_bad_wgid(self, config):
        login_response = config.freya.auth_gateway.login_with_auth_token(config.store.token, int(config.store.wgid) + 1)
        login_response.expect_failure(result_code='CLIENT_ERROR_409')

    @pytest.allure.feature('auth')
    @pytest.allure.story('auth token', 'banned login')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_login_with_token_should_fail_when_logging_in_with_tools_banned_email(self, config):
        config.log.info('create a tools ban on the current account')
        ban_response = config.banw.service.create_ban(config.store.wgid,
                                                      config.data.TEST_BAN.GAME,
                                                      config.data.TEST_BAN.PROJECT.lower(),
                                                      config.data.TEST_BAN.TYPE.lower(),
                                                      1, 1,
                                                      reason=config.data.TEST_BAN.REASON,
                                                      comment=config.data.TEST_BAN.REASON)

        assert_that(ban_response.content['data'], has_key('id'))

        config.log.info('try to log in again with the same account')
        login_response = config.freya.auth_gateway.login_with_auth_token(config.store.token, config.store.wgid)
        login_response.assert_is_success()

        assert_that(login_response.content['body'], has_key('client_session'))
        login_client_session = login_response.content['body']['client_session']

        assert_that(login_response.content['body']['restrictions'], has_length(1))
        assert_that(login_response.content['body']['restrictions'][0], has_key('banType'))
        assert_that(login_response.content['body']['restrictions'][0]['banType'], equal_to('access_denied'))

    @pytest.mark.skip_for_regions('trie')
    @pytest.allure.feature('auth')
    @pytest.allure.story('auth token', 'banned login')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_login_with_token_should_fail_when_logging_in_with_server_banned_email(self, config):
        config.log.info('create a server ban on the current account')
        ban_response = config.freya.server_gateway.create_ban(
            config.store.wgid,
            config.data.TEST_BAN.PROJECT,
            config.data.TEST_BAN.TYPE,
            config.data.TEST_BAN.REASON,
            config.data.TEST_BAN.AUTHOR
        )
        ban_response.assert_is_success()
        assert_that(ban_response.content['body'], has_key('ban_id'))

        config.log.info('try to log in again with the same account')
        login_response = config.freya.auth_gateway.login_with_auth_token(config.store.token, config.store.wgid)
        login_response.assert_is_success()

        assert_that(login_response.content['body'], has_key('client_session'))

        assert_that(login_response.content['body']['restrictions'], has_length(1))
        assert_that(login_response.content['body']['restrictions'][0], has_key('banType'))
        assert_that(login_response.content['body']['restrictions'][0]['banType'], equal_to('access_denied'))

    @pytest.allure.feature('auth')
    @pytest.allure.story('auth token')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('client_language', ['en', 'ru', '', 1, None])
    def test_login_with_auth_token_should_succeed_with_client_language(self, config, client_language):
        login_response = config.freya.auth_gateway.login_with_auth_token(
            config.store.token,
            config.store.wgid,
            auth_token_target_application=config.environment['test_title_pgn'],
            client_language=client_language
        )
        login_response.assert_is_success()
