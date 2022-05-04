import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities
from integration.main.request import RequestConstants, ResponseMessage


class TestAccountCreated(object):

    @pytest.fixture(autouse=True)
    def setup(self, config):
        ###
        # Test setup
        account = AccountUtilities.create_account()
        account_created = config.spa.http.create_account(account.__dict__)
        account_created.assert_is_success()
        update_account = config.spa.http.update(account_created.content['id'],
                                                game=config.environment['test_title_pgn'])

        wgid = account_created.content['id']
        config.store.profile_id = account_created.content['id']

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(wgid)
        delete_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('account created')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_account_created(self, config, content_type):
        account_response = config.freya.server_gateway.account_created(
            config.store.profile_id,
            content_type=content_type
        )
        account_response.assert_is_success()

        assert_that(str(account_response.content['body']['profile_id']), equal_to(str(config.store.profile_id)))
        assert_that(account_response.content['body'], has_key('name'))
        assert_that(account_response.content['body']['game'], equal_to(config.environment['integration_title']))

    @pytest.allure.feature('server')
    @pytest.allure.story('account created')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_profile_id', [-1, 0, .50, '', None])
    def test_account_created_invalid_profile(self, config, invalid_profile_id):
        invalid_account_response = config.freya.server_gateway.account_created(invalid_profile_id)
        invalid_account_response.expect_failure(result_code=ResponseMessage.INVALID_PROFILE_ID)

    @pytest.allure.feature('server')
    @pytest.allure.story('account created')
    @pytest.allure.severity(severity_level.MINOR)
    def test_account_created_bad_profile(self, config):
        bad_account_response = config.freya.server_gateway.account_created('bad_profile_id')
        bad_account_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                            result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)
