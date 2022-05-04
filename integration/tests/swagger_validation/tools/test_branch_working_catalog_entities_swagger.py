import pytest

from integration.schemas import Schemas


class TestBranchWorkingCatalogEntitiesSwagger(object):

    @pytest.fixture(autouse=True)
    def setup(self, config):
        ###
        # Test setup
        login_response = config.freya.tools_gateway.login.auth_adfs_login(config.admin.username, config.admin.password)
        login_response.assert_is_success()

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_branch_working_catalog_entities_currencies(self, config):
        list_response = config.freya.tools_gateway.working_catalog_entities.get_entity_list(
            config.data.TEST_TITLE,
            config.data.TEST_TITLE_BRANCH,
            'currency')
        list_response.assert_is_success()
        Schemas.swagger_validate(list_response,
                                 '/api/v1/get_title/{title_code}/branch/{branch_name}/catalog/working/currency')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_branch_working_catalog_entities_entitlements(self, config):
        list_response = config.freya.tools_gateway.working_catalog_entities.get_entity_list(
            config.data.TEST_TITLE,
            config.data.TEST_TITLE_BRANCH,
            'entitlement')
        list_response.assert_is_success()
        Schemas.swagger_validate(list_response,
                                 '/api/v1/get_title/{title_code}/branch/{branch_name}/catalog/working/entitlement')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_branch_working_catalog_entities_overrides(self, config):
        list_response = config.freya.tools_gateway.working_catalog_entities.get_entity_list(
            config.data.TEST_TITLE,
            config.data.TEST_TITLE_BRANCH,
            'override')
        list_response.assert_is_success()
        Schemas.swagger_validate(list_response,
                                 '/api/v1/get_title/{title_code}/branch/{branch_name}/catalog/working/override')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_branch_working_catalog_entities_products(self, config):
        list_response = config.freya.tools_gateway.working_catalog_entities.get_entity_list(
            config.data.TEST_TITLE,
            config.data.TEST_TITLE_BRANCH,
            'product')
        list_response.assert_is_success()
        Schemas.swagger_validate(list_response,
                                 '/api/v1/get_title/{title_code}/branch/{branch_name}/catalog/working/product')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_branch_working_catalog_entities_promotions(self, config):
        list_response = config.freya.tools_gateway.working_catalog_entities.get_entity_list(
            config.data.TEST_TITLE,
            config.data.TEST_TITLE_BRANCH,
            'promotion')
        list_response.assert_is_success()
        Schemas.swagger_validate(list_response,
                                 '/api/v1/get_title/{title_code}/branch/{branch_name}/catalog/working/promotion')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_branch_working_catalog_entities_singleCurrency(self, config):
        entity_response = config.freya.tools_gateway.working_catalog_entities.get_entity(
            config.data.TEST_TITLE,
            config.data.TEST_TITLE_BRANCH,
            config.data.TEST_CURRENCY.CURRENCY_CODE,
            'currency')
        entity_response.assert_is_success()
        Schemas.swagger_validate(entity_response,
                                 '/api/v1/get_title/{title_code}/branch/{branch_name}/catalog/working/currency/{entity_code}')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_branch_working_catalog_entities_singleEntitlement(self, config):
        entity_response = config.freya.tools_gateway.working_catalog_entities.get_entity(
            config.data.TEST_TITLE,
            config.data.TEST_TITLE_BRANCH,
            config.data.TEST_ENTITLEMENT.ENTITLEMENT_CODE,
            'entitlement')
        entity_response.assert_is_success()
        Schemas.swagger_validate(entity_response,
                                 '/api/v1/get_title/{title_code}/branch/{branch_name}/catalog/working/entitlement/{entity_code}')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_branch_working_catalog_entities_singleOverride(self, config):
        entity_response = config.freya.tools_gateway.working_catalog_entities.get_entity(
            config.data.TEST_TITLE,
            config.data.TEST_TITLE_BRANCH,
            config.data.TEST_OVERRIDE.CODE,
            'override')
        entity_response.assert_is_success()
        Schemas.swagger_validate(entity_response,
                                 '/api/v1/get_title/{title_code}/branch/{branch_name}/catalog/working/override/{entity_code}')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_branch_working_catalog_entities_singleProduct(self, config):
        entity_response = config.freya.tools_gateway.working_catalog_entities.get_entity(
            config.data.TEST_TITLE,
            config.data.TEST_TITLE_BRANCH,
            config.data.TEST_PRODUCT.PRODUCT_CODE,
            'product')
        entity_response.assert_is_success()
        Schemas.swagger_validate(entity_response,
                                 '/api/v1/get_title/{title_code}/branch/{branch_name}/catalog/working/product/{entity_code}')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_branch_working_catalog_entities_singlePromotion(self, config):
        entity_response = config.freya.tools_gateway.working_catalog_entities.get_entity(
            config.data.TEST_TITLE,
            config.data.TEST_TITLE_BRANCH,
            config.data.TEST_PROMOTION.CODE,
            'promotion')
        entity_response.assert_is_success()
        Schemas.swagger_validate(entity_response,
                                 '/api/v1/get_title/{title_code}/branch/{branch_name}/catalog/working/promotion/{entity_code}')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_branch_working_catalog_entities_singleStorefront(self, config):
        entity_response = config.freya.tools_gateway.working_catalog_entities.get_entity(
            config.data.TEST_TITLE,
            config.data.TEST_TITLE_BRANCH,
            config.data.TEST_STORE.STOREFRONT,
            'storefront')
        entity_response.assert_is_success()
        Schemas.swagger_validate(entity_response,
                                 '/api/v1/get_title/{title_code}/branch/{branch_name}/catalog/working/storefront/{entity_code}')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_branch_working_catalog_entities_storefronts(self, config):
        list_response = config.freya.tools_gateway.working_catalog_entities.get_entity_list(
            config.data.TEST_TITLE,
            config.data.TEST_TITLE_BRANCH,
            'storefront')
        list_response.assert_is_success()
        Schemas.swagger_validate(list_response,
                                 '/api/v1/get_title/{title_code}/branch/{branch_name}/catalog/working/storefront')
