import pytest

from hamcrest import assert_that, equal_to, has_length, greater_than_or_equal_to, not_
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from ui.main.constants import FRIENDLY_NAME_INVALID_INPUT, PLATFORM_HEADER_TEXT
from ui.main.helpers import RandomUtilities
from ui.pages import Sidebar, Notification, Header, CatalogTabs, Products, AddEntityToEntity, EditProduct, \
    AddPricesToProduct


@pytest.allure.step('Validate elements on the edit product page')
def validate_page(edit_product_page, config):
    assert_that(edit_product_page.get_edit_product_header().text, equal_to('Edit Product'))

    assert_that(edit_product_page.get_friendly_name_label().text, equal_to('Friendly Name\n*'))
    assert_that(edit_product_page.get_friendly_name_input())

    assert_that(edit_product_page.get_code_label().text, equal_to('Code\n*'))
    assert_that(edit_product_page.get_code_input())

    assert_that(edit_product_page.get_version_label().text, equal_to('Version'))
    assert_that(edit_product_page.get_version_input())

    assert_that(edit_product_page.get_active_header().text, equal_to('Active'))
    assert_that(edit_product_page.get_active_toggle())

    assert_that(edit_product_page.get_metadata_header().text, equal_to('Metadata'))
    assert_that(edit_product_page.get_metadata_toggle())
    assert_that(edit_product_page.get_metadata_checkbox())
    assert_that(edit_product_page.get_metadata_field_editor_label().text, equal_to('Field Editor'))
    assert_that(edit_product_page.get_metadata_code_editor_label().text, equal_to('Code Editor'))

    assert_that(edit_product_page.get_tags_header().text, equal_to('Tags'))
    assert_that(edit_product_page.get_tags_input())
    # assert_that(edit_product_page.get_tags_drop_down_arrow())

    assert_that(edit_product_page.get_entity_heading('currencies').text, equal_to('Currencies'))
    assert_that(edit_product_page.get_entity_add_button('currencies').text, equal_to('Add'))
    assert_that(edit_product_page.get_entity_table_code_column('currencies').text, equal_to('Code'))
    assert_that(edit_product_page.get_entity_table_amount_column('currencies').text, equal_to('Amount'))
    assert_that(edit_product_page.get_entity_table_pct_value_column('currencies').text, equal_to('Percentage Value'))
    assert_that(edit_product_page.get_entity_by_name(config.data.TEST_CURRENCY.CODE))
    assert_that(edit_product_page.get_entity_list('currencies'), greater_than_or_equal_to(1))
    assert_that(edit_product_page.get_entity_amount_input(config.data.TEST_CURRENCY.CODE))
    assert_that(edit_product_page.get_entity_pct_value_input(config.data.TEST_CURRENCY.CODE))
    assert_that(edit_product_page.get_entity_remove_button(config.data.TEST_CURRENCY.CODE))

    assert_that(edit_product_page.get_entity_heading('entitlements').text, equal_to('Entitlements'))
    assert_that(edit_product_page.get_entity_add_button('entitlements').text, equal_to('Add'))
    assert_that(edit_product_page.get_entity_table_code_column('entitlements').text, equal_to('Code'))
    assert_that(edit_product_page.get_entity_table_amount_column('entitlements').text, equal_to('Amount'))
    assert_that(edit_product_page.get_entity_table_pct_value_column('entitlements').text, equal_to('Percentage Value'))
    assert_that(edit_product_page.get_entity_by_name(config.data.TEST_ENTITLEMENT.CODE))
    assert_that(edit_product_page.get_entity_list('entitlements'), greater_than_or_equal_to(1))
    assert_that(edit_product_page.get_entity_amount_input(config.data.TEST_ENTITLEMENT.CODE))
    assert_that(edit_product_page.get_entity_pct_value_input(config.data.TEST_ENTITLEMENT.CODE))
    assert_that(edit_product_page.get_entity_remove_button(config.data.TEST_ENTITLEMENT.CODE))

    assert_that(edit_product_page.get_entity_heading('prices').text, equal_to('Prices'))
    assert_that(edit_product_page.get_entity_add_button('prices').text, equal_to('Add'))

    assert_that(edit_product_page.get_entity_heading('prerequisites').text, equal_to('Prerequisites'))
    assert_that(edit_product_page.get_entity_add_button('prerequisites').text, equal_to('Add'))

    # assert_that(edit_product_page.get_name_header().text, equal_to('Name'))
    # assert_that(edit_product_page.get_name_key_label().text, equal_to('Key:'))
    # assert_that(edit_product_page.get_name_key_input())
    # assert_that(edit_product_page.get_name_value_label().text, equal_to('Value:'))
    # assert_that(edit_product_page.get_name_value_input())
    # assert_that(edit_product_page.get_name_add_button().text, equal_to('ADD'))
    #
    # assert_that(edit_product_page.get_description_header().text, equal_to('Description'))
    # assert_that(edit_product_page.get_description_key_label().text, equal_to('Key:'))
    # assert_that(edit_product_page.get_description_key_input())
    # assert_that(edit_product_page.get_description_value_label().text, equal_to('Value:'))
    # assert_that(edit_product_page.get_description_value_input())
    # assert_that(edit_product_page.get_description_add_button().text, equal_to('ADD'))

    assert_that(edit_product_page.get_purchasable_left().text, equal_to('Not purchasable'))
    assert_that(edit_product_page.get_purchasable_right().text, equal_to('Purchasable'))
    assert_that(edit_product_page.get_purchasable_toggle())

    assert_that(edit_product_page.get_visible_left().text, equal_to('Invisible'))
    assert_that(edit_product_page.get_visible_right().text, equal_to('Visible'))
    assert_that(edit_product_page.get_visible_toggle())

    assert_that(edit_product_page.get_restricted_countries_header().text, equal_to('Restricted Countries'))
    assert_that(edit_product_page.get_restricted_countries_input())
    # assert_that(edit_product_page.get_restricted_countries_drop_down_arrow())

    # assert_that(edit_product_page.get_spa_access_header().text, equal_to('SPA Access'))
    # assert_that(edit_product_page.get_spa_access_input())
    # assert_that(edit_product_page.get_spa_access_drop_down_arrow())

    assert_that(edit_product_page.get_prices_list(), greater_than_or_equal_to(1))
    assert_that(edit_product_page.get_prices_rm_header().text, equal_to('Real Money'))
    assert_that(edit_product_page.get_prices_currency_code_header().text, equal_to('Currency Code'))
    assert_that(edit_product_page.get_prices_amount_header().text, equal_to('Amount'))

    assert_that(edit_product_page.get_save_and_close_button().text, equal_to('Save and Close'))
    assert_that(edit_product_page.get_save_button().text, equal_to('Save'))
    assert_that(edit_product_page.get_cancel_button().text, equal_to('Cancel'))


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


@pytest.allure.step('Validate elements on the edit product sidebar page')
def validate_edit_product_sidebar_page(sidebar_page):
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


@pytest.allure.step('Validate elements on the edit product header page')
def validate_edit_product_header_page(header_page):
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
    edit_product_page = EditProduct(browser)
    products_page = Products(browser)
    catalog_tabs_page = CatalogTabs(browser)
    sidebar_page = Sidebar(browser)
    header_page = Header(browser)

    steps.login(config.admin.username, config.admin.password)
    steps.navigate_to_titles_page(config.data.TEST_STUDIO.CODE)
    steps.navigate_to_catalogs_page(config.data.TEST_TITLE.CODE)
    steps.navigate_to_catalog_tabs_page(config.data.TEST_CATALOG.CODE)
    steps.navigate_to_products_tab()

    products_page.click_product_button(config.data.TEST_PRODUCT_FULL.CODE)
    edit_product_page.wait_for_page_load()

    yield edit_product_page, products_page, catalog_tabs_page, sidebar_page, header_page


@pytest.fixture
def clean_up(setup, browser, config):
    yield
    edit_product_page, _, _, _, _ = setup
    notification = Notification(browser)

    edit_product_page.type_friendly_name_input(config.data.TEST_PRODUCT_FULL.FRIENDLY_NAME)
    notification.wait_for_notification_message_to_disappear()
    edit_product_page.click_save_and_close_button()

@pytest.fixture
def toggle_clean_up(setup, browser, config):
    yield
    edit_product_page, _, _, _, _ = setup
    notification = Notification(browser)

    if not edit_product_page.get_active_checkbox().is_selected():
        edit_product_page.click_active_toggle()

    if not edit_product_page.get_purchasable_checkbox().is_selected():
        edit_product_page.click_purchasable_toggle()

    if not edit_product_page.get_visible_checkbox().is_selected():
        edit_product_page.click_visible_toggle()

    notification.wait_for_notification_message_to_disappear()
    edit_product_page.click_save_and_close_button()

@pytest.fixture
def add_vc_price_clean_up(setup, browser, config):
    yield
    edit_product_page, _, _, _, _ = setup
    notification = Notification(browser)

    edit_product_page.click_prices_delete_button(config.data.XP.CODE)

    notification.wait_for_notification_message_to_disappear()
    edit_product_page.click_save_and_close_button()


@pytest.fixture
def add_rm_price_clean_up(setup, browser):
    yield
    edit_product_page, _, _, _, _ = setup
    notification = Notification(browser)
    edit_product_page.click_prices_delete_button('USD')

    notification.wait_for_notification_message_to_disappear()
    edit_product_page.click_save_and_close_button()


@pytest.allure.testcase("Validate edit product page")
def test_edit_product_page(setup, config):
    edit_product_page, _, _, _, _ = setup
    validate_page(edit_product_page, config)


@pytest.allure.testcase("Validate catalog tabs page")
def test_catalog_tabs_page(setup, config):
    _, _, catalog_tabs_page, _, _ = setup
    validate_catalog_tabs_page(catalog_tabs_page, config)


@pytest.allure.testcase("Validate edit product sidebar")
def test_edit_product_sidebar_page(setup):
    _, _, _, sidebar_page, _ = setup
    validate_edit_product_sidebar_page(sidebar_page)


@pytest.allure.testcase("Validate edit product header page")
def test_edit_product_header_page(setup):
    _, _, _, _, header_page = setup
    validate_edit_product_header_page(header_page)


@pytest.allure.testcase("Validate can edit a product through the UI, check it's version and code")
def test_edit_product_functions(browser, setup, config, clean_up):
    edit_product_page, products_page, _, _, _ = setup
    notification = Notification(browser)

    # Get the current version of a product
    version_input = edit_product_page.get_version_input()
    version_input_value = version_input.get_attribute('value')

    # Edit and save the product
    unique_id = RandomUtilities.create_unique_id_lowercase()
    friendly_name = 'Test Product Edit {}'.format(unique_id)
    edit_product_page.type_friendly_name_input(friendly_name)
    edit_product_page.click_save_and_close_button()

    # Get notification
    notification.wait_for_notification_message()
    notification_message = notification.get_notification_message()
    assert_that(notification_message.text,
                equal_to('Product: {} successfully saved!'.format(config.data.TEST_PRODUCT_FULL.CODE)))

    # Ensure the product is listed under it's edited name in the product list
    products_page.wait_for_page_load()
    assert_that(products_page.get_product_by_name(config.data.TEST_PRODUCT_FULL.CODE).text,
                equal_to(friendly_name))

    # Ensure the product's version is increased by 1, version and code input fields are disabled
    products_page.click_product_button(config.data.TEST_PRODUCT_FULL.CODE)
    edit_product_page.wait_for_page_load()

    assert_that(edit_product_page.get_version_input().is_enabled(), equal_to(False))
    version_input = edit_product_page.get_version_input()
    version_input_value_updated = version_input.get_attribute('value')
    assert_that(int(version_input_value_updated) - int(version_input_value), equal_to(1))

    assert_that(edit_product_page.get_code_input().is_enabled(), equal_to(False))
    code_input = edit_product_page.get_code_input()
    code_input_value = code_input.get_attribute('value')
    assert_that(code_input_value, equal_to(config.data.TEST_PRODUCT_FULL.CODE))


@pytest.mark.xfail(reason='PLAT-6334', raises=TimeoutException)
@pytest.allure.testcase("Validate Add Product toggles functions")
def test_edit_product_toggles(browser, setup, config, toggle_clean_up):
    edit_product_page, products_page, _, _, _ = setup
    notification = Notification(browser)

    # Edit and save the product
    edit_product_page.click_active_toggle()
    edit_product_page.click_metadata_toggle()
    edit_product_page.click_purchasable_toggle()
    edit_product_page.click_visible_toggle()

    assert_that(not_(edit_product_page.get_active_checkbox().is_selected()))
    assert_that(edit_product_page.get_metadata_checkbox().is_selected())
    assert_that(not_(edit_product_page.get_purchasable_checkbox().is_selected()))
    assert_that(not_(edit_product_page.get_visible_checkbox().is_selected()))

    edit_product_page.click_save_and_close_button()

    # Get notification
    notification.wait_for_notification_message()
    notification_message = notification.get_notification_message()
    assert_that(
        notification_message.text,
        equal_to('Product: {} successfully saved!'.format(config.data.TEST_PRODUCT_FULL.CODE))
    )

    # Ensure the product's active, purchasable, and visible are is still false
    products_page.wait_for_page_load()
    products_page.click_product_button(config.data.TEST_PRODUCT_FULL.CODE)
    edit_product_page.wait_for_page_load()

    assert_that(not_(edit_product_page.get_active_checkbox().is_selected()))
    assert_that(not_(edit_product_page.get_metadata_checkbox().is_selected()))
    assert_that(not_(edit_product_page.get_purchasable_checkbox().is_selected()))
    assert_that(not_(edit_product_page.get_visible_checkbox().is_selected()))


@pytest.allure.testcase("Ensure cancel button returns the user to the products page")
def test_edit_product_cancel_button_returns_to_products_page(setup):
    edit_product_page, products_page, _, _, _ = setup

    edit_product_page.click_cancel_button()

    products_page.wait_for_page_load()
    assert_that(products_page.get_products_list())


@pytest.allure.testcase("Ensure product won't get saved when friendly name is invalid")
@pytest.mark.parametrize('invalid_friendly_name', ['!', '@'])
def test_edit_product_does_not_save_product_when_friendly_name_is_invalid(invalid_friendly_name, setup):
    edit_product_page, _, _, _, _ = setup

    edit_product_page.type_friendly_name_input(invalid_friendly_name)
    edit_product_page.wait_for_friendly_name_invalid_message()
    assert_that(edit_product_page.get_friendly_name_invalid_message().text, equal_to(FRIENDLY_NAME_INVALID_INPUT))

    assert_that(edit_product_page.get_save_and_close_button().is_enabled(), equal_to(False))
    assert_that(edit_product_page.get_save_button().is_enabled(), equal_to(False))


@pytest.allure.testcase("Ensure product cannot be saved when friendly name is blank")
def test_edit_product_does_not_accept_blank_friendly_name(setup):
    edit_product_page, _, _, _, _ = setup

    edit_product_page.type_friendly_name_input(' ')
    assert_that(edit_product_page.get_save_and_close_button().is_enabled(), equal_to(False))
    assert_that(edit_product_page.get_save_button().is_enabled(), equal_to(False))


@pytest.allure.testcase("Ensure product cannot be saved with empty friendly name")
def test_edit_product_does_not_save_product_when_empty_friendly_name(setup):
    edit_product_page, _, _, _, _ = setup

    friendly_name = edit_product_page.get_friendly_name_input()
    friendly_name.clear()
    friendly_name.send_keys(' \b')
    assert_that(edit_product_page.get_save_and_close_button().is_enabled(), equal_to(False))
    assert_that(edit_product_page.get_save_button().is_enabled(), equal_to(False))


@pytest.mark.xfail(reason='PLAT-6334', raises=TimeoutException)
@pytest.allure.testcase("Validate currency and entitlement can be removed from the product")
def test_edit_product_can_remove_currency_and_entitlement_from_product(setup, browser, config):
    edit_product_page, products_page, _, _, _ = setup
    add_entity_to_entity_page = AddEntityToEntity(browser)
    notification = Notification(browser)

    edit_product_page.click_entity_add_button('currencies')
    add_entity_to_entity_page.wait_for_page_load('currencies')
    add_entity_to_entity_page.click_entity_plus_button(config.data.XP.CODE)
    add_entity_to_entity_page.click_close_button()
    assert_that(edit_product_page.get_entity_by_name(config.data.XP.CODE).text,
                equal_to(config.data.XP.CODE))
    assert_that(edit_product_page.get_entity_list('currencies'), equal_to(2))

    edit_product_page.click_entity_add_button('entitlements')
    add_entity_to_entity_page.wait_for_page_load('entitlements')
    add_entity_to_entity_page.click_entity_checkbox(config.data.TEST_ENTITLEMENT_2.CODE)
    add_entity_to_entity_page.click_add_button()
    assert_that(edit_product_page.get_entity_by_name(config.data.TEST_ENTITLEMENT_2.CODE))
    assert_that(edit_product_page.get_entity_list('entitlements'), has_length(2))

    edit_product_page.click_save_and_close_button()

    notification.wait_for_notification_message()
    assert_that(notification.get_notification_message().text,
                equal_to('Product: {} successfully saved!'.format(config.data.TEST_PRODUCT_FULL.CODE)))

    products_page.wait_for_page_load()

    products_page.click_product_button(config.data.TEST_PRODUCT_FULL.CODE)
    edit_product_page.wait_for_page_load()

    edit_product_page.click_entity_remove_button(config.data.XP.CODE)
    assert_that(edit_product_page.get_entity_list('currencies'), has_length(1))

    edit_product_page.click_entity_remove_button(config.data.TEST_ENTITLEMENT_2.CODE)
    assert_that(edit_product_page.get_entity_list('entitlements'), has_length(1))

    edit_product_page.click_save_and_close_button()

    notification.wait_for_notification_message()
    assert_that(notification.get_notification_message().text,
                equal_to('Product: {} successfully saved!'.format(config.data.TEST_PRODUCT_FULL.CODE)))

    products_page.wait_for_page_load()
    products_page.click_product_button(config.data.TEST_PRODUCT_FULL.CODE)
    edit_product_page.wait_for_page_load()
    assert_that(edit_product_page.get_entity_list('currencies'), has_length(1))
    assert_that(edit_product_page.get_entity_list('entitlements'), has_length(1))


@pytest.mark.xfail(reason='PLAT-6234, PLAT-6255, PLAT-6334', raises=TimeoutException)
@pytest.allure.testcase("Validate vc price can be removed from a product")
def test_edit_product_can_add_vc_price_from_product(setup, browser, config, add_vc_price_clean_up):
    edit_product_page, products_page, _, _, _ = setup
    add_price_page = AddPricesToProduct(browser)
    notification = Notification(browser)

    price_amount = '10'
    edit_product_page.click_entity_add_button('prices')
    add_price_page.wait_for_page_load()
    add_price_page.click_currency_code_drop_down()
    add_price_page.wait_for_drop_down_option_load(config.data.XP.CODE)
    add_price_page.click_drop_down_option_by_name(config.data.XP.CODE)
    add_price_page.type_amount_input('\b{}'.format(price_amount))
    add_price_page.click_add_button()

    edit_product_page.wait_for_page_load()
    assert_that(edit_product_page.get_prices_list(), has_length(2))
    assert_that(edit_product_page.get_prices_toggle(config.data.XP.CODE))
    assert_that(
        edit_product_page.get_prices_vc_currency_code(config.data.XP.CODE).text,
        equal_to(config.data.XP.CODE)
    )
    # assert_that(edit_product_page.get_prices_pricing_type(config.data.XP.CODE).text, equal_to('LINEAR'))
    assert_that(
        edit_product_page.get_prices_amount(config.data.XP.CODE).get_attribute('value'),
        equal_to(price_amount)
    )
    assert_that(edit_product_page.get_prices_delete_button(config.data.XP.CODE))

    edit_product_page.click_save_and_close_button()

    notification.wait_for_notification_message()
    notification_message = notification.get_notification_message()
    assert_that(
        notification_message.text,
        equal_to('Product: {} successfully saved!'.format(config.data.TEST_PRODUCT_FULL.CODE))
    )

    products_page.wait_for_page_load()

    products_page.click_product_button(config.data.TEST_PRODUCT_FULL.CODE)
    edit_product_page.wait_for_page_load()

    assert_that(edit_product_page.get_prices_list(), has_length(2))
    assert_that(edit_product_page.get_prices_toggle(config.data.XP.CODE))
    assert_that(
        edit_product_page.get_prices_vc_currency_code(config.data.XP.CODE).text,
        equal_to(config.data.XP.CODE)
    )
    # assert_that(edit_product_page.get_prices_pricing_type(config.data.XP.CODE).text, equal_to('LINEAR'))
    assert_that(
        edit_product_page.get_prices_amount(config.data.XP.CODE).get_attribute('value'),
        equal_to(price_amount)
    )
    assert_that(edit_product_page.get_prices_delete_button(config.data.XP.CODE))


@pytest.mark.xfail(reason='PLAT-6234, PLAT-6255, PLAT-6334', raises=TimeoutException)
@pytest.allure.testcase("Validate rm price can be removed from a product")
def test_edit_product_can_add_rm_price_from_product(setup, browser, config, add_rm_price_clean_up):
    edit_product_page, products_page, _, _, _ = setup
    add_price_page = AddPricesToProduct(browser)
    notification = Notification(browser)

    currency_code = 'USD'
    price_amount = '10'
    edit_product_page.click_entity_add_button('prices')
    add_price_page.wait_for_page_load()
    add_price_page.click_money_toggle()
    add_price_page.type_amount_input('\b{}'.format(price_amount))
    add_price_page.click_add_button()

    edit_product_page.wait_for_page_load()
    assert_that(edit_product_page.get_prices_list(), has_length(2))
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

    edit_product_page.click_save_and_close_button()

    notification.wait_for_notification_message()
    notification_message = notification.get_notification_message()
    assert_that(
        notification_message.text,
        equal_to('Product: {} successfully saved!'.format(config.data.TEST_PRODUCT_FULL.CODE))
    )

    products_page.wait_for_page_load()

    products_page.click_product_button(config.data.TEST_PRODUCT_FULL.CODE)
    edit_product_page.wait_for_page_load()

    assert_that(edit_product_page.get_prices_list(), has_length(2))
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


@pytest.allure.testcase("Validate exiting add prices page does not add a price to product")
def test_exit_add_prices_page(setup, browser):
    edit_product_page, products_page, _, _, _ = setup
    add_price_page = AddPricesToProduct(browser)

    edit_product_page.click_entity_add_button('prices')
    add_price_page.wait_for_page_load()
    add_price_page.click_close_button()

    edit_product_page.wait_for_page_load()
    assert_that(edit_product_page.get_prices_list(), has_length(1))
