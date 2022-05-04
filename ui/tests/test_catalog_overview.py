import pytest
from hamcrest import assert_that, equal_to, has_length, greater_than_or_equal_to

from ui.pages import Catalogs, Sidebar, CatalogOverview, CatalogTabs, Header
from ui.main.constants import PLATFORM_HEADER_TEXT


@pytest.allure.step('Validate elements on the catalog overview page')
def validate_page(catalog_overview_page):
    recent_activity_text = catalog_overview_page.get_recent_activity_text()
    assert_that(recent_activity_text.text, equal_to('Recent activity'))

    recent_activity_subheading_text = catalog_overview_page.get_recent_activity_subheading_text()
    assert_that(recent_activity_subheading_text.text, equal_to('Latest changes to the catalog'))

    see_all_activity_link_text = catalog_overview_page.get_see_all_activity_link()
    assert_that(see_all_activity_link_text.text, equal_to('See all activity'))

    recent_activity_date_column_text = catalog_overview_page.get_recent_activity_date_column()
    assert_that(recent_activity_date_column_text.text, equal_to('Date'))

    recent_activity_name_column_text = catalog_overview_page.get_recent_activity_name_column()
    assert_that(recent_activity_name_column_text.text, equal_to('Name'))

    recent_activity_activity_column_text = catalog_overview_page.get_recent_activity_activity_column()
    assert_that(recent_activity_activity_column_text.text, equal_to('Activity'))

    activity_list = catalog_overview_page.get_activity_list()
    assert_that(activity_list, has_length(greater_than_or_equal_to(1)))

    status_text = catalog_overview_page.get_status_text()
    assert_that(status_text.text, equal_to('Status across environments'))

    status_subheading_text = catalog_overview_page.get_status_subheading_text()
    assert_that(status_subheading_text.text, equal_to('Environments where the catalog has been promoted'))

    see_all_catalogs_link_text = catalog_overview_page.get_see_all_catalogs_link()
    assert_that(see_all_catalogs_link_text.text, equal_to('See all catalogs'))

    status_name_column_text = catalog_overview_page.get_status_name_column()
    assert_that(status_name_column_text.text, equal_to('Name'))

    status_last_promotion_date_column_text = catalog_overview_page.get_status_last_promotion_date_column()
    assert_that(status_last_promotion_date_column_text.text, equal_to('Last promotion date'))

    status_list = catalog_overview_page.get_status_list()
    assert_that(status_list, has_length(greater_than_or_equal_to(1)))


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


@pytest.allure.step('Validate elements on the catalog overview sidebar page')
def validate_catalog_overview_sidebar_page(sidebar_page):
    assert_that(sidebar_page.get_dashboard_button().text, equal_to('Dashboard'))
    assert_that(sidebar_page.get_catalogs_button().text, equal_to('Catalogs'))
    assert_that(sidebar_page.get_environments_button().text, equal_to('Environments'))
    assert_that(sidebar_page.get_title_components_button().text, equal_to('Title Components'))
    assert_that(sidebar_page.get_activity_button().text, equal_to('Activity'))
    assert_that(sidebar_page.get_users_button().text, equal_to('Users'))
    assert_that(sidebar_page.get_players_button().text, equal_to('Players'))
    assert_that(sidebar_page.get_reports_button().text, equal_to('Reports'))
    assert_that(sidebar_page.get_panel(), has_length(8))


@pytest.allure.step('Validate elements on the catalog overview header page')
def validate_catalog_overview_header_page(header_page):
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
    catalog_overview_page = CatalogOverview(browser)
    catalog_tabs_page = CatalogTabs(browser)
    sidebar_page = Sidebar(browser)
    header_page = Header(browser)

    steps.login(config.admin.username, config.admin.password)
    steps.navigate_to_titles_page(config.data.TEST_STUDIO.CODE)
    steps.navigate_to_catalogs_page(config.data.TEST_TITLE.CODE)
    steps.navigate_to_catalog_tabs_page(config.data.TEST_CATALOG.CODE)
    catalog_overview_page.wait_for_page_load()

    yield catalog_overview_page, catalog_tabs_page, sidebar_page, header_page


# @pytest.allure.testcase("Validate catalog overview page")
# def test_catalog_overview_page(setup):
#     catalog_overview_page, _, _, _ = setup
#     validate_page(catalog_overview_page)
#
#
# @pytest.allure.testcase("Validate catalog tabs page")
# def test_catalog_tabs_page(setup, config):
#     _, catalog_tabs_page, _, _ = setup
#     validate_catalog_tabs_page(catalog_tabs_page, config)
#
#
# @pytest.allure.testcase("Validate catalog overview sidebar page")
# def test_catalog_overview_sidebar_page(setup):
#     _, _, sidebar_page, _ = setup
#     validate_catalog_overview_sidebar_page(sidebar_page)
#
#
# @pytest.allure.testcase("Validate catalog overview header page")
# def test_catalog_overview_header_page(setup):
#     _, _, _, header_page = setup
#     validate_catalog_overview_header_page(header_page)
#
#
# @pytest.allure.testcase("Ensure done button returns the user to the catalogs page")
# def test_catalog_tabs_done_button_returns_to_catalogs_page(browser, setup):
#     _, catalog_tabs_page, _, _ = setup
#     catalogs_page = Catalogs(browser)
#
#     catalog_tabs_page.click_done_button()
#
#     catalogs_page.wait_for_page_load()
#
#
# @pytest.allure.testcase("Ensure 'See all catalogs' link returns the user to the catalogs page")
# def test_catalog_overview_see_all_catalogs_link_returns_to_catalogs_page(browser, setup):
#     catalog_overview_page, _, _, _ = setup
#     catalogs_page = Catalogs(browser)
#
#     catalog_overview_page.click_see_all_catalogs_link()
#
#     catalogs_page.wait_for_page_load()

# Comment out as soon as test for Catalog Activity tab is created
# @pytest.allure.testcase("Ensure 'See all activity' link leads to the catalog activity tab")
# def test_catalog_overview_see_all_activity_link_returns_to_catalog_activity_tab(browser, setup):
#     catalog_overview_page, _, _, _ = setup
#     catalog_activity_page = CatalogActivity(browser)
#
#     catalog_overview_page.click_see_all_activity_link()
#
#     catalog_activity_page.wait_for_page_load()
