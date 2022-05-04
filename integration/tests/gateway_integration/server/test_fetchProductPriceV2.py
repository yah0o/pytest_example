import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities
from integration.main.request import RequestConstants
from integration.main.request.constants import ResponseMessage


class TestFetchProductPriceV2(object):

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price v2')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_fetch_product_price_should_succeed_when_fixed_price_product_have_no_pm(self, config, content_type):
        fetch_response = config.freya.server_gateway.fetch_product_price_v2(
            config.data.TEST_PM.PRODUCT_WITHOUT_SETTINGS,
            config.data.TEST_PM.COUNTRY,
            1,
            wgid=0,
            response_fields={'client_payment_methods': True},
            content_type=content_type
        )
        fetch_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price v2')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_fetch_product_price_should_fail_when_fixed_price_product_quantity_have_no_pm(self, config, content_type):
        # PRODO-591
        product = config.data.TEST_PM.PRODUCT_WITHOUT_SETTINGS
        quantity = 500
        fetch_response = config.freya.server_gateway.fetch_product_price_v2(
            product,
            config.data.TEST_PM.COUNTRY,
            quantity,
            wgid=0,
            response_fields={'client_payment_methods': True},
            content_type=content_type
        )
        fetch_response.expect_failure(result_code=ResponseMessage.INVALID_PRODUCT_QUANTITY)

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price v2')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_fetch_product_price_should_succeed_when_fixed_price_product_have_pm(self, config, content_type):
        fetch_response = config.freya.server_gateway.fetch_product_price_v2(
            config.data.TEST_PM.PRODUCT,
            config.data.TEST_PM.COUNTRY,
            1,
            wgid=0,
            response_fields={'client_payment_methods': True},
            content_type=content_type
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body'], has_key('client_payment_methods'))
        assert_that(fetch_response.content['body']['client_payment_methods'], is_not(empty()))

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price v2')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_fetch_product_price_should_fail_when_fixed_price_product_quantity_have_pm(self, config, content_type):
        product = config.data.TEST_PM.PRODUCT
        quantity = 500
        fetch_response = config.freya.server_gateway.fetch_product_price_v2(
            product,
            config.data.TEST_PM.COUNTRY,
            quantity,
            wgid=0,
            response_fields={'client_payment_methods': True},
            content_type=content_type
        )
        fetch_response.expect_failure(result_code=ResponseMessage.INVALID_PRODUCT_QUANTITY)

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price v2')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    @pytest.mark.parametrize('response_fields', [None,
                                                 {'not_exist': True},
                                                 {'client_payment_methods': None},
                                                 {}])
    def test_fetch_product_price_should_empty_or_invalid_response_fields(self, config, content_type,
                                                                         response_fields):
        fetch_response = config.freya.server_gateway.fetch_product_price_v2(
            config.data.TEST_PM.PRODUCT,
            config.data.TEST_PM.COUNTRY,
            1,
            wgid=0,
            response_fields=response_fields,
            content_type=content_type
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body'], has_key('client_payment_methods'))

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price v2')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('receiver_country', ['RU', 'EU'])
    def test_fetch_product_price_should_succeed_with_valid_receiver_country(self,
                                                                            config,
                                                                            receiver_country):
        fetch_response = config.freya.server_gateway.fetch_product_price_v2(
            config.data.TEST_PM.PRODUCT,
            config.data.TEST_PM.COUNTRY,
            1,
            wgid=0,
            response_fields={'client_payment_methods': False},
            receiver_country=receiver_country
        )
        fetch_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price v2')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('receiver_country', ['', 'EN', 1])
    def test_fetch_product_price_should_fail_with_invalid_receiver_country(self,
                                                                           config,
                                                                           receiver_country
                                                                           ):
        fetch_response = config.freya.server_gateway.fetch_product_price_v2(
            config.data.TEST_PM.PRODUCT,
            config.data.TEST_PM.COUNTRY,
            1,
            wgid=0,
            response_fields={'client_payment_methods': False},
            receiver_country=receiver_country
        )
        fetch_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                      result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price v2')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('receiver_country', ['UNDEFINED', 'ZZ', 'BY'])
    def test_fetch_product_price_should_success_with_restricted_country_and_non_restricted_user(self,
                                                                                                config,
                                                                                                receiver_country):
        # PRODO-613 (restricted country check)
        # PRODO-1174 change flow of restricted
        fetch_response = config.freya.server_gateway.fetch_product_price_v2(
            config.data.TEST_PURCHASE_RESTRICTED.PRODUCT,
            config.data.TEST_PURCHASE_RESTRICTED.COUNTRY,
            1,
            wgid=0,
            response_fields={'client_payment_methods': False},
            receiver_country=receiver_country
        )
        fetch_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product price v2')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('receiver_country', ['UNDEFINED', 'ZZ', 'BY'])
    def test_fetch_product_price_should_success_with_restricted_country_and_restricted_user(self,
                                                                                            config,
                                                                                            receiver_country):
        # PRODO-613 (restricted country check)
        # PRODO-1174 change flow of restricted
        fetch_response = config.freya.server_gateway.fetch_product_price_v2(
            config.data.TEST_PURCHASE_RESTRICTED.PRODUCT,
            'BY',
            1,
            wgid=0,
            response_fields={'client_payment_methods': False},
            receiver_country=receiver_country
        )
        fetch_response.expect_failure(result_code=ResponseMessage.PRODUCT_NOT_ALLOWED)
