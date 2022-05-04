import uuid

import pytest
from allure import severity_level
from hamcrest import *
from integration.main.helpers import AccountUtilities, InventoryUtilities
from integration.main.request import RequestConstants


class TestGetPurchaseStatusByOrderId(object):

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

        inventory_response = config.freya.server_gateway.get_full_inventory(config.store.profile_id)
        inventory_response.assert_is_success()

        all_entitlements = InventoryUtilities.get_all_entitlements(inventory_response.content['body']['profile'])
        assert_that(sum(entitlement['amount'] for entitlement in all_entitlements), equal_to(0))

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(config.store.wgid)
        delete_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase status by order id')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_purchase_status_by_order_id(self, config, content_type):
        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PURCHASE.FREE.PRODUCT_CODE,
            config.data.TEST_PURCHASE.FREE.AMOUNT,
            [],
            storefront=config.data.TEST_PURCHASE.FREE.STOREFRONT
        )
        purchase_response.assert_is_success()
        order_id = purchase_response.content['body']['order_id']

        status_response = config.freya.server_gateway.get_purchase_status_by_order_id(order_id, config.store.profile_id,
                                                                                      content_type=content_type)
        status_response.assert_is_success()

        assert_that(status_response.content['body'], has_key('purchase_status'))
        assert_that(status_response.content['body']['order_id'], equal_to(order_id))

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase status by order id')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.xfail(reason='FREYA-894')
    @pytest.mark.parametrize('invalid_order_id', [
        '00000000-0000-0000-0000-000000000000',
        '00000000-0000-0000-0000-00000000000000',
        '00000000-0000-0000-0000-0000000000',
        '00000000-0000-XXXX-0000-000000000000',
        'bad_order_id',
        0,
        -1
    ])
    def test_purchase_status_by_order_id_invalid_order_id(self, config, invalid_order_id):
        status_response = config.freya.server_gateway.get_purchase_status_by_order_id(invalid_order_id,
                                                                                      config.store.profile_id)
        status_response.expect_failure(result_code='UNKNOWN_ORDER_ID')

    @pytest.mark.skip_for_regions('trie')
    @pytest.allure.feature('server')
    @pytest.allure.story('purchase status by order id')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_profile_id', [-1, 0, .50, '', None])
    def test_purchase_status_by_order_id_bad_profile_id(self, config, invalid_profile_id):
        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PURCHASE.FREE.PRODUCT_CODE,
            config.data.TEST_PURCHASE.FREE.AMOUNT,
            [],
            storefront=config.data.TEST_PURCHASE.FREE.STOREFRONT
        )
        purchase_response.assert_is_success()

        status_response = config.freya.server_gateway.get_purchase_status_by_order_id(
            purchase_response.content['body']['order_id'], invalid_profile_id)
        status_response.assert_is_success()
