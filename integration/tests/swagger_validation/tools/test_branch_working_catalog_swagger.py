import os

import pytest

from integration.schemas import Schemas


class TestBranchWorkingCatalogSwagger(object):

    @pytest.fixture(autouse=True)
    def setup(self, config):
        ###
        # Test setup
        login_response = config.freya.tools_gateway.login.auth_adfs_login(config.admin.username, config.admin.password)
        login_response.assert_is_success()

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_branch_working_catalog_getCatalog(self, config):
        catalog_response = config.freya.tools_gateway.working_catalog.get_catalog(config.data.TEST_TITLE,
                                                                                  config.data.TEST_TITLE_BRANCH)
        catalog_response.assert_is_success()
        Schemas.swagger_validate(catalog_response,
                                 '/api/v1/get_title/{title_code}/branch/{branch_name}/catalog/working')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_branch_working_catalog_getVersion(self, config):
        catalog_response = config.freya.tools_gateway.working_catalog.get_catalog(config.data.TEST_TITLE,
                                                                                  config.data.TEST_TITLE_BRANCH)
        catalog_response.assert_is_success()
        pub_version = catalog_response.content['pub_version']

        version_response = config.freya.tools_gateway.working_catalog.get_version(config.data.TEST_TITLE,
                                                                                  config.data.TEST_TITLE_BRANCH,
                                                                                  pub_version)
        version_response.assert_is_success()
        Schemas.swagger_validate(version_response,
                                 '/api/v1/get_title/{title_code}/branch/{branch_name}/catalog/{publish_version}')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_branch_working_catalog_import(self, config):
        path, catalog_file = os.path.split(config.data.path)
        full_catalog_path = os.path.abspath(os.path.join(path, config.data.CATALOG))

        import_response = config.freya.tools_gateway.working_catalog.import_catalog(config.data.TEST_TITLE,
                                                                                    config.data.TEST_TITLE_BRANCH,
                                                                                    full_catalog_path, True)
        import_response.assert_is_success()
        Schemas.swagger_validate(import_response, '/api/v1/get_title/{title_code}/branch/{branch_name}/import')
