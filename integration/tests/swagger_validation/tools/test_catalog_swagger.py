import time

import pytest

from integration.schemas import Schemas


class TestCatalogSwagger(object):

    @pytest.fixture(autouse=True)
    def setup(self, config):
        ###
        # Test setup
        login_response = config.freya.tools_gateway.login.auth_adfs_login(config.admin.username, config.admin.password)
        login_response.assert_is_success()

        title_response = config.freya.tools_gateway.title.get_title(config.data.TEST_TITLE)
        title_response.assert_is_success()
        title_versions = [version for version in title_response.content['title_versions']]

        title_version = next((title_version for title_version in title_versions if title_version['active']), None)
        config.store.catalog_code = next(
            (catalog_activation['catalog'] for catalog_activation in title_version['catalogs_activations'] if
             int(catalog_activation['active_at']) <= time.time()), None)

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_catalog_currencies(self, config):
        currencies_response = config.freya.tools_gateway.catalog.catalog_currencies(config.store.catalog_code)
        currencies_response.assert_is_success()
        Schemas.swagger_validate(currencies_response, '/api/v1/catalog/{catalog_code}/currency')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_catalog_entitlements(self, config):
        entitlements_response = config.freya.tools_gateway.catalog.catalog_entitlements(config.store.catalog_code)
        entitlements_response.assert_is_success()
        Schemas.swagger_validate(entitlements_response, '/api/v1/catalog/{catalog_code}/entitlement')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_catalog_getCatalog(self, config):
        catalog_response = config.freya.tools_gateway.catalog.catalog(config.store.catalog_code)
        catalog_response.assert_is_success()
        Schemas.swagger_validate(catalog_response, '/api/v1/catalog/{catalog_code}')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_catalog_products(self, config):
        products_response = config.freya.tools_gateway.catalog.catalog_products(config.store.catalog_code)
        products_response.assert_is_success()
        Schemas.swagger_validate(products_response, '/api/v1/catalog/{catalog_code}/product')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_catalog_specific_currency(self, config):
        currency_response = config.freya.tools_gateway.catalog.catalog_specific_currency(
            config.store.catalog_code,
            config.data.TEST_CURRENCY.CURRENCY_CODE
        )
        currency_response.assert_is_success()
        Schemas.swagger_validate(currency_response, '/api/v1/catalog/{catalog_code}/currency/{currency_code}')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_catalog_specific_entitlement(self, config):
        entitlement_response = config.freya.tools_gateway.catalog.catalog_specific_entitlement(config.store.catalog_code,
                                                                                             config.data.TEST_ENTITLEMENT.ENTITLEMENT_CODE)
        entitlement_response.assert_is_success()
        Schemas.swagger_validate(entitlement_response, '/api/v1/catalog/{catalog_code}/entitlement/{entitlement_code}')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_catalog_specific_product(self, config):
        product_response = config.freya.tools_gateway.catalog.catalog_specific_product(config.store.catalog_code,
                                                                                       config.data.TEST_PRODUCT.PRODUCT_CODE)
        product_response.assert_is_success()
        Schemas.swagger_validate(product_response, '/api/v1/catalog/{catalog_code}/product/{product_code}')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_catalog_specific_storefront(self, config):
        storefront_response = config.freya.tools_gateway.catalog.catalog_specific_storefront(config.store.catalog_code,
                                                                                             config.data.TEST_STORE.STOREFRONT)
        storefront_response.assert_is_success()
        Schemas.swagger_validate(storefront_response, '/api/v1/catalog/{catalog_code}/storefront')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_catalog_storefronts(self, config):
        storefronts_response = config.freya.tools_gateway.catalog.catalog_storefronts(config.store.catalog_code)
        storefronts_response.assert_is_success()
        Schemas.swagger_validate(storefronts_response, '/api/v1/catalog/{catalog_code}/storefront/{storefront_code}')
