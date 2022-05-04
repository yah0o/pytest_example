import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities
from integration.main.helpers.utils import random_transaction_id
from integration.main.request import RequestBuilder, RequestConstants


class TestFetchProductListState(object):

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

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product list state')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_fetch_product_list_state_succeeded(self, config, content_type):

        expected_products = config.data.TEST_STORE.PRODUCTS

        fetch_response = config.freya.server_gateway.fetch_product_list_state(
            config.data.TEST_STORE.STOREFRONT,
            config.store.profile_id,
            config.data.TEST_STORE.COUNTRY,
            config.data.TEST_STORE.LANGUAGE,
            content_type=content_type,
            product_codes=list(config.data.TEST_STORE.PRODUCTS),
            response_fields=['account_balance', 'items']

        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body'], has_key('items'), 'Response has items field')
        assert_that(fetch_response.content['body'], has_key('account_balance'), 'Response has account_balance field')

        original_list = fetch_response.content['body']['items']
        assert_that(len(original_list), equal_to(len(expected_products)), 'len of expected product equal to original')

        config.log.info('Ensuring returned URIs are unique')
        original_len = len([i['product_url'] for i in original_list])
        uri_set = set([i['product_url'] for i in original_list])
        assert_that(
            original_len,
            equal_to(len(uri_set)),
            '{} has duplicate entries'.format(i for i in original_list if i not in uri_set)
        )

        uri_list_products = []
        for uri in [i['product_url'] for i in original_list]:
            product_response = RequestBuilder(uri).get()
            product_response.assert_is_success()
            uri_list_products.append(product_response.content['product_code'])

        assert_that(sorted(expected_products), equal_to(sorted(uri_list_products)))

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product list state')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_fetch_product_list_state_succeeded_account_balace(self, config, content_type):

        grant_response = config.freya.server_gateway.grant_entitlement(
            config.store.profile_id,
            config.data.TEST_FRONTLINE_TANK_TAG.TOKEN,
            1,
            tx_id=random_transaction_id(),
            content_type=content_type)
        grant_response.assert_is_success()

        fetch_response = config.freya.server_gateway.fetch_product_list_state(
            config.data.TEST_FRONTLINE_TANK_TAG.STOREFRONT,
            config.store.profile_id,
            config.data.TEST_FRONTLINE_TANK_TAG.COUNTRY,
            config.data.TEST_FRONTLINE_TANK_TAG.LANGUAGE,
            content_type=content_type,
            product_codes=[config.data.TEST_FRONTLINE_TANK_TAG.PRODUCT],
            response_fields=['account_balance']

        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body'], has_key('account_balance'), 'Response has account_balance field')

        frontline_token = fetch_response.content['body']['account_balance']['personal_discounts'][0]
        assert_that(frontline_token['code'], equal_to(config.data.TEST_FRONTLINE_TANK_TAG.TOKEN),
                    'frontline token exist in repsonse')
