import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities, ProductUtilities
from integration.main.request import RequestBuilder


@pytest.allure.feature('functional')
@pytest.allure.story('country restrictions')
class TestCountryRestrictions(object):

    @pytest.fixture(autouse=True)
    def country(self):
        """
        This lets each test override the country being used both by the test and during setup
        https://docs.pytest.org/en/latest/fixture.html#override-a-fixture-with-direct-test-parametrization

        :return: String (country to use in the test)
        """
        return 'US'

    @pytest.fixture(autouse=True)
    def setup(self, config, country):
        ###
        # Test setup
        config.store.account = AccountUtilities.create_account(attrs='user_stated_country={}'.format(country))

        account_created = config.spa.http.create_account(config.store.account.__dict__)
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

    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('country', ['ZZ'])
    def test_fetch_product_list_should_succeed_when_products_storefront_normally_visible_if_user_country_unknown(
            self,
            config
    ):
        """
        Use case: if the user country is unknown(zz), then the country from the API call is used instead.
        """
        expected_products = config.data.TEST_STORE_COUNTRY_RESTRICTED.EXPECTED_PRODUCTS

        product_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_STORE_COUNTRY_RESTRICTED.STOREFRONT,
            config.store.profile_id,
            config.data.TEST_STORE_COUNTRY_RESTRICTED.COUNTRY,
            config.data.TEST_STORE_COUNTRY_RESTRICTED.LANGUAGE
        )
        product_response.assert_is_success()

        config.log.info('comparing product codes from uri list to expected')
        assert_that(product_response.content['body'], has_key('uriList'))
        uri_list_products = ProductUtilities.product_codes_from_uri_list(product_response.content['body']['uriList'])
        assert_that(sorted(expected_products), equal_to(sorted(uri_list_products)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_product_is_restricted_by_us_country(self, config):
        """
        Use case: user country is 'US' and one of the products is restricted in the US -- so that one will not be visible.
        """
        expected_products = config.data.TEST_STORE_COUNTRY_RESTRICTED.PRODUCTS_WITHOUT_COUNTRY_RESTRICTION

        product_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_STORE_COUNTRY_RESTRICTED.STOREFRONT,
            config.store.profile_id,
            config.data.TEST_STORE_COUNTRY_RESTRICTED.COUNTRY,
            config.data.TEST_STORE_COUNTRY_RESTRICTED.LANGUAGE
        )
        product_response.assert_is_success()

        config.log.info('comparing product codes from uri list to expected')
        assert_that(product_response.content['body'], has_key('uriList'))
        uri_list_products = ProductUtilities.product_codes_from_uri_list(product_response.content['body']['uriList'])
        assert_that(sorted(expected_products), equal_to(sorted(uri_list_products)))

    @pytest.allure.severity(severity_level.MINOR)
    def test_fetch_product_list_should_fail_when_country_is_unknown(self, config):
        """
        Use case: account country is unknown(zz), API call country is unknown(zz), and all products have country-based restrictions/prices -- so none will be visible;
        Use case: account country is UNDEFINED, API call country is UNDEFINED, and all products have country-based restrictions/prices -- so none will be visible;
        """
        # FREYA-982 country changed in that case on default
        product_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_STORE_COUNTRY_RESTRICTED.STOREFRONT,
            config.store.profile_id,
            'ZZ',
            config.data.TEST_STORE_COUNTRY_RESTRICTED.LANGUAGE
        )
        product_response.assert_is_success()

    @pytest.allure.severity(severity_level.MINOR)
    def test_fetch_product_list_should_success_when_country_is_undefined(self, config, country):
        """
        Use case: account country is unknown(zz), API call country is unknown(zz), and all products have country-based restrictions/prices -- so none will be visible;
        Use case: account country is UNDEFINED, API call country is UNDEFINED, and all products have country-based restrictions/prices -- so none will be visible;
        """
        # FREYA-982 country changed in that case on default
        product_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_STORE_COUNTRY_RESTRICTED.STOREFRONT,
            config.store.profile_id,
            'UNDEFINED',
            config.data.TEST_STORE_COUNTRY_RESTRICTED.LANGUAGE
        )
        product_response.assert_is_success()

    @pytest.allure.severity(severity_level.MINOR)
    def test_fetch_products_should_fail_when_product_has_us_restriction(self, config):
        """
        Use case: account country is US and product is restricted there -- so it will not be visible.
        """
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT_COUNTRY_RESTRICTED.PRODUCT_CODE],
            config.store.profile_id,
            config.data.TEST_PRODUCT_COUNTRY_RESTRICTED.RESTRICTED_COUNTRY,  # API call country is not important,
            config.data.TEST_PRODUCT_COUNTRY_RESTRICTED.LANGUAGE
        )
        fetch_response.expect_failure(result_code='NO_PRODUCTS')

    @pytest.allure.severity(severity_level.MINOR)
    def test_fetch_products_should_fail_when_country_is_unknown(self, config):
        """
        Use case: account country is unknown(zz), API call country is unknown(zz), and product has _a_ country restriction -- so it will not be visible.
        Use case: account country is UNDEFINED, API call country is UNDEFINED, and product has _a_ country restriction -- so it will not be visible.
        """
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT_COUNTRY_RESTRICTED.PRODUCT_CODE],
            config.store.profile_id,
            'ZZ',
            config.data.TEST_PRODUCT_COUNTRY_RESTRICTED.LANGUAGE
        )
        fetch_response.expect_failure(result_code='NO_PRODUCTS')

    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('country', ['ZZ'])
    def test_fetch_products_should_return_succeed_when_api_country_overrides_unknown_user_country(self, config):
        """
        Use case: account country is unknown(zz), API call country is FR, and product is only restricted in the US -- so it will be shown;
        This is intended to demonstrate that if the account country is unknown, the API call country overrides it.
        """
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT_COUNTRY_RESTRICTED.PRODUCT_CODE],
            config.store.profile_id,
            config.data.TEST_PRODUCT_COUNTRY_RESTRICTED.UNRESTRICTED_COUNTRY,
            # account country is different from the product's restricted country
            config.data.TEST_PRODUCT_COUNTRY_RESTRICTED.LANGUAGE
        )
        fetch_response.assert_is_success()

        product_urls = fetch_response.content['body']['uriList']
        assert_that(product_urls, has_length(1))
        product_response = RequestBuilder(product_urls[0]).get()
        product_response.assert_is_success()

        config.log.info('checking product returns expected fields/entitlement')
        product_info = product_response.content
        assert_that(product_info['product_code'], equal_to(config.data.TEST_PRODUCT_COUNTRY_RESTRICTED.PRODUCT_CODE))
        assert_that(product_info['friendly_name'],
                    equal_to(config.data.TEST_PRODUCT_COUNTRY_RESTRICTED.FRIENDLY_NAME))
        assert_that(product_info['applied_promotions'], is_(empty()))

    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('country', ['ZZ'])
    def test_fetch_products_should_succeed_when_product_has_base_price_and_normally_visible(self, config):
        """
        Use case: ensure that the product with a base price is normally visible when account country is unknown(zz).
        """
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT_COUNTRY_BASE_PRICE.PRODUCT_CODE],
            config.store.profile_id,
            config.data.TEST_PRODUCT_COUNTRY_BASE_PRICE.COUNTRY,
            config.data.TEST_PRODUCT_COUNTRY_BASE_PRICE.LANGUAGE
        )
        fetch_response.assert_is_success()

        product_urls = fetch_response.content['body']['uriList']
        assert_that(product_urls, has_length(1))
        product_response = RequestBuilder(product_urls[0]).get()
        product_response.assert_is_success()

        config.log.info('checking product returns expected fields/entitlement')
        product_info = product_response.content
        assert_that(product_info['product_code'], equal_to(config.data.TEST_PRODUCT_COUNTRY_BASE_PRICE.PRODUCT_CODE))
        assert_that(product_info['friendly_name'],
                    equal_to(config.data.TEST_PRODUCT_COUNTRY_BASE_PRICE.FRIENDLY_NAME))
        assert_that(product_info['applied_promotions'], is_(empty()))

    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('country', ['ZZ'])
    def test_fetch_products_should_succeed_when_product_has_price_override_and_normally_visible(self, config):
        """
        Use case: ensure that the product with a price override is normally visible when account country is unknown.
        """
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT_COUNTRY_PRICE_OVERRIDE.PRODUCT_CODE],
            config.store.profile_id,
            config.data.TEST_PRODUCT_COUNTRY_PRICE_OVERRIDE.RESTRICTED_COUNTRY,
            config.data.TEST_PRODUCT_COUNTRY_PRICE_OVERRIDE.LANGUAGE
        )
        fetch_response.assert_is_success()

        product_urls = fetch_response.content['body']['uriList']
        assert_that(product_urls, has_length(1))
        product_response = RequestBuilder(product_urls[0]).get()
        product_response.assert_is_success()

        config.log.info('checking product returns expected fields/entitlement')
        product_info = product_response.content
        assert_that(product_info['product_code'],
                    equal_to(config.data.TEST_PRODUCT_COUNTRY_PRICE_OVERRIDE.PRODUCT_CODE))
        assert_that(product_info['friendly_name'],
                    equal_to(config.data.TEST_PRODUCT_COUNTRY_PRICE_OVERRIDE.FRIENDLY_NAME))
        assert_that(product_info['applied_promotions'], is_(empty()))

    @pytest.allure.severity(severity_level.MINOR)
    def test_fetch_products_should_fail_when_product_has_region_specific_price_and_country_is_unknown(
            self,
            config
    ):
        """
        Use case: account country is unknown(zz), API call country is unknown(zz), and product has a region-specific(na) base price
        in addition to a default price -- so it will not be visible.
        Use case: account country is undefined, API call country is undefined, and product has a region-specific(na) base price
        in addition to a default price -- so it will not be visible.
        """
        # FREYA-982 country changed in that case on default
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT_COUNTRY_BASE_PRICE.PRODUCT_CODE],
            config.store.profile_id,
            'ZZ',
            config.data.TEST_PRODUCT_COUNTRY_BASE_PRICE.LANGUAGE
        )
        fetch_response.assert_is_success()

    @pytest.allure.severity(severity_level.MINOR)
    def test_fetch_products_should_fail_when_product_has_region_specific_price_and_country_is_undefined(
            self,
            config
    ):
        """
        Use case: account country is unknown(zz), API call country is unknown(zz), and product has a region-specific(na) base price
        in addition to a default price -- so it will not be visible.
        Use case: account country is undefined, API call country is undefined, and product has a region-specific(na) base price
        in addition to a default price -- so it will not be visible.
        """
        # FREYA-982 country changed in that case on default
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT_COUNTRY_BASE_PRICE.PRODUCT_CODE],
            config.store.profile_id,
            'UNDEFINED',
            config.data.TEST_PRODUCT_COUNTRY_BASE_PRICE.LANGUAGE
        )
        fetch_response.assert_is_success()

    @pytest.allure.feature('functional')
    @pytest.allure.story('country restrictions')
    @pytest.allure.severity(severity_level.MINOR)
    def test_fetch_products_should_fail_when_product_has_override_price_and_if_country_is_unknown(
            self,
            config
    ):
        """
        Use case: account country is unknown, API call country is unknown, and product has _a_ price override -- so it will not be visible.
        Use case: account country is UNDEFINED, API call country is UNDEFINED, and product has _a_ price override -- so it will not be visible.
        """
        # FREYA-982 country changed in that case on default
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT_COUNTRY_PRICE_OVERRIDE.PRODUCT_CODE],
            config.store.profile_id,
            'ZZ',
            config.data.TEST_PRODUCT_COUNTRY_PRICE_OVERRIDE.LANGUAGE
        )
        fetch_response.assert_is_success()

    @pytest.allure.feature('functional')
    @pytest.allure.story('country restrictions')
    @pytest.allure.severity(severity_level.MINOR)
    def test_fetch_products_should_success_when_product_has_override_price_and_if_country_is_undefined(
            self,
            config
    ):
        """
        Use case: account country is unknown, API call country is unknown, and product has _a_ price override -- so it will not be visible.
        Use case: account country is UNDEFINED, API call country is UNDEFINED, and product has _a_ price override -- so it will not be visible.
        """
        # FREYA-982 country changed in that case on default
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT_COUNTRY_PRICE_OVERRIDE.PRODUCT_CODE],
            config.store.profile_id,
            'UNDEFINED',
            config.data.TEST_PRODUCT_COUNTRY_PRICE_OVERRIDE.LANGUAGE
        )
        fetch_response.assert_is_success()
