import pytest

from hamcrest import assert_that, equal_to, has_length
from selenium.common.exceptions import TimeoutException

from ui.main.helpers import RandomUtilities
from ui.pages import Sidebar, Notification, Header, CatalogTabs, AddCurrency, Currencies
from ui.main.constants import FRIENDLY_NAME_INVALID_INPUT, CODE_INVALID_INPUT, PLATFORM_HEADER_TEXT


@pytest.allure.step('Validate elements on the add currency page')
def validate_page(add_currency_page):
    assert_that(add_currency_page.get_add_currency_header().text, equal_to('Create Currency'))

    assert_that(add_currency_page.get_friendly_name_label().text, equal_to('Friendly Name'))
    assert_that(add_currency_page.get_friendly_name_input())

    assert_that(add_currency_page.get_code_label().text, equal_to('Code'))
    assert_that(add_currency_page.get_code_input())

    assert_that(add_currency_page.get_active_header().text, equal_to('Active'))
    assert_that(add_currency_page.get_active_toggle())

    assert_that(add_currency_page.get_metadata_header().text, equal_to('Metadata'))
    assert_that(add_currency_page.get_metadata_toggle())
    assert_that(add_currency_page.get_metadata_checkbox())
    assert_that(add_currency_page.get_metadata_field_editor_label().text, equal_to('Field Editor'))
    assert_that(add_currency_page.get_metadata_code_editor_label().text, equal_to('Code Editor'))

    assert_that(add_currency_page.get_tags_header().text, equal_to('Tags'))
    assert_that(add_currency_page.get_tags_input())
    # assert_that(add_currency_page.get_tags_drop_down_arrow())

    assert_that(add_currency_page.get_include_currency_fin_report_label().text,
                equal_to('Include Currency in Finance Reports'))
    assert_that(add_currency_page.get_include_currency_fin_report_toggle())

    assert_that(add_currency_page.get_decimal_reported_fin_report_label().text,
                equal_to('Decimal Reported to Finance Report'))
    assert_that(add_currency_page.get_decimal_reported_fin_report_input())

    assert_that(add_currency_page.get_save_button().text, equal_to('Create'))
    assert_that(add_currency_page.get_cancel_button().text, equal_to('Cancel'))


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


@pytest.allure.step('Validate elements on the add currency sidebar page')
def validate_add_currency_sidebar_page(sidebar_page):
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


@pytest.allure.step('Validate elements on the add currency header page')
def validate_add_currency_header_page(header_page):
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
    add_currency_page = AddCurrency(browser)
    currencies_page = Currencies(browser)
    catalog_tabs_page = CatalogTabs(browser)
    sidebar_page = Sidebar(browser)
    header_page = Header(browser)

    steps.login(config.admin.username, config.admin.password)
    steps.navigate_to_titles_page(config.data.TEST_STUDIO.CODE)
    steps.navigate_to_catalogs_page(config.data.TEST_TITLE.CODE)
    steps.navigate_to_catalog_tabs_page(config.data.TEST_CATALOG.CODE)
    steps.navigate_to_currencies_page()

    currencies_page.click_add_button()
    add_currency_page.wait_for_page_load()

    yield add_currency_page, currencies_page, catalog_tabs_page, sidebar_page, header_page


@pytest.allure.testcase("Validate add currency page")
def test_add_currency_page(setup):
    add_currency_page, _, _, _, _ = setup
    validate_page(add_currency_page)


@pytest.allure.testcase("Validate catalog tabs page")
def test_catalog_tabs_page(setup, config):
    _, _, catalog_tabs_page, _, _ = setup
    validate_catalog_tabs_page(catalog_tabs_page, config)


@pytest.allure.testcase("Validate add currency sidebar")
def test_add_currency_sidebar_page(setup):
    _, _, _, sidebar_page, _ = setup
    validate_add_currency_sidebar_page(sidebar_page)


@pytest.allure.testcase("Validate add currency header page")
def test_add_currency_header_page(setup):
    _, _, _, _, header_page = setup
    validate_add_currency_header_page(header_page)


@pytest.allure.testcase("Validate can add a currency through the UI")
def test_add_currency_functions(browser, setup):
    add_currency_page, currencies_page, _, _, _ = setup
    notification = Notification(browser)

    unique_id = RandomUtilities.create_unique_id_lowercase()

    friendly_name = 'Test UI Create Currency {}'.format(unique_id)
    currency_code = 'test_ui_create_currency_{}'.format(unique_id)

    add_currency_page.type_friendly_name_input(friendly_name)
    add_currency_page.type_code_input(currency_code)
    add_currency_page.click_save_button()

    notification.wait_for_notification_message()
    notification_message = notification.get_notification_message()
    assert_that(notification_message.text, equal_to('Currency: {} successfully created!'.format(currency_code)))

    currencies_page.wait_for_page_load()
    assert_that(currencies_page.get_currency_by_name(currency_code).text, equal_to(friendly_name))


@pytest.mark.xfail(reason='PLAT-6334', raises=TimeoutException)
@pytest.allure.testcase("Validate cannot add a duplicate currency through the UI")
def test_add_currency_does_not_create_duplicate_currencies(config, browser, setup):
    add_currency_page, currencies_page, catalog_tabs_page, _, _ = setup
    notification = Notification(browser)

    add_currency_page.type_friendly_name_input('Test UI Create Duplicate Currency')
    add_currency_page.type_code_input(config.data.TEST_CURRENCY.CODE)
    add_currency_page.click_save_button()

    notification.wait_for_notification_message()
    assert_that(
        notification.get_notification_message().text,
        equal_to("\"Entity '{}' of title '{}' of studio '{}' already exists, creation impossible\"".format(
            config.data.TEST_CURRENCY.CODE,
            config.data.TEST_TITLE.CODE,
            config.data.TEST_STUDIO.CODE
        ))
    )

    catalog_tabs_page.click_currencies_tab()
    currencies_page.wait_for_page_load()
    currencies_list = currencies_page.get_currencies_list()

    count = 0
    for currency in currencies_list:
        if config.data.TEST_CURRENCY.FRIENDLY_NAME in currency.get_attribute('innerHTML'):
            count = count + 1
    assert_that(count, equal_to(1))


@pytest.allure.testcase("Ensure cancel button returns the user to the currencies page")
def test_add_currency_cancel_button_returns_to_currencies_page(setup):
    add_currency_page, currencies_page, _, _, _ = setup

    add_currency_page.click_cancel_button()

    currencies_page.wait_for_page_load()
    assert_that(currencies_page.get_currencies_list())


@pytest.allure.testcase("Ensure currency won't get created when friendly name input is invalid")
@pytest.mark.parametrize('invalid_friendly_name', ['!', '@'])
def test_add_currency_does_not_create_currency_when_friendly_name_is_invalid(invalid_friendly_name, setup):
    add_currency_page, _, _, _, _ = setup

    unique_id = RandomUtilities.create_unique_id_lowercase()
    currency_code = 'test_ui_create_currency_{}'.format(unique_id)

    add_currency_page.type_friendly_name_input(invalid_friendly_name)
    add_currency_page.wait_for_friendly_name_invalid_message()
    assert_that(add_currency_page.get_friendly_name_invalid_message().text, equal_to(FRIENDLY_NAME_INVALID_INPUT))

    add_currency_page.type_code_input(currency_code)
    assert_that(add_currency_page.get_save_button().is_enabled(), equal_to(False))


@pytest.allure.testcase("Ensure currency won't get created when code input is invalid")
@pytest.mark.parametrize('invalid_code', ['!', '@'])
def test_add_currency_does_not_create_currency_when_code_is_invalid(invalid_code, setup):
    add_currency_page, _, _, _, _ = setup

    unique_id = RandomUtilities.create_unique_id_lowercase()
    friendly_name = 'Test UI Create Currency {}'.format(unique_id)

    add_currency_page.type_friendly_name_input(friendly_name)
    add_currency_page.type_code_input(invalid_code)
    add_currency_page.wait_for_code_invalid_message()
    assert_that(add_currency_page.get_code_invalid_message().text, equal_to(CODE_INVALID_INPUT))

    assert_that(add_currency_page.get_save_button().is_enabled(), equal_to(False))


@pytest.allure.testcase("Ensure the currency is not being created when saving with empty input data")
@pytest.mark.parametrize('page_input', [('', ''), ('friendly_name_input', ''), ('', 'code_input')])
def test_add_currency_does_not_create_currency_when_empty_input_data(setup, page_input):
    add_currency_page, _, _, _, _ = setup
    friendly_name_input, code_input = page_input

    add_currency_page.type_friendly_name_input(friendly_name_input)
    add_currency_page.type_code_input(code_input)
    assert_that(add_currency_page.get_save_button().is_enabled(), equal_to(False))
