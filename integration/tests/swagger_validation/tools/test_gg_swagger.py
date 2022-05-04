import pytest

from integration.schemas import Schemas


class TestGGSwagger(object):

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
    def test_gg_discover(self, config):
        discovery_response = config.freya.tools_gateway.gg.discover(config.data.TEST_TITLE,
                                                                    config.environment['api']['key'])
        discovery_response.assert_is_success()
        Schemas.swagger_validate(discovery_response, '/api/v1/gg/{title_code}/discover')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_gg_execute(self, config):
        create_resonse = config.freya.tools_gateway.gg.execute(config.data.TEST_TITLE, "createplayer",
                                                               config.environment['api']['key'])
        create_resonse.assert_is_success()
        Schemas.swagger_validate(create_resonse, '/api/v1/gg/{title_code}/execute')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_gg_methods(self, config):
        methods_response = config.freya.tools_gateway.gg.methods(config.data.TEST_TITLE,
                                                                 config.environment['api']['key'])
        methods_response.assert_is_success()
        Schemas.swagger_validate(methods_response, '/api/v1/gg/{title_code}/methods')
