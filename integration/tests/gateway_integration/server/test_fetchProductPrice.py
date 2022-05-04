from math import ceil

import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities
from integration.main.request import RequestConstants
from integration.main.request.constants import ResponseMessage


class TestFetchProductPrice(object):

    @pytest.fixture(autouse=True)
    def setup(self, config):

        ###
        # Test setup


        # account with default null country
        account = AccountUtilities.create_account(attrs=None)
        account_created = config.spa.http.create_account(account.__dict__)
        account_created.assert_is_success()
        update_account = config.spa.http.update(account_created.content['id'],
                                                game=config.environment['test_title_pgn'])
        update_account.assert_is_success()

        config.store.profile_id = account_created.content['id']
        ###

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(config.store.profile_id)
        delete_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    @pytest.mark.parametrize('any_quantity', [1, 10000])
    def test_fetch_product_price_should_succeed_when_product_is_linear_variable_priced(self, config, content_type,
                                                                                       any_quantity):

        config.log.info(
            'fetching {} price for {} amount of {}'.format(config.data.TEST_PRODUCT_VARIABLE.PRICE.CURRENCY_CODE,
                                                           any_quantity,
                                                           config.data.TEST_PRODUCT_VARIABLE.CURRENCIES.CODE))

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            any_quantity,
            content_type=content_type
        )
        fetch_response.assert_is_success()

        linear_calculation = 1.00 / config.data.TEST_PRODUCT_VARIABLE.LINEAR_CONSTANT * any_quantity
        total_price_usd = format(ceil(linear_calculation * 1000) / 1000, '.2f')
        config.log.info('total calculated USD price after rounding: {}'.format(total_price_usd))

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], not_none())

        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        assert_that(fetch_response.content['body']['price']['real_price'], not_none())

        real_price = fetch_response.content['body']['price']['real_price']
        assert_that(real_price['code'], equal_to(config.data.TEST_PRODUCT_VARIABLE.PRICE.CURRENCY_CODE))
        assert_that(real_price['amount'], equal_to(total_price_usd))


    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    @pytest.mark.parametrize('any_quantity', [1, 5])
    def test_fetch_product_price_should_succeed_when_product_is_power_variable_priced(self, config, content_type,
                                                                                      any_quantity):
        # PRODO-910
        config.log.info('fetching {} price for {} amount of {}'.format(
            config.data.TEST_PRODUCT_VARIABLE_POWER.PRICE.CURRENCY_CODE, any_quantity,
            config.data.TEST_PRODUCT_VARIABLE_POWER.CURRENCIES.CODE))

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_PRODUCT_VARIABLE_POWER.PRODUCT_CODE,
            config.data.TEST_PRODUCT_VARIABLE_POWER.COUNTRY,
            any_quantity,
            content_type=content_type
        )
        fetch_response.assert_is_success()

        a = config.data.TEST_PRODUCT_VARIABLE_POWER.POWER_CONSTANT.A
        b = config.data.TEST_PRODUCT_VARIABLE_POWER.POWER_CONSTANT.B
        c = config.data.TEST_PRODUCT_VARIABLE_POWER.POWER_CONSTANT.C

        power_calculation = any_quantity / (a * (float(any_quantity) / b) ** c)

        total_price_usd = format(ceil(power_calculation * 1000) / 1000, '.2f')

        config.log.info('total calculated USD price after rounding: {}'.format(total_price_usd))

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], not_none())

        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        assert_that(fetch_response.content['body']['price']['real_price'], not_none())

        real_price = fetch_response.content['body']['price']['real_price']
        assert_that(real_price['code'], equal_to(config.data.TEST_PRODUCT_VARIABLE_POWER.PRICE.CURRENCY_CODE))
        assert_that(real_price['amount'], equal_to(total_price_usd))

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    @pytest.mark.parametrize('quantity', [1, 499, 500, 501, 25299, 25300, 25301, 30000])
    def test_fetch_product_price_should_succeed_when_fetch_na_trilogy_product(self, config, content_type, quantity):

        config.log.info('The value we divide {} with depends on the quantity of {}'.format(
            config.data.TEST_PRODUCT_VARIABLE_NA_TRILOGY.CURRENCIES.CODE,
            config.data.TEST_PRODUCT_VARIABLE_NA_TRILOGY.CURRENCIES.CODE
        ))

        if quantity < 500:
            denominator = 168.2
        elif quantity < 25300:
            denominator = 145 * ((quantity / 115.0) ** 0.101)
        else:
            denominator = 250.0

        config.log.info('Calculate the {} amount {} {} cost'.format(
            config.data.TEST_PRODUCT_VARIABLE_NA_TRILOGY.PRICE.CURRENCY_CODE,
            quantity,
            config.data.TEST_PRODUCT_VARIABLE_NA_TRILOGY.PRODUCT_CODE
        ))

        trilogy_calculation = round(quantity / denominator, 2)
        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_PRODUCT_VARIABLE_NA_TRILOGY.PRODUCT_CODE,
            config.data.TEST_PRODUCT_VARIABLE_NA_TRILOGY.COUNTRY,
            quantity,
            content_type=content_type
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], not_none())

        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        assert_that(fetch_response.content['body']['price']['real_price'], not_none())
        cost = fetch_response.content['body']['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_PRODUCT_VARIABLE_NA_TRILOGY.PRICE.CURRENCY_CODE))

        assert_that(cost, has_key('amount'))
        assert_that(float(cost['amount']), equal_to(trilogy_calculation))

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price')
    @pytest.allure.severity(severity_level.BLOCKER)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    @pytest.mark.parametrize('quantity', [1, 499, 500, 501, 25299, 25300, 25301, 30000])
    def test_fetch_product_price_should_succeed_when_fetch_na_trilogy_product_with_storefront(
            self,
            config,
            content_type,
            quantity
    ):

        config.log.info('The value we divide {} with depends on the quantity of {}'.format(
            config.data.TEST_PRODUCT_VARIABLE_NA_TRILOGY.CURRENCIES.CODE,
            config.data.TEST_PRODUCT_VARIABLE_NA_TRILOGY.CURRENCIES.CODE
        ))

        if quantity < 500:
            denominator = 168.2
        elif quantity < 25300:
            denominator = 145 * ((quantity / 115.0) ** 0.101)
        else:
            denominator = 250.0

        config.log.info('Calculate the {} amount {} {} cost'.format(
            config.data.TEST_PRODUCT_VARIABLE_NA_TRILOGY.PRICE.CURRENCY_CODE,
            quantity,
            config.data.TEST_PRODUCT_VARIABLE_NA_TRILOGY.PRODUCT_CODE
        ))

        trilogy_calculation = round(quantity / denominator, 2)
        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_PRODUCT_VARIABLE_NA_TRILOGY.PRODUCT_CODE,
            config.data.TEST_PRODUCT_VARIABLE_NA_TRILOGY.COUNTRY,
            quantity,
            content_type=content_type,
            storefront=config.data.TEST_PRODUCT_VARIABLE_NA_TRILOGY.STOREFRONT
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], not_none())

        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        assert_that(fetch_response.content['body']['price']['real_price'], not_none())
        cost = fetch_response.content['body']['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_PRODUCT_VARIABLE_NA_TRILOGY.PRICE.CURRENCY_CODE))

        assert_that(cost, has_key('amount'))
        assert_that(float(cost['amount']), equal_to(trilogy_calculation))

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    @pytest.mark.parametrize('quantity', [1, 499, 500, 501, 30395, 30396, 30397, 35000])
    def test_fetch_product_price_should_succeed_when_fetch_eu_trilogy_product(
            self,
            config,
            content_type,
            quantity
    ):

        config.log.info('The value we divide {} with depends on the quantity of {}'.format(
            config.data.TEST_PRODUCT_VARIABLE_EU_TRILOGY.CURRENCIES.CODE,
            config.data.TEST_PRODUCT_VARIABLE_EU_TRILOGY.CURRENCIES.CODE
        ))

        if quantity < 500:
            denominator = 200.0
        elif quantity < 30396:
            denominator = 200 * ((quantity / 500.0) ** 0.0765)
        else:
            denominator = 273.564

        config.log.info('Calculate the {} amount {} {} cost'.format(
            config.data.TEST_PRODUCT_VARIABLE_EU_TRILOGY.PRICE.CURRENCY_CODE,
            quantity,
            config.data.TEST_PRODUCT_VARIABLE_EU_TRILOGY.PRODUCT_CODE_MIN
        ))

        trilogy_calculation = round(quantity / denominator, 2)
        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_PRODUCT_VARIABLE_EU_TRILOGY.PRODUCT_CODE_MIN,
            config.data.TEST_PRODUCT_VARIABLE_EU_TRILOGY.COUNTRY,
            quantity,
            content_type=content_type
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], not_none())

        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        assert_that(fetch_response.content['body']['price']['real_price'], not_none())
        cost = fetch_response.content['body']['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_PRODUCT_VARIABLE_EU_TRILOGY.PRICE.CURRENCY_CODE))

        assert_that(cost, has_key('amount'))
        assert_that(float(cost['amount']), equal_to(trilogy_calculation))

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price')
    @pytest.allure.severity(severity_level.BLOCKER)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    @pytest.mark.parametrize('quantity', [1, 499, 500, 501, 30395, 30396, 30397, 35000])
    def test_fetch_product_price_should_succeed_when_fetch_eu_trilogy_product_with_storefront(
            self,
            config,
            content_type,
            quantity
    ):

        config.log.info('The value we divide {} with depends on the quantity of {}'.format(
            config.data.TEST_PRODUCT_VARIABLE_EU_TRILOGY.CURRENCIES.CODE,
            config.data.TEST_PRODUCT_VARIABLE_EU_TRILOGY.CURRENCIES.CODE
        ))

        if quantity < 500:
            denominator = 200.0
        elif quantity < 30396:
            denominator = 200 * ((quantity / 500.0) ** 0.0765)
        else:
            denominator = 273.564

        config.log.info('Calculate the {} amount {} {} cost'.format(
            config.data.TEST_PRODUCT_VARIABLE_EU_TRILOGY.PRICE.CURRENCY_CODE,
            quantity,
            config.data.TEST_PRODUCT_VARIABLE_EU_TRILOGY.PRODUCT_CODE
        ))

        trilogy_calculation = round(quantity / denominator, 2)
        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_PRODUCT_VARIABLE_EU_TRILOGY.PRODUCT_CODE_MIN,
            config.data.TEST_PRODUCT_VARIABLE_EU_TRILOGY.COUNTRY,
            quantity,
            content_type=content_type,
            storefront=config.data.TEST_PRODUCT_VARIABLE_EU_TRILOGY.STOREFRONT_MIN
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], not_none())

        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        assert_that(fetch_response.content['body']['price']['real_price'], not_none())
        cost = fetch_response.content['body']['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_PRODUCT_VARIABLE_EU_TRILOGY.PRICE.CURRENCY_CODE))

        assert_that(cost, has_key('amount'))
        assert_that(float(cost['amount']), equal_to(trilogy_calculation))


    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    @pytest.mark.parametrize('quantity', [1099, 1100, 1101, 24999, 25000, 25001, 30000])
    def test_fetch_product_price_should_succeed_when_fetch_asia_trilogy_product(
            self,
            config,
            content_type,
            quantity
    ):

        config.log.info('The value we divide {} with depends on the quantity of {}'.format(
            config.data.TEST_PRODUCT_VARIABLE_ASIA_TRILOGY.CURRENCIES.CODE,
            config.data.TEST_PRODUCT_VARIABLE_ASIA_TRILOGY.CURRENCIES.CODE
        ))

        if quantity < 1100:
            denominator = 222.0
        elif quantity < 25000:
            denominator = 222 * ((quantity / 1000.0) ** 0.0363)
        else:
            denominator = 250.0

        config.log.info('Calculate the {} amount {} {} cost'.format(
            config.data.TEST_PRODUCT_VARIABLE_ASIA_TRILOGY.PRICE.CURRENCY_CODE,
            quantity,
            config.data.TEST_PRODUCT_VARIABLE_ASIA_TRILOGY.PRODUCT_CODE
        ))
        trilogy_calculation = round(quantity / denominator, 2)
        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_PRODUCT_VARIABLE_ASIA_TRILOGY.PRODUCT_CODE,
            config.data.TEST_PRODUCT_VARIABLE_ASIA_TRILOGY.COUNTRY,
            quantity,
            content_type=content_type
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], not_none())

        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        assert_that(fetch_response.content['body']['price']['real_price'], not_none())
        cost = fetch_response.content['body']['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_PRODUCT_VARIABLE_ASIA_TRILOGY.PRICE.CURRENCY_CODE))

        assert_that(cost, has_key('amount'))
        assert_that(float(cost['amount']), equal_to(trilogy_calculation))

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_fetch_product_price_should_fail_when_fetch_asia_trilogy_product_0_price(
            self,
            config,
            content_type
    ):

        config.log.info('The value we divide {} with depends on the quantity of {}'.format(
            config.data.TEST_PRODUCT_VARIABLE_ASIA_TRILOGY.CURRENCIES.CODE,
            config.data.TEST_PRODUCT_VARIABLE_ASIA_TRILOGY.CURRENCIES.CODE
        ))
        quantity = 1

        if quantity < 1100:
            denominator = 222.0
        elif quantity < 25000:
            denominator = 222 * ((quantity / 1000.0) ** 0.0363)
        else:
            denominator = 250.0

        config.log.info('Calculate the {} amount {} {} cost'.format(
            config.data.TEST_PRODUCT_VARIABLE_ASIA_TRILOGY.PRICE.CURRENCY_CODE,
            quantity,
            config.data.TEST_PRODUCT_VARIABLE_ASIA_TRILOGY.PRODUCT_CODE_MIN
        ))
        trilogy_calculation = round(quantity / denominator, 2)
        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_PRODUCT_VARIABLE_ASIA_TRILOGY.PRODUCT_CODE_MIN,
            config.data.TEST_PRODUCT_VARIABLE_ASIA_TRILOGY.COUNTRY,
            quantity,
            content_type=content_type
        )
        fetch_response.expect_failure(ResponseMessage.PRODUCT_VALIDATION_ERROR)

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price')
    @pytest.allure.severity(severity_level.BLOCKER)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    @pytest.mark.parametrize('quantity', [1099, 1100, 1101, 24999, 25000, 25001, 30000])
    def test_fetch_product_price_should_succeed_when_fetch_asia_trilogy_product_with_storefront(
            self,
            config,
            content_type,
            quantity
    ):

        config.log.info('The value we divide {} with depends on the quantity of {}'.format(
            config.data.TEST_PRODUCT_VARIABLE_ASIA_TRILOGY.CURRENCIES.CODE,
            config.data.TEST_PRODUCT_VARIABLE_ASIA_TRILOGY.CURRENCIES.CODE
        ))

        if quantity < 1100:
            denominator = 222.0
        elif quantity < 25000:
            denominator = 222 * ((quantity / 1000.0) ** 0.0363)
        else:
            denominator = 250.0

        config.log.info('Calculate the {} amount {} {} cost'.format(
            config.data.TEST_PRODUCT_VARIABLE_ASIA_TRILOGY.PRICE.CURRENCY_CODE,
            quantity,
            config.data.TEST_PRODUCT_VARIABLE_ASIA_TRILOGY.PRODUCT_CODE
        ))
        trilogy_calculation = round(quantity / denominator, 2)
        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_PRODUCT_VARIABLE_ASIA_TRILOGY.PRODUCT_CODE,
            config.data.TEST_PRODUCT_VARIABLE_ASIA_TRILOGY.COUNTRY,
            quantity,
            content_type=content_type,
            storefront=config.data.TEST_PRODUCT_VARIABLE_ASIA_TRILOGY.STOREFRONT
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], not_none())

        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        assert_that(fetch_response.content['body']['price']['real_price'], not_none())
        cost = fetch_response.content['body']['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_PRODUCT_VARIABLE_ASIA_TRILOGY.PRICE.CURRENCY_CODE))

        assert_that(cost, has_key('amount'))
        assert_that(float(cost['amount']), equal_to(trilogy_calculation))

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price')
    @pytest.allure.severity(severity_level.BLOCKER)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_fetch_product_price_should_fail_when_fetch_asia_trilogy_product_with_storefront_0_price(
            self,
            config,
            content_type
    ):

        config.log.info('The value we divide {} with depends on the quantity of {}'.format(
            config.data.TEST_PRODUCT_VARIABLE_ASIA_TRILOGY.CURRENCIES.CODE,
            config.data.TEST_PRODUCT_VARIABLE_ASIA_TRILOGY.CURRENCIES.CODE
        ))
        quantity = 1

        denominator = 222.0

        config.log.info('Calculate the {} amount {} {} cost'.format(
            config.data.TEST_PRODUCT_VARIABLE_ASIA_TRILOGY.PRICE.CURRENCY_CODE,
            quantity,
            config.data.TEST_PRODUCT_VARIABLE_ASIA_TRILOGY.PRODUCT_CODE_MIN
        ))
        trilogy_calculation = round(quantity / denominator, 2)
        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_PRODUCT_VARIABLE_ASIA_TRILOGY.PRODUCT_CODE_MIN,
            config.data.TEST_PRODUCT_VARIABLE_ASIA_TRILOGY.COUNTRY,
            quantity,
            content_type=content_type,
            storefront=config.data.TEST_PRODUCT_VARIABLE_ASIA_TRILOGY.STOREFRONT_MIN
        )
        fetch_response.expect_failure(ResponseMessage.PRODUCT_VALIDATION_ERROR)

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    @pytest.mark.parametrize('quantity', [100, 10000])
    def test_fetch_product_price_should_succeed_when_fetch_ru_trilogy_product(
            self,
            config,
            content_type,
            quantity
    ):

        config.log.info('Calculate the {} amount {} {} cost'.format(
            config.data.TEST_PRODUCT_VARIABLE_RU_TRILOGY.PRICE.CURRENCY_CODE,
            quantity,
            config.data.TEST_PRODUCT_VARIABLE_RU_TRILOGY.PRODUCT_CODE
        ))
        trilogy_calculation = round(quantity / 250.0, 2)
        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_PRODUCT_VARIABLE_RU_TRILOGY.PRODUCT_CODE,
            config.data.TEST_PRODUCT_VARIABLE_RU_TRILOGY.COUNTRY,
            quantity,
            content_type=content_type
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], not_none())

        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        assert_that(fetch_response.content['body']['price']['real_price'], not_none())
        cost = fetch_response.content['body']['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_PRODUCT_VARIABLE_RU_TRILOGY.PRICE.CURRENCY_CODE))

        assert_that(cost, has_key('amount'))
        assert_that(float(cost['amount']), equal_to(trilogy_calculation))

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_fetch_product_price_should_fail_when_fetch_ru_trilogy_product_0_price(
            self,
            config,
            content_type
    ):
        quantity = 1

        config.log.info('Calculate the {} amount {} {} cost'.format(
            config.data.TEST_PRODUCT_VARIABLE_RU_TRILOGY.PRICE.CURRENCY_CODE,
            quantity,
            config.data.TEST_PRODUCT_VARIABLE_RU_TRILOGY.PRODUCT_CODE_MIN
        ))
        trilogy_calculation = round(quantity / 250.0, 2)
        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_PRODUCT_VARIABLE_RU_TRILOGY.PRODUCT_CODE_MIN,
            config.data.TEST_PRODUCT_VARIABLE_RU_TRILOGY.COUNTRY,
            quantity,
            content_type=content_type
        )
        fetch_response.expect_failure(result_code=ResponseMessage.PRODUCT_VALIDATION_ERROR)

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price')
    @pytest.allure.severity(severity_level.BLOCKER)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    @pytest.mark.parametrize('quantity', [100, 10000])
    def test_fetch_product_price_should_succeed_when_fetch_ru_trilogy_product_with_storefront(
            self,
            config,
            content_type,
            quantity
    ):

        config.log.info('Calculate the {} amount {} {} cost'.format(
            config.data.TEST_PRODUCT_VARIABLE_RU_TRILOGY.PRICE.CURRENCY_CODE,
            quantity,
            config.data.TEST_PRODUCT_VARIABLE_RU_TRILOGY.PRODUCT_CODE
        ))
        trilogy_calculation = round(quantity / 250.0, 2)
        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_PRODUCT_VARIABLE_RU_TRILOGY.PRODUCT_CODE,
            config.data.TEST_PRODUCT_VARIABLE_RU_TRILOGY.COUNTRY,
            quantity,
            content_type=content_type,
            storefront=config.data.TEST_PRODUCT_VARIABLE_RU_TRILOGY.STOREFRONT
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], not_none())

        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        assert_that(fetch_response.content['body']['price']['real_price'], not_none())
        cost = fetch_response.content['body']['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_PRODUCT_VARIABLE_RU_TRILOGY.PRICE.CURRENCY_CODE))

        assert_that(cost, has_key('amount'))
        assert_that(float(cost['amount']), equal_to(trilogy_calculation))

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price')
    @pytest.allure.severity(severity_level.BLOCKER)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_fetch_product_price_should_fail_when_fetch_ru_trilogy_product_with_storefront_0_price(
            self,
            config,
            content_type
    ):
        # PRODO-910
        quantity = 1
        config.log.info('Calculate the {} amount {} {} cost'.format(
            config.data.TEST_PRODUCT_VARIABLE_RU_TRILOGY.PRICE.CURRENCY_CODE,
            quantity,
            config.data.TEST_PRODUCT_VARIABLE_RU_TRILOGY.PRODUCT_CODE_MIN
        ))
        trilogy_calculation = round(quantity / 250.0, 2)
        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_PRODUCT_VARIABLE_RU_TRILOGY.PRODUCT_CODE_MIN,
            config.data.TEST_PRODUCT_VARIABLE_RU_TRILOGY.COUNTRY,
            quantity,
            content_type=content_type,
            storefront=config.data.TEST_PRODUCT_VARIABLE_RU_TRILOGY.STOREFRONT_MIN
        )
        fetch_response.expect_failure(result_code=ResponseMessage.PRODUCT_VALIDATION_ERROR)

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    @pytest.mark.parametrize('any_quantity', [1, 5])
    def test_fetch_product_price_should_succeed_for_storefront_with_variable_power_product(self, config, content_type,
                                                                                           any_quantity):

        config.log.info('fetching {} price for {} amount of {}'.format(
            config.data.TEST_PRODUCT_VARIABLE_POWER.PRICE.CURRENCY_CODE, any_quantity,
            config.data.TEST_PRODUCT_VARIABLE_POWER.CURRENCIES.CODE))

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_PRODUCT_VARIABLE_POWER.PRODUCT_CODE,
            config.data.TEST_PRODUCT_VARIABLE_POWER.COUNTRY,
            any_quantity,
            storefront=config.data.TEST_PRODUCT_VARIABLE_POWER.STOREFRONT,
            content_type=content_type
        )
        fetch_response.assert_is_success()

        a = config.data.TEST_PRODUCT_VARIABLE_POWER.POWER_CONSTANT.A
        b = config.data.TEST_PRODUCT_VARIABLE_POWER.POWER_CONSTANT.B
        c = config.data.TEST_PRODUCT_VARIABLE_POWER.POWER_CONSTANT.C

        power_calculation = any_quantity / (a * (float(any_quantity) / b) ** c)

        total_price_usd = format(ceil(power_calculation * 1000) / 1000, '.2f')

        config.log.info('total calculated USD price after rounding: {}'.format(total_price_usd))

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], not_none())

        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        assert_that(fetch_response.content['body']['price']['real_price'], not_none())

        real_price = fetch_response.content['body']['price']['real_price']
        assert_that(real_price['code'], equal_to(config.data.TEST_PRODUCT_VARIABLE_POWER.PRICE.CURRENCY_CODE))

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_fetch_product_price_should_fail_for_storefront_with_variable_power_product_0_price(self, config,
                                                                                                content_type,
                                                                                                ):
        # PRODO-910
        # quantity / (a * pow((quantity / b), c)) of product >>> 0
        config.log.info('fetching {} price for {} amount of {}'.format(
            config.data.TEST_PRODUCT_VARIABLE_POWER.PRICE.CURRENCY_CODE, 10000,
            config.data.TEST_PRODUCT_VARIABLE_POWER.CURRENCIES.CODE))

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_PRODUCT_VARIABLE_POWER.PRODUCT_CODE,
            config.data.TEST_PRODUCT_VARIABLE_POWER.COUNTRY,
            10000,
            storefront=config.data.TEST_PRODUCT_VARIABLE_POWER.STOREFRONT,
            content_type=content_type
        )
        fetch_response.expect_failure(result_code=ResponseMessage.PRODUCT_VALIDATION_ERROR)

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    @pytest.mark.parametrize('any_quantity', [1, 10000])
    def test_fetch_product_price_should_succeed_for_storefront_with_variable_product(self, config, content_type,
                                                                                     any_quantity):

        config.log.info('fetching {} price for {} amount of {}'.format(
            config.data.TEST_PRODUCT_VARIABLE.PRICE.CURRENCY_CODE, any_quantity,
            config.data.TEST_PRODUCT_VARIABLE.CURRENCIES.CODE))

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            any_quantity,
            storefront=config.data.TEST_PRODUCT_VARIABLE.STOREFRONT,
            content_type=content_type
        )
        fetch_response.assert_is_success()

        linear_calculation = 1.00 / config.data.TEST_PRODUCT_VARIABLE.LINEAR_CONSTANT * any_quantity
        total_price_usd = format(ceil(linear_calculation * 1000) / 1000, '.2f')
        config.log.info('total calculated USD price after rounding: {}'.format(total_price_usd))

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], not_none())

        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        assert_that(fetch_response.content['body']['price']['real_price'], not_none())

        real_price = fetch_response.content['body']['price']['real_price']
        assert_that(real_price['code'], equal_to(config.data.TEST_PRODUCT_VARIABLE.PRICE.CURRENCY_CODE))
        assert_that(real_price['amount'], equal_to(total_price_usd))

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('storefront', ['invalid_storefront', 0])
    def test_fetch_product_price_should_fail_for_invalid_storefront(self, config, storefront):

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.QUANTITY,
            storefront=storefront
        )
        fetch_response.expect_failure(result_code=ResponseMessage.STOREFRONT_NOT_FOUND)

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('any_quantity, result_code', [(1, ResponseMessage.PRODUCT_VALIDATION_ERROR),
                                                           (10000, ResponseMessage.INVALID_PRODUCT_QUANTITY)])
    def test_fetch_product_price_should_fail_for_storefront_without_product(self, config, any_quantity, result_code):

        fetch_response = config.freya.server_gateway.fetch_product_price(
            "test_product_xp",
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            any_quantity,
            storefront=config.data.TEST_PRODUCT_VARIABLE.STOREFRONT
        )
        fetch_response.expect_failure(result_code=result_code)

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_product_code', [0, '',
                                                      None,
                                                      'invalid_product_code'])
    def test_fetch_product_price_should_fail_when_product_code_is_invalid(self, config, invalid_product_code):

        fetch_response = config.freya.server_gateway.fetch_product_price(
            invalid_product_code,
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.QUANTITY
        )
        fetch_response.expect_failure(result_code=ResponseMessage.PRODUCT_NOT_FOUND)

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price')
    @pytest.allure.severity(severity_level.MINOR)
    def test_fetch_product_price_should_fail_when_country_code_is_undefined(self, config):

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
            'UNDEFINED',
            config.data.TEST_PRODUCT_VARIABLE.QUANTITY
        )
        fetch_response.expect_failure(result_code=ResponseMessage.PAYER_COUNTRY_NOT_DEFINED)

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_country_code', [0, '', 'bad_country'])
    def test_fetch_product_price_should_fail_when_country_code_is_invalid(self, config, invalid_country_code):

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
            invalid_country_code,
            config.data.TEST_PRODUCT_VARIABLE.QUANTITY
        )
        fetch_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                      result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_quantity', ['', None])
    def test_fetch_product_price_should_fail_when_quantity_is_null(self, config, invalid_quantity):

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            invalid_quantity
        )
        fetch_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                      result_message='fetchProductPrice.arg1.body.quantity: may not be null')

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_quantity', [-1, 0])
    def test_fetch_product_price_should_fail_when_quantity_less_than_zero(self, config, invalid_quantity):

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            invalid_quantity
        )
        fetch_response.expect_failure(result_code=ResponseMessage.LESS_THAN_ZERO,
                                      result_message='Quantity must be greater than 0')

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price')
    @pytest.allure.severity(severity_level.MINOR)
    def test_fetch_product_price_should_fail_when_quantity_is_decimal(self, config):

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            1.3
        )
        fetch_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                      result_message='NOT_WHOLE_INT31')

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price')
    @pytest.allure.severity(severity_level.MINOR)
    def test_fetch_product_price_should_fail_when_quantity_is_string(self, config):

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            'bad_quantity'
        )
        fetch_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                      result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price')
    @pytest.allure.severity(severity_level.MINOR)
    def test_fetch_product_price_should_fail_when_quantity_is_too_large(self, config):

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            2147483648
        )
        fetch_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                      result_message='NOT_WHOLE_INT31')

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price')
    @pytest.allure.severity(severity_level.MINOR)
    def test_fetch_product_price_should_succeed_when_fetch_one_product_with_min_of_two(self, config):

        fetch_prod_price_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_MIN_OF_2.PRODUCT,
            config.data.TEST_MIN_OF_2.COUNTRY,
            2
        )
        fetch_prod_price_response.assert_is_success()

        assert_that(fetch_prod_price_response.content['body'], has_key('price'))
        assert_that(fetch_prod_price_response.content['body']['price'], has_key('real_price'))

        price = fetch_prod_price_response.content['body']['price']['real_price']
        assert_that(price['code'], equal_to(config.data.TEST_MIN_OF_2.COST.CODE))
        #  price = (1/a) * quantity (0.17 for 2)
        assert_that(float(price['amount']), equal_to(config.data.TEST_MIN_OF_2.COST.AMOUNT))

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price')
    @pytest.allure.severity(severity_level.MINOR)
    def test_fetch_product_price_should_fail_when_fetch_two_product_with_min_of_three(self, config):

        fetch_prod_price_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_MIN_OF_3.PRODUCT,
            config.data.TEST_MIN_OF_3.COUNTRY,
            config.data.TEST_MIN_OF_3.AMOUNT
        )
        fetch_prod_price_response.expect_failure(result_code=ResponseMessage.INVALID_QUANTITY)

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price')
    @pytest.allure.severity(severity_level.NORMAL)
    def test_fetch_product_price_should_fail_restricted_country(self, config
                                                                ):
        config.log.info(
            'fetching price for {}'.format(config.data.TEST_PM_RESTRICTED.PRODUCT))

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_PM_RESTRICTED.PRODUCT,
            config.data.TEST_PM_RESTRICTED.RESTRICTED_COUNTRY,
            1
        )
        fetch_response.expect_failure(result_code=ResponseMessage.PRODUCT_NOT_ALLOWED)
