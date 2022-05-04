import uuid

import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities
from integration.main.request import RequestConstants, ResponseMessage
from integration.main.services import LegacyProductItem


class TestGetInventory(object):

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

    @pytest.mark.skip_for_regions('wgs11')
    @pytest.allure.feature('server')
    @pytest.allure.story('inventory')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_get_inventory_should_succeed_when_granting_xp(self, config, content_type):
        inventory_response = config.freya.server_gateway.get_inventory(config.store.wgid, content_type=content_type)
        inventory_response.assert_is_success()

        assert_that(inventory_response.content['body'], has_key('profile'))
        profile = inventory_response.content['body']['profile']
        assert_that(profile, has_key('profile_id'))

        xp = sum(int(el['amount']) for el in profile['currencies'] if
                 el['code'] == config.data.TEST_PRODUCT_XP.CURRENCIES.CODE)
        assert_that(xp, equal_to(0))

        grant_product_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_XP.COUNTRY,
            config.data.TEST_PRODUCT_XP.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT_XP.CODE, config.data.TEST_PRODUCT_XP.AMOUNT)]
        )
        grant_product_response.assert_is_success()

        re_inventory_response = config.freya.server_gateway.get_inventory(config.store.wgid, content_type=content_type)
        re_inventory_response.assert_is_success()

        assert_that(re_inventory_response.content['body'], has_key('profile'))
        profile = re_inventory_response.content['body']['profile']
        new_xp = sum(int(currency['amount']) for currency in profile['currencies'] if
                     currency['code'] == config.data.TEST_PRODUCT_XP.CURRENCIES.CODE)

        assert_that(xp + config.data.TEST_PRODUCT_XP.CURRENCIES.AMOUNT, equal_to(new_xp))

    @pytest.allure.feature('server')
    @pytest.allure.story('inventory')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_wgid', [-1, 0, .50, '', None])
    def test_get_inventory_should_fail_when_wgid_is_invalid(self, config, invalid_wgid):
        inventory_response = config.freya.server_gateway.get_inventory(invalid_wgid)
        inventory_response.expect_failure(result_code=ResponseMessage.INVALID_PROFILE_ID)

    @pytest.allure.feature('server')
    @pytest.allure.story('inventory')
    @pytest.allure.severity(severity_level.MINOR)
    def test_get_inventory_should_succeed_when_wgid_is_string(self, config):
        inventory_response = config.freya.server_gateway.get_inventory('invalid_wgid')
        inventory_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                          result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)
