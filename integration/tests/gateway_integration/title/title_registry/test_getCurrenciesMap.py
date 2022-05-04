import pytest
from allure import severity_level
from hamcrest import *


@pytest.allure.feature('title')
@pytest.allure.story('title registry')
@pytest.allure.severity(severity_level.MINOR)
class TestGetCurrenciesMap(object):

    def test_get_currencies_map_should_succeed_when_requested(self, config):
        currencies_response = config.freya.title_registry.get_currencies_virtual()
        currencies_response.assert_is_success()
        print(config.freya.title_registry.get_currencies_virtual().request)

        assert_that(currencies_response.content, has_key('data'))
        assert_that(currencies_response.content['data'], not_none())

        data = currencies_response.content['data']
        test_title = next((title for title in data if
                           title['title'] == config.environment['integration_title']), None)

        assert_that(test_title, has_key('currencies'))
        assert_that(test_title, has_key('title'))
        assert_that(test_title['title'], not_none())
        assert_that(test_title['title'], equal_to(config.environment['integration_title']))

        assert_that(test_title['currencies'], not_none())
        test_title_currencies = test_title['currencies']
        test_currency = next((currency for currency in test_title_currencies if
                              currency['local_code'] == config.data.TEST_CURRENCY.CURRENCY_CODE), None)

        assert_that(test_currency, not_none())
        assert_that(test_currency['local_code'], equal_to(config.data.TEST_CURRENCY.CURRENCY_CODE))
        assert_that(test_currency, has_key('platform_code'))
        assert_that(test_currency['platform_code'], equal_to('{}.{}'.format(
            config.environment['integration_title'],
            config.data.TEST_CURRENCY.CURRENCY_CODE
        )))
        assert_that(test_currency, has_key('owner_title'))
        assert_that(test_currency['owner_title'], equal_to(config.environment['integration_title']))
