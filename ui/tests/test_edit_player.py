import pytest
from hamcrest import assert_that, equal_to, greater_than_or_equal_to, has_length
from selenium.common.exceptions import NoSuchElementException

from ui.pages import Players, Sidebar, Header, EditPlayer, AddGameRegistration
from ui.main.constants import PLATFORM_HEADER_TEXT


@pytest.allure.step('Validate elements on the edit player page')
def validate_page(edit_player_page, config):
    assert_that(edit_player_page.get_page_header().text, equal_to('Players'))
    assert_that(edit_player_page.get_page_subheader())
    assert_that(edit_player_page.get_id_label().text, equal_to('ID'))
    assert_that(edit_player_page.get_id_input())
    assert_that(edit_player_page.get_name_label().text, equal_to('Name'))
    assert_that(edit_player_page.get_name_input())
    assert_that(edit_player_page.get_realm_label().text, equal_to('Realm'))
    assert_that(edit_player_page.get_realm_input())

    assert_that(edit_player_page.get_game_registrations_header().text, equal_to('Game Registrations'))
    assert_that(edit_player_page.get_game_registrations_name_column().text, equal_to('Name'))
    assert_that(edit_player_page.get_game(config.data.TEST_TITLE.CODE))
    assert_that(edit_player_page.get_game_list(), greater_than_or_equal_to(1))
    assert_that(edit_player_page.get_create_game_button().text, equal_to('Create'))
    assert_that(edit_player_page.get_game_registrations_showing_results_text().text, equal_to('Showing 1 Results'))
    # to be decided whether to include the count or not

    assert_that(edit_player_page.get_bans_header().text, equal_to('Bans'))

    assert_that(edit_player_page.get_field_label().text, equal_to('Field'))
    assert_that(edit_player_page.get_field_input().text, equal_to('Status'))  # this is a default value for now
    assert_that(edit_player_page.get_field_drop_down_list_arrow())
    assert_that(edit_player_page.get_field_drop_down_list(), has_length(3))

    assert_that(edit_player_page.get_operator_label().text, equal_to('Operator'))
    assert_that(edit_player_page.get_operator_input().text, equal_to('equal (=)'))
    assert_that(edit_player_page.get_operator_drop_down_list_arrow())

    assert_that(edit_player_page.get_value_label().text, equal_to('Value'))
    assert_that(edit_player_page.get_value_input().text, equal_to('active'))  # this is a default value for now
    assert_that(edit_player_page.get_value_drop_down_list_arrow())
    assert_that(edit_player_page.get_value_drop_down_list(), has_length(3))

    assert_that(edit_player_page.get_add_button().is_enabled(), equal_to(True))
    assert_that(edit_player_page.get_create_ban_button().text, equal_to('Create'))
    assert_that(edit_player_page.get_filter_button().text, equal_to('Filter'))
    assert_that(edit_player_page.get_reset_button().text, equal_to('Reset'))

    assert_that(edit_player_page.get_bans_showing_results_text().text, equal_to('Showing Results'))  # the text might
    # include the count in the future

    assert_that(edit_player_page.get_bans_table_column_header('id').text, equal_to('ID'))
    assert_that(edit_player_page.get_bans_table_column_header('wgid').text, equal_to('WGID'))
    assert_that(edit_player_page.get_bans_table_column_header('bantype').text, equal_to('Ban Type'))
    assert_that(edit_player_page.get_bans_table_column_header('status').text, equal_to('Status'))
    assert_that(edit_player_page.get_bans_table_column_header('realm').text, equal_to('Realm'))
    assert_that(edit_player_page.get_bans_table_column_header('game').text, equal_to('Game'))
    assert_that(edit_player_page.get_bans_table_column_header('started_at').text, equal_to('Started At'))
    assert_that(edit_player_page.get_bans_table_column_header('expires_at').text, equal_to('Expires At'))
    assert_that(edit_player_page.get_bans_table_column_header('actions').text, equal_to('Actions'))
    assert_that(edit_player_page.get_bans_table_column_list(), has_length(9))
    assert_that(edit_player_page.get_no_bans_found().text, equal_to('No Bans found.'))


@pytest.allure.step('Validate elements on the edit player sidebar page')
def validate_edit_player_sidebar_page(sidebar_page):
    assert_that(sidebar_page.get_studios_button().text, equal_to('Studios'))
    assert_that(sidebar_page.get_titles_button().text, equal_to('Titles'))
    assert_that(sidebar_page.get_players_button().text, equal_to('Players'))
    assert_that(sidebar_page.get_panel(), has_length(3))


@pytest.allure.step('Validate elements on the edit player header page')
def validate_edit_player_header_page(header_page):
    assert_that(header_page.get_home_button())
    assert_that(header_page.get_top_bar_header().text, equal_to(PLATFORM_HEADER_TEXT))
    assert_that(header_page.get_settings_icon())
    assert_that(header_page.get_drop_down_menu())
    assert_that(header_page.get_drop_down_options(), has_length(2))


@pytest.fixture
def setup(config, browser, steps):
    players_page = Players(browser)
    edit_player_page = EditPlayer(browser)
    sidebar_page = Sidebar(browser)
    header_page = Header(browser)

    steps.login(config.admin.username, config.admin.password)
    steps.navigate_to_titles_page(config.data.TEST_STUDIO.CODE)
    sidebar_page.click_players_button()
    players_page.wait_for_page_load()
    players_page.click_player_id(config.data.TEST_PLAYER.NAME)
    edit_player_page.wait_for_page_load()

    yield players_page, edit_player_page, sidebar_page, header_page


@pytest.mark.xfail(reason='PLAT-6305', raises=NoSuchElementException)
@pytest.allure.testcase('Validate edit player page')
def test_edit_player_page(setup, config):
    _, edit_player_page, _, _ = setup
    validate_page(edit_player_page, config)


@pytest.mark.xfail(reason='PLAT-6305', raises=NoSuchElementException)
@pytest.allure.testcase('Validate edit player sidebar page')
def test_edit_player_sidebar_page(setup):
    _, _, sidebar_page, _ = setup
    validate_edit_player_sidebar_page(sidebar_page)


@pytest.mark.xfail(reason='PLAT-6305', raises=NoSuchElementException)
@pytest.allure.testcase('Validate edit player header page')
def test_edit_player_header_page(setup):
    _, _, _, header_page = setup
    validate_edit_player_header_page(header_page)


@pytest.mark.xfail(reason='PLAT-6305', raises=NoSuchElementException)
@pytest.allure.testcase("Ensure page header button returns the user to the players page")
def test_edit_player_header_button_returns_to_players_page(setup):
    players_page, edit_player_page, _, _ = setup

    edit_player_page.click_page_header()

    players_page.wait_for_page_load()
    assert_that(players_page.get_player_list(), greater_than_or_equal_to(1))


@pytest.mark.xfail(reason='PLAT-6305', raises=NoSuchElementException)
@pytest.allure.testcase("Validate create game button leads the user to the create game registration page")
def test_edit_player_create_game_button_leads_to_add_game_registration_page(setup, browser):
    _, edit_player_page, _, _ = setup
    add_game_registration_page = AddGameRegistration(browser)

    edit_player_page.click_create_game_button()

    add_game_registration_page.wait_for_page_load()
    assert_that(add_game_registration_page.get_save_button())
