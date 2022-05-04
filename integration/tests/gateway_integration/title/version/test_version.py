import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers.matchers import has_keys


@pytest.allure.feature('title')
@pytest.allure.story('titleconfig')
@pytest.allure.severity(severity_level.MINOR)
class TestGetVersion(object):

    def test_get_version(self, config):
        version_response = config.freya.title_config.get_version()
        version_response.assert_is_success()
        assert_that(version_response.content, has_keys('name', 'realm', 'version'))
        assert_that(version_response.content['realm'], equal_to(config.environment['region']))
        assert_that(version_response.content['name'], not_none())
        assert_that(version_response.content['version'], not_none())