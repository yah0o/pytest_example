import pytest
from allure import severity_level
from hamcrest import *


@pytest.allure.feature('title')
@pytest.allure.story('title registry')
@pytest.allure.severity(severity_level.MINOR)
class TestGetNamespaces(object):

    def check_is_unique(self, res, property):
        return len(res) == len(set(i[property] for i in res))

    def test_get_namespaces_should_succeed_when_requested(self, config):
        namespaces_response = config.freya.title_registry.get_namespaces()
        namespaces_response.assert_is_success()

        assert_that(namespaces_response.content, has_key('namespaces'))
        assert_that(namespaces_response.content['namespaces'], not_none())
        assert_that(namespaces_response.content, has_key('updated_at'))
        assert_that(namespaces_response.content['updated_at'], not_none())

        namespaces = namespaces_response.content['namespaces']
        players_namespace = next((namespace for namespace in namespaces if
                                  namespace['namespace'] == config.environment['namespace']), None)

        assert_that(players_namespace, not_none())
        assert_that(players_namespace['namespace'], equal_to(config.environment['namespace']))
        assert_that(players_namespace, has_key('title_id'))
        assert_that(players_namespace, has_key('entity_type_id'))
        assert_that(players_namespace, has_key('full_title_id'))
        assert_that(players_namespace, has_key('nsid'))

        clans_namespace = next((namespace for namespace in namespaces if
                                namespace['namespace'] == '{}.{}'.format(config.environment['integration_title'],
                                                                         'players')), None)
        assert_that(clans_namespace, not_none())
        assert_that(clans_namespace['namespace'], equal_to('{}.{}'.format(config.environment['integration_title'],
                                                                          'players')))
        assert_that(clans_namespace, has_key('title_id'))
        assert_that(clans_namespace, has_key('entity_type_id'))
        assert_that(clans_namespace, has_key('full_title_id'))
        assert_that(clans_namespace, has_key('nsid'))

    def test_get_namespaces_nsid_should_be_unique(self, config):
        # TCS-12
        namespaces_response = config.freya.title_registry.get_namespaces()
        namespaces_response.assert_is_success()
        res = namespaces_response.content['namespaces']
        assert_that(self.check_is_unique(res, property='nsid'), equal_to(True), 'nsid is not unique')
