import pytest
from allure import severity_level
from hamcrest import *


@pytest.allure.feature('title')
@pytest.allure.story('title registry')
@pytest.allure.severity(severity_level.MINOR)
class TestGetEntitlementsMap(object):

    def test_get_entitlements_should_succeed_when_requested(self, config):
        title_response = config.freya.title_registry.get_entitlements_map()
        title_response.assert_is_success()

        assert_that(title_response.content, has_key('data'))
        assert_that(title_response.content['data'], not_none())

        data = title_response.content['data']
        shared_entitlement = next((entitlement for entitlement in data
                                   if entitlement['title'] == config.environment['shared_entitlement']), None)
        assert_that(shared_entitlement, not_none())
        assert_that(shared_entitlement['title'], equal_to(config.environment['shared_entitlement']))

        entitlements = shared_entitlement['entitlements']
        shared_premium = next((entitlement for entitlement in entitlements if
                               entitlement['owner_title'] == config.environment['shared_entitlement']), None)
        assert_that(shared_premium, not_none())
        assert_that(shared_premium, has_key('local_code'))
        assert_that(shared_premium, has_key('owner_title'))
        assert_that(shared_premium, has_key('platform_code'))
