import pytest
from allure import severity_level
from hamcrest import *


@pytest.allure.feature('title')
@pytest.allure.story('title registry')
@pytest.allure.severity(severity_level.MINOR)
class TestGetComponents(object):

    def test_get_components_should_succeed_when_requested(self, config):
        components_response = config.freya.title_registry.get_components()
        components_response.assert_is_success()

        assert_that(components_response.content, has_key('resources'))
        assert_that(components_response.content['resources'], not_none())

        resources = components_response.content['resources']
        chat_resource = next((resource for resource in resources if
                              resource['component'] == 'chat'), None)

        assert_that(chat_resource, not_none())
        assert_that(chat_resource['component'], equal_to('chat'))
        assert_that(chat_resource, has_key('title'))
        assert_that(chat_resource, has_key('pgn'))

        game_resource = next((resource for resource in resources if
                              resource['component'] == 'game'), None)

        assert_that(game_resource, not_none())
        assert_that(game_resource['component'], equal_to('game'))
        assert_that(game_resource, has_key('title'))
        assert_that(game_resource, has_key('pgn'))
