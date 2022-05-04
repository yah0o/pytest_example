import pytest
from allure import severity_level
from hamcrest import *


@pytest.allure.feature('title')
@pytest.allure.story('titleconfig')
@pytest.allure.severity(severity_level.MINOR)
class TestGetActiveTitles(object):

    def test_get_active_titles(self, config):
        title_response = config.freya.title_config.get_active_titles()
        title_response.assert_is_success()
        # assert_that(title_response.content['titles'], not_none(), 'Empty list of titles')
        titles = title_response.content['titles']
        is_active = next((title for title in titles if title['title_versions'][0]['active'] is True), None)
        assert_that(is_active, 'There are inactive titles in response')
