import pytest
from allure import severity_level
from hamcrest import *


@pytest.allure.feature('title')
@pytest.allure.story('title registry')
@pytest.allure.severity(severity_level.MINOR)
class TestGetTitles(object):

    def test_get_title_should_succeed_when_requested_with_no_parameter(self, config):
        title_response = config.freya.title_registry.get_titles()
        title_response.assert_is_success()

        assert_that(title_response.content, has_key('titles'))
        assert_that(title_response.content['titles'], not_none())

        titles = title_response.content['titles']
        test_title = next((title for title in titles if title['code'] == config.environment['integration_title']), None)

        assert_that(test_title, not_none())
        assert_that(test_title['code'], equal_to(config.environment['integration_title']))
        assert_that(test_title, has_key('id'))
        assert_that(test_title, has_key('access'))
        assert_that(test_title, has_key('state'))
        assert_that(test_title, has_key('full_title_id'))
        assert_that(test_title, has_key('title'))
        assert_that(test_title, has_key('server_api_key'))
        assert_that(test_title['server_api_key'], equal_to(config.environment['api']['key']))
        assert_that(test_title, has_key('pgn'))
        assert_that(test_title['pgn'], equal_to(config.environment['test_title_pgn']))
        assert_that(test_title, has_key('pop'))
        assert_that(test_title, has_key('type'))
        assert_that(test_title, has_key('region'))
        assert_that(test_title, has_key('include_titles'))
        assert_that(test_title, has_key('public'))

    def test_get_title_should_succeed_when_requested_with_valid_parameter(self, config):
        title_response = config.freya.title_registry.get_titles(
            include=config.environment['integration_title']
        )
        title_response.assert_is_success()

        assert_that(title_response.content, has_key('titles'))
        assert_that(title_response.content['titles'], not_none())

        titles = title_response.content['titles']
        test_title = next((title for title in titles if title['code'] == config.environment['integration_title']), None)

        assert_that(test_title, not_none())
        assert_that(test_title['code'], equal_to(config.environment['integration_title']))
        assert_that(test_title, has_key('id'))
        assert_that(test_title, has_key('access'))
        assert_that(test_title, has_key('state'))
        assert_that(test_title, has_key('full_title_id'))
        assert_that(test_title, has_key('title'))
        assert_that(test_title, has_key('server_api_key'))
        assert_that(test_title['server_api_key'], equal_to(config.environment['api']['key']))
        assert_that(test_title, has_key('pgn'))
        assert_that(test_title['pgn'], equal_to(config.environment['test_title_pgn']))
        assert_that(test_title, has_key('pop'))
        assert_that(test_title, has_key('type'))
        assert_that(test_title, has_key('region'))
        assert_that(test_title, has_key('include_titles'))
        assert_that(test_title, has_key('public'))
