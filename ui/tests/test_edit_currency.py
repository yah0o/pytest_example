import pytest
from hamcrest import assert_that, equal_to, has_length, not_
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from ui.main.constants import FRIENDLY_NAME_INVALID_INPUT, PLATFORM_HEADER_TEXT
from ui.main.helpers import RandomUtilities
from ui.pages import Sidebar, Notification, Header, Currencies, CatalogTabs, EditCurrency


@pytest.allure.step('Validate elements on the edit currency page')
def validate_edit_currency_page(edit_currency_page):
    assert_that(edit_currency_page.get_edit_currency_header().text, equal_to('Edit Currency'))
    assert_that(edit_currency_page.get_info_box().text, equal_to('All required fields are marked with *.'))

    assert_that(edit_currency_page.get_basic_info_header().text, equal_to('BASIC INFORMATION'))
    assert_that(edit_currency_page.get_friendly_name_label().text, equal_to('Friendly Name\n*'))
    assert_that(edit_currency_page.get_friendly_name_input())
    assert_that(edit_currency_page.get_friendly_name_invalid_message())

    assert_that(edit_currency_page.get_active_header().text, equal_to('Active'))
    assert_that(edit_currency_page.get_active_toggle())
    assert_that(edit_currency_page.get_inactive_label().text, equal_to('Inactive'))
    assert_that(edit_currency_page.get_active_label().text, equal_to('Active'))

    assert_that(edit_currency_page.get_tags_header().text, equal_to('Tags'))
    assert_that(edit_currency_page.get_tags_input())

    assert_that(edit_currency_page.get_platform_info_header().text, equal_to('PLATFORM INFORMATION'))
    assert_that(edit_currency_page.get_code_label().text, equal_to('Code\n*'))
    assert_that(edit_currency_page.get_code_input())

    assert_that(edit_currency_page.get_version_label().text, equal_to('Version'))
    assert_that(edit_currency_page.get_version_input())

    assert_that(edit_currency_page.get_currency_settings_header().text, equal_to('CURRENCY SETTINGS'))
    assert_that(edit_currency_page.get_reported_header().text, equal_to('Currency Data in Reports'))
    assert_that(edit_currency_page.get_reported_toggle())
    assert_that(edit_currency_page.get_not_included_label().text, equal_to('Not Included'))
    assert_that(edit_currency_page.get_included_label().text, equal_to('Included'))

    assert_that(edit_currency_page.get_price_precision_label().text, equal_to('Currency Price Precision'))
    assert_that(edit_currency_page.get_price_precision_input())
    assert_that(edit_currency_page.get_price_precision_invalid_message())

    assert_that(edit_currency_page.get_custom_data_header().text, equal_to('CUSTOM DATA'))
    assert_that(edit_currency_page.get_metadata_label().text, equal_to('Metadata'))
    assert_that(edit_currency_page.get_metadata_toggle())
    assert_that(edit_currency_page.get_field_editor_label().text, equal_to('Field Editor'))
    assert_that(edit_currency_page.get_code_editor_label().text, equal_to('Code Editor'))

    assert_that(edit_currency_page.get_save_and_close_button().text, equal_to('Save and Close'))
    assert_that(edit_currency_page.get_save_button().text, equal_to('Save'))
    assert_that(edit_currency_page.get_cancel_button().text, equal_to('Cancel'))


@pytest.allure.step('Validate elements on the edit currency catalog tabs page')
def validate_catalog_tabs_page(catalog_tabs_page, config):
    catalog_title_text = catalog_tabs_page.get_catalog_title()
    assert_that(catalog_title_text.text, equal_to(config.data.TEST_CATALOG.FRIENDLY_NAME))

    assert_that(catalog_tabs_page.get_secondary_heading())

    download_config_button = catalog_tabs_page.get_download_config_button()
    assert_that(download_config_button.text, equal_to('Download Config'))

    # done_button_text = catalog_tabs_page.get_done_button()
    # assert_that(done_button_text.text, equal_to('DONE'))

    publish_button_text = catalog_tabs_page.get_publish_button()
    assert_that(publish_button_text.text, equal_to('Publish'))

    # overview_tab_text = catalog_tabs_page.get_overview_tab()
    # assert_that(overview_tab_text.text, equal_to('Overview'))

    storefronts_tab_text = catalog_tabs_page.get_storefronts_tab()
    assert_that(storefronts_tab_text.text, equal_to('Storefronts'))

    products_tab_text = catalog_tabs_page.get_products_tab()
    assert_that(products_tab_text.text, equal_to('Products'))

    entitlements_tab_text = catalog_tabs_page.get_entitlements_tab()
    assert_that(entitlements_tab_text.text, equal_to('Entitlements'))

    currencies_tab_text = catalog_tabs_page.get_currencies_tab()
    assert_that(currencies_tab_text.text, equal_to('Currencies'))

    # campaigns_tab_text = catalog_tabs_page.get_campaigns_tab()
    # assert_that(campaigns_tab_text.text, equal_to('Campaigns'))
    #
    # activity_tab_text = catalog_tabs_page.get_activity_tab()
    # assert_that(activity_tab_text.text, equal_to('Activity'))

    assert_that(catalog_tabs_page.get_tab_list(), has_length(4))


@pytest.allure.step('Validate elements on the edit currency sidebar page')
def validate_edit_currency_sidebar_page(sidebar_page):
    # assert_that(sidebar_page.get_dashboard_button().text, equal_to('Dashboard'))
    # assert_that(sidebar_page.get_titles_button().text, equal_to('Titles'))
    assert_that(sidebar_page.get_back_to_titles_button().text, equal_to('< Back to Titles'))
    assert_that(sidebar_page.get_catalogs_button().text, equal_to('Catalogs'))
    assert_that(sidebar_page.get_environments_button().text, equal_to('Environments'))
    assert_that(sidebar_page.get_title_components_button().text, equal_to('Components'))
    # assert_that(sidebar_page.get_activity_button().text, equal_to('Activity'))
    # assert_that(sidebar_page.get_users_button().text, equal_to('Users'))
    assert_that(sidebar_page.get_data_button().text, equal_to('Data'))
    assert_that(sidebar_page.get_players_button().text, equal_to('Players'))
    # assert_that(sidebar_page.get_reports_button().text, equal_to('Reports'))
    assert_that(sidebar_page.get_panel(), has_length(6))


@pytest.allure.step('Validate elements on the edit currency header page')
def validate_edit_currency_header_page(header_page):
    assert_that(header_page.get_home_button())

    top_bar_header = header_page.get_top_bar_header()
    assert_that(top_bar_header.text, equal_to(PLATFORM_HEADER_TEXT))

    assert_that(header_page.get_settings_icon())

    assert_that(header_page.get_drop_down_menu())

    assert_that(header_page.get_user_icon())

    assert_that(header_page.get_user_id())

    assert_that(header_page.get_logout_button())


@pytest.fixture
def setup(config, browser, steps):
    edit_currency_page = EditCurrency(browser)
    currencies_page = Currencies(browser)
    catalog_tabs_page = CatalogTabs(browser)
    sidebar_page = Sidebar(browser)
    header_page = Header(browser)

    steps.login(config.admin.username, config.admin.password)
    steps.navigate_to_titles_page(config.data.TEST_STUDIO.CODE)
    steps.navigate_to_catalogs_page(config.data.TEST_TITLE.CODE)
    steps.navigate_to_catalog_tabs_page(config.data.TEST_CATALOG.CODE)
    steps.navigate_to_currencies_page()

    currencies_page.click_currency_button(config.data.TEST_CURRENCY.CODE)
    edit_currency_page.wait_for_page_load()

    yield edit_currency_page, currencies_page, catalog_tabs_page, sidebar_page, header_page


@pytest.fixture
def clean_up(setup, browser, config):
    yield
    edit_currency_page, _, _, _, _ = setup
    notification = Notification(browser)

    edit_currency_page.type_friendly_name_input(config.data.TEST_CURRENCY.FRIENDLY_NAME)
    notification.wait_for_notification_message_to_disappear()
    edit_currency_page.click_save_button()


@pytest.fixture
def toggle_clean_up(setup, browser):
    yield
    edit_currency_page, _, _, _, _ = setup
    notification = Notification(browser)

    if not edit_currency_page.get_active_checkbox().is_selected():
        edit_currency_page.click_active_toggle()
    if not edit_currency_page.get_reported_checkbox().is_selected():
        edit_currency_page.click_reported_toggle()
    notification.wait_for_notification_message_to_disappear()
    edit_currency_page.click_save_button()


@pytest.allure.testcase('Validate edit currency page')
def test_edit_currency_page(setup):
    edit_currency_page, _, _, _, _ = setup
    validate_edit_currency_page(edit_currency_page)


@pytest.allure.testcase("Validate edit currency catalog tabs page")
def test_catalog_tabs_page(setup, config):
    _, _, catalog_tabs_page, _, _ = setup
    validate_catalog_tabs_page(catalog_tabs_page, config)


@pytest.allure.testcase("Validate edit currency sidebar page")
@pytest.mark.xfail(reason='PLAT-6175', raises=NoSuchElementException)
def test_edit_currency_sidebar_page(setup):
    _, _, _, sidebar_page, _ = setup
    validate_edit_currency_sidebar_page(sidebar_page)


@pytest.allure.testcase("Validate edit currency header page")
def test_edit_currency_header_page(setup):
    _, _, _, _, header_page = setup
    validate_edit_currency_header_page(header_page)


@pytest.allure.testcase("Validate can edit an currency through the UI, check it's version and code")
@pytest.mark.xfail(reason='PLAT-6334', raises=TimeoutException)
def test_edit_currency_functions(browser, setup, config, clean_up):
    edit_currency_page, currencies_page, _, _, _ = setup
    notification = Notification(browser)

    # Get the current version of an currency
    version_input = edit_currency_page.get_version_input()
    version_input_value = version_input.get_attribute('value')

    # Edit the currency
    unique_id = RandomUtilities.create_unique_id_lowercase()
    friendly_name = 'Test Currency Edit {}'.format(unique_id)
    edit_currency_page.type_friendly_name_input(friendly_name)
    edit_currency_page.click_save_and_close_button()

    # Get notification
    notification.wait_for_notification_message()
    notification_message = notification.get_notification_message()
    assert_that(
        notification_message.text,
        equal_to('Currency: {} successfully saved!'.format(config.data.TEST_CURRENCY.CODE))
    )

    # Ensure the currency is listed under it's edited name in the currency list
    currencies_page.wait_for_page_load()
    assert_that(
        currencies_page.get_currency_friendly_name_by_name(config.data.TEST_CURRENCY.CODE).text,
        equal_to(friendly_name)
    )

    # Ensure the currency's version is increased by 1, version and input fields are disabled
    currencies_page.click_currency_button(config.data.TEST_CURRENCY.CODE)
    edit_currency_page.wait_for_page_load()

    assert_that(edit_currency_page.get_version_input().is_enabled(), equal_to(False))
    version_input = edit_currency_page.get_version_input()
    version_input_value_updated = version_input.get_attribute('value')
    assert_that(int(version_input_value_updated) - int(version_input_value), equal_to(1))

    assert_that(edit_currency_page.get_code_input().is_enabled(), equal_to(False))
    code_input = edit_currency_page.get_code_input()
    code_input_value = code_input.get_attribute('value')
    assert_that(code_input_value, equal_to(config.data.TEST_CURRENCY.CODE))


@pytest.allure.testcase("Validate edit currency toggles functions")
@pytest.mark.xfail(reason='PLAT-6334', raises=TimeoutException)
def test_edit_currency_toggles(browser, setup, config, toggle_clean_up):
    edit_currency_page, currencies_page, _, _, _ = setup
    notification = Notification(browser)

    # Edit the currency
    edit_currency_page.click_active_toggle()
    edit_currency_page.click_reported_toggle()
    edit_currency_page.click_metadata_toggle()

    assert_that(not_(edit_currency_page.get_active_checkbox().is_selected()))
    assert_that(not_(edit_currency_page.get_reported_checkbox().is_selected()))
    assert_that(edit_currency_page.get_metadata_checkbox().is_selected())

    edit_currency_page.click_save_and_close_button()

    # Get notification
    notification.wait_for_notification_message()
    notification_message = notification.get_notification_message()
    assert_that(
        notification_message.text,
        equal_to('Currency: {} successfully saved!'.format(config.data.TEST_CURRENCY.CODE))
    )

    # Ensure Active and Included reports is false
    currencies_page.wait_for_page_load()
    currencies_page.click_currency_button(config.data.TEST_CURRENCY.CODE)

    edit_currency_page.wait_for_page_load()
    assert_that(not_(edit_currency_page.get_active_checkbox().is_selected()))
    assert_that(not_(edit_currency_page.get_reported_checkbox().is_selected()))
    assert_that(not_(edit_currency_page.get_metadata_checkbox().is_selected()))


@pytest.allure.testcase("Ensure cancel button returns the user to the currencies page")
def test_edit_currency_cancel_button_returns_to_currencies_page(setup):
    edit_currency_page, currencies_page, _, _, _ = setup

    edit_currency_page.click_cancel_button()

    currencies_page.wait_for_page_load()
    assert_that(currencies_page.get_currencies_list())


@pytest.allure.testcase("Ensure currency won't get saved when friendly name is invalid")
@pytest.mark.parametrize('invalid_friendly_name', ['!', '@'])
def test_edit_currency_does_not_save_currency_when_friendly_name_is_invalid(invalid_friendly_name, setup):
    edit_currency_page, _, _, _, _ = setup

    edit_currency_page.type_friendly_name_input(invalid_friendly_name)
    edit_currency_page.wait_for_friendly_name_invalid_message()
    assert_that(edit_currency_page.get_friendly_name_invalid_message().text, equal_to(FRIENDLY_NAME_INVALID_INPUT))

    assert_that(edit_currency_page.get_save_button().is_enabled(), equal_to(False))


@pytest.allure.testcase("Ensure currency cannot be saved when friendly name is blank")
def test_edit_currency_does_not_accept_blank_friendly_name(setup):
    edit_currency_page, _, _, _, _ = setup

    edit_currency_page.type_friendly_name_input(' ')
    assert_that(not_(edit_currency_page.get_save_button().is_enabled()))


@pytest.allure.testcase("Ensure currency cannot be saved with empty friendly name")
def test_edit_currency_does_not_save_currency_when_empty_friendly_name(setup):
    edit_currency_page, _, _, _, _ = setup

    friendly_name = edit_currency_page.get_friendly_name_input()
    friendly_name.clear()
    friendly_name.send_keys(' \b')
    assert_that(not_(edit_currency_page.get_save_button().is_enabled()))


@pytest.allure.testcase("Ensure currency cannot be saved with invalid price precision")
@pytest.mark.parametrize('invalid_price_precision', ['-1', 'abc'])
def test_edit_currency_does_not_save_currency_when_price_precision_is_invalid(setup, invalid_price_precision):
    edit_currency_page, _, _, _, _ = setup

    price_precision = edit_currency_page.get_price_precision_input()
    price_precision.clear()
    price_precision.send_keys(invalid_price_precision)

    assert_that(
        edit_currency_page.get_price_precision_invalid_message().text,
        equal_to('Please input a positive number value.')
    )

    assert_that(not_(edit_currency_page.get_save_button().is_enabled()))
