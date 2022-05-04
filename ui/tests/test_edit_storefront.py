import pytest

from selenium.common.exceptions import TimeoutException
from hamcrest import assert_that, equal_to, has_length, greater_than_or_equal_to, not_

from ui.main.helpers import RandomUtilities
from ui.pages import Sidebar, Notification, Header, Storefronts, CatalogTabs, EditStorefront, AddEntityToEntity
from ui.main.constants import FRIENDLY_NAME_INVALID_INPUT, PLATFORM_HEADER_TEXT


@pytest.allure.step('Validate elements on the edit storefront page')
def validate_page(edit_storefront_page, config):
    assert_that(edit_storefront_page.get_edit_storefront_header().text, equal_to('Edit Storefront'))

    assert_that(edit_storefront_page.get_friendly_name_label().text, equal_to('Friendly Name'))
    assert_that(edit_storefront_page.get_friendly_name_input())

    assert_that(edit_storefront_page.get_code_label().text, equal_to('Code'))
    assert_that(edit_storefront_page.get_code_input())

    assert_that(edit_storefront_page.get_version_label().text, equal_to('Version'))
    assert_that(edit_storefront_page.get_version_input())

    assert_that(edit_storefront_page.get_active_header().text, equal_to('Active'))
    assert_that(edit_storefront_page.get_active_toggle())

    assert_that(edit_storefront_page.get_metadata_header().text, equal_to('Metadata'))
    assert_that(edit_storefront_page.get_metadata_toggle())
    assert_that(edit_storefront_page.get_metadata_checkbox())
    assert_that(edit_storefront_page.get_metadata_field_editor_label().text, equal_to('Field Editor'))
    assert_that(edit_storefront_page.get_metadata_code_editor_label().text, equal_to('Code Editor'))

    assert_that(edit_storefront_page.get_tags_header().text, equal_to('Tags'))
    assert_that(edit_storefront_page.get_tags_input())
    # assert_that(edit_storefront_page.get_tags_drop_down_arrow())

    assert_that(edit_storefront_page.get_products_header().text, equal_to('Products'))
    assert_that(edit_storefront_page.get_product_add_button().text, equal_to('ADD'))
    assert_that(edit_storefront_page.get_product_table_code_column().text, equal_to('Code'))
    assert_that(edit_storefront_page.get_product_by_name(config.data.TEST_PRODUCT_FULL.CODE))
    assert_that(edit_storefront_page.get_product_list(), greater_than_or_equal_to(1))
    # assert_that(edit_storefront_page.get_product_table_display_weight_column().text, equal_to('Display Weight'))  # greyed out for GP
    # assert_that(edit_storefront_page.get_product_display_weight_input(config.data.TEST_PRODUCT_FULL.CODE))  # greyed out for GP
    assert_that(edit_storefront_page.get_product_remove_button(config.data.TEST_PRODUCT_FULL.CODE))
    assert_that(edit_storefront_page.get_save_and_close_button().text, equal_to('Save and Close'))
    assert_that(edit_storefront_page.get_save_button().text, equal_to('Save'))
    assert_that(edit_storefront_page.get_cancel_button().text, equal_to('Cancel'))


@pytest.allure.step('Validate elements on the edit storefront catalog tabs page')
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


@pytest.allure.step('Validate elements on the edit storefront sidebar page')
def validate_edit_storefront_sidebar_page(sidebar_page):
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


@pytest.allure.step('Validate elements on the edit storefront header page')
def validate_edit_storefront_header_page(header_page):
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
    edit_storefront_page = EditStorefront(browser)
    storefronts_page = Storefronts(browser)
    catalog_tabs_page = CatalogTabs(browser)
    sidebar_page = Sidebar(browser)
    header_page = Header(browser)

    steps.login(config.admin.username, config.admin.password)
    steps.navigate_to_titles_page(config.data.TEST_STUDIO.CODE)
    steps.navigate_to_catalogs_page(config.data.TEST_TITLE.CODE)
    steps.navigate_to_catalog_tabs_page(config.data.TEST_CATALOG.CODE)
    steps.navigate_to_storefronts_page()

    storefronts_page.click_storefront_button(config.data.TEST_ONE_PRODUCT_STOREFRONT.CODE)
    edit_storefront_page.wait_for_page_load()

    yield edit_storefront_page, storefronts_page, catalog_tabs_page, sidebar_page, header_page


@pytest.fixture
def clean_up(setup, browser, config):
    yield
    edit_storefront_page, _, _, _, _ = setup
    notification = Notification(browser)

    edit_storefront_page.type_friendly_name_input(config.data.TEST_ONE_PRODUCT_STOREFRONT.FRIENDLY_NAME)
    notification.wait_for_notification_message_to_disappear()
    edit_storefront_page.click_save_and_close_button()


@pytest.fixture
def toggle_clean_up(setup, browser):
    yield
    edit_storefront_page, _, _, _, _ = setup
    notification = Notification(browser)

    if not edit_storefront_page.get_active_checkbox().is_selected():
        edit_storefront_page.click_active_toggle()
    notification.wait_for_notification_message_to_disappear()
    edit_storefront_page.click_save_and_close_button()


@pytest.mark.xfail(reason='PLAT-5684', raises=TimeoutException)
@pytest.allure.testcase("Validate edit storefront page")
def test_edit_storefront_page(setup, config):
    edit_storefront_page, _, _, _, _ = setup
    validate_page(edit_storefront_page, config)


@pytest.allure.testcase("Validate edit storefront catalog tabs page")
def test_catalog_tabs_page(setup, config):
    _, _, catalog_tabs_page, _, _ = setup
    validate_catalog_tabs_page(catalog_tabs_page, config)


@pytest.allure.testcase("Validate edit storefront sidebar page")
def test_edit_storefront_sidebar_page(setup):
    _, _, _, sidebar_page, _ = setup
    validate_edit_storefront_sidebar_page(sidebar_page)


@pytest.allure.testcase("Validate edit storefront header page")
def test_edit_storefront_header_page(setup):
    _, _, _, _, header_page = setup
    validate_edit_storefront_header_page(header_page)


@pytest.allure.testcase("Validate can edit a storefront through the UI, check it's version and code")
def test_edit_storefront_functions(browser, setup, config, clean_up):
    edit_storefront_page, storefronts_page, _, _, _ = setup
    notification = Notification(browser)

    # Get the current version of a storefront
    version_input = edit_storefront_page.get_version_input()
    version_input_value = version_input.get_attribute('value')

    # Edit and save the storefront
    unique_id = RandomUtilities.create_unique_id_lowercase()
    friendly_name = 'Test Storefront Edit {}'.format(unique_id)
    edit_storefront_page.type_friendly_name_input(friendly_name)
    edit_storefront_page.click_save_and_close_button()

    # Get notification
    notification.wait_for_notification_message()
    notification_message = notification.get_notification_message()
    assert_that(notification_message.text,
                equal_to('Storefront: {} successfully saved!'.format(config.data.TEST_ONE_PRODUCT_STOREFRONT.CODE)))

    # Ensure the storefront is listed under it's edited name in the storefront list
    storefronts_page.wait_for_page_load()
    assert_that(storefronts_page.get_storefront_by_name(config.data.TEST_ONE_PRODUCT_STOREFRONT.CODE).text,
                equal_to(friendly_name))

    # Ensure the storefront's version is increased by 1, version and code input fields are disabled
    storefronts_page.click_storefront_button(config.data.TEST_ONE_PRODUCT_STOREFRONT.CODE)
    edit_storefront_page.wait_for_page_load()

    assert_that(edit_storefront_page.get_version_input().is_enabled(), equal_to(False))
    version_input = edit_storefront_page.get_version_input()
    version_input_value_updated = version_input.get_attribute('value')
    assert_that(int(version_input_value_updated) - int(version_input_value), equal_to(1))

    assert_that(edit_storefront_page.get_code_input().is_enabled(), equal_to(False))
    code_input = edit_storefront_page.get_code_input()
    code_input_value = code_input.get_attribute('value')
    assert_that(code_input_value, equal_to(config.data.TEST_ONE_PRODUCT_STOREFRONT.CODE))


@pytest.mark.xfail(reason='PLAT-6334', raises=TimeoutException)
@pytest.allure.testcase("Validate Edit Storefront toggles")
def test_edit_storefront_toggles(browser, setup, config, toggle_clean_up):
    edit_storefront_page, storefronts_page, _, _, _ = setup
    notification = Notification(browser)

    # Edit and save the storefront
    edit_storefront_page.click_active_toggle()
    edit_storefront_page.click_metadata_toggle()

    assert_that(not_(edit_storefront_page.get_active_checkbox().is_selected()))
    assert_that(edit_storefront_page.get_metadata_checkbox().is_selected())

    edit_storefront_page.click_save_and_close_button()

    # Get notification
    notification.wait_for_notification_message()
    notification_message = notification.get_notification_message()
    assert_that(
        notification_message.text,
        equal_to('Storefront: {} successfully saved!'.format(config.data.TEST_ONE_PRODUCT_STOREFRONT.CODE))
    )

    # Ensure that Active is still false
    storefronts_page.wait_for_page_load()
    storefronts_page.click_storefront_button(config.data.TEST_ONE_PRODUCT_STOREFRONT.CODE)
    edit_storefront_page.wait_for_page_load()

    assert_that(not_(edit_storefront_page.get_active_checkbox().is_selected()))
    assert_that(not_(edit_storefront_page.get_metadata_checkbox().is_selected()))


@pytest.allure.testcase("Ensure cancel button returns the user to the storefronts page")
def test_edit_storefront_cancel_button_returns_to_storefronts_page(setup):
    edit_storefront_page, storefronts_page, _, _, _ = setup

    edit_storefront_page.click_cancel_button()

    storefronts_page.wait_for_page_load()
    assert_that(storefronts_page.get_storefronts_list())


@pytest.allure.testcase("Ensure storefront won't get saved when friendly name is invalid")
@pytest.mark.parametrize('invalid_friendly_name', ['!', '@'])
def test_edit_storefront_does_not_save_storefront_when_friendly_name_is_invalid(invalid_friendly_name, setup):
    edit_storefront_page, _, _, _, _ = setup

    edit_storefront_page.type_friendly_name_input(invalid_friendly_name)
    edit_storefront_page.wait_for_friendly_name_invalid_message()
    assert_that(edit_storefront_page.get_friendly_name_invalid_message().text, equal_to(FRIENDLY_NAME_INVALID_INPUT))

    assert_that(edit_storefront_page.get_save_and_close_button().is_enabled(), equal_to(False))
    assert_that(edit_storefront_page.get_save_button().is_enabled(), equal_to(False))


@pytest.allure.testcase("Ensure storefront cannot be saved when friendly name is blank")
def test_edit_storefront_does_not_accept_blank_friendly_name(setup):
    edit_storefront_page, _, _, _, _ = setup

    edit_storefront_page.type_friendly_name_input(' ')
    assert_that(edit_storefront_page.get_save_and_close_button().is_enabled(), equal_to(False))
    assert_that(edit_storefront_page.get_save_button().is_enabled(), equal_to(False))


@pytest.allure.testcase("Ensure storefront cannot be saved with empty friendly name")
def test_edit_storefront_does_not_save_storefront_when_empty_friendly_name(setup):
    edit_storefront_page, _, _, _, _ = setup

    friendly_name = edit_storefront_page.get_friendly_name_input()
    friendly_name.clear()
    friendly_name.send_keys(' \b')
    assert_that(edit_storefront_page.get_save_and_close_button().is_enabled(), equal_to(False))
    assert_that(edit_storefront_page.get_save_button().is_enabled(), equal_to(False))


@pytest.mark.xfail(reason='PLAT-5684, PLAT-6334', raises=TimeoutException)
@pytest.allure.testcase("Validate the product can be removed from the storefront")
def test_edit_storefront_can_remove_product_from_storefront(setup, browser, config):
    edit_storefront_page, storefronts_page, _, _, _ = setup
    add_entity_to_entity_page = AddEntityToEntity(browser)
    notification = Notification(browser)

    edit_storefront_page.click_product_add_button()
    add_entity_to_entity_page.wait_for_page_load('products')
    add_entity_to_entity_page.click_entity_checkbox(config.data.TEST_PRODUCT.CODE)
    add_entity_to_entity_page.click_add_button()
    assert_that(edit_storefront_page.get_product_by_name(config.data.TEST_PRODUCT.CODE))
    assert_that(edit_storefront_page.get_product_list(), equal_to(2))
    edit_storefront_page.click_save_and_close_button()

    notification.wait_for_notification_message()
    notification_message = notification.get_notification_message()
    assert_that(notification_message.text,
                equal_to('Storefront: {} successfully saved!'.format(config.data.TEST_ONE_PRODUCT_STOREFRONT.CODE)))

    storefronts_page.wait_for_page_load()

    storefronts_page.click_storefront_button(config.data.TEST_ONE_PRODUCT_STOREFRONT.CODE)
    edit_storefront_page.wait_for_page_load()

    assert_that(edit_storefront_page.get_product_by_name(config.data.TEST_PRODUCT.CODE))
    # assert_that(edit_storefront_page.get_product_display_weight_input(config.data.TEST_PRODUCT.CODE))  #greyed out for GP
    assert_that(edit_storefront_page.get_product_remove_button(config.data.TEST_PRODUCT.CODE))

    edit_storefront_page.click_product_remove_button(config.data.TEST_PRODUCT.CODE)
    assert_that(edit_storefront_page.get_product_list(), equal_to(1))
    edit_storefront_page.click_save_and_close_button()

    notification.wait_for_notification_message()
    notification_message = notification.get_notification_message()
    assert_that(notification_message.text,
                equal_to('Storefront: {} successfully saved!'.format(config.data.TEST_ONE_PRODUCT_STOREFRONT.CODE)))

    storefronts_page.wait_for_page_load()

    storefronts_page.click_storefront_button(config.data.TEST_ONE_PRODUCT_STOREFRONT.CODE)
    edit_storefront_page.wait_for_page_load()
    assert_that(edit_storefront_page.get_product_list(), equal_to(1))
