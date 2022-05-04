import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities
from integration.main.request import RequestConstants


class TestGetAccountsByLogin(object):

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
    @pytest.allure.story('account by login')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_get_accounts_by_login(self, config, content_type):
        get_response = config.freya.server_gateway.get_accounts_by_login([config.store.account.email],
                                                                         content_type=content_type)
        get_response.assert_is_success()

        assert_that(get_response.content['body']['accounts'], has_length(1))
        account = get_response.content['body']['accounts'][0]
        assert_that(str(account['profile_id']), equal_to(str(config.store.profile_id)))
        assert_that(str(account['wg_id']), equal_to(str(config.store.wgid)))
        assert_that(account['nickname'], equal_to(config.store.account.name))
        assert_that(account, has_key('allowed'))
        assert_that(account['restrictions'], empty())

    @pytest.allure.feature('server')
    @pytest.allure.story('account by login')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_email', [0, 'invalid_email',
                                               'NN56PfvynvpKA2izSxQGH4mH0gMbJ6DEGXvRGEDozocnUCUoziEj46IuMXXVlhVU1C12o69hDt5sKAF7bhZVb6c7MmNXBD8XwmZE'])
    def test_get_accounts_by_login_invalid_email(self, config, invalid_email):
        get_response = config.freya.server_gateway.get_accounts_by_login([invalid_email])
        get_response.expect_failure()

    @pytest.allure.feature('server')
    @pytest.allure.story('account by login')
    @pytest.allure.severity(severity_level.MINOR)
    def test_get_accounts_by_login_none_email(self, config):
        get_response = config.freya.server_gateway.get_accounts_by_login([''])
        get_response.expect_failure(result_code='CLIENT_ERROR_404')

    @pytest.allure.feature('server')
    @pytest.allure.story('account by login')
    @pytest.allure.severity(severity_level.MINOR)
    def test_get_accounts_by_login_none_email(self, config):
        get_response = config.freya.server_gateway.get_accounts_by_login([None])
        get_response.expect_failure(result_code='EXCEPTION')
