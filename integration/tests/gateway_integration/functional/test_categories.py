import pytest
from allure import severity_level
from hamcrest import *

from integration.main.request import RequestBuilder
from integration.main.session import Version


@pytest.allure.feature('functional')
@pytest.allure.story('categories')
@pytest.mark.skipif(**Version.is_before('1.52'))
class TestCategories(object):

    @pytest.allure.severity(severity_level.NORMAL)
    def test_fetch_product_list_should_succeed_when_storefront_has_empty_category_with_no_validation_errors(self,
                                                                                                            config):
        expected_products = [config.data.TEST_EMPTY_CAT_STORE.PRODUCT]
        entity_type = 'storefront'

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_EMPTY_CAT_STORE.CODE,
            0,
            config.data.TEST_EMPTY_CAT_STORE.COUNTRY,
            config.data.TEST_EMPTY_CAT_STORE.LANGUAGE
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(equal_to(len(expected_products))))

        uri_list_products = []
        for uri in fetch_response.content['body']['uriList']:
            product_response = RequestBuilder(uri).get()
            product_response.assert_is_success()
            uri_list_products.append(product_response.content['product_code'])

        assert_that(sorted(expected_products), equal_to(sorted(uri_list_products)))

    @pytest.allure.severity(severity_level.NORMAL)
    def test_fetch_product_list_should_succeed_when_storefront_has_single_full_category_with_no_validation_errors(self,
                                                                                                                  config):
        expected_products = [config.data.TEST_SINGLE_EXIST_CAT_FULL_STORE.PRODUCT]
        entity_type = 'storefront'

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_SINGLE_EXIST_CAT_FULL_STORE.CODE,
            0,
            config.data.TEST_SINGLE_EXIST_CAT_FULL_STORE.COUNTRY,
            config.data.TEST_SINGLE_EXIST_CAT_FULL_STORE.LANGUAGE
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(equal_to(len(expected_products))))

        uri_list_products = []
        for uri in fetch_response.content['body']['uriList']:
            product_response = RequestBuilder(uri).get()
            product_response.assert_is_success()
            uri_list_products.append(product_response.content['product_code'])

        assert_that(sorted(expected_products), equal_to(sorted(uri_list_products)))

    @pytest.allure.severity(severity_level.NORMAL)
    def test_fetch_product_list_should_succeed_when_storefront_has_single_empty_category_with_no_validation_errors(self,
                                                                                                                   config):
        expected_products = [config.data.TEST_SINGLE_EXIST_CAT_EMPTY_STORE.PRODUCT]
        entity_type = 'storefront'

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_SINGLE_EXIST_CAT_EMPTY_STORE.CODE,
            0,
            config.data.TEST_SINGLE_EXIST_CAT_EMPTY_STORE.COUNTRY,
            config.data.TEST_SINGLE_EXIST_CAT_EMPTY_STORE.LANGUAGE
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(equal_to(len(expected_products))))

        uri_list_products = []
        for uri in fetch_response.content['body']['uriList']:
            product_response = RequestBuilder(uri).get()
            product_response.assert_is_success()
            uri_list_products.append(product_response.content['product_code'])

        assert_that(sorted(expected_products), equal_to(sorted(uri_list_products)))

    @pytest.allure.severity(severity_level.NORMAL)
    def test_fetch_product_list_should_succeed_when_storefront_has_multi_full_category_with_no_validation_errors(self,
                                                                                                                 config):
        expected_products = [config.data.TEST_MULTI_EXIST_CAT_FULL_STORE.PRODUCT]
        entity_type = 'storefront'

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_MULTI_EXIST_CAT_FULL_STORE.CODE,
            0,
            config.data.TEST_MULTI_EXIST_CAT_FULL_STORE.COUNTRY,
            config.data.TEST_MULTI_EXIST_CAT_FULL_STORE.LANGUAGE
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(equal_to(len(expected_products))))

        uri_list_products = []
        for uri in fetch_response.content['body']['uriList']:
            product_response = RequestBuilder(uri).get()
            product_response.assert_is_success()
            uri_list_products.append(product_response.content['product_code'])

        assert_that(sorted(expected_products), equal_to(sorted(uri_list_products)))

    @pytest.allure.severity(severity_level.NORMAL)
    def test_fetch_product_list_should_succeed_when_storefront_has_both_existing_and_non_existing_categories_with_no_validation_errors(
            self, config):
        expected_products = [config.data.TEST_MULTI_EXIST_CAT_HALF_STORE.PRODUCT]
        entity_type = 'storefront'

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_MULTI_EXIST_CAT_HALF_STORE.CODE,
            0,
            config.data.TEST_MULTI_EXIST_CAT_HALF_STORE.COUNTRY,
            config.data.TEST_MULTI_EXIST_CAT_HALF_STORE.LANGUAGE
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(equal_to(len(expected_products))))

        uri_list_products = []
        for uri in fetch_response.content['body']['uriList']:
            product_response = RequestBuilder(uri).get()
            product_response.assert_is_success()
            uri_list_products.append(product_response.content['product_code'])

        assert_that(sorted(expected_products), equal_to(sorted(uri_list_products)))

    @pytest.allure.severity(severity_level.NORMAL)
    def test_fetch_product_list_should_succeed_when_storefront_has_non_existing_categories_with_no_validation_errors(
            self, config):
        expected_products = [config.data.TEST_NON_EXIST_CAT_STORE.PRODUCT]
        entity_type = 'storefront'

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_NON_EXIST_CAT_STORE.CODE,
            0,
            config.data.TEST_NON_EXIST_CAT_STORE.COUNTRY,
            config.data.TEST_NON_EXIST_CAT_STORE.LANGUAGE
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(equal_to(len(expected_products))))

        uri_list_products = []
        for uri in fetch_response.content['body']['uriList']:
            product_response = RequestBuilder(uri).get()
            product_response.assert_is_success()
            uri_list_products.append(product_response.content['product_code'])

        assert_that(sorted(expected_products), equal_to(sorted(uri_list_products)))

    @pytest.allure.severity(severity_level.NORMAL)
    def test_fetch_products_should_succeed_when_product_has_empty_category_with_no_validation_errors(self, config):
        entity_type = 'product'

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_EMPTY_CAT_STORE.PRODUCT],
            0,
            config.data.TEST_EMPTY_CAT_STORE.COUNTRY,
            config.data.TEST_EMPTY_CAT_STORE.LANGUAGE,
            config.data.TEST_EMPTY_CAT_STORE.CODE
        )
        fetch_response.assert_is_success()

        product_urls = fetch_response.content['body']['uriList']
        assert_that(product_urls, has_length(1))
        uri = product_urls[0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        product_info = product_response.content
        assert_that(product_info['product_code'], equal_to(config.data.TEST_EMPTY_CAT_STORE.PRODUCT))

    @pytest.allure.severity(severity_level.NORMAL)
    def test_fetch_products_should_succeed_when_product_has_single_full_category_with_no_validation_errors(self,
                                                                                                           config):
        entity_type = 'product'

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_SINGLE_EXIST_CAT_FULL_STORE.PRODUCT],
            0,
            config.data.TEST_SINGLE_EXIST_CAT_FULL_STORE.COUNTRY,
            config.data.TEST_SINGLE_EXIST_CAT_FULL_STORE.LANGUAGE,
            config.data.TEST_SINGLE_EXIST_CAT_FULL_STORE.CODE
        )
        fetch_response.assert_is_success()

        product_urls = fetch_response.content['body']['uriList']
        assert_that(product_urls, has_length(1))
        uri = product_urls[0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        product_info = product_response.content
        assert_that(product_info['product_code'], equal_to(config.data.TEST_SINGLE_EXIST_CAT_FULL_STORE.PRODUCT))

    @pytest.allure.severity(severity_level.NORMAL)
    def test_fetch_products_should_succeed_when_product_has_single_empty_category_with_no_validation_errors(self,
                                                                                                            config):
        entity_type = 'product'

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_SINGLE_EXIST_CAT_EMPTY_STORE.PRODUCT],
            0,
            config.data.TEST_SINGLE_EXIST_CAT_EMPTY_STORE.COUNTRY,
            config.data.TEST_SINGLE_EXIST_CAT_EMPTY_STORE.LANGUAGE,
            config.data.TEST_SINGLE_EXIST_CAT_EMPTY_STORE.CODE
        )
        fetch_response.assert_is_success()

        product_urls = fetch_response.content['body']['uriList']
        assert_that(product_urls, has_length(1))
        uri = product_urls[0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        product_info = product_response.content
        assert_that(product_info['product_code'], equal_to(config.data.TEST_SINGLE_EXIST_CAT_EMPTY_STORE.PRODUCT))

    @pytest.allure.severity(severity_level.NORMAL)
    def test_fetch_products_should_succeed_when_product_has_multi_full_category_with_no_validation_errors(self, config):
        entity_type = 'product'

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_MULTI_EXIST_CAT_FULL_STORE.PRODUCT],
            0,
            config.data.TEST_MULTI_EXIST_CAT_FULL_STORE.COUNTRY,
            config.data.TEST_MULTI_EXIST_CAT_FULL_STORE.LANGUAGE,
            config.data.TEST_MULTI_EXIST_CAT_FULL_STORE.CODE
        )
        fetch_response.assert_is_success()

        product_urls = fetch_response.content['body']['uriList']
        assert_that(product_urls, has_length(1))
        uri = product_urls[0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        product_info = product_response.content
        assert_that(product_info['product_code'], equal_to(config.data.TEST_MULTI_EXIST_CAT_FULL_STORE.PRODUCT))

    @pytest.allure.severity(severity_level.NORMAL)
    def test_fetch_products_should_succeed_when_product_has_both_existing_and_non_existing_categories_with_validation_errors(
            self, config):
        entity_type = 'product'

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_MULTI_EXIST_CAT_HALF_STORE.PRODUCT],
            0,
            config.data.TEST_MULTI_EXIST_CAT_HALF_STORE.COUNTRY,
            config.data.TEST_MULTI_EXIST_CAT_HALF_STORE.LANGUAGE,
            config.data.TEST_MULTI_EXIST_CAT_HALF_STORE.CODE
        )
        fetch_response.assert_is_success()

        product_urls = fetch_response.content['body']['uriList']
        assert_that(product_urls, has_length(1))
        uri = product_urls[0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        product_info = product_response.content
        assert_that(product_info['product_code'], equal_to(config.data.TEST_MULTI_EXIST_CAT_HALF_STORE.PRODUCT))

    @pytest.allure.severity(severity_level.NORMAL)
    def test_fetch_products_should_succeed_when_product_has_non_existing_category_with_validation_errors(self, config):
        entity_type = 'product'

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_NON_EXIST_CAT_STORE.PRODUCT],
            0,
            config.data.TEST_NON_EXIST_CAT_STORE.COUNTRY,
            config.data.TEST_NON_EXIST_CAT_STORE.LANGUAGE,
            config.data.TEST_NON_EXIST_CAT_STORE.CODE
        )
        fetch_response.assert_is_success()

        product_urls = fetch_response.content['body']['uriList']
        assert_that(product_urls, has_length(1))
        uri = product_urls[0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        product_info = product_response.content
        assert_that(product_info['product_code'], equal_to(config.data.TEST_NON_EXIST_CAT_STORE.PRODUCT))
