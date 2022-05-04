import random
import pytest
from hamcrest import assert_that, equal_to, greater_than_or_equal_to, has_length, none
from selenium.common.exceptions import NoSuchElementException

from ui.pages import Players, Sidebar, Header, EditPlayer, AddGameRegistration, Notification
from ui.main.constants import PLATFORM_HEADER_TEXT


@pytest.allure.step('Validate elements on the add game registration page')
def validate_page(add_game_registration_page):
    assert_that(add_game_registration_page.get_page_header().text, equal_to('Players'))
    assert_that(add_game_registration_page.get_page_subheader_1())
    assert_that(add_game_registration_page.get_page_subheader_2().text, equal_to('Create Game Registration'))
    assert_that(add_game_registration_page.get_wgid_label().text, equal_to('WGID'))
    assert_that(add_game_registration_page.get_wgid_input())
    assert_that(add_game_registration_page.get_realm_label().text, equal_to('Realm'))
    assert_that(add_game_registration_page.get_realm_input())
    assert_that(add_game_registration_page.get_realm_drop_down_arrow())
    assert_that(add_game_registration_page.get_game_label().text, equal_to('Game'))
    assert_that(add_game_registration_page.get_game_input())
    assert_that(add_game_registration_page.get_game_drop_down_arrow())
    assert_that(add_game_registration_page.get_game_drop_down_list(), greater_than_or_equal_to(1))
    assert_that(add_game_registration_page.get_save_button().text, equal_to('Save'))
    assert_that(add_game_registration_page.get_cancel_button().text, equal_to('Cancel'))


@pytest.allure.step('Validate elements on the add game registration sidebar page')
def validate_add_game_registration_sidebar_page(sidebar_page):
    assert_that(sidebar_page.get_studios_button().text, equal_to('Studios'))
    assert_that(sidebar_page.get_titles_button().text, equal_to('Titles'))
    assert_that(sidebar_page.get_players_button().text, equal_to('Players'))
    assert_that(sidebar_page.get_panel(), has_length(3))


@pytest.allure.step('Validate elements on the add game registration header page')
def validate_add_game_registration_header_page(header_page):
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
    add_game_registration_page = AddGameRegistration(browser)

    steps.login(config.admin.username, config.admin.password)
    steps.navigate_to_titles_page(config.data.TEST_STUDIO.CODE)
    sidebar_page.click_players_button()
    players_page.wait_for_page_load()
    players_page.click_player_id(config.data.TEST_PLAYER.NAME)
    edit_player_page.wait_for_page_load()
    edit_player_page.click_create_game_button()
    add_game_registration_page.wait_for_page_load()

    yield players_page, edit_player_page, sidebar_page, header_page, add_game_registration_page


@pytest.mark.xfail(reason='PLAT-6305', raises=NoSuchElementException)
@pytest.allure.testcase('Validate add game registration page')
def test_add_game_registration_page(setup, config):
    _, _, _, _, add_game_registration_page = setup
    validate_page(add_game_registration_page, config)


@pytest.mark.xfail(reason='PLAT-6305', raises=NoSuchElementException)
@pytest.allure.testcase('Validate add game registration sidebar page')
def test_add_game_registration_sidebar_page(setup):
    _, _, sidebar_page, _, _ = setup
    validate_add_game_registration_sidebar_page(sidebar_page)


@pytest.mark.xfail(reason='PLAT-6305', raises=NoSuchElementException)
@pytest.allure.testcase('Validate add game registration header page')
def test_add_game_registration_header_page(setup):
    _, _, _, header_page, _ = setup
    validate_add_game_registration_header_page(header_page)


@pytest.mark.xfail(reason='PLAT-6281, PLAT-6305, Notification, WGPTX-126', raises=NoSuchElementException)
@pytest.allure.testcase("Validate can add a game registration through the UI")
def test_add_game_registration_functions(browser, setup, config):
    _, edit_player_page, _, _, add_game_registration_page = setup
    notification = Notification(browser)

    # Check fields are disabled
    assert_that(add_game_registration_page.get_wgid_input().is_enabled(), equal_to(False))
    assert_that(add_game_registration_page.get_realm_input().is_enabled(), equal_to(False))

    # Define random game
    drop_down_options = add_game_registration_page.get_game_drop_down_list().options
    game_list_length = len(drop_down_options)
    random_game_index = random.randint(1, game_list_length)
    random_game = drop_down_options[random_game_index].text

    # Add game registration
    add_game_registration_page.click_game_drop_down_arrow()
    add_game_registration_page.wait_for_game_list_item_to_be_clickable_by_index(random_game_index)
    add_game_registration_page.click_game_drop_down_list_item_by_index(random_game_index)
    add_game_registration_page.click_save_button()

    notification.wait_for_notification_message()
    notification_message = notification.get_notification_message()
    assert_that(notification_message.text, equal_to('Game Registration: {} successfully created!'.format(random_game)))

    # Check game was successfully added to player account
    edit_player_page.wait_for_page_load()
    assert_that(edit_player_page.get_game(random_game))

    # Check there are no duplicated games in the player account
    game_list = edit_player_page.get_game_list()
    count = 0
    for game in game_list:
        if random_game.text in game.get_attribute('innerHTML'):
            count = count + 1
    assert_that(count, equal_to(1))

    # Get id and realm values on the edit_player_page for future validation
    id_input = edit_player_page.get_id_input().get_attribute('value')
    edit_player_realm_input = edit_player_page.get_realm_input().get_attribute('value')

    # Make sure the game that was just added to the player account can not be added again
    edit_player_page.click_create_game_button()
    add_game_registration_page.wait_for_page_load()
    add_game_registration_page.click_game_drop_down_arrow()

    game_drop_down_list = add_game_registration_page.get_game_drop_down_list()
    game = next((game for game in game_drop_down_list
                 if game == random_game.text), None)
    assert_that(game, none(), 'The game that was already added is still on the game drop down list')

    # Validate wgid/realm values (on the add_game_registration_page) do equal id/realm values (on the edit_player_page)
    wgid_input = add_game_registration_page.get_wgid_input().get_attribute('value')
    assert_that(wgid_input, equal_to(id_input))

    add_game_registration_realm_input = add_game_registration_page.get_realm_input().get_attribute('value')
    assert_that(add_game_registration_realm_input, equal_to(edit_player_realm_input))


@pytest.mark.xfail(reason='PLAT-6305', raises=NoSuchElementException)
@pytest.allure.testcase("Ensure page header button returns the user to the players page")
def test_add_game_registration_header_button_returns_to_players_page(setup):
    players_page, _, _, _, add_game_registration_page = setup

    add_game_registration_page.click_page_header()

    players_page.wait_for_page_load()
    assert_that(players_page.get_player_list(), greater_than_or_equal_to(1))


@pytest.mark.xfail(reason='PLAT-6305', raises=NoSuchElementException)
@pytest.allure.testcase("Ensure page subheader button returns the user to the edit player page")
def test_add_game_registration_subheader_button_returns_to_edit_player_page(setup):
    _, edit_player_page, _, _, add_game_registration_page = setup

    add_game_registration_page.click_page_subheader_1()

    edit_player_page.wait_for_page_load()
    assert_that(edit_player_page.get_create_game_button())


@pytest.mark.xfail(reason='PLAT-6305', raises=NoSuchElementException)
@pytest.allure.testcase("Validate cancel button leads the user to the edit player page")
def test_add_game_registration_cancel_button_leads_to_edit_player_page(setup, browser):
    _, edit_player_page, _, _, add_game_registration_page = setup

    add_game_registration_page.click_cancel_button()

    edit_player_page.wait_for_page_load()
    assert_that(edit_player_page.get_create_game_button())
