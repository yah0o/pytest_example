import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities
from integration.main.request import RequestConstants


class TestGetAccountsByWgId(object):

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
    @pytest.allure.story('account by wgId')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_get_accounts_by_wgid_should_succeed_when_account_have_profile(self, config, content_type):
        get_response = config.freya.server_gateway.get_accounts_by_wgid([config.store.wgid], content_type=content_type)
        get_response.assert_is_success()

        assert_that(get_response.content['body']['accounts'], has_length(1))
        account = get_response.content['body']['accounts'][0]

        assert_that(str(account['profile_id']), equal_to(str(config.store.profile_id)))
        assert_that(str(account['wg_id']), equal_to(str(config.store.wgid)))
        assert_that(account['nickname'], equal_to(config.store.account.name))

        assert_that(account, has_key('allowed'))
        assert_that(account['restrictions'], empty())
        assert_that(account['allowed'], equal_to(True))

    @pytest.mark.skip_for_regions('trie', 'wgt1')
    @pytest.allure.feature('server')
    @pytest.allure.story('account by wgId')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_get_accounts_by_wgid_should_succeed_when_account_do_not_have_profile(self, config, content_type):
        get_account_response = config.freya.server_gateway.get_accounts_by_wgid(
            [config.store.wgid],
            content_type=content_type
        )
        get_account_response.assert_is_success()

        assert_that(get_account_response.content['body']['accounts'], has_length(1))
        account = get_account_response.content['body']['accounts'][0]

        assert_that(str(account['wg_id']), equal_to(str(config.store.wgid)))
        assert_that(account['nickname'], equal_to(config.store.account.name))
        assert_that(str(account['profile_id']), equal_to(str(config.store.wgid)))
        assert_that(account['restrictions'], has_length(0))
        assert_that(account['allowed'], equal_to(True))

    @pytest.mark.skip_for_regions('trie')
    @pytest.allure.feature('server')
    @pytest.allure.story('account by wgId')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_get_accounts_by_wgid_should_succeed_when_account_with_profile_is_banned(self, config, content_type):

        ban_response = config.freya.server_gateway.create_ban(
            config.store.wgid,
            config.data.TEST_BAN.PROJECT,
            config.data.TEST_BAN.TYPE,
            config.data.TEST_BAN.REASON,
            config.data.TEST_BAN.AUTHOR
        )
        ban_response.assert_is_success()
        ban_info = ban_response.content

        get_account_response = config.freya.server_gateway.get_accounts_by_wgid([config.store.wgid],
                                                                             content_type=content_type)
        get_account_response.assert_is_success()

        assert_that(get_account_response.content['body']['accounts'], has_length(1))
        account = get_account_response.content['body']['accounts'][0]

        assert_that(str(account['wg_id']), equal_to(str(config.store.wgid)))
        assert_that(account['nickname'], equal_to(config.store.account.name))
        assert_that(str(account['profile_id']), equal_to(str(config.store.profile_id)))
        assert_that(account['allowed'], equal_to(True))
        assert_that(account['restrictions'], has_length(1))

        restriction = account['restrictions'][0]
        assert_that(str(restriction['banId']), equal_to(str(ban_info['body']['ban_id'])))
        assert_that(restriction['reason'], equal_to(config.data.TEST_BAN.REASON))
        assert_that(restriction['project'], equal_to(config.data.TEST_BAN.PROJECT.lower()))
        assert_that(account['allowed'], equal_to(True))

    @pytest.allure.feature('server')
    @pytest.allure.story('account by wgId')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_wgid', [-1, 0, .50])
    def test_get_accounts_by_wgid_should_fail_when_wgid_is_invalid(self, config, invalid_wgid):
        get_account_response = config.freya.server_gateway.get_accounts_by_wgid([invalid_wgid])
        get_account_response.expect_failure(result_code='INVALID_WGID')

    @pytest.allure.feature('server')
    @pytest.allure.story('account by wgId')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('bad_wgid', ['', None])
    def test_get_accounts_by_wgid_should_fail_when_wgid_is_empty_string_or_none(self, config, bad_wgid):
        get_account_response = config.freya.server_gateway.get_accounts_by_wgid([bad_wgid])
        get_account_response.expect_failure(result_code='EXCEPTION')
