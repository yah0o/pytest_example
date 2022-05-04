import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities


@pytest.allure.feature('functional')
@pytest.allure.story('login with banned account')
class TestLoginWithBannedAccount(object):

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

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(config.store.wgid)
        delete_response.assert_is_success()

    def login_with_email(self, config):
        login_response = config.freya.auth_gateway.login_with_email(config.store.account.email,
                                                                    config.store.account.password)
        login_response.assert_is_success()

        assert_that(login_response.content['body'], has_key('client_session'))
        assert_that(login_response.content['body']['restrictions'], empty())

        client_session = login_response.content['body']['client_session']

        return client_session

    @pytest.mark.skip_for_regions('trie')
    def login_with_banned_email(self, config):
        login_response = config.freya.auth_gateway.login_with_email(config.store.account.email,
                                                                    config.store.account.password)
        login_response.assert_is_success()

        assert_that(login_response.content['body'], has_key('client_session'))
        assert_that(login_response.content['body']['restrictions'], has_length(greater_than(0)))

        restriction = login_response.content['body']['restrictions'][0]
        assert_that(restriction, has_key('id'))
        assert_that(restriction, has_key('game'))
        assert_that(restriction['project'], equal_to_ignoring_case(config.data.TEST_BAN.PROJECT))
        assert_that(restriction, has_key('started_at'))
        assert_that(restriction['reason'], equal_to(config.data.TEST_BAN.REASON))
        assert_that(restriction['ban_type'], equal_to_ignoring_case(config.data.TEST_BAN.TYPE))

        client_session = login_response.content['body']['client_session']

        return client_session

    def createBanwBan(self, config):
        ban_response = config.banw.service.create_ban(config.store.wgid,
                                                      config.data.TEST_BAN.GAME,
                                                      config.data.TEST_BAN.PROJECT.lower(),
                                                      config.data.TEST_BAN.TYPE.lower(),
                                                      1, 1,
                                                      reason=config.data.TEST_BAN.REASON,
                                                      comment=config.data.TEST_BAN.REASON)

        assert_that(ban_response.content['data'], has_key('id'))

    def createServerBan(self, config):
        ban_response = config.freya.server_gateway.create_ban(
            config.store.wgid,
            config.data.TEST_BAN.PROJECT,
            config.data.TEST_BAN.TYPE,
            config.data.TEST_BAN.REASON,
            config.data.TEST_BAN.AUTHOR
        )
        ban_response.assert_is_success()

        assert_that(ban_response.content['body'], has_key('ban_id'))

    def kickPlayer(self, config):
        kick_response = config.freya.tools_gateway.player.kick_by_wgid_and_title(
            config.environment['integration_title'],
            config.store.wgid
        )
        kick_response.assert_is_success()

        assert_that(kick_response.content['title_code'], equal_to(config.environment['integration_title']))
        assert_that(kick_response.content['profile_id'], equal_to(config.store.wgid))

    # TOOLS GATEWAY TESTS STARTS HERE
    @pytest.mark.skip(reason='tools sunset')
    @pytest.allure.severity(severity_level.NORMAL)
    def test_ban_account_before_login(self, config):
        config.log.info('create a ban FIRST on the account')
        self.createBanwBan(config)

        config.log.info('try to log in for the first time with the banned account')
        self.login_with_banned_email(config)

    @pytest.mark.skip(reason='https://jira.wargaming.net/browse/FREYA-487')
    @pytest.allure.severity(severity_level.NORMAL)
    def test_banned_account_with_kick(self, config):
        config.log.info('make sure the account is valid, can log in, restriction fields are empty')
        login_client_session = self.login_with_email(config)

        config.log.info('kick player of current account')
        self.kickPlayer(config)

        config.log.info('create a ban on the account')
        self.createBanwBan(config)

        config.log.info('try to log in for with the same account')
        relogin_client_session = self.login_with_banned_email(config)

        assert_that(login_client_session, is_not(relogin_client_session))

    @pytest.mark.skip_for_regions('trie')
    # SERVER GATEWAY TESTS STARTS HERE
    @pytest.allure.severity(severity_level.NORMAL)
    def test_ban_account_server_before_login(self, config):
        config.log.info('create a ban FIRST on the account')
        self.createServerBan(config)

        config.log.info('try to log in for the first time with the banned account')
        self.login_with_banned_email(config)

    @pytest.mark.skip(reason='https://jira.wargaming.net/browse/FREYA-487')
    @pytest.allure.severity(severity_level.NORMAL)
    def test_banned_account_server_with_kick(self, config):
        config.log.info('make sure the account is valid, can log in, restriction fields are empty')
        login_client_session = self.login_with_email(config)

        config.log.info('kick player of current account')
        self.kickPlayer(config)

        config.log.info('create a ban on the account')
        self.createServerBan(config)

        config.log.info('try to log in for with the same account')
        relogin_client_session = self.login_with_banned_email(config)

        assert_that(login_client_session, is_not(relogin_client_session))
