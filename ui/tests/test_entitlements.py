import os
import pytest
from hamcrest import assert_that, equal_to, greater_than_or_equal_to, has_length

from ui.main.constants import SEARCH_TEXT, PLATFORM_HEADER_TEXT
from ui.pages import Entitlements, Sidebar, Header, CatalogTabs, AddEntitlement, EditEntitlement, ActionsMenu


@pytest.allure.step('Validate elements on the entitlements page')
def validate_page(entitlements_page, config):
    import_button = entitlements_page.get_import_button()
    assert_that(import_button.text, equal_to('IMPORT ENTITLEMENTS'))

    add_button = entitlements_page.get_add_button()
    assert_that(add_button.text, equal_to('CREATE ENTITLEMENT'))

    # search_box = entitlements_page.get_search_box()
    # assert_that(search_box.get_attribute('placeholder'), equal_to(SEARCH_TEXT))
    #
    # assert_that(entitlements_page.get_drop_down_list())
    #
    # assert_that(entitlements_page.get_drop_down_list_arrow())

    assert_that(entitlements_page.get_info_box())

    assert_that(entitlements_page.get_info_box_exit_button())

    info_box_strong = entitlements_page.get_info_box_strong()
    assert_that(info_box_strong.text, equal_to('Entitlements'))

    table_header_name_column = entitlements_page.get_table_header_name_column()
    assert_that(table_header_name_column.text, equal_to('Friendly Name'))

    # table_header_actions_column = entitlements_page.get_table_header_actions_column()
    # assert_that(table_header_actions_column.text, equal_to('Actions'))

    # assert_that(entitlements_page.get_table_select_all_checkbox())

    entitlements_list = entitlements_page.get_entitlements_list()
    assert_that(entitlements_list, greater_than_or_equal_to(1))

    test_entitlement = entitlements_page.get_entitlement_by_name(config.data.TEST_ENTITLEMENT.CODE)
    assert_that(test_entitlement.text, equal_to(config.data.TEST_ENTITLEMENT.FRIENDLY_NAME))

    # assert_that(entitlements_page.get_entitlement_checkbox_by_name(config.data.TEST_ENTITLEMENT.CODE))

    # assert_that(entitlements_page.get_entitlement_actions_button_by_name(config.data.TEST_ENTITLEMENT.CODE))


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


@pytest.allure.step('Validate elements on the entitlements sidebar page')
def validate_entitlements_sidebar_page(sidebar_page):
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


@pytest.allure.step('Validate elements on the entitlements header page')
def validate_entitlements_header_page(header_page):
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


@pytest.allure.step('Validate elements on the entitlements actions menu')
def validate_entitlements_actions_menu(actions_menu, config):
    assert_that(actions_menu.get_actions_edit_by_name(config.data.TEST_ENTITLEMENT.CODE).text, equal_to('Edit'))
    assert_that(actions_menu.get_actions_duplicate_by_name(config.data.TEST_ENTITLEMENT.CODE).text,
                equal_to('Duplicate'))
    assert_that(actions_menu.get_actions_remove_by_name(config.data.TEST_ENTITLEMENT.CODE).text, equal_to('Remove'))
    assert_that(actions_menu.get_actions_menu_list_by_name(config.data.TEST_ENTITLEMENT.CODE), has_length(3))


@pytest.fixture
def setup(config, browser, steps):
    entitlements_page = Entitlements(browser)
    catalog_tabs_page = CatalogTabs(browser)
    sidebar_page = Sidebar(browser)
    header_page = Header(browser)
    actions_menu = ActionsMenu(browser)

    steps.login(config.admin.username, config.admin.password)
    steps.navigate_to_titles_page(config.data.TEST_STUDIO.CODE)
    steps.navigate_to_catalogs_page(config.data.TEST_TITLE.CODE)
    steps.navigate_to_catalog_tabs_page(config.data.TEST_CATALOG.CODE)
    steps.navigate_to_entitlements_page()

    yield entitlements_page, catalog_tabs_page, sidebar_page, header_page, actions_menu


@pytest.allure.testcase('Validate entitlements page')
def test_entitlements_page(setup, config):
    entitlements_page, _, _, _, _ = setup
    validate_page(entitlements_page, config)


@pytest.allure.testcase("Validate catalog tabs page")
def test_catalog_tabs_page(setup, config):
    _, catalog_tabs_page, _, _, _ = setup
    validate_catalog_tabs_page(catalog_tabs_page, config)


@pytest.allure.testcase('Validate entitlements sidebar page')
def test_entitlements_sidebar_page(setup):
    _, _, sidebar_page, _, _ = setup
    validate_entitlements_sidebar_page(sidebar_page)


@pytest.allure.testcase('Validate entitlements header page')
def test_entitlements_header_page(setup):
    _, _, _, header_page, _ = setup
    validate_entitlements_header_page(header_page)


# @pytest.allure.testcase('Validate entitlements actions menu')
# def test_entitlements_actions_menu(setup, config):
#     entitlements_page, _, _, _, actions_menu = setup
#
#     entitlements_page.click_entitlement_actions_button_by_name(config.data.TEST_ENTITLEMENT.CODE)
#     actions_menu.wait_for_actions_menu_load(config.data.TEST_ENTITLEMENT.CODE)
#     validate_entitlements_actions_menu(actions_menu, config)


@pytest.allure.testcase("Validate add button leads the user to the add entitlement page")
def test_entitlements_add_button_leads_to_add_entitlement_page(setup, browser):
    entitlements_page, _, _, _, _ = setup
    add_entitlement_page = AddEntitlement(browser)

    entitlements_page.click_add_button()

    add_entitlement_page.wait_for_page_load()
    assert_that(add_entitlement_page.get_save_button())


@pytest.mark.skip(reason='file format is not defined yet')
@pytest.allure.testcase("Validate import button uploads a new entitlement")
def test_entitlements_import_button_uploads_new_entitlement(setup):
    entitlements_page, _, _, _, _ = setup

    entitlements_page.get_import_button().send_keys(os.getcwd() + "/catalog.json")


@pytest.allure.testcase("Validate checking the 'select all' checkbox checks all the entitlements")
def test_entitlements_select_all_checkbox_checks_all_entitlements(setup, config):
    entitlements_page, _, _, _, _ = setup

    entitlements_page.click_table_select_all_checkbox()
    assert_that(entitlements_page.get_entitlement_checkbox_by_name(config.data.TEST_ENTITLEMENT.CODE).is_selected())


@pytest.allure.testcase("Validate info box exit button closes the info box")
def test_entitlements_info_box_exit_button_closes_the_box(setup):
    entitlements_page, _, _, _, _ = setup

    entitlements_page.click_info_box_exit_button()
    entitlements_page.wait_for_info_box_to_disappear()


@pytest.allure.testcase("Validate clicking on the entitlement leads the user to the edit entitlement page")
def test_entitlements_click_on_entitlement_leads_to_edit_entitlement_page(setup, browser, config):
    entitlements_page, _, _, _, _ = setup
    edit_entitlement_page = EditEntitlement(browser)

    entitlements_page.click_entitlement_by_name(config.data.TEST_ENTITLEMENT.CODE)

    edit_entitlement_page.wait_for_page_load()
    assert_that(edit_entitlement_page.get_save_button())
