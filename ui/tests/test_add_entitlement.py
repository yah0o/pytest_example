import pytest

from selenium.common.exceptions import TimeoutException
from hamcrest import assert_that, equal_to, has_length, not_

from ui.main.helpers import RandomUtilities
from ui.pages import Sidebar, Notification, Header, Entitlements, CatalogTabs, AddEntitlement, EditEntitlement
from ui.main.constants import FRIENDLY_NAME_INVALID_INPUT, CODE_INVALID_INPUT, PLATFORM_HEADER_TEXT


@pytest.allure.step('Validate elements on the add entitlement page')
def validate_page(add_entitlement_page):
    assert_that(add_entitlement_page.get_add_entitlement_header().text, equal_to('Create Entitlement'))

    assert_that(add_entitlement_page.get_friendly_name_label().text, equal_to('Friendly Name\n*'))
    assert_that(add_entitlement_page.get_friendly_name_input())

    assert_that(add_entitlement_page.get_code_label().text, equal_to('Code\n*'))
    assert_that(add_entitlement_page.get_code_input())

    assert_that(add_entitlement_page.get_active_header().text, equal_to('Active'))
    assert_that(add_entitlement_page.get_active_toggle())
    assert_that(add_entitlement_page.get_active_checkbox())
    assert_that(add_entitlement_page.get_inactive_label().text, equal_to('Inactive'))
    assert_that(add_entitlement_page.get_active_label().text, equal_to('Active'))

    assert_that(add_entitlement_page.get_metadata_header().text, equal_to('Metadata'))
    assert_that(add_entitlement_page.get_metadata_toggle())
    assert_that(add_entitlement_page.get_metadata_checkbox())
    assert_that(add_entitlement_page.get_metadata_field_editor_label().text, equal_to('Field Editor'))
    assert_that(add_entitlement_page.get_metadata_code_editor_label().text, equal_to('Code Editor'))

    assert_that(add_entitlement_page.get_tags_header().text, equal_to('Tags'))
    assert_that(add_entitlement_page.get_tags_input())
    # assert_that(add_entitlement_page.get_tags_drop_down_arrow())

    assert_that(add_entitlement_page.get_save_button().text, equal_to('Create'))
    assert_that(add_entitlement_page.get_cancel_button().text, equal_to('Cancel'))


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


@pytest.allure.step('Validate elements on the add entitlement sidebar page')
def validate_add_entitlement_sidebar_page(sidebar_page):
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


@pytest.allure.step('Validate elements on the add entitlement header page')
def validate_add_entitlement_header_page(header_page):
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
    add_entitlement_page = AddEntitlement(browser)
    entitlements_page = Entitlements(browser)
    catalog_tabs_page = CatalogTabs(browser)
    sidebar_page = Sidebar(browser)
    header_page = Header(browser)

    steps.login(config.admin.username, config.admin.password)
    steps.navigate_to_titles_page(config.data.TEST_STUDIO.CODE)
    steps.navigate_to_catalogs_page(config.data.TEST_TITLE.CODE)
    steps.navigate_to_catalog_tabs_page(config.data.TEST_CATALOG.CODE)
    steps.navigate_to_entitlements_page()

    entitlements_page.click_add_button()
    add_entitlement_page.wait_for_page_load()

    yield add_entitlement_page, entitlements_page, catalog_tabs_page, sidebar_page, header_page


@pytest.allure.testcase("Validate add entitlement page")
def test_add_entitlement_page(setup):
    add_entitlement_page, _, _, _, _ = setup
    validate_page(add_entitlement_page)


@pytest.allure.testcase("Validate catalog tabs page")
def test_catalog_tabs_page(setup, config):
    _, _, catalog_tabs_page, _, _ = setup
    validate_catalog_tabs_page(catalog_tabs_page, config)


@pytest.allure.testcase("Validate add entitlement sidebar")
def test_add_entitlement_sidebar_page(setup):
    _, _, _, sidebar_page, _ = setup
    validate_add_entitlement_sidebar_page(sidebar_page)


@pytest.allure.testcase("Validate add entitlement header page")
def test_add_entitlement_header_page(setup):
    _, _, _, _, header_page = setup
    validate_add_entitlement_header_page(header_page)


@pytest.allure.testcase("Validate can add an entitlement through the UI")
@pytest.mark.xfail(reason='PLAT-6334', raises=TimeoutException)
def test_add_entitlement_functions(browser, setup):
    add_entitlement_page, entitlements_page, _, _, _ = setup
    notification = Notification(browser)

    unique_id = RandomUtilities.create_unique_id_lowercase()

    friendly_name = 'Test UI Create Entitlement {}'.format(unique_id)
    entitlement_code = 'test_ui_create_entitlement_{}'.format(unique_id)

    add_entitlement_page.type_friendly_name_input(friendly_name)
    add_entitlement_page.type_code_input(entitlement_code)
    add_entitlement_page.click_save_button()

    notification.wait_for_notification_message()
    notification_message = notification.get_notification_message()
    assert_that(notification_message.text, equal_to('Entitlement: {} successfully created!'.format(entitlement_code)))

    entitlements_page.wait_for_page_load()
    assert_that(entitlements_page.get_entitlement_by_name(entitlement_code).text, equal_to(friendly_name))


@pytest.allure.testcase("Validate Add Entitlement toggles functions")
@pytest.mark.xfail(reason='PLAT-6334', raises=TimeoutException)
def test_add_entitlement_toggles(browser, setup):
    add_entitlement_page, entitlements_page, _, _, _ = setup
    notification = Notification(browser)
    edit_entitlement_page = EditEntitlement(browser)

    unique_id = RandomUtilities.create_unique_id_lowercase()

    friendly_name = 'Test UI Create Entitlement {}'.format(unique_id)
    entitlement_code = 'test_ui_create_entitlement_{}'.format(unique_id)

    add_entitlement_page.type_friendly_name_input(friendly_name)
    add_entitlement_page.type_code_input(entitlement_code)

    add_entitlement_page.click_active_toggle()
    assert_that(not_(add_entitlement_page.get_active_checkbox().is_selected()))

    add_entitlement_page.click_metadata_toggle()
    assert_that(add_entitlement_page.get_metadata_checkbox().is_selected())

    add_entitlement_page.click_save_button()

    notification.wait_for_notification_message()
    notification_message = notification.get_notification_message()
    assert_that(notification_message.text, equal_to('Entitlement: {} successfully created!'.format(entitlement_code)))

    entitlements_page.wait_for_page_load()
    assert_that(entitlements_page.get_entitlement_by_name(entitlement_code).text, equal_to(friendly_name))

    entitlements_page.click_entitlement_by_name(entitlement_code)
    edit_entitlement_page.wait_for_page_load()

    assert_that(not_(edit_entitlement_page.get_active_checkbox().is_selected()))
    assert_that(not_(edit_entitlement_page.get_metadata_checkbox().is_selected()))


@pytest.mark.xfail(reason='PLAT-6334', raises=TimeoutException)
@pytest.allure.testcase("Validate cannot add a duplicate entitlement through the UI")
def test_add_entitlement_does_not_create_duplicate_entitlements(config, browser, setup):
    add_entitlement_page, entitlements_page, catalog_tabs_page, _, _ = setup
    notification = Notification(browser)

    add_entitlement_page.type_friendly_name_input('Test UI Create Duplicate Entitlement')
    add_entitlement_page.type_code_input(config.data.TEST_ENTITLEMENT.CODE)
    add_entitlement_page.click_save_button()

    notification.wait_for_notification_message()
    assert_that(
        notification.get_notification_message().text,
        equal_to("\"Entity '{}' of title '{}' of studio '{}' already exists, creation impossible\"".format(
            config.data.TEST_ENTITLEMENT.CODE,
            config.data.TEST_TITLE.CODE,
            config.data.TEST_STUDIO.CODE
        ))
    )

    catalog_tabs_page.click_entitlements_tab()
    entitlements_page.wait_for_page_load()
    entitlements_list = entitlements_page.get_entitlements_list()

    count = 0
    for entitlement in entitlements_list:
        if config.data.TEST_ENTITLEMENT.FRIENDLY_NAME in entitlement.get_attribute('innerHTML'):
            count = count + 1
    assert_that(count, equal_to(1))


@pytest.allure.testcase("Ensure cancel button returns the user to the entitlements page")
def test_add_entitlement_cancel_button_returns_to_entitlements_page(setup):
    add_entitlement_page, entitlements_page, _, _, _ = setup

    add_entitlement_page.click_cancel_button()

    entitlements_page.wait_for_page_load()
    assert_that(entitlements_page.get_entitlements_list())


@pytest.allure.testcase("Ensure entitlement won't get created when friendly name input is invalid")
@pytest.mark.parametrize('invalid_friendly_name', ['!', '@'])
def test_add_entitlement_does_not_create_entitlement_when_friendly_name_is_invalid(invalid_friendly_name, setup):
    add_entitlement_page, _, _, _, _ = setup

    unique_id = RandomUtilities.create_unique_id_lowercase()
    entitlement_code = 'test_ui_create_entitlement_{}'.format(unique_id)

    add_entitlement_page.type_friendly_name_input(invalid_friendly_name)
    add_entitlement_page.wait_for_friendly_name_invalid_message()
    assert_that(add_entitlement_page.get_friendly_name_invalid_message().text, equal_to(FRIENDLY_NAME_INVALID_INPUT))

    add_entitlement_page.type_code_input(entitlement_code)
    assert_that(add_entitlement_page.get_save_button().is_enabled(), equal_to(False))


@pytest.allure.testcase("Ensure entitlement won't get created when code input is invalid")
@pytest.mark.parametrize('invalid_code', ['!', '@'])
def test_add_entitlement_does_not_create_entitlement_when_code_is_invalid(invalid_code, setup):
    add_entitlement_page, _, _, _, _ = setup

    unique_id = RandomUtilities.create_unique_id_lowercase()
    friendly_name = 'Test UI Create Entitlement {}'.format(unique_id)

    add_entitlement_page.type_friendly_name_input(friendly_name)
    add_entitlement_page.type_code_input(invalid_code)
    add_entitlement_page.wait_for_code_invalid_message()
    assert_that(add_entitlement_page.get_code_invalid_message().text, equal_to(CODE_INVALID_INPUT))

    assert_that(add_entitlement_page.get_save_button().is_enabled(), equal_to(False))


@pytest.allure.testcase("Ensure the entitlement is not being created when saving with empty input data")
@pytest.mark.parametrize('page_input', [('', ''), ('friendly_name_input', ''), ('', 'code_input')])
def test_add_entitlement_does_not_create_entitlement_when_empty_input_data(setup, page_input):
    add_entitlement_page, _, _, _, _ = setup
    friendly_name_input, code_input = page_input

    add_entitlement_page.type_friendly_name_input(friendly_name_input)
    add_entitlement_page.type_code_input(code_input)
    assert_that(add_entitlement_page.get_save_button().is_enabled(), equal_to(False))
