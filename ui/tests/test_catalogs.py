import os
import pytest

from hamcrest import assert_that, equal_to, has_length, greater_than_or_equal_to

from ui.pages import Catalogs, Sidebar, Header, AddCatalog, ActionsMenu
from ui.main.constants import PLATFORM_HEADER_TEXT


@pytest.allure.step('Validate elements on the catalogs page')
def validate_page(catalogs_page, config):
    catalogs_title_text = catalogs_page.get_catalogs_title()
    assert_that(catalogs_title_text.text, equal_to('Catalogs'))

    assert_that(catalogs_page.get_info_box())

    assert_that(catalogs_page.get_info_box_exit_button())

    info_box_strong = catalogs_page.get_info_box_strong()
    assert_that(info_box_strong.text, equal_to('catalogs'))

    info_box_strong2 = catalogs_page.get_info_box_strong2()
    assert_that(info_box_strong2.text, equal_to('Entities'))

    import_catalog_button_text = catalogs_page.get_import_catalog_button()
    assert_that(import_catalog_button_text.text, equal_to('IMPORT CATALOG'))

    add_catalog_button_text = catalogs_page.get_add_catalog_button()
    assert_that(add_catalog_button_text.text, equal_to('CREATE CATALOG'))

    choose_catalog_text = catalogs_page.get_choose_catalog_text()
    assert_that(choose_catalog_text.text, equal_to('Choose a catalog'))

    # search_box_input = catalogs_page.get_search_box()
    # assert_that(search_box_input.get_attribute('placeholder'), equal_to(SEARCH_PLACEHOLDER_TEXT))
    #
    # filter_name = catalogs_page.get_filter_name()
    # assert_that(filter_name.text, equal_to('Filter...'))
    #
    # assert_that(catalogs_page.get_filter_dropdown_arrow())

    first_column_name = catalogs_page.get_first_column_name()
    assert_that(first_column_name.text, equal_to('Friendly Name'))

    second_column_name = catalogs_page.get_second_column_name()
    assert_that(second_column_name.text, equal_to('Actions'))

    # assert_that(catalogs_page.get_select_all_checkbox())

    catalogs_list = catalogs_page.get_catalogs_list()
    assert_that(catalogs_list, has_length(greater_than_or_equal_to(1)))

    assert_that(catalogs_page.get_catalog_by_name(config.data.TEST_CATALOG.CODE))

    # assert_that(catalogs_page.get_catalog_checkbox_by_name(config.data.TEST_CATALOG.CODE))

    assert_that(catalogs_page.get_catalog_actions_button_by_name(config.data.TEST_CATALOG.CODE))


@pytest.allure.step('Validate elements on the catalogs sidebar page')
def validate_catalogs_sidebar_page(sidebar_page):
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


@pytest.allure.step('Validate elements on the catalogs header page')
def validate_catalogs_header_page(header_page):
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


@pytest.allure.step('Validate elements on the catalogs actions menu')
def validate_catalogs_actions_menu(actions_menu, config):
    assert_that(actions_menu.get_actions_download_config_by_name(config.data.TEST_CATALOG.CODE).text,
                equal_to('Download Config'))
    assert_that(actions_menu.get_actions_edit_by_name(config.data.TEST_CATALOG.CODE).text, equal_to('Edit'))
    # assert_that(actions_menu.get_actions_duplicate_by_name(config.data.TEST_CATALOG.CODE).text, equal_to('Duplicate'))
    # assert_that(actions_menu.get_actions_remove_by_name(config.data.TEST_CATALOG.CODE).text, equal_to('Remove'))
    assert_that(actions_menu.get_actions_menu_list_by_name(config.data.TEST_CATALOG.CODE), has_length(2))


@pytest.fixture
def setup(config, browser, steps):
    catalogs_page = Catalogs(browser)
    sidebar_page = Sidebar(browser)
    header_page = Header(browser)
    actions_menu = ActionsMenu(browser)

    steps.login(config.admin.username, config.admin.password)
    steps.navigate_to_titles_page(config.data.TEST_STUDIO.CODE)
    steps.navigate_to_catalogs_page(config.data.TEST_TITLE.CODE)

    yield catalogs_page, sidebar_page, header_page, actions_menu


@pytest.allure.testcase("Validate catalogs page")
def test_catalogs_page(setup, config):
    catalogs_page, _, _, _ = setup
    validate_page(catalogs_page, config)


@pytest.allure.testcase("Validate catalogs sidebar page")
def test_catalogs_sidebar_page(setup):
    _, sidebar_page, _, _ = setup
    validate_catalogs_sidebar_page(sidebar_page)


@pytest.allure.testcase("Validate catalogs header page")
def test_catalogs_header_page(setup):
    _, _, header_page, _ = setup
    validate_catalogs_header_page(header_page)


@pytest.allure.testcase('Validate catalogs actions menu')
def test_catalogs_actions_menu(setup, config):
    catalogs_page, _, _, actions_menu = setup

    catalogs_page.click_catalog_actions_button_by_name(config.data.TEST_CATALOG.CODE)
    actions_menu.wait_for_actions_menu_load(config.data.TEST_CATALOG.CODE)
    validate_catalogs_actions_menu(actions_menu, config)


@pytest.allure.testcase("Validate add button leads the user to the add catalog page")
def test_catalogs_add_button_leads_to_add_catalog_page(setup, browser):
    catalogs_page, _, _, _ = setup
    add_catalog_page = AddCatalog(browser)

    catalogs_page.click_add_catalog_button()

    add_catalog_page.wait_for_page_load()
    assert_that(add_catalog_page.get_save_button())


@pytest.mark.skip(reason='file format is not defined yet')
@pytest.allure.testcase("Validate import button uploads a new catalog")
def test_catalogs_import_button_uploads_new_catalog(setup):
    catalogs_page, _, _, _ = setup

    catalogs_page.get_import_catalog_button().send_keys(os.getcwd() + "/catalog.json")


@pytest.allure.testcase("Validate checking the 'select all' checkbox checks all the catalogs")
def test_catalogs_select_all_checkbox_checks_all_catalogs(setup, config):
    catalogs_page, _, _, _ = setup

    catalogs_page.check_select_all_checkbox()
    assert_that(catalogs_page.get_catalog_checkbox_by_name(config.data.TEST_CATALOG.CODE).is_selected())


@pytest.allure.testcase("Validate info box exit button closes the info box")
def test_catalogs_info_box_exit_button_closes_the_box(setup):
    catalogs_page, _, _, _ = setup

    catalogs_page.click_info_box_exit_button()
    catalogs_page.wait_for_info_box_to_disappear()
