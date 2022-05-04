import time

import pytest

from integration.schemas import Schemas


class TestBranchPublishCatalogSwagger(object):

    @pytest.fixture(autouse=True)
    def setup(self, config):
        ###
        # Test setup
        login_response = config.freya.tools_gateway.login.auth_adfs_login(config.admin.username, config.admin.password)
        login_response.assert_is_success()

        title_response = config.freya.tools_gateway.title.get_title(config.data.TEST_TITLE)
        title_response.assert_is_success()
        config.store.title_versions = [version for version in title_response.content['title_versions']]

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_branch_publish_catalog_activateCatalog(self, config):
        title_version = next(
            (title_version for title_version in config.store.title_versions if title_version['active']), None)
        catalog_code = next(
            (catalog_activation['catalog'] for catalog_activation in title_version['catalogs_activations'] if
             int(catalog_activation['active_at']) <= time.time()), None)

        activate_response = config.freya.tools_gateway.publish_catalog.activate_catalog(config.data.TEST_TITLE,
                                                                                        title_version['id'],
                                                                                        catalog_code)
        activate_response.assert_is_success()
        Schemas.swagger_validate(activate_response,
                                 '/api/v1/get_title/{title_code}/version/{version_id}/activatecatalog')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_branch_publish_catalog_catalogPublished(self, config):
        title_version = next(
            (title_version for title_version in config.store.title_versions if title_version['active']), None)
        catalog_code = next(
            (catalog_activation['catalog'] for catalog_activation in title_version['catalogs_activations'] if
             int(catalog_activation['active_at']) <= time.time()), None)
        pub_version = catalog_code.split('-')[2]

        version_response = config.freya.tools_gateway.publish_catalog.get_published_version(config.data.TEST_TITLE,
                                                                                            config.data.TEST_TITLE_BRANCH,
                                                                                            pub_version)
        version_response.assert_is_success()
        Schemas.swagger_validate(version_response,
                                 '/api/v1/get_title/{title_code}/branch/{branch_name}/catalog/{pub_version}/published')

    # Integration with new tools flow
    @pytest.mark.skip_for_regions('nps1', 'nps11', 'wgt1', 'wgs11', 'trie')
    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_branch_publish_catalog_publish(self, config):
        title_version_ids = [version['id'] for version in config.store.title_versions]

        publish_response = config.freya.tools_gateway.publish_catalog.publish_working_catalog(config.data.TEST_TITLE,
                                                                                              config.data.TEST_TITLE_BRANCH,
                                                                                              title_version_ids,
                                                                                              int(time.time()))
        publish_response.assert_is_success()
        Schemas.swagger_validate(publish_response, '/api/v1/get_title/{title_code}/branch/{branch_name}/publish')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_branch_publish_catalog_validate(self, config):
        validate_response = config.freya.tools_gateway.publish_catalog.validate_working_catalog(config.data.TEST_TITLE,
                                                                                                config.data.TEST_TITLE_BRANCH)
        validate_response.assert_is_success()
        Schemas.swagger_validate(validate_response, '/api/v1/get_title/{title_code}/branch/{branch_name}/validate')
