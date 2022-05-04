import pytest
from hamcrest import assert_that, equal_to, has_length, not_
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from ui.main.helpers import RandomUtilities
from ui.main.constants import PLATFORM_HEADER_TEXT, FRIENDLY_NAME_INVALID_INPUT, CODE_INVALID_INPUT
from ui.pages import AddCatalog, Catalogs, Sidebar, Header, Notification
from ui.main.constants import PLATFORM_HEADER_TEXT


@pytest.allure.step('Validate elements on the add catalog page')
def validate_page(add_catalog_page):
    add_catalog_header = add_catalog_page.get_add_catalog_header()
    assert_that(add_catalog_header.text, equal_to('Create Catalog'))

    assert_that(add_catalog_page.get_field_header('Basic Information').text, equal_to('BASIC INFORMATION'))
    assert_that(add_catalog_page.get_field_label('friendly_name').text, equal_to('Friendly Name\n*'))
    assert_that(add_catalog_page.get_field_input('friendly_name'))
    assert_that(add_catalog_page.get_field_invalid_message('friendly_name'))

    assert_that(add_catalog_page.get_field_header('Platform Information').text, equal_to('PLATFORM INFORMATION'))
    assert_that(add_catalog_page.get_field_label('code').text, equal_to('Code\n*'))
    assert_that(add_catalog_page.get_field_input('code'))
    assert_that(add_catalog_page.get_field_invalid_message('code'))

    assert_that(add_catalog_page.get_active_header().text, equal_to('Active'))
    assert_that(add_catalog_page.get_field_toggle_left_label('active').text, equal_to('Inactive'))
    assert_that(add_catalog_page.get_field_toggle_right_label('active').text, equal_to('Active'))
    assert_that(add_catalog_page.get_field_toggle('active'))

    assert_that(add_catalog_page.get_field_label('tags').text, equal_to('Tags'))
    assert_that(add_catalog_page.get_tags_input())

    assert_that(add_catalog_page.get_field_header('Endpoints').text, equal_to('ENDPOINTS'))
    assert_that(add_catalog_page.get_field_label('webhook_endpoint').text, equal_to('Notification Endpoint'))
    assert_that(add_catalog_page.get_field_input('webhook_endpoint'))
    assert_that(add_catalog_page.get_field_invalid_message('webhook_endpoint'))

    assert_that(add_catalog_page.get_field_label('webhook_security_token').text, equal_to('Webhook Security Token'))
    assert_that(add_catalog_page.get_field_input('webhook_security_token'))

    assert_that(add_catalog_page.get_field_label('ggapi_endpoint').text, equal_to('GGAPI Endpoint'))
    assert_that(add_catalog_page.get_field_input('ggapi_endpoint'))
    assert_that(add_catalog_page.get_field_invalid_message('ggapi_endpoint'))

    assert_that(add_catalog_page.get_field_header('Starting Inventory Code').text, equal_to('STARTING INVENTORY CODE'))
    assert_that(add_catalog_page.get_field_label('starting_inventory_code').text, equal_to('Starting Inventory Code'))
    assert_that(add_catalog_page.get_field_input('starting_inventory_code'))

    assert_that(add_catalog_page.get_field_header('Notification Templates').text, equal_to('NOTIFICATION TEMPLATES'))
    assert_that(add_catalog_page.get_field_label('notification_templates').text, equal_to('Notification Templates'))
    assert_that(add_catalog_page.get_notification_templates_add_json_button().text, equal_to('Add New JSON Field'))
    assert_that(add_catalog_page.get_field_toggle('notification_templates'))
    assert_that(add_catalog_page.get_field_toggle_left_label('notification_templates').text, equal_to('Field Editor'))
    assert_that(add_catalog_page.get_field_toggle_right_label('notification_templates').text, equal_to('Code Editor'))

    assert_that(add_catalog_page.get_field_header('Feature Flags').text, equal_to('FEATURE FLAGS'))
    assert_that(add_catalog_page.get_field_label('feature_flags').text, equal_to('Feature Flags'))
    assert_that(add_catalog_page.get_feature_flags_add_json_button().text, equal_to('Add New JSON Field'))
    assert_that(add_catalog_page.get_field_toggle('feature_flags'))
    assert_that(add_catalog_page.get_field_toggle_left_label('feature_flags').text, equal_to('Field Editor'))
    assert_that(add_catalog_page.get_field_toggle_right_label('feature_flags').text, equal_to('Code Editor'))

    assert_that(add_catalog_page.get_field_header('Custom Data').text, equal_to('CUSTOM DATA'))
    assert_that(add_catalog_page.get_field_label('metadata').text, equal_to('Metadata'))
    assert_that(add_catalog_page.get_metadata_add_namespace_button().text, equal_to('+ Add Namespace'))
    assert_that(add_catalog_page.get_field_toggle('metadata'))
    assert_that(add_catalog_page.get_field_toggle_left_label('metadata').text, equal_to('Field Editor'))
    assert_that(add_catalog_page.get_field_toggle_right_label('metadata').text, equal_to('Code Editor'))

    assert_that(add_catalog_page.get_save_button().text, equal_to('Save and Close'))

    assert_that(add_catalog_page.get_cancel_button().text, equal_to('Cancel'))


@pytest.allure.step('Validate elements on the add catalog sidebar page')
def validate_add_catalog_sidebar_page(sidebar_page):
    # assert_that(sidebar_page.get_dashboard_button().text, equal_to('Dashboard'))
    assert_that(sidebar_page.get_back_to_titles_button().text, equal_to('< Back to Titles'))
    assert_that(sidebar_page.get_catalogs_button().text, equal_to('Catalogs'))
    assert_that(sidebar_page.get_environments_button().text, equal_to('Environments'))
    assert_that(sidebar_page.get_title_components_button().text, equal_to('Title Components'))
    # assert_that(sidebar_page.get_activity_button().text, equal_to('Activity'))
    # assert_that(sidebar_page.get_users_button().text, equal_to('Users'))
    assert_that(sidebar_page.get_data_button().text, equal_to('Data'))
    assert_that(sidebar_page.get_players_button().text, equal_to('Players'))
    # assert_that(sidebar_page.get_reports_button().text, equal_to('Reports'))
    assert_that(sidebar_page.get_panel(), has_length(6))


@pytest.allure.step('Validate elements on the add catalog header page')
def validate_add_catalog_header_page(header_page):
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
    add_catalog_page = AddCatalog(browser)
    catalogs_page = Catalogs(browser)
    sidebar_page = Sidebar(browser)
    header_page = Header(browser)

    steps.login(config.admin.username, config.admin.password)
    steps.navigate_to_titles_page(config.data.TEST_STUDIO.CODE)
    steps.navigate_to_catalogs_page(config.data.TEST_TITLE.CODE)

    catalogs_page.click_add_catalog_button()
    add_catalog_page.wait_for_page_load()

    yield add_catalog_page, catalogs_page, sidebar_page, header_page


@pytest.allure.testcase("Validate add catalog page")
def test_add_catalog_page(setup):
    add_catalog_page, _, _, _ = setup
    validate_page(add_catalog_page)


@pytest.allure.testcase("Validate add catalog sidebar page")
@pytest.mark.xfail(reason='PLAT-6175', raises=NoSuchElementException)
def test_add_catalog_sidebar_page(setup):
    _, _, sidebar_page, _ = setup
    validate_add_catalog_sidebar_page(sidebar_page)


@pytest.allure.testcase("Validate add catalog header page")
def test_add_catalogs_header_page(setup):
    _, _, _, header_page = setup
    validate_add_catalog_header_page(header_page)


@pytest.allure.testcase("Validate that a catalog can be added through the UI")
def test_add_catalog_functions(browser, setup):
    add_catalog_page, catalogs_page, _, _ = setup
    notification = Notification(browser)

    unique_id = RandomUtilities.create_unique_id_lowercase()

    catalog_code = 'ui_created_catalog_{}'.format(unique_id)
    add_catalog_page.type_field_input('code', catalog_code)
    friendly_name = 'Created by UI Catalog {}'.format(unique_id)
    add_catalog_page.type_field_input('friendly_name', friendly_name)
    add_catalog_page.click_save_button()

    notification.wait_for_notification_message()
    assert_that(
        notification.get_notification_message().text,
        equal_to('Catalog: {} successfully created!'.format(catalog_code))
    )

    catalogs_page.wait_for_page_load()

    ui_created_catalog = catalogs_page.get_catalog_by_name(catalog_code)
    assert_that(ui_created_catalog.text, equal_to(friendly_name))


@pytest.allure.testcase("Validate that cancel button go back to Catalogs page")
def test_add_catalog_cancel_function(setup):
    add_catalog_page, catalogs_page, _, _ = setup

    add_catalog_page.click_cancel_button()

    catalogs_page.wait_for_page_load()
    assert_that(catalogs_page.get_catalogs_list())


@pytest.allure.testcase("Validate that a duplicate catalog cannot be created")
def test_add_catalog_does_not_create_duplicate_catalogs(config, browser, setup):
    add_catalog_page, catalogs_page, sidebar_page, _ = setup
    notification = Notification(browser)

    add_catalog_page.type_field_input('code', config.data.TEST_CATALOG.CODE)
    add_catalog_page.type_field_input('friendly_name', 'Test creating duplicate catalog')
    add_catalog_page.click_save_button()

    notification.wait_for_notification_message()
    assert_that(
        notification.get_notification_message().text,
        equal_to("Catalog '{}' with title '{}' of studio '{}' already exists, creation impossible".format(
            config.data.TEST_CATALOG.CODE,
            config.data.TEST_TITLE.CODE,
            config.data.TEST_STUDIO.CODE
        ))
    )

    sidebar_page.click_catalogs_button()
    catalogs_page.wait_for_page_load()
    catalogs_list = catalogs_page.get_catalogs_list()

    count = 0
    for catalog in catalogs_list:
        if config.data.TEST_CATALOG.CODE in catalog.get_attribute('innerHTML'):
            count = count + 1
    assert_that(count, equal_to(1))


@pytest.allure.testcase("Validate that a catalog cannot be created when notification endpoint is not a url")
def test_add_catalog_does_not_create_catalog_when_notification_endpoint_not_url(setup):
    add_catalog_page, _, _, _ = setup

    unique_id = RandomUtilities.create_unique_id_lowercase()

    catalog_code = 'ui_created_catalog_{}'.format(unique_id)
    add_catalog_page.type_field_input('code', catalog_code)
    friendly_name = 'Created by UI Catalog {}'.format(unique_id)
    add_catalog_page.type_field_input('friendly_name', friendly_name)
    add_catalog_page.type_field_input('webhook_endpoint', 'not url')
    notification_endpoint_invalid_message = add_catalog_page.get_field_invalid_message('webhook_endpoint')
    assert_that(notification_endpoint_invalid_message.text, equal_to('Please input a valid URL.'))

    assert_that(add_catalog_page.get_save_button().is_enabled(), equal_to(False))


@pytest.allure.testcase("Validate that a catalog cannot be created when GGAPI endpoint is not a url")
def test_add_catalog_does_not_create_catalog_when_ggapi_endpoint_not_url(setup):
    add_catalog_page, _, _, _ = setup

    unique_id = RandomUtilities.create_unique_id_lowercase()

    catalog_code = 'ui_created_catalog_{}'.format(unique_id)
    add_catalog_page.type_field_input('code', catalog_code)
    friendly_name = 'Created by UI Catalog {}'.format(unique_id)
    add_catalog_page.type_field_input('friendly_name', friendly_name)
    add_catalog_page.type_field_input('ggapi_endpoint', 'not url')
    ggapi_endpoint_invalid_message = add_catalog_page.get_field_invalid_message('ggapi_endpoint')
    assert_that(ggapi_endpoint_invalid_message.text, equal_to('Please input a valid URL.'))

    assert_that(not_(add_catalog_page.get_save_button().is_enabled()))


@pytest.allure.testcase("Validate that a catalog cannot be created when friendly name is invalid")
def test_add_catalog_cannot_create_catalog_when_friendly_name_is_invalid(setup):
    add_catalog_page, _, _, _ = setup

    unique_id = RandomUtilities.create_unique_id_lowercase()
    catalog_code = 'ui_created_catalog_{}'.format(unique_id)

    add_catalog_page.type_field_input('code', catalog_code)
    add_catalog_page.type_field_input('friendly_name', '!')
    friendly_name_invalid_message = add_catalog_page.get_field_invalid_message('friendly_name')
    assert_that(friendly_name_invalid_message.text, equal_to(FRIENDLY_NAME_INVALID_INPUT))

    save_button = add_catalog_page.get_save_button()
    assert_that(not_(save_button.is_enabled()))


@pytest.allure.testcase("Validate that a catalog cannot be created when code is invalid")
def test_add_catalog_cannot_create_catalog_when_code_is_invalid(setup):
    add_catalog_page, _, _, _ = setup

    unique_id = RandomUtilities.create_unique_id_lowercase()
    friendly_name = 'Created by UI Catalog {}'.format(unique_id)

    add_catalog_page.type_field_input('code', '!')
    code_invalid_message = add_catalog_page.get_field_invalid_message('code')
    assert_that(code_invalid_message.text, equal_to(CODE_INVALID_INPUT))
    add_catalog_page.type_field_input('friendly_name', friendly_name)

    save_button = add_catalog_page.get_save_button()
    assert_that(not_(save_button.is_enabled()))
