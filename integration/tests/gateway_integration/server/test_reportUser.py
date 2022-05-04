import pytest
from allure import severity_level

from integration.main.helpers import AccountUtilities
from integration.main.request import RequestConstants


#  Delete test module after FREYA-898

@pytest.mark.skip(reason='FREYA-898')
class TestReportUser(object):

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
    @pytest.allure.story('report user')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.xfail(reason='Not yet implemented', raises=AssertionError)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_report_user(self, config, content_type):
        report_response = config.freya.server_gateway.report_user(str(config.store.reporter_id),
                                                                  content_type=content_type)
        report_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('report user')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_reporter_id', [-1, 0, .50, '', None])
    def test_report_user_invalid_reporter_id(self, config, invalid_reporter_id):
        report_response = config.freya.server_gateway.report_user(invalid_reporter_id)
        report_response.expect_failure(code=404, message='HTTP 404 Not Found')

    @pytest.allure.feature('server')
    @pytest.allure.story('report user')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('bad_reporter_id', ['bad_reporter_id',
                                                 'N5rLegBEESn3ZtEYq3vxEwIYHedqx6ULE4o67hnzWhjpeE2Bf9qHJsrVEHMzAtqlbbOmMmD8rSjlkiqNHXO50DexvOqxeHa1WMGJ'])
    def test_report_user_bad_reporter_id(self, config, bad_reporter_id):
        report_response = config.freya.server_gateway.report_user(bad_reporter_id)
        report_response.expect_failure(code=404, message='HTTP 404 Not Found')
