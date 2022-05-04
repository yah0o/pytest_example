import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities, RandomUtilities
from integration.main.request import RequestConstants

EXTERNAL_NAME = 'china360'


class TestGetAccountByUid(object):

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

        config.store.uid = RandomUtilities.create_unique_id()
        create_external_account = config.spa.http.create_external_service_for_account(config.store.profile_id,
                                                                                      name=EXTERNAL_NAME,
                                                                                      uid=config.store.uid)
        create_external_account.assert_is_success()


        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(config.store.profile_id)
        delete_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('account by uid')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    @pytest.mark.parametrize('region', [
        'env',
        None
    ])
    def test_get_account_by_external_uid(self, config, content_type, region):
        if region:
            region = config.environment['region']
        get_response = config.freya.server_gateway.get_account_by_uid(config.store.uid, external_name=EXTERNAL_NAME,
                                                                      content_type=content_type,
                                                                      region=region)
        get_response.assert_is_success()

        account = get_response.content['body']['accounts']
        assert_that(str(account['profile_id']), equal_to(str(config.store.profile_id)))
        assert_that(str(account['wg_id']), equal_to(str(config.store.profile_id)))
        assert_that(account['nickname'], equal_to(config.store.account.name))
        assert_that(account, has_key('allowed'))
        assert_that(account['restrictions'], empty())

    @pytest.allure.feature('server')
    @pytest.allure.story('account by uid')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize(
        ('invalid_uid', 'result_code'), [
            (0, 'CLIENT_ERROR_404'),
            ('invalid_uid', 'CLIENT_ERROR_404'),
            (None, 'INVALID_UID'),
            ('', 'INVALID_UID'),
            ('NN56PfvynvpKA2izSxQGH4mH0gMbJ6DEGXvRGEDozocnUCUoziEj46IuMXXVlhVU1C12o69hDt5sKAF7bhZVb6c7MmNXBD8XwmZE',
             'CLIENT_ERROR_404')
        ])
    def test_get_account_by_uid_invalid_uid(self, config, invalid_uid, result_code):
        get_response = config.freya.server_gateway.get_account_by_uid(invalid_uid, external_name=EXTERNAL_NAME)
        get_response.expect_failure(result_code=result_code)

    @pytest.allure.feature('server')
    @pytest.allure.story('account by uid')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize(
        ('external_name', 'result_code'), [
            (0, 'CLIENT_ERROR_404'),
            ('invalid_uid', 'CLIENT_ERROR_409'),
            (None, 'INVALID_EXTERNAL_NAME'),
            ('', 'INVALID_EXTERNAL_NAME'),
            ('NN56PfvynvpKA2izSxQGH4mH0gMbJ6DEGXvRGEDozocnUCUoziEj46IuMXXVlhVU1C12o69hDt5sKAF7bhZVb6c7MmNXBD8XwmZE',
             'CLIENT_ERROR_409')
        ])
    def test_get_account_by_uid_invalid_external_name(self, config, result_code, external_name):
        get_response = config.freya.server_gateway.get_account_by_uid(config.store.uid, external_name=external_name)
        get_response.expect_failure(result_code=result_code)

    @pytest.allure.feature('server')
    @pytest.allure.story('account by uid')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize(
        ('region', 'result_code'), [
            (0, 'EXCEPTION'),
            ('invalid_uid', 'EXCEPTION'),
            ('', 'EXCEPTION'),
            ('XX', 'EXCEPTION')
        ])
    def test_get_account_by_uid_invalid_region(self, config, result_code, region):
        get_response = config.freya.server_gateway.get_account_by_uid(config.store.uid, external_name=EXTERNAL_NAME,
                                                                      region=region)
        get_response.expect_failure(result_code=result_code)