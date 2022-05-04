import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities
from integration.main.request import RequestBuilder, RequestConstants, ResponseMessage
from integration.schemas import Schemas


class TestFetchProducts(object):

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
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(config.store.profile_id)
        delete_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch products')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_fetch_products_should_succeed_when_no_storefront_is_provided(self, config, content_type):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT.PRODUCT_CODE],
            config.store.profile_id,
            config.data.TEST_PRODUCT.COUNTRY,
            config.data.TEST_PRODUCT.LANGUAGE,
            content_type=content_type
        )
        fetch_response.assert_is_success()
        product_urls = fetch_response.content['body']['uriList']
        assert_that(product_urls, has_length(1))
        uri = product_urls[0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()
        product_info = product_response.content
        Schemas.validate(product_response.content, Schemas.PURCHASE_PRODUCT)

        config.log.info('checking base product returns expected fields/entitlement')
        assert_that(product_info['product_code'], equal_to(config.data.TEST_PRODUCT.PRODUCT_CODE))
        assert_that(product_info['friendly_name'],
                    equal_to(config.data.TEST_PRODUCT.FRIENDLY_NAME))
        assert_that(product_info['applied_promotions'], is_(empty()))

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch products')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_product_code', [0, '',
                                                      None,
                                                      'invalid_product_code'])
    def test_fetch_products_should_fail_when_product_code_is_invalid(self, config, invalid_product_code):
        fetch_response = config.freya.server_gateway.fetch_products(
            [invalid_product_code],
            config.store.profile_id,
            config.data.TEST_PRODUCT.COUNTRY,
            config.data.TEST_PRODUCT.LANGUAGE)
        fetch_response.expect_failure(result_code=ResponseMessage.NO_PRODUCTS)

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch products')
    @pytest.allure.severity(severity_level.MINOR)
    def test_fetch_products_should_fail_when_wgid_is_invalid(self, config):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT.PRODUCT_CODE],
            -1,
            config.data.TEST_PRODUCT.COUNTRY,
            config.data.TEST_PRODUCT.LANGUAGE
        )
        fetch_response.expect_failure(result_code=ResponseMessage.INVALID_WGID)

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch products')
    @pytest.allure.severity(severity_level.MINOR)
    def test_fetch_products_should_fail_when_wgid_is_a_string(self, config):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT.PRODUCT_CODE],
            'bad_wgid',
            config.data.TEST_PRODUCT.COUNTRY,
            config.data.TEST_PRODUCT.LANGUAGE
        )
        fetch_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                      result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch products')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_country_code', [0, '', 'bad_country'])
    def test_fetch_products_should_fail_when_country_is_invalid(self, config, invalid_country_code):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT.PRODUCT_CODE],
            config.store.profile_id,
            invalid_country_code,
            config.data.TEST_PRODUCT.LANGUAGE
        )
        fetch_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                      result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch products')
    @pytest.allure.severity(severity_level.MINOR)
    def test_fetch_products_passed_when_country_is_none(self, config):
        # FREYA-1066
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT.PRODUCT_CODE],
            config.store.profile_id,
            None,
            config.data.TEST_PRODUCT.LANGUAGE
        )
        fetch_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch products')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_language', [0, '', 'bad_language'])
    def test_fetch_products_should_succeed_when_language_is_invalid(self, config, invalid_language):
        """
        Validate that the fallback language is used when the provided language is invalid.
        """

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT.PRODUCT_CODE],
            config.store.profile_id,
            config.data.TEST_PRODUCT.COUNTRY,
            invalid_language
        )
        fetch_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch products')
    @pytest.allure.severity(severity_level.MINOR)
    def test_fetch_products_should_fail_when_language_is_none(self, config):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT.PRODUCT_CODE],
            config.store.profile_id,
            config.data.TEST_PRODUCT.COUNTRY,
            None
        )
        fetch_response.expect_failure(result_code=ResponseMessage.LANGUAGE_NOT_DEFINED)

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch products')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_should_succeed_when_product_is_in_provided_storefront(self, config):
        fetch_prod_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE],
            config.store.profile_id,
            config.data.TEST_STORE_FULL.COUNTRY,
            config.data.TEST_STORE_FULL.LANGUAGE,
            config.data.TEST_STORE_FULL.STOREFRONT
        )
        fetch_prod_response.assert_is_success()
        assert_that(fetch_prod_response.content['body']['uriList'], has_length(1))
        uri = fetch_prod_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(
            prod_response.content['product_code'],
            equal_to(config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE)
        )

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch products')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_should_fail_when_product_is_not_in_provided_storefront(self, config):
        fetch_prod_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT_ENTITLEMENT.CODE],
            config.store.profile_id,
            config.data.TEST_STORE_FULL.COUNTRY,
            config.data.TEST_STORE_FULL.LANGUAGE,
            config.data.TEST_STORE_FULL.STOREFRONT
        )
        fetch_prod_response.expect_failure(result_code=ResponseMessage.NO_PRODUCTS)

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch products')
    @pytest.allure.severity(severity_level.MINOR)
    def test_fetch_product_should_succeed_when_product_have_min_of_two(self, config):
        fetch_prod_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_MIN_OF_2.PRODUCT],
            config.store.profile_id,
            config.data.TEST_MIN_OF_2.COUNTRY,
            config.data.TEST_MIN_OF_2.LANGUAGE
        )
        fetch_prod_response.assert_is_success()

        assert_that(fetch_prod_response.content['body'], has_key('uriList'))
        assert_that(fetch_prod_response.content['body']['uriList'], has_length(1))
        uri = fetch_prod_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        price = prod_response.content['price']['real_price']

        assert_that(price, has_key('code'))
        assert_that(price['code'], equal_to(config.data.TEST_MIN_OF_2.COST.CODE))
        assert_that(price, has_key('amount'))
        assert_that(float(price['amount']), equal_to(config.data.TEST_MIN_OF_2.COST.AMOUNT))

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch products')
    @pytest.allure.severity(severity_level.NORMAL)
    def test_fetch_products_should_succeed_with_case_sensitive_product(self, config):
        # FREYA-854 check
        fetch_prod_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT_CASE_SENSITIVE.PRODUCT_CODE],
            config.store.profile_id,
            config.data.TEST_PRODUCT_CASE_SENSITIVE.COUNTRY,
            config.data.TEST_PRODUCT_CASE_SENSITIVE.LANGUAGE,
            config.data.TEST_PRODUCT_CASE_SENSITIVE.STOREFRONT
        )
        fetch_prod_response.assert_is_success()
        assert_that(fetch_prod_response.content['body']['uriList'], has_length(1))
        uri = fetch_prod_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(
            prod_response.content['product_code'],
            equal_to(config.data.TEST_PRODUCT_CASE_SENSITIVE.PRODUCT_CODE)
        )
