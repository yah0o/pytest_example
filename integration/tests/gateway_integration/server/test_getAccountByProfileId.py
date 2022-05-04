import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities
from integration.main.request import RequestConstants, ResponseMessage


class TestGetAccountsByProfileId(object):

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
    @pytest.allure.story('account by profileId')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_get_account_by_profile_id(self, config, content_type):
        get_response = config.freya.server_gateway.get_accounts_by_profile_id([config.store.profile_id],
                                                                              content_type=content_type)
        get_response.assert_is_success()

        assert_that(get_response.content['body']['accounts'], has_length(1))
        account = get_response.content['body']['accounts'][0]
        assert_that(str(account['profile_id']), equal_to(str(config.store.profile_id)))
        assert_that(str(account['wg_id']), equal_to(str(config.store.profile_id)))
        assert_that(account['nickname'], equal_to(config.store.account.name))
        assert_that(account, has_key('allowed'))
        assert_that(account['restrictions'], empty())

    @pytest.allure.feature('server')
    @pytest.allure.story('account by profileId')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_profile_id', [-1, 0, .50])
    def test_get_account_by_profile_id_invalid_profile_id(self, config, invalid_profile_id):
        get_response = config.freya.server_gateway.get_accounts_by_profile_id([invalid_profile_id])
        get_response.expect_failure(result_code=ResponseMessage.INVALID_PROFILE_ID)

    @pytest.allure.feature('server')
    @pytest.allure.story('account by profileId')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('none_profile_id', ['', None])
    def test_get_account_by_profile_id_none_profile_id(self, config, none_profile_id):
        get_response = config.freya.server_gateway.get_accounts_by_profile_id([none_profile_id])
        get_response.expect_failure(result_code='EXCEPTION')

    @pytest.allure.feature('server')
    @pytest.allure.story('account by profileId')
    @pytest.allure.severity(severity_level.MINOR)
    def test_get_account_by_profile_id_bad_profile_id(self, config):
        get_response = config.freya.server_gateway.get_accounts_by_profile_id(['invalid_profile_id'])
        get_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                    result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)
