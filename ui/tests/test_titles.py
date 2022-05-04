import pytest
from hamcrest import assert_that, equal_to, has_length, greater_than_or_equal_to, less_than

from ui.pages import Sidebar, Titles, Header
from ui.main.constants import SEARCH_PLACEHOLDER_TEXT, PLATFORM_HEADER_TEXT


@pytest.allure.step('Validate elements on the titles page')
def validate_page(titles_page, config):
    assert_that(titles_page.get_studio_code_span().text, equal_to(config.data.TEST_STUDIO.CODE))

    titles_text = titles_page.get_page_title()
    assert_that(titles_text.text, equal_to('Titles'))

    add_title_button_text = titles_page.get_add_title_button()
    assert_that(add_title_button_text.text, equal_to('Create Title'))

    # get_search_box = titles_page.get_search_box()
    # assert_that(get_search_box.get_attribute('placeholder'), equal_to(SEARCH_PLACEHOLDER_TEXT))

    titles_list = titles_page.get_titles_list()
    assert_that(titles_list, has_length(greater_than_or_equal_to(1)))

    assert_that(titles_page.get_title_button_by_name(config.data.TEST_TITLE.CODE).text,
                equal_to(config.data.TEST_TITLE.FRIENDLY_NAME))

    assert_that(titles_page.get_title_edit_button_by_name(config.data.TEST_TITLE.CODE))

    assert_that(titles_page.get_title_image_by_name(config.data.TEST_TITLE.CODE))


@pytest.allure.step('Validate elements on the titles sidebar page')
def validate_titles_sidebar_page(sidebar_page):
    # dashboard_button = sidebar_page.get_dashboard_button()
    # assert_that(dashboard_button.text, equal_to('Dashboard'))

    # studio_button = sidebar_page.get_studios_button()
    # assert_that(studio_button.text, equal_to('Studios'))

    titles_button = sidebar_page.get_titles_button()
    assert_that(titles_button.text, equal_to('Titles'))

    # activity_button = sidebar_page.get_activity_button()
    # assert_that(activity_button.text, equal_to('Activity'))
    #
    # users_button = sidebar_page.get_users_button()
    # assert_that(users_button.text, equal_to('Users'))

    players_button = sidebar_page.get_players_button()
    assert_that(players_button.text, equal_to('Players'))

    # reports_button = sidebar_page.get_reports_button()
    # assert_that(reports_button.text, equal_to('Reports'))

    sidebar_panel = sidebar_page.get_panel()
    assert_that(sidebar_panel, has_length(3))


@pytest.allure.step('Validate elements on the titles header page')
def validate_titles_header_page(header_page):
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


@pytest.allure.step('Validate titles list is sorted alphabetically')
def validate_titles_list(titles_page):
    titles_list = titles_page.get_titles_list()

    for i in range(len(titles_list) - 1):
        assert_that(titles_list[i].getAttribute('id'), less_than(titles_list[i+1].getAttribute('id')))


@pytest.fixture
def setup(config, browser, steps):
    titles_page = Titles(browser)
    sidebar_page = Sidebar(browser)
    header_page = Header(browser)

    steps.login(config.admin.username, config.admin.password)
    steps.navigate_to_titles_page(config.data.TEST_STUDIO.CODE)

    yield titles_page, sidebar_page, header_page


@pytest.allure.testcase("Validate titles page")
def test_titles_page(setup, config):
    titles_page, _, _ = setup
    validate_page(titles_page, config)


@pytest.allure.testcase("Validate titles sidebar page")
def test_titles_sidebar_page(setup):
    _, sidebar_page, _ = setup
    validate_titles_sidebar_page(sidebar_page)


@pytest.allure.testcase("Validate titles header page")
def test_titles_header_page(setup):
    _, _, header_page = setup
    validate_titles_header_page(header_page)


@pytest.allure.testcase("Validate titles list")
def test_titles_list(setup):
    titles_page, _, _ = setup
    validate_titles_list(titles_page)
