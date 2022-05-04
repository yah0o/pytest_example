import pytest
from allure import severity_level


@pytest.allure.feature('auth')
@pytest.allure.story('ping')
class TestAuthPing(object):

    @pytest.fixture(autouse=True)
    def setup(self, config):
        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here

    @pytest.allure.severity(severity_level.TRIVIAL)
    def test_ping(self, config):
        response = config.freya.auth_gateway.ping()
        response.assert_is_success()

    @pytest.allure.severity(severity_level.TRIVIAL)
    def test_ping_client(self, config):
        response = config.freya.auth_gateway.ping_client()
        response.assert_is_success()
