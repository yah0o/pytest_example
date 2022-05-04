import time

import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities
from integration.main.request import RequestConstants, ResponseMessage


class TestCreateBan(object):

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
        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(config.store.profile_id)
        delete_response.assert_is_success()

    @pytest.fixture
    def setup_no_profile(self, config):
        account = AccountUtilities.create_account()
        account_created = config.spa.http.create_account(account.__dict__)
        account_created.assert_is_success()
        config.store.profile_id = account_created.content['id']

    @pytest.mark.skip_for_regions('trie')
    @pytest.allure.feature('server')
    @pytest.allure.story('create ban')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_create_ban_should_succeed_when_player_is_banned(self, config, content_type):
        create_response = config.freya.server_gateway.create_ban(
            config.store.profile_id,
            config.data.TEST_BAN.PROJECT,
            config.data.TEST_BAN.TYPE,
            config.data.TEST_BAN.REASON,
            config.data.TEST_BAN.AUTHOR,
            content_type=content_type
        )
        create_response.assert_is_success()
        assert_that(create_response.content['body'], has_key('ban_id'))
        bans_response = config.banw.service.get_ban(config.store.profile_id)
        bans_response.assert_is_success()
        assert_that(bans_response.content['data']['bans'], has_length(1))

    @pytest.allure.feature('server')
    @pytest.allure.story('create ban')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.skip(reason='requires us to wait one minute to pass')
    def test_create_ban_should_succeed_when_ban_expires(self, config):
        # skipped from test running. for local run only (long test)
        ban_start = time.time()
        ban_end = ban_start + 15

        create_ban_response = config.freya.server_gateway.create_ban(
            config.store.profile_id,
            config.data.TEST_BAN.PROJECT,
            config.data.TEST_BAN.TYPE,
            config.data.TEST_BAN.REASON,
            config.data.TEST_BAN.AUTHOR,
            start_at=ban_start,
            expire_at=ban_end
        )
        create_ban_response.assert_is_success()
        assert_that(create_ban_response.content['body'], has_key('ban_id'))
        ban_id = int(create_ban_response.content['body']['ban_id'])

        pre_expire_ban_get_account_response = config.freya.server_gateway.get_accounts_by_wgid(
            [config.store.profile_id]
        )
        pre_expire_ban_get_account_response.assert_is_success()

        assert_that(pre_expire_ban_get_account_response.content['body']['accounts'], not_none())
        pre_ban_expire_account = pre_expire_ban_get_account_response.content['body']['accounts'][0]

        assert_that(pre_ban_expire_account['restrictions'], not_none())
        restriction = pre_ban_expire_account['restrictions'][0]

        assert_that(restriction['id'], equal_to(ban_id))

        time.sleep(30)

        post_expire_ban_get_account_response = config.freya.server_gateway.get_accounts_by_wgid(
            [config.store.profile_id]
        )
        post_expire_ban_get_account_response.assert_is_success()

        assert_that(post_expire_ban_get_account_response.content['body']['accounts'], not_none())
        post_ban_expire_account = post_expire_ban_get_account_response.content['body']['accounts'][0]

        assert_that(post_ban_expire_account['restrictions'], has_length(0))

    @pytest.mark.skip_for_regions('trie')
    @pytest.allure.feature('server')
    @pytest.allure.story('create ban')
    @pytest.allure.severity(severity_level.MINOR)
    def test_create_ban_should_succeed_when_account_have_no_profile(self, config, setup_no_profile):
        # FREYA-782
        create_response = config.freya.server_gateway.create_ban(
            config.store.profile_id,
            config.data.TEST_BAN.PROJECT,
            config.data.TEST_BAN.TYPE,
            config.data.TEST_BAN.REASON,
            config.data.TEST_BAN.AUTHOR
        )
        create_response.assert_is_success()
        assert_that(create_response.content['body'], has_key('ban_id'))

    @pytest.allure.feature('server')
    @pytest.allure.story('create ban')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_profile_id', [-1, 0, .50, '', None])
    def test_create_ban_should_fail_when_profile_id_is_invalid(self, config, invalid_profile_id):
        create_response = config.freya.server_gateway.create_ban(
            invalid_profile_id,
            config.data.TEST_BAN.PROJECT,
            config.data.TEST_BAN.TYPE,
            config.data.TEST_BAN.REASON,
            config.data.TEST_BAN.AUTHOR
        )
        create_response.expect_failure(result_code=ResponseMessage.INVALID_PROFILE_ID)

    @pytest.allure.feature('server')
    @pytest.allure.story('create ban')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_project', ['', 656, 'bad_project',
                                                 'iZVwQGdhlAGSlLHOowx436Cflr2r8jOoWHXioY2s69K4VOsH6eI4oXIXXCDbbNm5GeW5of1dbLy0680DkUVeSJmHu57wQGVd2gxF'])
    def test_create_ban_should_fail_when_project_is_invalid(self, config, invalid_project):
        create_response = config.freya.server_gateway.create_ban(
            config.store.profile_id,
            invalid_project,
            config.data.TEST_BAN.TYPE,
            config.data.TEST_BAN.REASON,
            config.data.TEST_BAN.AUTHOR
        )
        create_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                       result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.feature('server')
    @pytest.allure.story('create ban')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_type', ['', 656, 'bad_type',
                                              '3eZF4iTsOYMTuWjUtmGN2Wr2c7bhHkxjRLzqfBCjKfLr9ugYq1tO0zz3n0Y5Rmteb94NRqeoLaPlIOHzwD0PonjLnmu99grUQ3SH'])
    def test_create_ban_should_fail_when_type_is_invalid(self, config, invalid_type):
        create_response = config.freya.server_gateway.create_ban(
            config.store.profile_id,
            config.data.TEST_BAN.PROJECT,
            invalid_type,
            config.data.TEST_BAN.REASON,
            config.data.TEST_BAN.AUTHOR
        )
        create_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                       result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.feature('server')
    @pytest.allure.story('create ban')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_author', ['', None])
    def test_create_ban_should_fail_when_author_is_invalid(self, config, invalid_author):
        create_response = config.freya.server_gateway.create_ban(
            config.store.profile_id,
            config.data.TEST_BAN.PROJECT,
            config.data.TEST_BAN.TYPE,
            config.data.TEST_BAN.REASON,
            invalid_author
        )
        create_response.expect_failure(result_code='ERROR')

    @pytest.allure.feature('server')
    @pytest.allure.story('create ban')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_create_ban_should_fail_with_empty_project(self, config, content_type):
        create_response = config.freya.server_gateway.create_ban(
            config.store.profile_id,
            None,
            config.data.TEST_BAN.TYPE,
            config.data.TEST_BAN.REASON,
            config.data.TEST_BAN.AUTHOR,
            content_type=content_type
        )
        create_response.expect_failure(result_code=ResponseMessage.INVALID_PROJECT,
                                       result_message=ResponseMessage.REQUIRED_PROJECT)

    @pytest.allure.feature('server')
    @pytest.allure.story('create ban')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_create_ban_should_fail_with_empty_ban_type(self, config, content_type):
        create_response = config.freya.server_gateway.create_ban(
            config.store.profile_id,
            config.data.TEST_BAN.PROJECT,
            None,
            config.data.TEST_BAN.REASON,
            config.data.TEST_BAN.AUTHOR,
            content_type=content_type
        )
        create_response.expect_failure(result_code=ResponseMessage.INVALID_BAN_TYPE,
                                       result_message=ResponseMessage.REQUIRED_BAN_TYPE)
