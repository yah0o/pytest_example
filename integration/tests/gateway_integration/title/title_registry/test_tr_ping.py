import pytest
from allure import severity_level
from hamcrest import *


@pytest.allure.feature('title')
@pytest.allure.story('title registry')
@pytest.allure.severity(severity_level.MINOR)
class TestPing(object):

    def test_ping(self, config):
        title_response = config.freya.title_registry.ping()
        title_response.assert_is_success()
        assert_that(title_response.content, equal_to('pong'))
