import os
import pytest
from hamcrest import assert_that, equal_to, greater_than_or_equal_to, has_length

from ui.main.constants import SEARCH_TEXT, PLATFORM_HEADER_TEXT
from ui.pages import Products, Sidebar, Header, CatalogTabs, AddProduct, ActionsMenu


def validate_page(products_page, config):
    import_button = products_page.get_import_button()
    assert_that(import_button.text, equal_to('IMPORT PRODUCTS'))

    add_button = products_page.get_add_button()
    assert_that(add_button.text, equal_to('CREATE PRODUCT'))

    # search_box = products_page.get_search_box()
    # assert_that(search_box.get_attribute('placeholder'), equal_to(SEARCH_TEXT))
    #
    # drop_down_list = products_page.get_drop_down_list()
    # assert_that(drop_down_list.text, equal_to(''))
    #
    # assert_that(products_page.get_drop_down_list_arrow())

    assert_that(products_page.get_info_box())

    assert_that(products_page.get_info_box_exit_button())

    info_box_strong = products_page.get_info_box_strong()
    assert_that(info_box_strong.text, equal_to('Products'))

    table_name_column = products_page.get_table_name_column()
    assert_that(table_name_column.text, equal_to('Friendly Name'))

    # table_actions_column = products_page.get_table_actions_column()
    # assert_that(table_actions_column.text, equal_to('Actions'))

    # assert_that(products_page.get_table_select_all_checkbox())

    products_list = products_page.get_products_list()
    assert_that(products_list, greater_than_or_equal_to(1))

    test_product = products_page.get_product_by_name(config.data.TEST_PRODUCT.CODE)
    assert_that(test_product.text, equal_to(config.data.TEST_PRODUCT.FRIENDLY_NAME))

    # assert_that(products_page.get_product_checkbox_by_name(config.data.TEST_PRODUCT.CODE))

    # assert_that(products_page.get_product_actions_button_by_name(config.data.TEST_PRODUCT.CODE))


@pytest.allure.step('Validate elements on the products sidebar page')
def validate_products_sidebar_page(sidebar_page):
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


@pytest.allure.step('Validate elements on the products header page')
def validate_products_header_page(header_page):
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


@pytest.allure.step('Validate elements on the products actions menu')
def validate_products_actions_menu(actions_menu, config):
    assert_that(actions_menu.get_actions_edit_by_name(config.data.TEST_PRODUCT.CODE).text, equal_to('Edit'))
    assert_that(actions_menu.get_actions_duplicate_by_name(config.data.TEST_PRODUCT.CODE).text, equal_to('Duplicate'))
    assert_that(actions_menu.get_actions_remove_by_name(config.data.TEST_PRODUCT.CODE).text, equal_to('Remove'))
    assert_that(actions_menu.get_actions_menu_list_by_name(config.data.TEST_PRODUCT.CODE), has_length(3))


@pytest.fixture
def setup(config, browser, steps):
    products_page = Products(browser)
    catalog_tabs_page = CatalogTabs(browser)
    sidebar_page = Sidebar(browser)
    header_page = Header(browser)
    actions_menu = ActionsMenu(browser)

    steps.login(config.admin.username, config.admin.password)
    steps.navigate_to_titles_page(config.data.TEST_STUDIO.CODE)
    steps.navigate_to_catalogs_page(config.data.TEST_TITLE.CODE)
    steps.navigate_to_catalog_tabs_page(config.data.TEST_CATALOG.CODE)
    steps.navigate_to_products_tab()

    yield products_page, catalog_tabs_page, sidebar_page, header_page, actions_menu


@pytest.allure.testcase('Validate products page')
def test_products_page(setup, config):
    products_page, _, _, _, _ = setup
    validate_page(products_page, config)


@pytest.allure.testcase('Validate products sidebar page')
def test_product_sidebar_page(setup):
    _, _, sidebar_page, _, _ = setup
    validate_products_sidebar_page(sidebar_page)


@pytest.allure.testcase('Validate products header page')
def test_product_header_page(setup):
    _, _, _, header_page, _ = setup
    validate_products_header_page(header_page)


@pytest.allure.testcase('Validate products tabs page')
def test_product_catalog_tabs_page(setup, config):
    _, catalog_tabs_page, _, _, _ = setup
    validate_catalog_tabs_page(catalog_tabs_page, config)


# @pytest.allure.testcase('Validate products actions menu')
# def test_products_actions_menu(setup, config):
#     products_page, _, _, _, actions_menu = setup
#
#     products_page.click_product_actions_button(config.data.TEST_PRODUCT.CODE)
#     actions_menu.wait_for_actions_menu_load(config.data.TEST_PRODUCT.CODE)
#     validate_products_actions_menu(actions_menu, config)


@pytest.allure.testcase("Validate add button leads the user to the add product page")
def test_products_add_button_leads_to_add_product_page(setup, browser):
    products_page, _, _, _, _ = setup
    add_product_page = AddProduct(browser)

    products_page.click_add_button()

    add_product_page.wait_for_page_load()
    assert_that(add_product_page.get_save_button())


@pytest.mark.skip(reason='file format is not defined yet')
@pytest.allure.testcase("Validate import button uploads a new product")
def test_products_import_button_uploads_new_product(setup):
    products_page, _, _, _, _ = setup

    products_page.get_import_button().send_keys(os.getcwd() + "/catalog.json")


@pytest.allure.testcase("Validate checking the 'select all' checkbox checks all the products")
def test_products_select_all_checkbox_checks_all_products(setup, config):
    products_page, _, _, _, _ = setup

    products_page.click_table_select_all_checkbox()
    assert_that(products_page.get_product_checkbox_by_name(config.data.TEST_PRODUCT.CODE).is_selected())


@pytest.allure.testcase("Validate info box exit button closes the info box")
def test_products_info_box_exit_button_closes_the_box(setup):
    products_page, _, _, _, _ = setup

    products_page.click_info_box_exit_button()
    products_page.wait_for_info_box_to_disappear()
