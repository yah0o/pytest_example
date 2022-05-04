import pytest
from allure import severity_level
from hamcrest import *


@pytest.allure.feature('title')
@pytest.allure.story('titleconfig')
@pytest.allure.severity(severity_level.MINOR)
class TestGetTitles(object):

    def test_get_titles(self, config):
        title_response = config.freya.title_config.get_all_titles()
        title_response.assert_is_success()
        assert_that(title_response.content['titles'], not_none(), 'Empty list of titles')
