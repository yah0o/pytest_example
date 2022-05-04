import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers.matchers import has_keys


@pytest.allure.feature('title')
@pytest.allure.story('titleconfig')
@pytest.allure.severity(severity_level.MINOR)
class TestGetTitle(object):

    def test_get_single_title_should_succeed_with_valid_title_code(self, config):
        title_code = config.environment['integration_title']
        title_response = config.freya.title_config.get_titles(title_id_or_code=title_code)
        assert_that(title_response, not_none(), 'Title is empty')
        assert_that(title_response[0], has_keys('access', 'state', 'id', 'title_id',
                                                'friendly_name', 'pgn', 'pop', 'code',
                                                'created_at', 'updated_at',
                                                'automatic_registration', 'internal', 'external_product_cdn',
                                                'enforce_prerequisites', 'event_schemas', 'document_schemas',
                                                'namespaces', 'title_versions', 'permitting_titles', 'type', 'public',
                                                'ggapi'))
