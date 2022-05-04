import pytest
from allure import severity_level
from hamcrest import *


@pytest.allure.feature('title')
@pytest.allure.story('title registry')
@pytest.allure.severity(severity_level.MINOR)
class TestGetCurrencies(object):

    def test_get_currencies_should_succeed_when_requested(self, config):
        currencies_response = config.freya.title_registry.get_currencies()
        currencies_response.assert_is_success()

        assert_that(currencies_response.content, has_key('data'))
        assert_that(currencies_response.content['data'], not_none())

        currencies = currencies_response.content['data']
        test_currency = next((currency for currency in currencies if
                              currency['code'] == '{}.{}'.format(
                                  config.environment['integration_title'],
                                  config.data.TEST_CURRENCY.CURRENCY_CODE
                              )), None)

        assert_that(test_currency, not_none())
        assert_that(test_currency, has_key('title'))
        assert_that(test_currency['title'], equal_to(config.environment['integration_title']))
        assert_that(test_currency, has_key('code'))
        assert_that(test_currency['code'], equal_to('{}.{}'.format(
            config.environment['integration_title'],
            config.data.TEST_CURRENCY.CURRENCY_CODE
        )))
        assert_that(test_currency, has_key('decimal_places'))
        assert_that(test_currency, has_key('is_real'))
        assert_that(test_currency, has_key('is_reported'))
