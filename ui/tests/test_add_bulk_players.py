import pytest
from hamcrest import assert_that, equal_to, has_length, greater_than_or_equal_to, empty
from selenium.common.exceptions import TimeoutException

from ui.pages import AddBulkPlayers, Players, Sidebar, Header, Notification
from ui.main.constants import PLATFORM_HEADER_TEXT
from ui.main.helpers import RandomUtilities


@pytest.allure.step('Validate elements on the add bulk players page')
def validate_page(add_bulk_players_page):
    assert_that(add_bulk_players_page.get_page_header().text, equal_to('Players'))
    assert_that(add_bulk_players_page.get_page_subheader().text, equal_to('Create Bulk Players'))
    assert_that(add_bulk_players_page.get_context_text().text, equal_to('Context'))

    assert_that(add_bulk_players_page.get_iterations_label().text, equal_to('Iterations'))
    assert_that(add_bulk_players_page.get_iterations_input().get_attribute('value'), equal_to('10'))

    assert_that(add_bulk_players_page.get_realm_label().text, equal_to('Realm'))
    assert_that(add_bulk_players_page.get_realm_input().text, equal_to('RU'))
    assert_that(add_bulk_players_page.get_realm_drop_down_arrow())
    assert_that(add_bulk_players_page.get_realm_drop_down_list(), has_length(4))

    assert_that(add_bulk_players_page.get_games_label().text, equal_to('Games'))
    assert_that(add_bulk_players_page.get_games_input().text, empty())
    assert_that(add_bulk_players_page.get_games_drop_down_arrow())
    assert_that(add_bulk_players_page.get_games_drop_down_list(), greater_than_or_equal_to(1))  # check this list
    # contains profiles for games in selected studio only (when permissions are in)

    assert_that(add_bulk_players_page.get_game_tag())  # this will change with Contract API
    assert_that(add_bulk_players_page.get_game_tag_exit_button())  # this will change with Contract API

    assert_that(add_bulk_players_page.get_template_text().text, equal_to('Template'))
    assert_that(add_bulk_players_page.get_info_box())
    assert_that(add_bulk_players_page.get_info_box_button())
    assert_that(add_bulk_players_page.get_info_box_strong().text, equal_to('Info'))

    assert_that(add_bulk_players_page.get_login_label().text, equal_to('Login'))
    assert_that(add_bulk_players_page.get_login_input())
    assert_that(add_bulk_players_page.get_password_label().text, equal_to('Password'))
    assert_that(add_bulk_players_page.get_password_input())
    assert_that(add_bulk_players_page.get_name_label().text, equal_to('Name'))
    assert_that(add_bulk_players_page.get_name_input())

    assert_that(add_bulk_players_page.get_authentication_method_label().text, equal_to('Authentication Method'))
    assert_that(add_bulk_players_page.get_authentication_method_input().text, equal_to('basic'))
    assert_that(add_bulk_players_page.get_authentication_method_drop_down_arrow())
    assert_that(add_bulk_players_page.get_authentication_method_drop_down_list(), has_length(3))

    assert_that(add_bulk_players_page.get_ip_label().text, equal_to('IP'))
    assert_that(add_bulk_players_page.get_ip_input().get_attribute('value'), equal_to('127.0.0.1'))  # this field will
    # be empty soon

    assert_that(add_bulk_players_page.get_save_button().text, equal_to('Save'))
    assert_that(add_bulk_players_page.get_cancel_button().text, equal_to('Cancel'))


@pytest.allure.step('Validate elements on the add bulk players sidebar page')
def validate_add_bulk_players_sidebar_page(sidebar_page):
    assert_that(sidebar_page.get_studios_button().text, equal_to('Studios'))
    assert_that(sidebar_page.get_titles_button().text, equal_to('Titles'))
    assert_that(sidebar_page.get_players_button().text, equal_to('Players'))
    assert_that(sidebar_page.get_panel(), has_length(3))


@pytest.allure.step('Validate elements on the add bulk players header page')
def validate_add_bulk_players_header_page(header_page):
    assert_that(header_page.get_home_button())
    assert_that(header_page.get_top_bar_header().text, equal_to(PLATFORM_HEADER_TEXT))
    assert_that(header_page.get_settings_icon())
    assert_that(header_page.get_drop_down_menu())
    assert_that(header_page.get_drop_down_options(), has_length(2))


@pytest.fixture
def setup(config, browser, steps):
    add_bulk_players_page = AddBulkPlayers(browser)
    players_page = Players(browser)
    sidebar_page = Sidebar(browser)
    header_page = Header(browser)

    steps.login(config.admin.username, config.admin.password)
    steps.navigate_to_titles_page(config.data.TEST_STUDIO.CODE)
    sidebar_page.click_players_button()
    players_page.wait_for_page_load()
    players_page.click_create_bulk_button()
    add_bulk_players_page.wait_for_page_load()

    yield add_bulk_players_page, players_page, sidebar_page, header_page


@pytest.allure.testcase("Validate add bulk players page")
def test_add_bulk_players_page(setup):
    add_bulk_players_page, _, _, _ = setup
    validate_page(add_bulk_players_page)


@pytest.allure.testcase("Validate add bulk players sidebar page")
def test_add_bulk_players_sidebar_page(setup):
    _, _, sidebar_page, _ = setup
    validate_add_bulk_players_sidebar_page(sidebar_page)


@pytest.allure.testcase("Validate add bulk players header page")
def test_add_bulk_players_header_page(setup):
    _, _, _, header_page = setup
    validate_add_bulk_players_header_page(header_page)


@pytest.mark.xfail(reason='PLAT-6031; WGPTX-126; WGPTX-219; PLAT-6305, PLAT-6307; no notification;'
                          'player is being created on all 4 realms (this behavior should change with Contract API)',
                   raises=TimeoutException)
@pytest.allure.testcase("Validate that a player can be added through the UI")
def test_add_bulk_players_functions(config, browser, setup):
    add_bulk_players_page, players_page, sidebar_page, _ = setup
    notification = Notification(browser)

    add_bulk_players_page.type_iterations_input(5)
    add_bulk_players_page.click_realm_drop_down_arrow()
    add_bulk_players_page.wait_for_realm_list_item_to_be_clickable('SG')
    add_bulk_players_page.click_realm_drop_down_list_item('SG')

    add_bulk_players_page.click_game_tag_exit_button()
    add_bulk_players_page.type_games_input(config.data.TEST_TITLE.CODE)

    unique_id = RandomUtilities.create_unique_id_lowercase()
    email = '{}_{{{{idx}}}}@qa.wargaming.net'.format(unique_id)
    password = '{}'.format(unique_id)
    base_name = 'test_player_{}'.format(unique_id)
    name_with_idx = '{}_{{{{idx}}}}'.format(base_name)

    add_bulk_players_page.type_login_input(email)
    add_bulk_players_page.type_password_input(password)
    add_bulk_players_page.type_name_input(name_with_idx)
    add_bulk_players_page.click_save_button()

    players_page.wait_for_page_load()

    notification.wait_for_notification_message()
    assert_that(notification.get_notification_message().text,
                equal_to('Bulk Players: {} successfully created!'.format(base_name)))

    players_page.type_value_input(base_name)
    players_page.click_add_button()
    players_page.wait_for_player_list_load()
    assert_that(players_page.get_player_list(), has_length(5))

    player_names = [i.find_elements_by_tag_name('td')[1].text for i in players_page.get_player_list()]
    for idx, player_name in enumerate(player_names):
        assert_that(player_name, equal_to('{}_{}'.format(base_name, idx)))

    assert_that(players_page.get_player_realm(base_name).text, equal_to('SG'))
    assert_that(
        players_page.get_player_game(config.data.TEST_TITLE.CODE))  # for now it will be the code (not friendly_name)

    # Right now the player is created on all 4 realms even if the user selects just one realm upon creation. The code
    # below checks for this behavior. But this will change in the future, the player will be created on the selected
    # environment only. Then we should adjust that part of the code.
    players_page.click_field_drop_down_list_arrow()
    players_page.wait_for_field_list_item_to_be_clickable('Realm')
    players_page.click_field_drop_down_list_item('Realm')
    players_page.click_value_drop_down_list_arrow()
    players_page.wait_for_value_realm_item_to_be_clickable('NA')
    players_page.click_realm('NA')
    players_page.click_add_button()
    players_page.wait_for_player_list_load()
    assert_that(players_page.get_player_list(), has_length(5))

    player_names = [i.find_elements_by_tag_name('td')[1].text for i in players_page.get_player_list()]
    for idx, player_name in enumerate(player_names):
        assert_that(player_name, equal_to('{}_{}'.format(base_name, idx)))

    assert_that(players_page.get_player_realm(base_name).text, equal_to('NA'))
    assert_that(
        players_page.get_player_game(config.data.TEST_TITLE.CODE))  # for now it will be the code (not friendly_name)


@pytest.allure.testcase("Ensure cancel button returns the user to the players page")
def test_add_bulk_players_cancel_button_returns_to_players_page(setup):
    add_bulk_players_page, players_page, _, _ = setup

    add_bulk_players_page.click_cancel_button()

    players_page.wait_for_page_load()
    assert_that(players_page.get_player_list(), greater_than_or_equal_to(1))


@pytest.allure.testcase("Ensure page header button returns the user to the players page")
def test_add_bulk_players_header_button_returns_to_players_page(setup):
    add_bulk_players_page, players_page, _, _ = setup

    add_bulk_players_page.click_page_header()

    players_page.wait_for_page_load()
    assert_that(players_page.get_player_list(), greater_than_or_equal_to(1))
