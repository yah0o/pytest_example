import pytest

from selenium.common.exceptions import TimeoutException
from hamcrest import assert_that, equal_to, has_length, none, empty, not_

from ui.main.helpers import RandomUtilities
from ui.main.constants import FRIENDLY_NAME_INVALID_INPUT, CODE_INVALID_INPUT, PLATFORM_HEADER_TEXT
from ui.pages import Sidebar, Notification, Header, Storefronts, CatalogTabs, AddStorefront, AddEntityToEntity, \
    EditStorefront


@pytest.allure.step('Validate elements on the add storefront page')
def validate_page(add_storefront_page):
    add_storefront_header = add_storefront_page.get_add_storefront_header()
    assert_that(add_storefront_header.text, equal_to('Create Storefront'))

    friendly_name_label = add_storefront_page.get_friendly_name_label()
    assert_that(friendly_name_label.text, equal_to('Friendly Name'))
    assert_that(add_storefront_page.get_friendly_name_input())
    assert_that(add_storefront_page.get_friendly_name_invalid_message())

    code_label = add_storefront_page.get_code_label()
    assert_that(code_label.text, equal_to('Code'))
    assert_that(add_storefront_page.get_code_input())

    active_header = add_storefront_page.get_active_header()
    assert_that(active_header.text, equal_to('Active'))
    assert_that(add_storefront_page.get_active_toggle())

    metadata_header = add_storefront_page.get_metadata_header()
    assert_that(metadata_header.text, equal_to('Metadata'))
    assert_that(add_storefront_page.get_metadata_toggle())
    assert_that(add_storefront_page.get_metadata_checkbox())
    assert_that(add_storefront_page.get_metadata_field_editor_label().text, equal_to('Field Editor'))
    assert_that(add_storefront_page.get_metadata_code_editor_label().text, equal_to('Code Editor'))

    tags_header = add_storefront_page.get_tags_header()
    assert_that(tags_header.text, equal_to('Tags'))
    assert_that(add_storefront_page.get_tags_input())
    # assert_that(add_storefront_page.get_tags_drop_down_arrow())

    products_header = add_storefront_page.get_products_header()
    assert_that(products_header.text, equal_to('Products'))
    product_add_button = add_storefront_page.get_product_add_button()
    assert_that(product_add_button.text, equal_to('ADD'))

    save_button = add_storefront_page.get_save_button()
    assert_that(save_button.text, equal_to('Create'))

    cancel_button = add_storefront_page.get_cancel_button()
    assert_that(cancel_button.text, equal_to('Cancel'))


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


@pytest.allure.step('Validate elements on the add storefront sidebar page')
def validate_add_storefront_sidebar_page(sidebar_page):
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


@pytest.allure.step('Validate elements on the add storefront header page')
def validate_add_storefront_header_page(header_page):
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
    add_storefront_page = AddStorefront(browser)
    storefronts_page = Storefronts(browser)
    catalog_tabs_page = CatalogTabs(browser)
    sidebar_page = Sidebar(browser)
    header_page = Header(browser)

    steps.login(config.admin.username, config.admin.password)
    steps.navigate_to_titles_page(config.data.TEST_STUDIO.CODE)
    steps.navigate_to_catalogs_page(config.data.TEST_TITLE.CODE)
    steps.navigate_to_catalog_tabs_page(config.data.TEST_CATALOG.CODE)
    steps.navigate_to_storefronts_page()

    storefronts_page.click_add_button()
    add_storefront_page.wait_for_page_load()

    yield add_storefront_page, storefronts_page, catalog_tabs_page, sidebar_page, header_page


@pytest.allure.testcase("Validate add storefront page")
def test_add_storefront_page(setup):
    add_storefront_page, _, _, _, _ = setup
    validate_page(add_storefront_page)


@pytest.allure.testcase("Validate catalog tabs page")
def test_catalog_tabs_page(setup, config):
    _, _, catalog_tabs_page, _, _ = setup
    validate_catalog_tabs_page(catalog_tabs_page, config)


@pytest.allure.testcase("Validate add storefront sidebar")
def test_add_storefront_sidebar_page(setup):
    _, _, _, sidebar_page, _ = setup
    validate_add_storefront_sidebar_page(sidebar_page)


@pytest.allure.testcase("Validate add storefront header page")
def test_add_storefront_header_page(setup):
    _, _, _, _, header_page = setup
    validate_add_storefront_header_page(header_page)


@pytest.allure.testcase("Validate can add a storefront through the UI")
def test_add_storefront_functions(browser, setup):
    add_storefront_page, storefronts_page, _, _, _ = setup
    notification = Notification(browser)

    unique_id = RandomUtilities.create_unique_id_lowercase()
    friendly_name = 'Create Through UI Storefront {}'.format(unique_id)
    storefront_code = 'test_ui_create_storefront_{}'.format(unique_id)

    add_storefront_page.type_friendly_name_input(friendly_name)
    add_storefront_page.type_code_input(storefront_code)
    add_storefront_page.click_save_button()

    notification.wait_for_notification_message()
    notification_message = notification.get_notification_message()
    assert_that(notification_message.text, equal_to('Storefront: {} successfully created!'.format(storefront_code)))

    storefronts_page.wait_for_page_load()
    storefront = storefronts_page.get_storefront_by_name(storefront_code)
    assert_that(storefront.text, equal_to(friendly_name))


@pytest.mark.xfail(reason='PLAT-6334', raises=TimeoutException)
@pytest.allure.testcase("Validate Add Storefront toggles")
def test_add_storefront_toggles(browser, setup):
    add_storefront_page, storefronts_page, _, _, _ = setup
    notification = Notification(browser)
    edit_storefront_page = EditStorefront(browser)

    unique_id = RandomUtilities.create_unique_id_lowercase()
    friendly_name = 'Create Through UI Storefront {}'.format(unique_id)
    storefront_code = 'test_ui_create_storefront_{}'.format(unique_id)

    add_storefront_page.type_friendly_name_input(friendly_name)
    add_storefront_page.type_code_input(storefront_code)
    add_storefront_page.click_active_toggle()
    add_storefront_page.click_metadata_toggle()

    assert_that(not_(add_storefront_page.get_active_checkbox().is_selected()))
    assert_that(add_storefront_page.get_metadata_checkbox().is_selected())

    add_storefront_page.click_save_button()

    notification.wait_for_notification_message()
    notification_message = notification.get_notification_message()
    assert_that(notification_message.text, equal_to('Storefront: {} successfully created!'.format(storefront_code)))

    storefronts_page.wait_for_page_load()
    storefront = storefronts_page.get_storefront_by_name(storefront_code)
    assert_that(storefront.text, equal_to(friendly_name))

    storefronts_page.click_storefront_button(storefront_code)
    edit_storefront_page.wait_for_page_load()

    assert_that(not_(edit_storefront_page.get_active_checkbox().is_selected()))
    assert_that(not_(edit_storefront_page.get_metadata_checkbox().is_selected()))


@pytest.allure.testcase("Validate that cancel button go back to Storefronts page")
def test_add_storefront_cancel_function(setup):
    add_storefront_page, storefronts_page, _, _, _ = setup

    add_storefront_page.click_cancel_button()

    storefronts_page.wait_for_page_load()
    assert_that(storefronts_page.get_storefronts_list())


@pytest.mark.xfail(reason='PLAT-5468', raises=AssertionError)
@pytest.allure.testcase("Validate cannot add a duplicate storefront through the UI")
def test_add_storefront_does_not_create_duplicate_storefronts(config, browser, setup):
    add_storefront_page, storefronts_page, _, _, _ = setup
    notification = Notification(browser)

    add_storefront_page.type_friendly_name_input('Test UI Create Duplicate Storefront')
    add_storefront_page.type_code_input(config.data.TEST_STOREFRONT.CODE)
    add_storefront_page.click_save_button()

    notification.wait_for_notification_message()
    assert_that(
        notification.get_notification_message().text,
        equal_to("\"Storefront '{}' of title '{}' of studio '{}' already exists, creation impossible\"".format(
            config.data.TEST_STOREFRONT.CODE,
            config.data.TEST_TITLE.CODE,
            config.data.TEST_STUDIO.CODE
        ))
    )

    add_storefront_page.click_cancel_button()
    storefronts_page.wait_for_page_load()
    storefronts_list = storefronts_page.get_storefronts_list()

    count = 0
    for storefront in storefronts_list:
        if config.data.TEST_STOREFRONT.FRIENDLY_NAME in storefront.get_attribute('innerHTML'):
            count = count + 1
    assert_that(count, equal_to(1))


@pytest.allure.testcase("Ensure storefront won't get created when friendly name is invalid")
def test_add_storefront_does_not_create_storefront_when_friendly_name_is_invalid(setup):
    add_storefront_page, _, _, _, _ = setup

    unique_id = RandomUtilities.create_unique_id_lowercase()
    storefront_code = 'test_ui_create_storefront_{}'.format(unique_id)

    add_storefront_page.type_code_input(storefront_code)
    add_storefront_page.type_friendly_name_input('!')
    add_storefront_page.wait_for_friendly_name_invalid_message()
    friendly_name_invalid_message = add_storefront_page.get_friendly_name_invalid_message()
    assert_that(friendly_name_invalid_message.text, equal_to(FRIENDLY_NAME_INVALID_INPUT))

    assert_that(add_storefront_page.get_save_button().is_enabled(), equal_to(False))


@pytest.allure.testcase("Ensure storefront won't get created when code input is invalid")
@pytest.mark.parametrize('invalid_code', ['!', '@'])
def test_add_storefront_does_not_create_storefront_when_code_is_invalid(invalid_code, setup):
    add_storefront_page, _, _, _, _ = setup

    unique_id = RandomUtilities.create_unique_id_lowercase()
    friendly_name = 'Test UI Create Storefront {}'.format(unique_id)

    add_storefront_page.type_friendly_name_input(friendly_name)
    add_storefront_page.type_code_input(invalid_code)
    add_storefront_page.wait_for_code_invalid_message()
    assert_that(add_storefront_page.get_code_invalid_message().text, equal_to(CODE_INVALID_INPUT))

    assert_that(add_storefront_page.get_save_button().is_enabled(), equal_to(False))


@pytest.mark.xfail(reason='PLAT-5684, PLAT-6334', raises=TimeoutException)
@pytest.allure.testcase("Validate can add a product to a storefront")
def test_add_one_product_to_storefront(setup, browser, config):
    add_storefront_page, storefronts_page, _, _, _ = setup
    add_entity_to_entity_page = AddEntityToEntity(browser)
    notification = Notification(browser)
    edit_storefront_page = EditStorefront(browser)

    # Fill out storefront's friendly name and code fields
    unique_id = RandomUtilities.create_unique_id_lowercase()
    storefront_friendly_name = 'Create Through UI Storefront {}'.format(unique_id)
    storefront_code = 'test_ui_create_storefront_{}'.format(unique_id)
    add_storefront_page.type_friendly_name_input(storefront_friendly_name)
    add_storefront_page.type_code_input(storefront_code)

    # Add product to the storefront
    add_storefront_page.click_product_add_button()
    add_entity_to_entity_page.wait_for_page_load('products')
    add_entity_to_entity_page.click_entity_checkbox(config.data.TEST_PRODUCT.CODE)

    # Make sure the product that was just added to the storefront is not on the list anymore
    product_list = add_entity_to_entity_page.get_entity_list_by_entity_type('products')
    product = next((product for product in product_list
                    if product == config.data.TEST_PRODUCT.CODE), None)
    assert_that(product, none(), 'The product that was already added to the storefront is still on the list')

    # Check the product was successfully added to the storefront
    add_entity_to_entity_page.click_add_button()
    assert_that(add_storefront_page.get_product_by_name(config.data.TEST_PRODUCT.CODE))

    # display_weight_input = add_storefront_page.get_product_display_weight_input(config.data.TEST_PRODUCT.CODE)
    # display_weight_input_value = display_weight_input.get_attribute('value')
    # assert_that(display_weight_input_value), equal_to('0')

    assert_that(add_storefront_page.get_product_remove_button(config.data.TEST_PRODUCT.CODE))

    # Check the storefront with the product is created
    add_storefront_page.click_save_button()

    notification.wait_for_notification_message()
    notification_message = notification.get_notification_message()
    assert_that(notification_message.text, equal_to('Storefront: {} successfully created!'.format(storefront_code)))

    storefronts_page.wait_for_page_load()

    storefronts_page.click_storefront_button(storefront_code)
    edit_storefront_page.wait_for_page_load()

    assert_that(edit_storefront_page.get_friendly_name_input().get_attribute('value'),
                equal_to(storefront_friendly_name))

    assert_that(edit_storefront_page.get_code_input().is_enabled(), equal_to(False))
    code_input = edit_storefront_page.get_code_input()
    code_input_value = code_input.get_attribute('value')
    assert_that(code_input_value, equal_to(storefront_code))

    assert_that(edit_storefront_page.get_version_input().is_enabled(), equal_to(False))
    version_input = edit_storefront_page.get_version_input()
    version_input_value = version_input.get_attribute('value')
    assert_that(version_input_value, equal_to('1'))

    assert_that(edit_storefront_page.get_product_by_name(config.data.TEST_PRODUCT.CODE))
    # assert_that(edit_storefront_page.get_product_display_weight_input(config.data.TEST_PRODUCT.CODE))
    assert_that(edit_storefront_page.get_product_remove_button(config.data.TEST_PRODUCT.CODE))
