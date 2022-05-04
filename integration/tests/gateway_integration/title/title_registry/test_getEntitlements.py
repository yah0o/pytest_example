import pytest
from allure import severity_level
from hamcrest import *


@pytest.allure.feature('title')
@pytest.allure.story('title registry')
@pytest.allure.severity(severity_level.MINOR)
class TestGetEntitlements(object):

    def test_get_entitlements_should_succeed_when_requested(self, config):
        entitlements_response = config.freya.title_registry.get_entitlements()
        entitlements_response.assert_is_success()

        assert_that(entitlements_response.content, has_key('entitlements'))
        assert_that(entitlements_response.content['entitlements'], not_none())

        entitlements = entitlements_response.content['entitlements']
        test_entitlement = next((entitlement for entitlement in entitlements if
                                 entitlement['title_code'] == config.environment['shared_entitlement']), None)

        assert_that(test_entitlement, not_none())
        assert_that(test_entitlement['title_code'], equal_to(config.environment['shared_entitlement']))
        assert_that(test_entitlement, has_key('id'))
        assert_that(test_entitlement, has_key('code'))
        assert_that(test_entitlement, has_key('version'))
        assert_that(test_entitlement, has_key('friendly_name'))
        assert_that(test_entitlement, has_key('reported'))
