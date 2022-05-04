import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities
from integration.main.request import RequestConstants


class TestGetAccountsByNickname(object):

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
    @pytest.allure.story('account by nickname')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_get_accounts_nickname(self, config, content_type):
        get_response = config.freya.server_gateway.get_accounts_by_nickname([config.store.account.name],
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
    @pytest.allure.story('account by nickname')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_nickname', [
        pytest.param('', marks=pytest.mark.xfail(reason='', raises=AssertionError)),
        'invalid_nickname'
    ])
    def test_get_accounts_nickname_invalid_nickname(self, config, invalid_nickname):
        get_response = config.freya.server_gateway.get_accounts_by_nickname([invalid_nickname])
        get_response.expect_failure(result_code='CLIENT_ERROR_404')

    @pytest.allure.feature('server')
    @pytest.allure.story('account by nickname')
    @pytest.allure.severity(severity_level.MINOR)
    def test_get_accounts_nickname_none_nickname(self, config):
        get_response = config.freya.server_gateway.get_accounts_by_nickname([None])
        get_response.expect_failure(result_code='EXCEPTION')

    @pytest.allure.feature('server')
    @pytest.allure.story('account by nickname')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('bad_nickname', [
        'G1sMaHUbGxePOvjUm7Qo5YsBuBgkEYJ2l21u3qIg1gIj8u2ITd9mnbrVMMOLVGPtVEZaDdgTEheXg3vKnwz7Y4fe24f41StTGD5J', -1])
    def test_get_accounts_nickname_bad_nickname(self, config, bad_nickname):
        get_response = config.freya.server_gateway.get_accounts_by_nickname([bad_nickname])
        get_response.expect_failure()
