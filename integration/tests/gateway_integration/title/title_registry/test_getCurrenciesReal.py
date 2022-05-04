import pytest
from allure import severity_level
from hamcrest import *


@pytest.allure.feature('title')
@pytest.allure.story('title registry')
@pytest.allure.severity(severity_level.MINOR)
class TestGetCurrenciesReal(object):

    def test_get_currencies_real_should_succeed_when_requested(self, config):
        currencies_response = config.freya.title_registry.get_currencies_real()
        currencies_response.assert_is_success()

        assert_that(currencies_response.content, has_key('data'))
        assert_that(currencies_response.content['data'], not_none())

        real_currencies = currencies_response.content['data']
        usd_currency = next((currency for currency in real_currencies if
                             currency['code'] == config.data.TEST_PRODUCT_FULL_REAL_PRICE.PRICE.CURRENCY_CODE), None)

        assert_that(usd_currency, not_none())
        assert_that(usd_currency['code'], equal_to(config.data.TEST_PRODUCT_FULL_REAL_PRICE.PRICE.CURRENCY_CODE))
        assert_that(usd_currency, has_key('decimal_places'))
        assert_that(usd_currency['decimal_places'], equal_to(2))
        assert_that(usd_currency, has_key('is_real'))
        assert_that(usd_currency, has_key('is_reported'))
        assert_that(usd_currency, has_key('title'))
