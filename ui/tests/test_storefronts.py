import os
import pytest
from hamcrest import assert_that, equal_to, greater_than_or_equal_to, has_length

from ui.main.constants import SEARCH_TEXT, PLATFORM_HEADER_TEXT
from ui.pages import Storefronts, Sidebar, Header, CatalogTabs, AddStorefront, ActionsMenu, EditStorefront


@pytest.allure.step('Validate elements on the storefronts page')
def validate_page(storefronts_page, config):
    import_button = storefronts_page.get_import_button()
    assert_that(import_button.text, equal_to('IMPORT STOREFRONTS'))

    add_button = storefronts_page.get_add_button()
    assert_that(add_button.text, equal_to('CREATE STOREFRONT'))

    # search_box = storefronts_page.get_search_box()
    # assert_that(search_box.get_attribute('placeholder'), equal_to(SEARCH_TEXT))
    #
    # drop_down_list = storefronts_page.get_drop_down_list()
    # assert_that(drop_down_list.text, equal_to(''))

    assert_that(storefronts_page.get_info_box())

    assert_that(storefronts_page.get_info_box_exit_button())

    info_box_strong = storefronts_page.get_info_box_strong()
    assert_that(info_box_strong.text, equal_to('Storefronts'))

    table_name_column = storefronts_page.get_table_name_column()
    assert_that(table_name_column.text, equal_to('Friendly Name'))

    # table_actions_column = storefronts_page.get_table_actions_column()
    # assert_that(table_actions_column.text, equal_to('Actions'))

    # assert_that(storefronts_page.get_table_select_all_checkbox())

    storefronts_list = storefronts_page.get_storefronts_list()
    assert_that(storefronts_list, has_length(greater_than_or_equal_to(1)))

    test_storefront = storefronts_page.get_storefront_by_name(config.data.TEST_STOREFRONT.CODE)
    assert_that(test_storefront.text, equal_to(config.data.TEST_STOREFRONT.FRIENDLY_NAME))

    # assert_that(storefronts_page.get_storefront_checkbox_by_name(config.data.TEST_STOREFRONT.CODE))

    # assert_that(storefronts_page.get_storefront_actions_button_by_name(config.data.TEST_STOREFRONT.CODE))


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


@pytest.allure.step('Validate elements on the storefronts sidebar page')
def validate_storefronts_sidebar_page(sidebar_page):
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


@pytest.allure.step('Validate elements on the storefronts header page')
def validate_storefronts_header_page(header_page):
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


@pytest.allure.step('Validate elements on the storefronts actions menu')
def validate_storefronts_actions_menu(actions_menu, config):
    assert_that(actions_menu.get_actions_edit_by_name(config.data.TEST_STOREFRONT.CODE).text, equal_to('Edit'))
    assert_that(actions_menu.get_actions_duplicate_by_name(config.data.TEST_STOREFRONT.CODE).text,
                equal_to('Duplicate'))
    assert_that(actions_menu.get_actions_remove_by_name(config.data.TEST_STOREFRONT.CODE).text, equal_to('Remove'))
    assert_that(actions_menu.get_actions_menu_list_by_name(config.data.TEST_STOREFRONT.CODE), has_length(3))


@pytest.fixture
def setup(config, browser, steps):
    storefronts_page = Storefronts(browser)
    catalog_tabs_page = CatalogTabs(browser)
    sidebar_page = Sidebar(browser)
    header_page = Header(browser)
    actions_menu = ActionsMenu(browser)

    steps.login(config.admin.username, config.admin.password)
    steps.navigate_to_titles_page(config.data.TEST_STUDIO.CODE)
    steps.navigate_to_catalogs_page(config.data.TEST_TITLE.CODE)
    steps.navigate_to_catalog_tabs_page(config.data.TEST_CATALOG.CODE)
    steps.navigate_to_storefronts_page()

    yield storefronts_page, catalog_tabs_page, sidebar_page, header_page, actions_menu


@pytest.allure.testcase('Validate storefronts page')
def test_storefronts_page(setup, config):
    storefronts_page, _, _, _, _ = setup
    validate_page(storefronts_page, config)


@pytest.allure.testcase("Validate catalog tabs page")
def test_catalog_tabs_page(setup, config):
    _, catalog_tabs_page, _, _, _ = setup
    validate_catalog_tabs_page(catalog_tabs_page, config)


@pytest.allure.testcase('Validate storefronts sidebar page')
def test_storefront_sidebar_page(setup):
    _, _, sidebar_page, _, _ = setup
    validate_storefronts_sidebar_page(sidebar_page)


@pytest.allure.testcase('Validate storefronts header page')
def test_storefront_header_page(setup):
    _, _, _, header_page, _ = setup
    validate_storefronts_header_page(header_page)


# @pytest.allure.testcase('Validate storefronts actions menu')
# def test_storefronts_actions_menu(setup, config):
#     storefronts_page, _, _, _, actions_menu = setup
#
#     storefronts_page.click_storefront_actions_button(config.data.TEST_STOREFRONT.CODE)
#     actions_menu.wait_for_actions_menu_load(config.data.TEST_STOREFRONT.CODE)
#     validate_storefronts_actions_menu(actions_menu, config)


@pytest.allure.testcase("Validate add button leads the user to the add storefront page")
def test_storefronts_add_button_leads_to_add_storefront_page(setup, browser):
    storefronts_page, _, _, _, _ = setup
    add_storefront_page = AddStorefront(browser)

    storefronts_page.click_add_button()

    add_storefront_page.wait_for_page_load()
    assert_that(add_storefront_page.get_save_button())


@pytest.mark.skip(reason='file format is not defined yet')
@pytest.allure.testcase("Validate import button uploads a new storefront")
def test_storefronts_import_button_uploads_new_storefront(setup):
    storefronts_page, _, _, _, _ = setup

    storefronts_page.get_import_button().send_keys(os.getcwd() + "/catalog.json")


@pytest.allure.testcase("Validate checking the 'select all' checkbox checks all the storefronts")
def test_storefronts_select_all_checkbox_checks_all_storefronts(setup, config):
    storefronts_page, _, _, _, _ = setup

    storefronts_page.click_table_select_all_checkbox()
    assert_that(storefronts_page.get_storefront_checkbox_by_name(config.data.TEST_STOREFRONT.CODE).is_selected())


@pytest.allure.testcase("Validate info box exit button closes the info box")
def test_storefronts_info_box_exit_button_closes_the_box(setup):
    storefronts_page, _, _, _, _ = setup

    storefronts_page.click_info_box_exit_button()
    storefronts_page.wait_for_info_box_to_disappear()


@pytest.allure.testcase("Validate clicking on the storefront leads the user to the edit storefront page")
def test_storefronts_click_on_storefront_leads_to_edit_storefront_page(setup, browser, config):
    storefronts_page, _, _, _, _ = setup
    edit_storefront_page = EditStorefront(browser)

    storefronts_page.click_storefront_button(config.data.TEST_STOREFRONT.CODE)

    edit_storefront_page.wait_for_page_load()
    assert_that(edit_storefront_page.get_save_button())
