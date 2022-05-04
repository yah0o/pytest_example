import pytest
from jsonschema import ValidationError

from integration.schemas import Schemas


class TestTitleSwagger(object):

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
    def test_title_branch(self, config):

        branch_response = config.freya.tools_gateway.title.branch(config.data.TEST_TITLE)
        branch_response.assert_is_success()
        Schemas.swagger_validate(branch_response, '/api/v1/get_title/{title_code}/branch')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_title_branchCatalog(self, config):

        branch_response = config.freya.tools_gateway.title.branch_catalog(config.data.TEST_TITLE,
                                                                          config.data.TEST_TITLE_BRANCH)
        branch_response.assert_is_success()
        Schemas.swagger_validate(branch_response, '/api/v1/get_title/{title_code}/branch/{branch_name}/catalog')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_title_branchName(self, config):

        branch_response = config.freya.tools_gateway.title.branch_name(config.data.TEST_TITLE,
                                                                       config.data.TEST_TITLE_BRANCH)
        branch_response.assert_is_success()
        Schemas.swagger_validate(branch_response, '/api/v1/get_title/{title_code}/branch/{branch_name}')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_title_code(self, config):

        title_response = config.freya.tools_gateway.title.get_title(config.data.TEST_TITLE)
        title_response.assert_is_success()
        Schemas.swagger_validate(title_response, '/api/v1/get_title/{title_code}')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_title_count(self, config):

        # No schema
        pass

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_title_groups(self, config):

        # No schema
        pass

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_title_list(self, config):

        title_response = config.freya.tools_gateway.title.title_list()
        title_response.assert_is_success()
        Schemas.swagger_validate(title_response, '/api/v1/get_title')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_title_publish(self, config):

        publish_response = config.freya.tools_gateway.title.publish(config.data.TEST_TITLE)
        publish_response.assert_is_success()
        Schemas.swagger_validate(publish_response, '/api/v1/get_title/{title_code}/publish')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_title_version(self, config):

        version_response = config.freya.tools_gateway.title.version(config.data.TEST_TITLE,
                                                                    config.environment['version'])
        version_response.assert_is_success()
        Schemas.swagger_validate(version_response, '/api/v1/get_title/{title_code}/titleversion/{tv_id}')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_title_versionList(self, config):

        versions_response = config.freya.tools_gateway.title.title_version_list(config.data.TEST_TITLE)
        versions_response.assert_is_success()
        Schemas.swagger_validate(versions_response, '/api/v1/get_title/{title_code}/titleversion')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_title_permissions(self, config):

        error = None
        new_apis = ["/test", "/potato"]

        try:
            changes = [{
                'type': 'CLIENT_API',
                'action': 'ADD',
                'title_code': config.data.TEST_TITLE,
                'data': api
            } for api in new_apis]

            updated_permissions_response = config.freya.tools_gateway.title.update_permissions(config.data.TEST_TITLE,
                                                                                               changes)
            updated_permissions_response.assert_is_success()
            Schemas.swagger_validate(updated_permissions_response, '/api/v1/get_title/{title_code}/permissions')
        except (ValidationError, AssertionError), argument:
            error = argument

        changes = [{
            'type': 'CLIENT_API',
            'action': 'REMOVE',
            'title_code': config.data.TEST_TITLE,
            'data': api
        } for api in new_apis]

        updated_empty_permissions_response = config.freya.tools_gateway.title.update_permissions(config.data.TEST_TITLE,
                                                                                                 changes)
        updated_empty_permissions_response.assert_is_success()

        if error:
            pytest.fail(error)
