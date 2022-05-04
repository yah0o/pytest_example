import pytest
from allure import severity_level


class TestServerPing(object):

    @pytest.allure.feature('server')
    @pytest.allure.story('ping')
    @pytest.allure.severity(severity_level.TRIVIAL)
    def test_ping(self, config):
        response = config.freya.server_gateway.ping()
        response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('ping')
    @pytest.allure.severity(severity_level.TRIVIAL)
    def test_ping_client(self, config):
        response = config.freya.server_gateway.ping_client()
        response.assert_is_success()
