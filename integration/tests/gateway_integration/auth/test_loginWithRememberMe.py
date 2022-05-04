import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities
from integration.main.helpers.matchers import has_keys


@pytest.allure.feature('auth')
@pytest.allure.story('remember me')
class TestLoginWithRememberMe(object):

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

        create_response = config.freya.server_gateway.create_remember_me_token(config.store.account.email,
                                                                               config.store.account.password)
        create_response.assert_is_success()

        config.store.remember_me = create_response.content['body']['remember_me']

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(config.store.wgid)
        delete_response.assert_is_success()

    @pytest.allure.severity(severity_level.BLOCKER)
    def test_login_with_remember_me(self, config):
        login_response = config.freya.auth_gateway.login_with_remember_me(config.store.remember_me,
                                                                          config.environment['region'])
        login_response.assert_is_success()

        assert_that(int(login_response.content['body']['wgid']), equal_to(config.store.wgid))
        assert_that(login_response.content['body'], has_keys('first_login', 'allowed', 'restrictions', 'activated',
                                                             'remember_me', 'first_login', 'profile_id', 'wgid',
                                                             'client_session', 'nickname', 'result_code',
                                                             'spa_session_id'))
        assert_that(login_response.content['body']['restrictions'], empty())
        assert_that(login_response.content['body']['spa_session_id'], is_not(empty()))

    @pytest.allure.severity(severity_level.MINOR)
    def test_login_with_remember_me_should_change_per_login_and_old_token_shouldnt_work(self, config):
        login_response = config.freya.auth_gateway.login_with_remember_me(config.store.remember_me,
                                                                          config.environment['region'])
        login_response.assert_is_success()

        assert_that(login_response.content['body'], has_entry('remember_me', not_(config.store.remember_me)))
        new_remember_me = login_response.content['body']['remember_me']

        relogin_response = config.freya.auth_gateway.login_with_remember_me(new_remember_me,
                                                                            config.environment['region'])
        relogin_response.assert_is_success()

        rerelogin_response = config.freya.auth_gateway.login_with_remember_me(config.store.remember_me,
                                                                              config.environment['region'])
        rerelogin_response.expect_failure(result_code="CLIENT_ERROR_409")

    @pytest.allure.severity(severity_level.MINOR)
    def test_login_with_remember_me_should_fail_with_bad_remember_me(self, config):
        create_response = config.freya.server_gateway.create_remember_me_token(config.store.account.email,
                                                                               config.store.account.password)
        create_response.assert_is_success()

        login_response = config.freya.auth_gateway.login_with_remember_me('bad', config.environment['region'])
        login_response.expect_failure(result_code='CLIENT_ERROR_409', code=200)

    @pytest.allure.story('remember me', 'banned login')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_login_with_banned_email(self, config):
        config.log.info('make sure the account is valid, can log in, restriction fields are empty')
        login_response = config.freya.auth_gateway.login_with_remember_me(config.store.remember_me,
                                                                          config.environment['region'])
        login_response.assert_is_success()

        assert_that(login_response.content['body'], has_key('client_session'))
        assert_that(login_response.content['body']['client_session'], is_not(empty()))
        login_client_session = login_response.content['body']['client_session']

        assert_that(login_response.content['body']['restrictions'], empty())

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
        relogin_response = config.freya.auth_gateway.login_with_remember_me(config.store.remember_me,
                                                                            config.environment['region'])
        relogin_response.assert_is_success()

        assert_that(relogin_response.content['body'], has_key('client_session'))
        assert_that(relogin_response.content['body']['client_session'], is_not(empty()))
        relogin_client_session = relogin_response.content['body']['client_session']

        assert_that(relogin_response.content['body']['restrictions'], has_length(1))
        assert_that(relogin_response.content['body']['restrictions'][0], has_key('id'))
        assert_that(relogin_response.content['body']['restrictions'][0]['game'], equal_to(config.data.TEST_BAN.GAME))
        assert_that(relogin_response.content['body']['restrictions'][0]['project'],
                    equal_to(config.data.TEST_BAN.PROJECT.lower()))
        assert_that(relogin_response.content['body']['restrictions'][0], has_key('started_at'))
        assert_that(relogin_response.content['body']['restrictions'][0]['reason'],
                    equal_to(config.data.TEST_BAN.REASON))
        assert_that(relogin_response.content['body']['restrictions'][0]['banType'],
                    equal_to(config.data.TEST_BAN.TYPE.lower()))

        config.log.info('ensure the login sessions are not the same')
        assert_that(login_client_session, is_not(relogin_client_session))

    @pytest.mark.skip_for_regions('trie')
    @pytest.allure.story('remember me', 'banned login')
    @pytest.allure.severity(severity_level.BLOCKER)
    def test_login_with_server_banned_email(self, config):
        config.log.info('make sure the account is valid, can log in, restriction fields are empty')
        login_response = config.freya.auth_gateway.login_with_remember_me(config.store.remember_me,
                                                                          config.environment['region'])
        login_response.assert_is_success()

        assert_that(login_response.content['body'], has_key('client_session'))
        assert_that(login_response.content['body']['client_session'], is_not(empty()))
        login_client_session = login_response.content['body']['client_session']

        assert_that(login_response.content['body']['restrictions'], empty())

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
        relogin_response = config.freya.auth_gateway.login_with_remember_me(config.store.remember_me,
                                                                            config.environment['region'])
        relogin_response.assert_is_success()

        assert_that(relogin_response.content['body'], has_key('client_session'))
        assert_that(relogin_response.content['body']['client_session'], is_not(empty()))
        relogin_client_session = relogin_response.content['body']['client_session']

        assert_that(relogin_response.content['body']['restrictions'], has_length(1))
        assert_that(relogin_response.content['body']['restrictions'][0], has_key('id'))
        assert_that(
            relogin_response.content['body']['restrictions'][0]['game'],
            equal_to(config.environment['test_title_pgn'])
        )
        assert_that(relogin_response.content['body']['restrictions'][0]['project'],
                    equal_to(config.data.TEST_BAN.PROJECT.lower()))
        assert_that(relogin_response.content['body']['restrictions'][0], has_key('started_at'))
        assert_that(relogin_response.content['body']['restrictions'][0]['reason'],
                    equal_to(config.data.TEST_BAN.REASON))
        assert_that(relogin_response.content['body']['restrictions'][0]['banType'],
                    equal_to(config.data.TEST_BAN.TYPE.lower()))

        config.log.info('ensure the login sessions are not the same')
        assert_that(login_client_session, is_not(relogin_client_session))

    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('client_language', ['en', 'ru', '', 1, None])
    def test_login_with_remember_me_with_client_language_should_succeed(self, config, client_language):
        login_response = config.freya.auth_gateway.login_with_remember_me(config.store.remember_me,
                                                                          config.environment['region'],
                                                                          client_language=client_language)
        login_response.assert_is_success()
