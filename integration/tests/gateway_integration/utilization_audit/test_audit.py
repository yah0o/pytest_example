import pytest
from allure import severity_level
from hamcrest import assert_that, equal_to, has_key
from paudit_qa.clients import ClickHouseClient
from ulid import ulid
from waiting import wait

from integration.main.helpers import AccountUtilities
from integration.main.helpers.matchers import not_empty
from integration.main.request import RequestConstants


class TestGAPIUtilizationAudit(object):

    @pytest.fixture(autouse=True)
    def setup(self, config):
        ###
        # Test setup
        self.clickhouse_client = ClickHouseClient(host=config.environment['clickhouse'].host,
                                                  database=config.environment['clickhouse'].database,
                                                  user=config.environment['clickhouse'].user,
                                                  password=config.environment['clickhouse'].password
                                                  )

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

    @pytest.allure.feature('utilization audit')
    @pytest.allure.story('tracking id')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_tracking_id_ok(self, config):
        # test that /fetrchProductList server method is tracked in Clickhouse(audit storage)
        tr_id = ulid()
        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_STORE.STOREFRONT,
            config.store.wgid,
            config.data.TEST_STORE.COUNTRY,
            config.data.TEST_STORE.LANGUAGE,
            content_type=RequestConstants.ContentTypes.JSON,
            tracking_id=tr_id
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body'], has_key('uriList'))
        tracking_id = fetch_response.content['header']['log_id']
        assert_that(tracking_id, not_empty(),
                    'fetch_product_list_response key tracking_id is empty')
        assert_that(tracking_id, equal_to(tr_id), 'x-np-tracking-id in req in resp are different')
        wait(
            lambda: self.clickhouse_client.get_log(where='tracking=\'{}\''.format(tr_id)),
            timeout_seconds=30, sleep_seconds=1)
        clickhouse_record = self.clickhouse_client.get_log(
            where='tracking=\'{}\' AND requester=\'{}\''.format(tr_id, config.environment['integration_title']))[0]
        assert_that(clickhouse_record.tracking_id, equal_to(tr_id), 'tracking_ids in req and Clickhouse'
                                                                    'are different')
        assert_that(clickhouse_record.action, equal_to('/api/v1/fetchProductList/'), 'incorrect method name'
                                                                                     'in Clickhouse')
        assert_that(clickhouse_record.created_at, not_empty())
        assert_that(clickhouse_record.event_id, not_empty())
        assert_that(clickhouse_record.requester, equal_to(config.environment['integration_title']),
                    'incorrect requester in Clickhouse')
        assert_that(clickhouse_record.processor, equal_to(config.environment['clickhouse'].server_processor),
                    'incorrect processor in Clickhouse')

    @pytest.allure.feature('utilization audit')
    @pytest.allure.story('tracking id')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('track_id', [None, '', 'test'])
    def test_fetch_product_list_invalid_tracking_id_on_req(self, config, track_id):
        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_STORE.STOREFRONT,
            config.store.wgid,
            config.data.TEST_STORE.COUNTRY,
            config.data.TEST_STORE.LANGUAGE,
            content_type=RequestConstants.ContentTypes.JSON,
            tracking_id=track_id
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body'], has_key('uriList'))
        tracking_id = fetch_response.content['header']['log_id']
        assert_that(tracking_id, not_empty(),
                    'fetch_product_list_response key tracking_id is empty')

        wait(
            lambda: self.clickhouse_client.get_log(where='tracking=\'{}\''.format(tracking_id)),
            timeout_seconds=30, sleep_seconds=1)
        clickhouse_record = self.clickhouse_client.get_log(where='tracking=\'{}\''.format(tracking_id))[0]
        assert_that(clickhouse_record.tracking_id, equal_to(tracking_id))

    @pytest.allure.feature('utilization audit')
    @pytest.allure.story('tracking id')
    @pytest.allure.severity(severity_level.NORMAL)
    def test_tracking_id_with_auth_method(self, config):
        # Test on checking GAPI auth method stored in Clickhouse
        tr_id = ulid()
        login_response = config.freya.auth_gateway.login_with_email(config.store.account.email,
                                                                    config.store.account.password,
                                                                    tracking_id=tr_id)
        login_response.assert_is_success()
        wait(
            lambda: self.clickhouse_client.get_log(where='tracking=\'{}\''.format(tr_id)),
            timeout_seconds=30, sleep_seconds=1)
        clickhouse_record = self.clickhouse_client.get_log(
            where='tracking=\'{}\' AND requester=\'{}\''.format(tr_id, config.environment['integration_title']))[0]
        assert_that(clickhouse_record.tracking_id, not_empty())
        assert_that(clickhouse_record.action, equal_to('/api/v1/loginWithEmail/'), 'incorrect method name'
                                                                                   'in Clickhouse')
        assert_that(clickhouse_record.processor, equal_to(config.environment['clickhouse'].auth_processor),
                    'incorrect processor in Clickhouse')
