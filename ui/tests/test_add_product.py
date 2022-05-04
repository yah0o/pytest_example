import pytest

from selenium.common.exceptions import WebDriverException, TimeoutException
from hamcrest import assert_that, equal_to, has_length, none, not_
from selenium.common.exceptions import WebDriverException, TimeoutException

from ui.main.constants import FRIENDLY_NAME_INVALID_INPUT, CODE_INVALID_INPUT, PLATFORM_HEADER_TEXT
from ui.main.helpers import RandomUtilities
from ui.pages import Sidebar, Notification, Header, CatalogTabs, AddProduct, Products, AddEntityToEntity, EditProduct, \
    AddPricesToProduct


@pytest.allure.step('Validate elements on the add product page')
def validate_page(add_product_page):
    assert_that(add_product_page.get_add_product_header().text, equal_to('Create Product'))

    assert_that(add_product_page.get_friendly_name_label().text, equal_to('Friendly Name\n*'))
    assert_that(add_product_page.get_friendly_name_input())

    assert_that(add_product_page.get_code_label().text, equal_to('Code\n*'))
    assert_that(add_product_page.get_code_input())

    assert_that(add_product_page.get_active_header().text, equal_to('Active'))
    assert_that(add_product_page.get_active_toggle())
    assert_that(add_product_page.get_inactive_label().text, equal_to('Inactive'))
    assert_that(add_product_page.get_active_label().text, equal_to('Active'))

    assert_that(add_product_page.get_metadata_header().text, equal_to('Metadata'))
    assert_that(add_product_page.get_metadata_toggle())
    assert_that(add_product_page.get_field_editor_label().text, equal_to('Field Editor'))
    assert_that(add_product_page.get_code_editor_label().text, equal_to('Code Editor'))

    assert_that(add_product_page.get_tags_header().text, equal_to('Tags'))
    assert_that(add_product_page.get_tags_input())
    # assert_that(add_product_page.get_tags_drop_down_arrow())

    assert_that(add_product_page.get_entity_heading('currencies').text, equal_to('Currencies'))
    assert_that(add_product_page.get_entity_add_button('currencies').text, equal_to('Add'))

    assert_that(add_product_page.get_entity_heading('entitlements').text, equal_to('Entitlements'))
    assert_that(add_product_page.get_entity_add_button('entitlements').text, equal_to('Add'))

    assert_that(add_product_page.get_entity_heading('prices').text, equal_to('Prices'))
    assert_that(add_product_page.get_entity_add_button('prices').text, equal_to('Add'))

    assert_that(add_product_page.get_entity_heading('prerequisites').text, equal_to('Prerequisites'))
    assert_that(add_product_page.get_entity_add_button('prerequisites').text, equal_to('Add'))

    # assert_that(add_product_page.get_name_header().text, equal_to('Name'))
    # assert_that(add_product_page.get_name_key_label().text, equal_to('Key:'))
    # assert_that(add_product_page.get_name_key_input())
    # assert_that(add_product_page.get_name_value_label().text, equal_to('Value:'))
    # assert_that(add_product_page.get_name_value_input())
    # assert_that(add_product_page.get_name_add_button().text, equal_to('ADD'))
    #
    # assert_that(add_product_page.get_description_header().text, equal_to('Description'))
    # assert_that(add_product_page.get_description_key_label().text, equal_to('Key:'))
    # assert_that(add_product_page.get_description_key_input())
    # assert_that(add_product_page.get_description_value_label().text, equal_to('Value:'))
    # assert_that(add_product_page.get_description_value_input())
    # assert_that(add_product_page.get_description_add_button().text, equal_to('ADD'))

    assert_that(add_product_page.get_purchasable_header().text, equal_to('Purchasable'))
    assert_that(add_product_page.get_purchasable_toggle())
    assert_that(add_product_page.get_not_purchasable_label().text, equal_to('Not purchasable'))
    assert_that(add_product_page.get_purchasable_label().text, equal_to('Purchasable'))

    assert_that(add_product_page.get_visible_header().text, equal_to('Visible'))
    assert_that(add_product_page.get_visible_toggle())
    assert_that(add_product_page.get_invisible_label().text, equal_to('Invisible'))
    assert_that(add_product_page.get_visible_label().text, equal_to('Visible'))

    assert_that(add_product_page.get_restricted_countries_header().text, equal_to('Restricted Countries'))
    assert_that(add_product_page.get_restricted_countries_input())
    # assert_that(add_product_page.get_restricted_countries_drop_down_arrow())

    assert_that(add_product_page.get_spa_access_header().text, equal_to('SPA Access'))
    assert_that(add_product_page.get_spa_access_input())
    # assert_that(add_product_page.get_spa_access_drop_down_arrow())

    assert_that(add_product_page.get_save_button().text, equal_to('Create'))
    assert_that(add_product_page.get_cancel_button().text, equal_to('Cancel'))


@pytest.allure.step('Validate elements on the catalog tabs page')
def validate_catalog_tabs_page(catalog_tabs_page, config):
    assert_that(catalog_tabs_page.get_catalog_title().text, equal_to(config.data.TEST_CATALOG.FRIENDLY_NAME))
    assert_that(catalog_tabs_page.get_secondary_heading())
    assert_that(catalog_tabs_page.get_download_config_button().text, equal_to('Download Config'))
    assert_that(catalog_tabs_page.get_publish_button().text, equal_to('Publish'))
    # assert_that(catalog_tabs_page.get_overview_tab().text, equal_to('Overview'))
    assert_that(catalog_tabs_page.get_storefronts_tab().text, equal_to('Storefronts'))
    assert_that(catalog_tabs_page.get_products_tab().text, equal_to('Products'))
    assert_that(catalog_tabs_page.get_entitlements_tab().text, equal_to('Entitlements'))
    assert_that(catalog_tabs_page.get_currencies_tab().text, equal_to('Currencies'))
    # assert_that(catalog_tabs_page.get_campaigns_tab().text, equal_to('Campaigns'))
    # assert_that(catalog_tabs_page.get_activity_tab().text, equal_to('Activity'))
    assert_that(catalog_tabs_page.get_tab_list(), has_length(4))


@pytest.allure.step('Validate elements on the add product sidebar page')
def validate_add_product_sidebar_page(sidebar_page):
    # assert_that(sidebar_page.get_dashboard_button().text, equal_to('Dashboard'))
    assert_that(sidebar_page.get_titles_button().text, equal_to('Titles'))
    assert_that(sidebar_page.get_catalogs_button().text, equal_to('Catalogs'))
    assert_that(sidebar_page.get_environments_button().text, equal_to('Environments'))
    assert_that(sidebar_page.get_title_components_button().text, equal_to('Title Components'))
    # assert_that(sidebar_page.get_activity_button().text, equal_to('Activity'))
    # assert_that(sidebar_page.get_users_button().text, equal_to('Users'))
    assert_that(sidebar_page.get_players_button().text, equal_to('Players'))
    # assert_that(sidebar_page.get_reports_button().text, equal_to('Reports'))
    assert_that(sidebar_page.get_panel(), has_length(5))


@pytest.allure.step('Validate elements on the add product header page')
def validate_add_product_header_page(header_page):
    assert_that(header_page.get_home_button())

    top_bar_header = header_page.get_top_bar_header()
    assert_that(top_bar_header.text, equal_to(PLATFORM_HEADER_TEXT))

    # assert_that(header_page.get_network_status())
    #
    # assert_that(header_page.get_notification_icon())

    assert_that(header_page.get_settings_icon())

    assert_that(header_page.get_drop_down_menu())

    # drop_down_options = header_page.get_drop_down_options()
    # assert_that(drop_down_options, has_length(2))

    assert_that(header_page.get_user_icon())

    assert_that(header_page.get_user_id())

    assert_that(header_page.get_logout_button())


@pytest.fixture
def setup(config, browser, steps):
    add_product_page = AddProduct(browser)
    products_page = Products(browser)
    catalog_tabs_page = CatalogTabs(browser)
    sidebar_page = Sidebar(browser)
    header_page = Header(browser)

    steps.login(config.admin.username, config.admin.password)
    steps.navigate_to_titles_page(config.data.TEST_STUDIO.CODE)
    steps.navigate_to_catalogs_page(config.data.TEST_TITLE.CODE)
    steps.navigate_to_catalog_tabs_page(config.data.TEST_CATALOG.CODE)
    steps.navigate_to_products_tab()

    products_page.click_add_button()
    add_product_page.wait_for_page_load()

    yield add_product_page, products_page, catalog_tabs_page, sidebar_page, header_page


@pytest.allure.testcase("Validate add product page")
def test_add_product_page(setup):
    add_product_page, _, _, _, _ = setup
    validate_page(add_product_page)


@pytest.allure.testcase("Validate catalog tabs page")
def test_catalog_tabs_page(setup, config):
    _, _, catalog_tabs_page, _, _ = setup
    validate_catalog_tabs_page(catalog_tabs_page, config)


@pytest.allure.testcase("Validate add product sidebar")
def test_add_product_sidebar_page(setup):
    _, _, _, sidebar_page, _ = setup
    validate_add_product_sidebar_page(sidebar_page)


@pytest.allure.testcase("Validate add product header page")
def test_add_product_header_page(setup):
    _, _, _, _, header_page = setup
    validate_add_product_header_page(header_page)


@pytest.mark.xfail(reason='PLAT-6334', raises=TimeoutException)
@pytest.allure.testcase("Validate can add a product through the UI")
def test_add_product_functions(browser, setup):
    add_product_page, products_page, _, _, _ = setup
    notification = Notification(browser)

    unique_id = RandomUtilities.create_unique_id_lowercase()

    friendly_name = 'Test UI Create Product {}'.format(unique_id)
    product_code = 'test_ui_create_product_{}'.format(unique_id)

    add_product_page.type_friendly_name_input(friendly_name)
    add_product_page.type_code_input(product_code)
    add_product_page.click_save_button()

    notification.wait_for_notification_message()
    notification_message = notification.get_notification_message()
    assert_that(notification_message.text, equal_to('Product: {} successfully created!'.format(product_code)))

    products_page.wait_for_page_load()
    assert_that(products_page.get_product_by_name(product_code).text, equal_to(friendly_name))


@pytest.mark.xfail(reason='PLAT-6334', raises=TimeoutException)
@pytest.allure.testcase("Validate Add Product toggles functions")
def test_add_product_toggles(browser, setup):
    add_product_page, products_page, _, _, _ = setup
    notification = Notification(browser)
    edit_product_page = EditProduct(browser)

    unique_id = RandomUtilities.create_unique_id_lowercase()

    friendly_name = 'Test UI Create Product {}'.format(unique_id)
    product_code = 'test_ui_create_product_{}'.format(unique_id)

    add_product_page.type_friendly_name_input(friendly_name)
    add_product_page.type_code_input(product_code)
    add_product_page.click_active_toggle()
    add_product_page.click_metadata_toggle()
    add_product_page.click_purchasable_toggle()
    add_product_page.click_visible_toggle()

    assert_that(not_(add_product_page.get_active_checkbox().is_selected()))
    assert_that(add_product_page.get_metadata_checkbox().is_selected())
    assert_that(not_(add_product_page.get_purchasable_checkbox().is_selected()))
    assert_that(not_(add_product_page.get_visible_checkbox().is_selected()))

    add_product_page.click_save_button()

    notification.wait_for_notification_message()
    notification_message = notification.get_notification_message()
    assert_that(notification_message.text, equal_to('Product: {} successfully created!'.format(product_code)))

    products_page.click_product_button(product_code)
    edit_product_page.wait_for_page_load()

    assert_that(not_(edit_product_page.get_active_checkbox().is_selected()))
    assert_that(not_(edit_product_page.get_metadata_checkbox().is_selected()))
    assert_that(not_(edit_product_page.get_purchasable_checkbox().is_selected()))
    assert_that(not_(edit_product_page.get_visible_checkbox().is_selected()))


@pytest.mark.xfail(reason='PLAT-6334', raises=TimeoutException)
@pytest.allure.testcase("Validate cannot add a duplicate product through the UI")
def test_add_product_does_not_create_duplicate_products(config, browser, setup):
    add_product_page, products_page, catalog_tabs_page, _, _ = setup
    notification = Notification(browser)

    add_product_page.type_friendly_name_input('Test UI Create Duplicate Product')
    add_product_page.type_code_input(config.data.TEST_PRODUCT.CODE)
    add_product_page.click_save_button()

    notification.wait_for_notification_message()
    assert_that(
        notification.get_notification_message().text,
        equal_to("\"Entity '{}' of title '{}' of studio '{}' already exists, creation impossible\"".format(
            config.data.TEST_PRODUCT.CODE,
            config.data.TEST_TITLE.CODE,
            config.data.TEST_STUDIO.CODE
        ))
    )

    catalog_tabs_page.click_products_tab()
    products_page.wait_for_page_load()
    products_list = products_page.get_products_list()

    count = 0
    for product in products_list:
        if config.data.TEST_PRODUCT.FRIENDLY_NAME in product.get_attribute('innerHTML'):
            count = count + 1
    assert_that(count, equal_to(1))


@pytest.allure.testcase("Ensure cancel button returns the user to the products page")
def test_add_product_cancel_button_returns_to_products_page(setup):
    add_product_page, products_page, _, _, _ = setup

    add_product_page.click_cancel_button()

    products_page.wait_for_page_load()
    assert_that(products_page.get_products_list())


@pytest.allure.testcase("Ensure product won't get created when friendly name input is invalid")
@pytest.mark.parametrize('invalid_friendly_name', ['!', '@'])
def test_add_product_does_not_create_product_when_friendly_name_is_invalid(invalid_friendly_name, setup):
    add_product_page, _, _, _, _ = setup

    unique_id = RandomUtilities.create_unique_id_lowercase()
    product_code = 'test_ui_create_product_{}'.format(unique_id)

    add_product_page.type_friendly_name_input(invalid_friendly_name)
    add_product_page.wait_for_friendly_name_invalid_message()
    assert_that(add_product_page.get_friendly_name_invalid_message().text, equal_to(FRIENDLY_NAME_INVALID_INPUT))

    add_product_page.type_code_input(product_code)
    assert_that(add_product_page.get_save_button().is_enabled(), equal_to(False))


@pytest.allure.testcase("Ensure product won't get created when code input is invalid")
@pytest.mark.parametrize('invalid_code', ['!', '@'])
def test_add_product_does_not_create_product_when_code_is_invalid(invalid_code, setup):
    add_product_page, _, _, _, _ = setup

    unique_id = RandomUtilities.create_unique_id_lowercase()
    friendly_name = 'Test UI Create Product {}'.format(unique_id)

    add_product_page.type_friendly_name_input(friendly_name)
    add_product_page.type_code_input(invalid_code)
    add_product_page.wait_for_code_invalid_message()
    assert_that(add_product_page.get_code_invalid_message().text, equal_to(CODE_INVALID_INPUT))

    assert_that(add_product_page.get_save_button().is_enabled(), equal_to(False))


@pytest.allure.testcase("Ensure the product is not being created when saving with empty input data")
@pytest.mark.parametrize('page_input', [('', ''), ('friendly_name_input', ''), ('', 'code_input')])
def test_add_product_does_not_create_product_when_empty_input_data(setup, page_input):
    add_product_page, _, _, _, _ = setup
    friendly_name_input, code_input = page_input

    add_product_page.type_friendly_name_input(friendly_name_input)
    add_product_page.type_code_input(code_input)
    assert_that(add_product_page.get_save_button().is_enabled(), equal_to(False))


@pytest.mark.xfail(reason='PLAT-6334', raises=TimeoutException)
@pytest.allure.testcase("Validate can add a currency to a product")
def test_add_one_currency_to_product(setup, browser, config):
    add_product_page, products_page, _, _, _ = setup
    add_entity_to_entity_page = AddEntityToEntity(browser)
    notification = Notification(browser)
    edit_product_page = EditProduct(browser)

    # Fill out product's friendly name and code fields
    unique_id = RandomUtilities.create_unique_id_lowercase()
    product_friendly_name = 'Test UI Create Product {}'.format(unique_id)
    product_code = 'test_ui_create_product_{}'.format(unique_id)
    add_product_page.type_friendly_name_input(product_friendly_name)
    add_product_page.type_code_input(product_code)

    # Add currency to the product
    add_product_page.click_entity_add_button('currencies')
    add_entity_to_entity_page.wait_for_page_load('currencies')
    add_entity_to_entity_page.click_entity_checkbox(config.data.TEST_CURRENCY.CODE)

    # Make sure the currency that was just added to the product is not on the list anymore
    currency_list = add_entity_to_entity_page.get_entity_list_by_entity_type('currencies')
    currency = next((currency for currency in currency_list
                     if currency == config.data.TEST_CURRENCY.CODE), None)
    assert_that(currency, none(), 'The currency that was already added to the product is still on the list')
    add_entity_to_entity_page.click_add_button()

    # Check the currency was successfully added to the product
    assert_that(add_product_page.get_entity_by_name(config.data.TEST_CURRENCY.CODE))

    amount_input = add_product_page.get_entity_amount_input(config.data.TEST_CURRENCY.CODE)
    amount_input_value = amount_input.get_attribute('value')
    assert_that(amount_input_value), equal_to('0')

    pct_value_input = add_product_page.get_entity_pct_value_input(config.data.TEST_CURRENCY.CODE)
    pct_value_input_value = pct_value_input.get_attribute('value')
    assert_that(pct_value_input_value), equal_to('0')

    assert_that(add_product_page.get_entity_remove_button(config.data.TEST_CURRENCY.CODE))

    # Check the product with the currency is created
    add_product_page.click_save_button()

    notification.wait_for_notification_message()
    assert_that(notification.get_notification_message().text,
                equal_to('Product: {} successfully created!'.format(product_code)))

    products_page.wait_for_page_load()
    assert_that(products_page.get_product_by_name(product_code).text, equal_to(product_friendly_name))

    products_page.click_product_button(product_code)
    edit_product_page.wait_for_page_load()

    assert_that(edit_product_page.get_friendly_name_input().get_attribute('value'), equal_to(product_friendly_name))

    assert_that(edit_product_page.get_code_input().is_enabled(), equal_to(False))
    code_input = edit_product_page.get_code_input()
    code_input_value = code_input.get_attribute('value')
    assert_that(code_input_value, equal_to(product_code))

    assert_that(edit_product_page.get_version_input().is_enabled(), equal_to(False))
    version_input = edit_product_page.get_version_input()
    version_input_value = version_input.get_attribute('value')
    assert_that(version_input_value, equal_to('1'))

    assert_that(edit_product_page.get_entity_by_name(config.data.TEST_CURRENCY.CODE))
    assert_that(edit_product_page.get_entity_amount_input(config.data.TEST_CURRENCY.CODE))
    assert_that(edit_product_page.get_entity_pct_value_input(config.data.TEST_CURRENCY.CODE))
    assert_that(edit_product_page.get_entity_remove_button(config.data.TEST_CURRENCY.CODE))


@pytest.mark.xfail(reason='PLAT-6334', raises=TimeoutException)
@pytest.allure.testcase("Validate can add an entitlement to a product")
def test_add_one_entitlement_to_product(setup, browser, config):
    add_product_page, products_page, _, _, _ = setup
    add_entity_to_entity_page = AddEntityToEntity(browser)
    notification = Notification(browser)
    edit_product_page = EditProduct(browser)

    # Fill out product's friendly name and code fields
    unique_id = RandomUtilities.create_unique_id_lowercase()
    product_friendly_name = 'Test UI Create Product {}'.format(unique_id)
    product_code = 'test_ui_create_product_{}'.format(unique_id)
    add_product_page.type_friendly_name_input(product_friendly_name)
    add_product_page.type_code_input(product_code)

    # Add entitlement to the product
    add_product_page.click_entity_add_button('entitlements')
    add_entity_to_entity_page.wait_for_page_load('entitlements')
    add_entity_to_entity_page.click_entity_checkbox(config.data.TEST_ENTITLEMENT.CODE)

    # Make sure the entitlement that was just added to the product is not on the list anymore
    entitlement_list = add_entity_to_entity_page.get_entity_list_by_entity_type('entitlements')
    entitlement = next((entitlement for entitlement in entitlement_list
                        if entitlement == config.data.TEST_ENTITLEMENT.CODE), None)
    assert_that(entitlement, none(), 'The entitlement that was already added to the product is still on the list')
    add_entity_to_entity_page.click_add_button()

    # Check the entitlement was successfully added to the product
    assert_that(add_product_page.get_entity_by_name(config.data.TEST_ENTITLEMENT.CODE))

    amount_input = add_product_page.get_entity_amount_input(config.data.TEST_ENTITLEMENT.CODE)
    amount_input_value = amount_input.get_attribute('value')
    assert_that(amount_input_value), equal_to('0')

    pct_value_input = add_product_page.get_entity_pct_value_input(config.data.TEST_ENTITLEMENT.CODE)
    pct_value_input_value = pct_value_input.get_attribute('value')
    assert_that(pct_value_input_value), equal_to('0')

    assert_that(add_product_page.get_entity_remove_button(config.data.TEST_ENTITLEMENT.CODE))

    # Check the product with the entitlement is created
    add_product_page.click_save_button()

    notification.wait_for_notification_message()
    assert_that(notification.get_notification_message().text,
                equal_to('Product: {} successfully created!'.format(product_code)))

    products_page.wait_for_page_load()
    assert_that(products_page.get_product_by_name(product_code).text, equal_to(product_friendly_name))

    products_page.click_product_button(product_code)
    edit_product_page.wait_for_page_load()

    assert_that(edit_product_page.get_friendly_name_input().get_attribute('value'), equal_to(product_friendly_name))

    assert_that(edit_product_page.get_code_input().is_enabled(), equal_to(False))
    code_input = edit_product_page.get_code_input()
    code_input_value = code_input.get_attribute('value')
    assert_that(code_input_value, equal_to(product_code))

    assert_that(edit_product_page.get_version_input().is_enabled(), equal_to(False))
    version_input = edit_product_page.get_version_input()
    version_input_value = version_input.get_attribute('value')
    assert_that(version_input_value, equal_to('1'))

    assert_that(edit_product_page.get_entity_by_name(config.data.TEST_ENTITLEMENT.CODE))
    assert_that(edit_product_page.get_entity_amount_input(config.data.TEST_ENTITLEMENT.CODE))
    assert_that(edit_product_page.get_entity_pct_value_input(config.data.TEST_ENTITLEMENT.CODE))
    assert_that(edit_product_page.get_entity_remove_button(config.data.TEST_ENTITLEMENT.CODE))


@pytest.mark.xfail(reason='PLAT-6334', raises=TimeoutException)
@pytest.allure.testcase("Validate can add currency and entitlement to a product")
def test_add_currency_and_entitlement_to_product(setup, browser, config):
    add_product_page, products_page, _, _, _ = setup
    add_entity_to_entity_page = AddEntityToEntity(browser)
    notification = Notification(browser)
    edit_product_page = EditProduct(browser)

    # Fill out product's friendly name and code fields
    unique_id = RandomUtilities.create_unique_id_lowercase()
    product_friendly_name = 'Test UI Create Product {}'.format(unique_id)
    product_code = 'test_ui_create_product_{}'.format(unique_id)
    add_product_page.type_friendly_name_input(product_friendly_name)
    add_product_page.type_code_input(product_code)

    # Add currency to the product
    add_product_page.click_entity_add_button('currencies')
    add_entity_to_entity_page.wait_for_page_load('currencies')
    add_entity_to_entity_page.click_entity_checkbox(config.data.TEST_CURRENCY.CODE)

    # Make sure the currency that was just added to the product is not on the list anymore
    currency_list = add_entity_to_entity_page.get_entity_list_by_entity_type('currencies')
    currency = next((currency for currency in currency_list
                     if currency == config.data.TEST_CURRENCY.CODE), None)
    assert_that(currency, none(), 'The currency that was already added to the product is still on the list')
    add_entity_to_entity_page.click_add_button()

    # Add entitlement to the product
    add_product_page.click_entity_add_button('entitlements')
    add_entity_to_entity_page.wait_for_page_load('entitlements')
    add_entity_to_entity_page.click_entity_checkbox(config.data.TEST_ENTITLEMENT.CODE)

    # Make sure the entitlement that was just added to the product is not on the list anymore
    entitlement_list = add_entity_to_entity_page.get_entity_list_by_entity_type('entitlements')
    entitlement = next((entitlement for entitlement in entitlement_list
                        if entitlement == config.data.TEST_ENTITLEMENT.CODE), None)
    assert_that(entitlement, none(), 'The entitlement that was already added to the product is still on the list')
    add_entity_to_entity_page.click_add_button()

    # Check the currency was successfully added to the product
    assert_that(add_product_page.get_entity_by_name(config.data.TEST_CURRENCY.CODE))

    amount_input = add_product_page.get_entity_amount_input(config.data.TEST_CURRENCY.CODE)
    amount_input_value = amount_input.get_attribute('value')
    assert_that(amount_input_value), equal_to('0')

    pct_value_input = add_product_page.get_entity_pct_value_input(config.data.TEST_CURRENCY.CODE)
    pct_value_input_value = pct_value_input.get_attribute('value')
    assert_that(pct_value_input_value), equal_to('0')

    assert_that(add_product_page.get_entity_remove_button(config.data.TEST_CURRENCY.CODE))

    # Check the entitlement was successfully added to the product
    assert_that(add_product_page.get_entity_by_name(config.data.TEST_ENTITLEMENT.CODE))

    amount_input = add_product_page.get_entity_amount_input(config.data.TEST_ENTITLEMENT.CODE)
    amount_input_value = amount_input.get_attribute('value')
    assert_that(amount_input_value), equal_to('0')

    pct_value_input = add_product_page.get_entity_pct_value_input(config.data.TEST_ENTITLEMENT.CODE)
    pct_value_input_value = pct_value_input.get_attribute('value')
    assert_that(pct_value_input_value), equal_to('0')

    assert_that(add_product_page.get_entity_remove_button(config.data.TEST_ENTITLEMENT.CODE))

    # Check the product with currency and entitlement is created
    add_product_page.click_save_button()

    notification.wait_for_notification_message()
    assert_that(notification.get_notification_message().text,
                equal_to('Product: {} successfully created!'.format(product_code)))

    products_page.wait_for_page_load()
    assert_that(products_page.get_product_by_name(product_code).text, equal_to(product_friendly_name))

    products_page.click_product_button(product_code)
    edit_product_page.wait_for_page_load()

    assert_that(edit_product_page.get_friendly_name_input().get_attribute('value'), equal_to(product_friendly_name))

    assert_that(edit_product_page.get_code_input().is_enabled(), equal_to(False))
    code_input = edit_product_page.get_code_input()
    code_input_value = code_input.get_attribute('value')
    assert_that(code_input_value, equal_to(product_code))

    assert_that(edit_product_page.get_version_input().is_enabled(), equal_to(False))
    version_input = edit_product_page.get_version_input()
    version_input_value = version_input.get_attribute('value')
    assert_that(version_input_value, equal_to('1'))

    assert_that(edit_product_page.get_entity_by_name(config.data.TEST_CURRENCY.CODE))
    assert_that(edit_product_page.get_entity_amount_input(config.data.TEST_CURRENCY.CODE))
    assert_that(edit_product_page.get_entity_pct_value_input(config.data.TEST_CURRENCY.CODE))
    assert_that(edit_product_page.get_entity_remove_button(config.data.TEST_CURRENCY.CODE))

    assert_that(edit_product_page.get_entity_by_name(config.data.TEST_ENTITLEMENT.CODE))
    assert_that(edit_product_page.get_entity_amount_input(config.data.TEST_ENTITLEMENT.CODE))
    assert_that(edit_product_page.get_entity_pct_value_input(config.data.TEST_ENTITLEMENT.CODE))
    assert_that(edit_product_page.get_entity_remove_button(config.data.TEST_ENTITLEMENT.CODE))


@pytest.mark.xfail(reason='PLAT-6334', raises=TimeoutException)
@pytest.allure.testcase("Validate can add vc price to a product")
def test_add_vc_price_to_product(setup, browser, config):
    add_product_page, products_page, _, _, _ = setup
    add_price_page = AddPricesToProduct(browser)
    notification_page = Notification(browser)
    edit_product_page = EditProduct(browser)

    # Fill out product's friendly name and code fields
    unique_id = RandomUtilities.create_unique_id_lowercase()
    product_friendly_name = 'Test UI Create Product {}'.format(unique_id)
    product_code = 'test_ui_create_product_{}'.format(unique_id)
    add_product_page.type_friendly_name_input(product_friendly_name)
    add_product_page.type_code_input(product_code)

    # Add price to Product
    price_amount = '100'
    add_product_page.click_entity_add_button('prices')
    add_price_page.wait_for_page_load()
    add_price_page.click_currency_code_drop_down()
    add_price_page.wait_for_drop_down_option_load(config.data.TEST_CURRENCY.CODE)
    add_price_page.click_drop_down_option_by_name(config.data.TEST_CURRENCY.CODE)
    add_price_page.type_amount_input('\b{}'.format(price_amount))
    add_price_page.click_add_button()

    # Validate that the price was added to the product
    add_product_page.wait_for_page_load()
    assert_that(add_product_page.get_prices_list(), has_length(1))
    assert_that(add_product_page.get_prices_rm_header().text, equal_to('Real Money'))
    assert_that(add_product_page.get_prices_currency_code_header().text, equal_to('Currency Code'))
    assert_that(add_product_page.get_prices_amount_header().text, equal_to('Amount'))
    assert_that(add_product_page.get_prices_toggle(config.data.TEST_CURRENCY.CODE))
    assert_that(
        add_product_page.get_prices_vc_currency_code(config.data.TEST_CURRENCY.CODE).text,
        equal_to(config.data.TEST_CURRENCY.CODE)
    )
    # assert_that(add_product_page.get_prices_pricing_type(config.data.TEST_CURRENCY.CODE).text, equal_to('LINEAR'))
    assert_that(
        add_product_page.get_prices_amount(config.data.TEST_CURRENCY.CODE).get_attribute('value'),
        equal_to(price_amount)
    )
    assert_that(add_product_page.get_prices_delete_button(config.data.TEST_CURRENCY.CODE))

    # Validate that the product was created
    add_product_page.click_save_button()

    notification_page.wait_for_notification_message()
    notification_message = notification_page.get_notification_message()
    assert_that(notification_message.text, equal_to('Product: {} successfully created!'.format(product_code)))

    products_page.wait_for_page_load()
    assert_that(products_page.get_product_by_name(product_code).text, equal_to(product_friendly_name))

    products_page.click_product_button(product_code)
    edit_product_page.wait_for_page_load()

    assert_that(edit_product_page.get_friendly_name_input().get_attribute('value'), equal_to(product_friendly_name))

    assert_that(edit_product_page.get_prices_list(), has_length(1))
    assert_that(edit_product_page.get_prices_toggle(config.data.TEST_CURRENCY.CODE))
    assert_that(
        edit_product_page.get_prices_vc_currency_code(config.data.TEST_CURRENCY.CODE).text,
        equal_to(config.data.TEST_CURRENCY.CODE)
    )
    # assert_that(edit_product_page.get_prices_pricing_type(config.data.TEST_CURRENCY.CODE).text, equal_to('LINEAR'))
    assert_that(
        edit_product_page.get_prices_amount(config.data.TEST_CURRENCY.CODE).get_attribute('value'),
        equal_to(price_amount)
    )
    assert_that(edit_product_page.get_prices_delete_button(config.data.TEST_CURRENCY.CODE))


# @pytest.mark.xfail(reason='PLAT-6334', raises=TimeoutException)
@pytest.allure.testcase("Validate can add rm price to a product")
def test_add_rm_price_to_product(setup, browser):
    add_product_page, products_page, _, _, _ = setup
    add_price_page = AddPricesToProduct(browser)
    notification_page = Notification(browser)
    edit_product_page = EditProduct(browser)

    currency_code = 'USD'

    # Fill out product's friendly name and code fields
    unique_id = RandomUtilities.create_unique_id_lowercase()
    product_friendly_name = 'Test UI Create Product {}'.format(unique_id)
    product_code = 'test_ui_create_product_{}'.format(unique_id)
    add_product_page.type_friendly_name_input(product_friendly_name)
    add_product_page.type_code_input(product_code)

    # Add price to Product
    price_amount = '100'
    add_product_page.click_entity_add_button('prices')
    add_price_page.wait_for_page_load()
    add_price_page.click_money_toggle()
    # add_price_page.type_currency_code(currency_code)
    add_price_page.type_amount_input('\b{}'.format(price_amount))
    add_price_page.click_add_button()

    # Validate that the price was added to the product
    add_product_page.wait_for_page_load()
    assert_that(add_product_page.get_prices_list(), has_length(1))
    assert_that(add_product_page.get_prices_toggle(currency_code))
    assert_that(
        add_product_page.get_prices_rm_currency_code(currency_code).text,
        equal_to(currency_code)
    )
    # assert_that(add_product_page.get_prices_pricing_type(currency_code).text, equal_to('LINEAR'))
    assert_that(
        add_product_page.get_prices_amount(currency_code).get_attribute('value'),
        equal_to(price_amount)
    )
    assert_that(add_product_page.get_prices_delete_button(currency_code))

    # Validate that the product was created
    add_product_page.click_save_button()

    notification_page.wait_for_notification_message()
    notification_message = notification_page.get_notification_message()
    assert_that(notification_message.text, equal_to('Product: {} successfully created!'.format(product_code)))

    products_page.wait_for_page_load()
    assert_that(products_page.get_product_by_name(product_code).text, equal_to(product_friendly_name))

    products_page.click_product_button(product_code)
    edit_product_page.wait_for_page_load()

    assert_that(edit_product_page.get_friendly_name_input().get_attribute('value'), equal_to(product_friendly_name))

    assert_that(edit_product_page.get_prices_list(), has_length(1))
    assert_that(edit_product_page.get_prices_toggle(currency_code))
    assert_that(
        edit_product_page.get_prices_rm_currency_code(currency_code).text,
        equal_to(currency_code)
    )
    # assert_that(edit_product_page.get_prices_pricing_type(currency_code).text, equal_to('LINEAR'))
    assert_that(
        edit_product_page.get_prices_amount(currency_code).get_attribute('value'),
        equal_to(price_amount)
    )
    assert_that(edit_product_page.get_prices_delete_button(currency_code))


@pytest.allure.testcase("Validate that exiting add price page will not add a price")
def test_exit_add_prices_page(setup, browser):
    add_product_page, products_page, _, _, _ = setup
    add_price_page = AddPricesToProduct(browser)

    # Fill out product's friendly name and code fields
    unique_id = RandomUtilities.create_unique_id_lowercase()
    product_friendly_name = 'Test UI Create Product {}'.format(unique_id)
    product_code = 'test_ui_create_product_{}'.format(unique_id)
    add_product_page.type_friendly_name_input(product_friendly_name)
    add_product_page.type_code_input(product_code)

    # Open add price to product page
    add_product_page.click_entity_add_button('prices')
    add_price_page.wait_for_page_load()
    add_price_page.click_close_button()

    # Validate that the no price was added to the product
    add_product_page.wait_for_page_load()
    assert_that(add_product_page.get_prices_list(), has_length(0))
