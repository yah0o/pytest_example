import pytest
from allure import severity_level
from hamcrest import assert_that, has_key, not_none, equal_to

from integration.main.request import RequestConstants, ResponseMessage


@pytest.allure.feature('server')
@pytest.allure.story('fetch categories')
class TestFetchCategories(object):

    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_fetch_categories_should_succeed_when_valid_storefront_with_categories_is_provided(self, config,
                                                                                               content_type):
        fetch_response = config.freya.server_gateway.fetch_categories(
            config.data.TEST_SINGLE_EXIST_CAT_FULL_STORE.CODE,
            config.data.TEST_SINGLE_EXIST_CAT_FULL_STORE.LANGUAGE,
            content_type=content_type
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body'], has_key('categories'))
        assert_that(fetch_response.content['body']['categories'], not_none())
        categories = fetch_response.content['body']['categories']
        category = next((category for category in categories
                         if category == config.data.TEST_SINGLE_EXIST_CAT_FULL_STORE.CATEGORY), None)
        assert_that(category, not_none())

    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_fetch_categories_should_succeed_when_valid_storefront_with_non_exist_categories_is_provided(self, config,
                                                                                                         content_type):
        fetch_response = config.freya.server_gateway.fetch_categories(
            config.data.TEST_NON_EXIST_CAT_STORE.CODE,
            config.data.TEST_NON_EXIST_CAT_STORE.LANGUAGE,
            content_type=content_type
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('categories'))
        assert_that(fetch_response.content['body']['categories'], not_none())
        categories = fetch_response.content['body']['categories']
        category = next((category for category in categories
                         if category == config.data.TEST_NON_EXIST_CAT_STORE.CATEGORY_STORE), None)
        assert_that(category, not_none())

    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_fetch_categories_should_succeed_when_valid_storefront_with_no_categories_is_provided(self, config,
                                                                                                  content_type):
        fetch_response = config.freya.server_gateway.fetch_categories(
            config.data.TEST_EMPTY_CAT_STORE.CODE,
            config.data.TEST_EMPTY_CAT_STORE.LANGUAGE,
            content_type=content_type
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('categories'))
        assert_that(fetch_response.content['body']['categories'], equal_to({}))

    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_storefront_code', [0, 'invalid_storefront_code'])
    def test_fetch_categories_should_fail_when_storefront_code_is_invalid(self, config, invalid_storefront_code):
        fetch_response = config.freya.server_gateway.fetch_categories(
            invalid_storefront_code,
            config.data.TEST_SINGLE_EXIST_CAT_FULL_STORE.LANGUAGE
        )
        fetch_response.expect_failure(result_code=ResponseMessage.STOREFRONT_NOT_FOUND)

    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('empty_storefront_code', ['', None])
    def test_fetch_categories_should_fail_when_storefront_code_is_empty_string_or_none(self, config,
                                                                                       empty_storefront_code):
        fetch_response = config.freya.server_gateway.fetch_categories(
            empty_storefront_code,
            config.data.TEST_SINGLE_EXIST_CAT_FULL_STORE.LANGUAGE
        )
        fetch_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR)

    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_language', [0, '', 'bad_language'])
    def test_fetch_categories_should_fail_when_language_is_invalid(self, config, invalid_language):
        fetch_response = config.freya.server_gateway.fetch_categories(
            config.data.TEST_SINGLE_EXIST_CAT_FULL_STORE.CODE,
            invalid_language
        )
        fetch_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR)

    @pytest.allure.severity(severity_level.MINOR)
    def test_fetch_categories_should_succeed_when_language_is_none(self, config):
        """
        The optional language parameter is not validated if language is none.
        """
        fetch_response = config.freya.server_gateway.fetch_categories(
            config.data.TEST_SINGLE_EXIST_CAT_FULL_STORE.CODE,
            None
        )
        fetch_response.assert_is_success()

    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('periods, expected_categories', [
        (['PAST'], {}),
        (['PRESENT'], {u'test_category_exist_full': {u'metadata': {u'meta': u'data'}}}),
        (['FUTURE'], {})
    ])
    def test_fetch_categories_should_succeed_when_periods_set(self, config, periods, expected_categories):
        """
        The optional periods parameter in req
        """
        fetch_response = config.freya.server_gateway.fetch_categories(
            config.data.TEST_SINGLE_EXIST_CAT_FULL_STORE.CODE,
            config.data.TEST_SINGLE_EXIST_CAT_FULL_STORE.LANGUAGE,
            periods=periods
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body'], has_key('categories'))
        assert_that(fetch_response.content['body']['categories'], equal_to(expected_categories))

    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('periods', [
        [123], 123, ['']
    ])
    def test_fetch_categories_should_fail_when_periods_invalid_type(self, config, periods):
        """
        The optional periods parameter in req has invalid type
        """
        fetch_response = config.freya.server_gateway.fetch_categories(
            config.data.TEST_SINGLE_EXIST_CAT_FULL_STORE.CODE,
            config.data.TEST_SINGLE_EXIST_CAT_FULL_STORE.LANGUAGE,
            periods=periods
        )
        fetch_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                      result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)
