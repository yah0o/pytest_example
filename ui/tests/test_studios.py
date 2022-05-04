import pytest
from hamcrest import assert_that, equal_to, has_length, greater_than_or_equal_to, less_than

from ui.pages import Studios, Sidebar, Header
from ui.main.constants import SEARCH_PLACEHOLDER_TEXT, PLATFORM_HEADER_TEXT


@pytest.allure.step('Validate elements on the studios page')
def validate_page(studios_page, config):
    studios_title_text = studios_page.get_studios_title()
    assert_that(studios_title_text.text, equal_to('Studios'))

    # import_button_text = studios_page.get_import_button()
    # assert_that(import_button_text.text, equal_to('IMPORT STUDIO'))

    add_button_text = studios_page.get_add_button()
    assert_that(add_button_text.text, equal_to('Create Studio'))

    # search_box_input = studios_page.get_search_box()
    # assert_that(search_box_input.get_attribute('placeholder'), equal_to(SEARCH_PLACEHOLDER_TEXT))

    studios_list = studios_page.get_studios_list()
    assert_that(studios_list, has_length(greater_than_or_equal_to(1)))

    assert_that(studios_page.get_studio_button_by_name(config.data.TEST_STUDIO.CODE).text,
                equal_to(config.data.TEST_STUDIO.FRIENDLY_NAME))

    assert_that(studios_page.get_studio_settings_icon_by_name(config.data.TEST_STUDIO.CODE))


@pytest.allure.step('Validate elements on the studios sidebar page')
def validate_studios_sidebar_page(sidebar_page):
    studios_button = sidebar_page.get_studios_button()
    assert_that(studios_button.text, equal_to('Studios'))

    # reports_button = sidebar_page.get_reports_button()
    # assert_that(reports_button.text, equal_to('Reports'))

    sidebar_panel = sidebar_page.get_panel()
    assert_that(sidebar_panel, has_length(1))


@pytest.allure.step('Validate elements on the studios header page')
def validate_studios_header_page(header_page):
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


@pytest.allure.step('Validate that the studios list is sorted alphabetically')
def validate_studios_list_is_sorted(studios_page):
    studios_list = studios_page.get_studios_list()

    for i in range(len(studios_list) - 1):
        assert_that(studios_list[i].getAttribute('id'), less_than(studios_list[i+1].getAttribute('id')))


@pytest.fixture
def setup(config, browser, steps):
    studios_page = Studios(browser)
    sidebar_page = Sidebar(browser)
    header_page = Header(browser)

    steps.login(config.admin.username, config.admin.password)

    yield studios_page, sidebar_page, header_page


@pytest.allure.testcase("Validate studios page")
def test_studios_page(setup, config):
    studios_page, _, _ = setup
    validate_page(studios_page, config)


@pytest.allure.testcase("Validate studios sidebar page")
def test_studios_sidebar_page(setup):
    _, sidebar_page, _ = setup
    validate_studios_sidebar_page(sidebar_page)


@pytest.allure.testcase("Validate studios header page")
def test_studios_header_page(setup):
    _, _, header_page = setup
    validate_studios_header_page(header_page)


@pytest.allure.testcase("Validate studios list")
def test_studios_list(setup):
    studios_page, _, _ = setup
    validate_studios_list_is_sorted(studios_page)
