import pytest
from allure import severity_level
from hamcrest import assert_that, equal_to, is_not, contains_string, contains_inanyorder

from integration.main.helpers import TCSTitleEntitiesv2, TCSSharedTitleEntitiesv2
from integration.main.helpers.matchers import has_keys
from integration.main.request import ResponseMessage


@pytest.allure.feature('title')
@pytest.allure.story('titleconfig')
@pytest.allure.severity(severity_level.NORMAL)
class TestPublishTitlev2(object):

    @pytest.mark.skip(reason='FOR LOCAL RUN ONLY IN CASE OF NOT HAVING CORRECT DELETE MECHANISM')
    def test_publish_title_v2_should_succeed_with_valid_title_schema(self, config):
        title_response = config.freya.title_config.publish_titles_v2(title_code=TCSTitleEntitiesv2.code,
                                                                     titleid=TCSTitleEntitiesv2.titleid,
                                                                     title_id=TCSTitleEntitiesv2.title_id,
                                                                     friendly_name=TCSTitleEntitiesv2.friendly_name,
                                                                     pgn=TCSTitleEntitiesv2.pgn,
                                                                     pop=TCSTitleEntitiesv2.pop,
                                                                     namespace_id=TCSTitleEntitiesv2.title_id,
                                                                     namespace_title_id=TCSTitleEntitiesv2.namespace_title_id,
                                                                     full_title_id=TCSTitleEntitiesv2.full_title_id,
                                                                     key=TCSTitleEntitiesv2.key,
                                                                     entity_type_id=TCSTitleEntitiesv2.entity_type_id,
                                                                     title_type="game")
        title_response.assert_is_success()

    @pytest.mark.parametrize(("title_id", "error_message"),
                             [
                                 (-1, 'titleId must be greater than 0'),
                                 (0, 'titleId must be greater than 0'),
                                 (.5, 'titleId must be greater than 0'),
                                 (65536, 'titleId must be less than 65536')
                             ])
    def test_publish_title_v2_should_fail_with_invalid_title_id(self, config, title_id, error_message):
        title_response = config.freya.title_config.publish_titles_v2(title_code=TCSTitleEntitiesv2.code,
                                                                     titleid=TCSTitleEntitiesv2.titleid,
                                                                     title_id=title_id,
                                                                     friendly_name=TCSTitleEntitiesv2.friendly_name,
                                                                     pgn=TCSTitleEntitiesv2.pgn,
                                                                     pop=TCSTitleEntitiesv2.pop,
                                                                     namespace_id=TCSTitleEntitiesv2.title_id,
                                                                     key=TCSTitleEntitiesv2.key,
                                                                     entity_type_id=TCSTitleEntitiesv2.entity_type_id,
                                                                     title_type="game")
        title_response.expect_failure(result_message=error_message)

    @pytest.mark.parametrize(("friendly_name"), ["", "s" * 121])
    def test_publish_title_v2_should_fail_with_invalid_friendly_name(self, config, friendly_name):
        title_response = config.freya.title_config.publish_titles_v2(title_code=TCSTitleEntitiesv2.code,
                                                                     titleid=TCSTitleEntitiesv2.titleid,
                                                                     title_id=TCSTitleEntitiesv2.title_id,
                                                                     friendly_name=friendly_name,
                                                                     pgn=TCSTitleEntitiesv2.pgn,
                                                                     pop=TCSTitleEntitiesv2.pop,
                                                                     namespace_id=TCSTitleEntitiesv2.title_id,
                                                                     key=TCSTitleEntitiesv2.key,
                                                                     entity_type_id=TCSTitleEntitiesv2.entity_type_id,
                                                                     title_type="game")
        title_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR)

    @pytest.mark.parametrize(("pgn"), ["", "s", "s" * 21])
    def test_publish_title_v2_should_fail_with_invalid_pgn(self, config, pgn):
        title_response = config.freya.title_config.publish_titles_v2(title_code=TCSTitleEntitiesv2.code,
                                                                     titleid=TCSTitleEntitiesv2.titleid,
                                                                     title_id=TCSTitleEntitiesv2.title_id,
                                                                     friendly_name=TCSTitleEntitiesv2.friendly_name,
                                                                     pgn=pgn,
                                                                     pop=TCSTitleEntitiesv2.pop,
                                                                     namespace_id=TCSTitleEntitiesv2.title_id,
                                                                     key=TCSTitleEntitiesv2.key,
                                                                     entity_type_id=TCSTitleEntitiesv2.entity_type_id,
                                                                     title_type="game")
        title_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR)

    @pytest.mark.parametrize(("titleid", "error_message"), [
        (-1, 'id must be greater than 0'),
        (0, 'id must be greater than 0'),
        (.5, 'id must be greater than 0')
    ])
    def test_publish_title_v2_should_fail_with_invalid_id(self, config, titleid, error_message):
        title_response = config.freya.title_config.publish_titles_v2(title_code=TCSTitleEntitiesv2.code,
                                                                     titleid=titleid,
                                                                     title_id=TCSTitleEntitiesv2.title_id,
                                                                     friendly_name=TCSTitleEntitiesv2.friendly_name,
                                                                     pgn=TCSTitleEntitiesv2.pgn,
                                                                     pop=TCSTitleEntitiesv2.pop,
                                                                     namespace_id=TCSTitleEntitiesv2.title_id,
                                                                     key=TCSTitleEntitiesv2.key,
                                                                     entity_type_id=TCSTitleEntitiesv2.entity_type_id,
                                                                     title_type="game")
        title_response.expect_failure(result_message=error_message)

    @pytest.mark.skip(reason='FOR LOCAL RUN ONLY IN CASE OF NOT HAVING CORRECT DELETE MECHANISM')
    def test_publish_title_v2_should_succeed_with_no_optional_params_req(self, config):
        # namespace_id could not be 0 after publishing title via e.g. Tools2.5 [FREYA-383]
        title_response = config.freya.title_config.publish_titles_v2(title_code=TCSTitleEntitiesv2.code,
                                                                     titleid=TCSTitleEntitiesv2.titleid,
                                                                     title_id=TCSTitleEntitiesv2.title_id,
                                                                     friendly_name=TCSTitleEntitiesv2.friendly_name,
                                                                     pgn=TCSTitleEntitiesv2.pgn,
                                                                     pop=TCSTitleEntitiesv2.pop,
                                                                     namespace_id=TCSTitleEntitiesv2.namespace_id,
                                                                     key=TCSTitleEntitiesv2.key,
                                                                     entity_type_id=TCSTitleEntitiesv2.entity_type_id,
                                                                     title_type="game")
        title_response.assert_is_success()

    @pytest.mark.skip(reason='FOR LOCAL RUN ONLY IN CASE OF NOT HAVING CORRECT DELETE MECHANISM')
    def test_publish_title_v2_should_update_title_components_for_title(self, config):
        title_response = config.freya.title_config.publish_titles_v2(title_code=TCSTitleEntitiesv2.code,
                                                                     titleid=TCSTitleEntitiesv2.titleid,
                                                                     title_id=TCSTitleEntitiesv2.title_id,
                                                                     friendly_name=TCSTitleEntitiesv2.friendly_name,
                                                                     pgn=TCSTitleEntitiesv2.pgn,
                                                                     pop=TCSTitleEntitiesv2.pop,
                                                                     namespace_id=TCSTitleEntitiesv2.namespace_id,
                                                                     entity_type_id=TCSTitleEntitiesv2.entity_type_id,
                                                                     key=TCSTitleEntitiesv2.key,
                                                                     platform_config=TCSTitleEntitiesv2.platfrom_config,
                                                                     title_type="game")
        title_response.assert_is_success()
        components_response = config.freya.title_registry.get_components()
        resources = components_response.content['resources']
        game_resource = next((resource for resource in resources if
                              resource['title'] == TCSTitleEntitiesv2.code and resource['component'] == 'game'), None)
        assert_that(game_resource, is_not(None), 'title components were not updated')

    @pytest.mark.skip(reason='FOR LOCAL RUN ONLY IN CASE OF NOT HAVING CORRECT DELETE MECHANISM')
    def test_publish_title_v2_should_delete_title_components_when_req_has_no_platform_config(self, config):
        # [FREYA-383]
        title_response = config.freya.title_config.publish_titles_v2(title_code=TCSTitleEntitiesv2.code,
                                                                     titleid=TCSTitleEntitiesv2.titleid,
                                                                     title_id=TCSTitleEntitiesv2.title_id,
                                                                     friendly_name=TCSTitleEntitiesv2.friendly_name,
                                                                     pgn=TCSTitleEntitiesv2.pgn,
                                                                     pop=TCSTitleEntitiesv2.pop,
                                                                     namespace_id=TCSTitleEntitiesv2.namespace_id,
                                                                     entity_type_id=TCSTitleEntitiesv2.entity_type_id,
                                                                     key=TCSTitleEntitiesv2.key,
                                                                     platform_config=TCSTitleEntitiesv2.platfrom_config,
                                                                     title_type="game")
        title_response.assert_is_success()
        title_response2 = config.freya.title_config.publish_titles_v2(title_code=TCSTitleEntitiesv2.code,
                                                                      titleid=TCSTitleEntitiesv2.titleid,
                                                                      title_id=TCSTitleEntitiesv2.title_id,
                                                                      friendly_name=TCSTitleEntitiesv2.friendly_name,
                                                                      pgn=TCSTitleEntitiesv2.pgn,
                                                                      pop=TCSTitleEntitiesv2.pop,
                                                                      namespace_id=TCSTitleEntitiesv2.namespace_id,
                                                                      entity_type_id=TCSTitleEntitiesv2.entity_type_id,
                                                                      key=TCSTitleEntitiesv2.key,
                                                                      title_type="game"
                                                                      )
        title_response2.assert_is_success()
        components_response = config.freya.title_registry.get_components()
        resources = components_response.content['resources']
        game_resource = next((resource for resource in resources if
                              resource['title'] == TCSTitleEntitiesv2.code and resource['component'] == 'game'), None)
        assert_that(game_resource, equal_to(None), 'title components were not deleted')

    @pytest.mark.skip(reason='FOR LOCAL RUN ONLY IN CASE OF NOT HAVING CORRECT DELETE MECHANISM')
    @pytest.mark.parametrize(("automatic_registration", "external_product_cdn", "access",
                              "enforce_prerequisites", "public", "internal", "state"), [
                                 (True, True, True, True, True, True, True),
                                 (False, False, False, False, False, False, False)
                             ])
    def test_publish_title_v2_should_succeed_with_additional_parameters(self, config,
                                                                        automatic_registration,
                                                                        external_product_cdn,
                                                                        access,
                                                                        enforce_prerequisites,
                                                                        public,
                                                                        internal,
                                                                        state):
        # FREYA-522
        title_code = TCSTitleEntitiesv2.code
        title_response = config.freya.title_config.publish_titles_v2(title_code=title_code,
                                                                     titleid=TCSTitleEntitiesv2.titleid,
                                                                     title_id=TCSTitleEntitiesv2.title_id,
                                                                     friendly_name=TCSTitleEntitiesv2.friendly_name,
                                                                     pgn=TCSTitleEntitiesv2.pgn,
                                                                     pop=TCSTitleEntitiesv2.pop,
                                                                     namespace_id=TCSTitleEntitiesv2.title_id,
                                                                     namespace_title_id=TCSTitleEntitiesv2.namespace_title_id,
                                                                     full_title_id=TCSTitleEntitiesv2.full_title_id,
                                                                     key=TCSTitleEntitiesv2.key,
                                                                     entity_type_id=TCSTitleEntitiesv2.entity_type_id,
                                                                     automatic_registration=True,
                                                                     external_product_cdn=True,
                                                                     access=True,
                                                                     enforce_prerequisites=True,
                                                                     public=True,
                                                                     view_entitlement_code='test',
                                                                     access_entitlement_code='test',
                                                                     comment='test',
                                                                     internal=True,
                                                                     state=False,
                                                                     title_type="game"
                                                                     )
        title_response.assert_is_success()
        get_title_response = config.freya.title_config.get_titles(title_id_or_code=title_code)
        assert_that(get_title_response[0], has_keys('automatic_registration', 'external_product_cdn', 'access',
                                                    'enforce_prerequisites', 'public', 'view_entitlement_code',
                                                    'comment', 'internal', 'state'))

    @pytest.mark.skip(reason='FOR LOCAL RUN ONLY IN CASE OF NOT HAVING CORRECT DELETE MECHANISM')
    def test_publish_shared_title_v2_should_succeed(self, config):
        title_response = config.freya.title_config.publish_titles_v2(title_code=TCSSharedTitleEntitiesv2.code,
                                                                     titleid=TCSSharedTitleEntitiesv2.titleid,
                                                                     title_id=TCSSharedTitleEntitiesv2.title_id,
                                                                     friendly_name=TCSSharedTitleEntitiesv2.friendly_name,
                                                                     pgn=TCSSharedTitleEntitiesv2.pgn,
                                                                     pop=TCSSharedTitleEntitiesv2.pop,
                                                                     namespace_id=TCSSharedTitleEntitiesv2.namespace_id,
                                                                     namespace_title_id=TCSSharedTitleEntitiesv2.namespace_title_id,
                                                                     full_title_id=TCSSharedTitleEntitiesv2.full_title_id,
                                                                     key=TCSSharedTitleEntitiesv2.key,
                                                                     entity_type_id=TCSSharedTitleEntitiesv2.entity_type_id,
                                                                     title_type=TCSSharedTitleEntitiesv2.title_type)
        title_response.assert_is_success()

    @pytest.mark.parametrize(("pgn"), ["", "s", "s" * 21])
    def test_publish_shared_title_v2_should_fail_with_invalid_pgn(self, config, pgn):
        title_response = config.freya.title_config.publish_titles_v2(title_code=TCSSharedTitleEntitiesv2.code,
                                                                     titleid=TCSSharedTitleEntitiesv2.titleid,
                                                                     title_id=TCSSharedTitleEntitiesv2.title_id,
                                                                     friendly_name=TCSSharedTitleEntitiesv2.friendly_name,
                                                                     pgn=pgn,
                                                                     pop=TCSSharedTitleEntitiesv2.pop,
                                                                     namespace_id=TCSSharedTitleEntitiesv2.title_id,
                                                                     key=TCSSharedTitleEntitiesv2.key,
                                                                     entity_type_id=TCSSharedTitleEntitiesv2.entity_type_id,
                                                                     title_type=TCSSharedTitleEntitiesv2.title_type)
        title_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR)
