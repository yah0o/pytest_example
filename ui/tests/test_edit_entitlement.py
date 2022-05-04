import time

import pytest

from hamcrest import assert_that, equal_to, has_length, not_
from selenium.common.exceptions import TimeoutException

from ui.main.helpers import RandomUtilities
from ui.pages import Sidebar, Notification, Header, Entitlements, CatalogTabs, EditEntitlement
from ui.main.constants import FRIENDLY_NAME_INVALID_INPUT, PLATFORM_HEADER_TEXT


@pytest.allure.step('Validate elements on the edit entitlement page')
def validate_page(edit_entitlement_page):
    assert_that(edit_entitlement_page.get_edit_entitlement_header().text, equal_to('Edit Entitlement'))

    assert_that(edit_entitlement_page.get_friendly_name_label().text, equal_to('Friendly Name\n*'))
    assert_that(edit_entitlement_page.get_friendly_name_input())

    assert_that(edit_entitlement_page.get_code_label().text, equal_to('Code\n*'))
    assert_that(edit_entitlement_page.get_code_input())

    assert_that(edit_entitlement_page.get_version_label().text, equal_to('Version'))
    assert_that(edit_entitlement_page.get_version_input())

    assert_that(edit_entitlement_page.get_active_header().text, equal_to('Active'))
    assert_that(edit_entitlement_page.get_active_toggle())
    assert_that(edit_entitlement_page.get_active_checkbox())
    assert_that(edit_entitlement_page.get_inactive_label().text, equal_to('Inactive'))
    assert_that(edit_entitlement_page.get_active_label().text, equal_to('Active'))

    assert_that(edit_entitlement_page.get_metadata_header().text, equal_to('Metadata'))
    assert_that(edit_entitlement_page.get_metadata_toggle())
    assert_that(edit_entitlement_page.get_metadata_checkbox())
    assert_that(edit_entitlement_page.get_metadata_field_editor_label().text, equal_to('Field Editor'))
    assert_that(edit_entitlement_page.get_metadata_code_editor_label().text, equal_to('Code Editor'))

    assert_that(edit_entitlement_page.get_tags_header().text, equal_to('Tags'))
    assert_that(edit_entitlement_page.get_tags_input())
    # assert_that(edit_entitlement_page.get_tags_drop_down_arrow())

    assert_that(edit_entitlement_page.get_save_and_close_button().text, equal_to('Save and Close'))
    assert_that(edit_entitlement_page.get_save_button().text, equal_to('Save'))
    assert_that(edit_entitlement_page.get_cancel_button().text, equal_to('Cancel'))


@pytest.allure.step('Validate elements on the edit entitlement catalog tabs page')
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


@pytest.allure.step('Validate elements on the edit entitlement sidebar page')
def validate_edit_entitlement_sidebar_page(sidebar_page):
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


@pytest.allure.step('Validate elements on the edit entitlement header page')
def validate_edit_entitlement_header_page(header_page):
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
    edit_entitlement_page = EditEntitlement(browser)
    entitlements_page = Entitlements(browser)
    catalog_tabs_page = CatalogTabs(browser)
    sidebar_page = Sidebar(browser)
    header_page = Header(browser)

    steps.login(config.admin.username, config.admin.password)
    steps.navigate_to_titles_page(config.data.TEST_STUDIO.CODE)
    steps.navigate_to_catalogs_page(config.data.TEST_TITLE.CODE)
    steps.navigate_to_catalog_tabs_page(config.data.TEST_CATALOG.CODE)
    steps.navigate_to_entitlements_page()

    entitlements_page.click_entitlement_by_name(config.data.TEST_ENTITLEMENT.CODE)
    edit_entitlement_page.wait_for_page_load()

    yield edit_entitlement_page, entitlements_page, catalog_tabs_page, sidebar_page, header_page


@pytest.fixture
def clean_up(setup, browser, config):
    yield
    edit_entitlement_page, entitlements_page, _, _, _ = setup
    notification = Notification(browser)

    edit_entitlement_page.type_friendly_name_input(config.data.TEST_ENTITLEMENT.FRIENDLY_NAME)
    notification.wait_for_notification_message_to_disappear()
    edit_entitlement_page.click_save_and_close_button()


@pytest.fixture
def toggle_clean_up(setup, browser):
    yield
    edit_entitlement_page, entitlements_page, _, _, _ = setup
    notification = Notification(browser)

    # Test clean up
    if not edit_entitlement_page.get_active_checkbox().is_selected():
        edit_entitlement_page.click_active_toggle()
    notification.wait_for_notification_message_to_disappear()
    edit_entitlement_page.click_save_and_close_button()


@pytest.allure.testcase("Validate edit entitlement page")
def test_edit_entitlement_page(setup):
    edit_entitlement_page, _, _, _, _ = setup
    validate_page(edit_entitlement_page)


@pytest.allure.testcase("Validate edit entitlement catalog tabs page")
def test_catalog_tabs_page(setup, config):
    _, _, catalog_tabs_page, _, _ = setup
    validate_catalog_tabs_page(catalog_tabs_page, config)


@pytest.allure.testcase("Validate edit entitlement sidebar page")
def test_edit_entitlement_sidebar_page(setup):
    _, _, _, sidebar_page, _ = setup
    validate_edit_entitlement_sidebar_page(sidebar_page)


@pytest.allure.testcase("Validate edit entitlement header page")
def test_edit_entitlement_header_page(setup):
    _, _, _, _, header_page = setup
    validate_edit_entitlement_header_page(header_page)


@pytest.allure.testcase("Validate can edit an entitlement through the UI, check it's version and code")
@pytest.mark.xfail(reason='PLAT-6334', raises=TimeoutException)
def test_edit_entitlement_functions(browser, setup, config, clean_up):
    edit_entitlement_page, entitlements_page, _, _, _ = setup
    notification = Notification(browser)

    # Get the current version of an entitlement
    version_input = edit_entitlement_page.get_version_input()
    version_input_value = version_input.get_attribute('value')

    # Edit the entitlement
    unique_id = RandomUtilities.create_unique_id_lowercase()
    friendly_name = 'Test Entitlement Edit {}'.format(unique_id)
    edit_entitlement_page.type_friendly_name_input(friendly_name)
    edit_entitlement_page.click_save_close_button()

    # Get notification
    notification.wait_for_notification_message()
    notification_message = notification.get_notification_message()
    assert_that(notification_message.text,
                equal_to('Entitlement: {} successfully saved!'.format(config.data.TEST_ENTITLEMENT.CODE)))

    # Ensure the entitlement is listed under it's edited name in the entitlement list
    entitlements_page.wait_for_page_load()
    assert_that(entitlements_page.get_entitlement_by_name(config.data.TEST_ENTITLEMENT.CODE).text,
                equal_to(friendly_name))

    # Ensure the entitlement's version is increased by 1, version and input fields are disabled
    entitlements_page.click_entitlement_by_name(config.data.TEST_ENTITLEMENT.CODE)
    edit_entitlement_page.wait_for_page_load()

    assert_that(edit_entitlement_page.get_version_input().is_enabled(), equal_to(False))
    version_input = edit_entitlement_page.get_version_input()
    version_input_value_updated = version_input.get_attribute('value')
    assert_that(int(version_input_value_updated) - int(version_input_value), equal_to(1))

    assert_that(edit_entitlement_page.get_code_input().is_enabled(), equal_to(False))
    code_input = edit_entitlement_page.get_code_input()
    code_input_value = code_input.get_attribute('value')
    assert_that(code_input_value, equal_to(config.data.TEST_ENTITLEMENT.CODE))

    # Test clean up
    edit_entitlement_page.type_friendly_name_input(config.data.TEST_ENTITLEMENT.FRIENDLY_NAME)
    notification.wait_for_notification_message_to_disappear()
    edit_entitlement_page.click_save_button()


@pytest.allure.testcase("Validate Edit Entitlement toggles functions")
@pytest.mark.xfail(reason='PLAT-6334', raises=TimeoutException)
def test_edit_entitlement_toggles(browser, setup, config, toggle_clean_up):
    edit_entitlement_page, entitlements_page, _, _, _ = setup
    notification = Notification(browser)

    # Edit the entitlement
    edit_entitlement_page.click_active_toggle()
    edit_entitlement_page.click_metadata_toggle()

    assert_that(not_(edit_entitlement_page.get_active_checkbox().is_selected()))
    assert_that(edit_entitlement_page.get_metadata_checkbox().is_selected())
    edit_entitlement_page.click_save_and_close_button()

    # Get notification
    notification.wait_for_notification_message()
    notification_message = notification.get_notification_message()
    assert_that(
        notification_message.text,
        equal_to('Entitlement: {} successfully saved!'.format(config.data.TEST_ENTITLEMENT.CODE))
    )

    entitlements_page.wait_for_page_load()
    entitlements_page.click_entitlement_by_name(config.data.TEST_ENTITLEMENT.CODE)
    edit_entitlement_page.wait_for_page_load()

    # Ensure that active is still false
    assert_that(not_(edit_entitlement_page.get_active_toggle().is_selected()))
    assert_that(not_(edit_entitlement_page.get_metadata_checkbox().is_selected()))


@pytest.allure.testcase("Ensure cancel button returns the user to the entitlements page")
def test_edit_entitlement_cancel_button_returns_to_entitlements_page(setup):
    edit_entitlement_page, entitlements_page, _, _, _ = setup

    edit_entitlement_page.click_cancel_button()

    entitlements_page.wait_for_page_load()
    assert_that(entitlements_page.get_entitlements_list())


@pytest.allure.testcase("Ensure entitlement won't get saved when friendly name is invalid")
@pytest.mark.parametrize('invalid_friendly_name', ['!', '@'])
def test_edit_entitlement_does_not_save_entitlement_when_friendly_name_is_invalid(invalid_friendly_name, setup):
    edit_entitlement_page, _, _, _, _ = setup

    edit_entitlement_page.type_friendly_name_input(invalid_friendly_name)
    edit_entitlement_page.wait_for_friendly_name_invalid_message()
    assert_that(edit_entitlement_page.get_friendly_name_invalid_message().text, equal_to(FRIENDLY_NAME_INVALID_INPUT))

    assert_that(edit_entitlement_page.get_save_button().is_enabled(), equal_to(False))


@pytest.allure.testcase("Ensure entitlement cannot be saved when friendly name is blank")
def test_edit_entitlement_does_not_accept_blank_friendly_name(setup):
    edit_entitlement_page, _, _, _, _ = setup

    edit_entitlement_page.type_friendly_name_input(' ')
    assert_that(edit_entitlement_page.get_save_button().is_enabled(), equal_to(False))


@pytest.allure.testcase("Ensure entitlement cannot be saved with empty friendly name")
def test_edit_entitlement_does_not_save_entitlement_when_empty_friendly_name(setup):
    edit_entitlement_page, _, _, _, _ = setup

    friendly_name = edit_entitlement_page.get_friendly_name_input()
    friendly_name.clear()
    friendly_name.send_keys(' \b')
    assert_that(edit_entitlement_page.get_save_button().is_enabled(), equal_to(False))
