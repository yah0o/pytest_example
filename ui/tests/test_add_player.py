import pytest
from hamcrest import assert_that, equal_to, has_length, greater_than_or_equal_to, empty
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from ui.main.expected_conditions.expected_conditions import exact_text

from ui.pages.add_player_page.locators import AddPlayerLocators
from ui.pages import AddPlayer, Players, Sidebar, Notification, Header, EditPlayer
from ui.main.helpers import RandomUtilities
from ui.main.constants import PLATFORM_HEADER_TEXT, DEFAULT_PAGE_TIMEOUT


@pytest.allure.step('Validate elements on the add player page')
def validate_page(add_player_page):
    assert_that(add_player_page.get_page_header().text, equal_to('Players'))
    assert_that(add_player_page.get_page_subheader().text, equal_to('Create Player'))

    assert_that(add_player_page.get_realm_label().text, equal_to('Realm'))
    assert_that(add_player_page.get_realm_input().text, equal_to('RU'))
    assert_that(add_player_page.get_realm_drop_down_arrow())
    assert_that(add_player_page.get_realm_drop_down_list(), has_length(4))

    assert_that(add_player_page.get_games_label().text, equal_to('Games'))
    assert_that(add_player_page.get_games_input().text, empty())
    assert_that(add_player_page.get_games_drop_down_arrow())
    assert_that(add_player_page.get_games_drop_down_list(), greater_than_or_equal_to(1))  # check this list contains
    # profiles for games in selected studio only (when permissions are in)

    assert_that(add_player_page.get_game_tag())  # this will change with Contract API
    assert_that(add_player_page.get_game_tag_exit_button())  # this will change with Contract API

    assert_that(add_player_page.get_login_label().text, equal_to('Login'))
    assert_that(add_player_page.get_login_input())
    assert_that(add_player_page.get_password_label().text, equal_to('Password'))
    assert_that(add_player_page.get_password_input())
    assert_that(add_player_page.get_name_label().text, equal_to('Name'))
    assert_that(add_player_page.get_name_input())

    assert_that(add_player_page.get_authentication_method_label().text, equal_to('Authentication Method'))
    assert_that(add_player_page.get_authentication_method_input().text, equal_to('basic'))
    assert_that(add_player_page.get_authentication_method_drop_down_arrow())
    assert_that(add_player_page.get_authentication_method_drop_down_list(), has_length(3))

    assert_that(add_player_page.get_ip_label().text, equal_to('IP'))
    assert_that(add_player_page.get_ip_input().get_attribute('value'), equal_to('127.0.0.1'))  # this field will
    # be empty soon

    assert_that(add_player_page.get_save_button().text, equal_to('Save'))
    assert_that(add_player_page.get_cancel_button().text, equal_to('Cancel'))


@pytest.allure.step('Validate elements on the add player sidebar page')
def validate_add_player_sidebar_page(sidebar_page):
    assert_that(sidebar_page.get_studios_button().text, equal_to('Studios'))
    assert_that(sidebar_page.get_titles_button().text, equal_to('Titles'))
    assert_that(sidebar_page.get_players_button().text, equal_to('Players'))
    assert_that(sidebar_page.get_panel(), has_length(3))


@pytest.allure.step('Validate elements on the add player header page')
def validate_add_player_header_page(header_page):
    assert_that(header_page.get_home_button())
    assert_that(header_page.get_top_bar_header().text, equal_to(PLATFORM_HEADER_TEXT))
    assert_that(header_page.get_settings_icon())
    assert_that(header_page.get_drop_down_menu())
    assert_that(header_page.get_drop_down_options(), has_length(2))


@pytest.fixture
def setup(config, browser, steps):
    add_player_page = AddPlayer(browser)
    players_page = Players(browser)
    sidebar_page = Sidebar(browser)
    header_page = Header(browser)

    steps.login(config.admin.username, config.admin.password)
    steps.navigate_to_titles_page(config.data.TEST_STUDIO.CODE)
    sidebar_page.click_players_button()
    players_page.wait_for_page_load()
    players_page.click_create_button()
    add_player_page.wait_for_page_load()

    yield add_player_page, players_page, sidebar_page, header_page


@pytest.allure.testcase("Validate add player page")
def test_add_player_page(setup):
    add_player_page, _, _, _ = setup
    validate_page(add_player_page)


@pytest.allure.testcase("Validate add player sidebar page")
def test_add_player_sidebar_page(setup):
    _, _, sidebar_page, _ = setup
    validate_add_player_sidebar_page(sidebar_page)


@pytest.allure.testcase("Validate add player header page")
def test_add_player_header_page(setup):
    _, _, _, header_page = setup
    validate_add_player_header_page(header_page)


@pytest.mark.xfail(reason='PLAT-6031; WGPTX-126; WGPTX-219; PLAT-6306, PLAT-6305; no notification;'
                          'player is being created on all 4 realms (this behavior should change with Contract API)',
                   raises=TimeoutException)
@pytest.allure.testcase("Validate that a player can be added through the UI")
def test_add_player_functions(config, browser, setup):
    add_player_page, players_page, sidebar_page, _ = setup
    notification = Notification(browser)
    edit_player_page = EditPlayer(browser)

    add_player_page.click_realm_drop_down_arrow()
    add_player_page.wait_for_realm_list_item_to_be_clickable('SG')
    add_player_page.click_realm_drop_down_list_item('SG')

    add_player_page.click_game_tag_exit_button()
    add_player_page.type_games_input(config.data.TEST_TITLE.CODE)

    unique_id = RandomUtilities.create_unique_id_lowercase()
    email = '{}@qa.wargaming.net'.format(unique_id)
    password = '{}'.format(unique_id)
    name = 'test_player_{}'.format(unique_id)

    add_player_page.type_login_input(email)
    add_player_page.type_password_input(password)
    add_player_page.type_name_input(name)
    add_player_page.click_save_button()

    notification.wait_for_notification_message()
    assert_that(notification.get_notification_message().text, equal_to('Player: {} successfully created!'.format(name)))

    edit_player_page.wait_for_page_load()
    assert_that(edit_player_page.get_id_input().is_enabled(), equal_to(False))
    assert_that(edit_player_page.get_name_input().is_enabled(), equal_to(False))
    assert_that(edit_player_page.get_name_input().get_attribute('value'), equal_to(name))
    assert_that(edit_player_page.get_realm_input().is_enabled(), equal_to(False))
    assert_that(edit_player_page.get_realm_input().get_attribute('value'), equal_to('SG'))
    assert_that(
        edit_player_page.get_game(config.data.TEST_TITLE.CODE))  # for now it will be the code (not friendly_name)
    edit_player_page.click_page_header()
    players_page.wait_for_page_load()
    assert_that(players_page.get_player_name(name))
    assert_that(players_page.get_player_realm().text, equal_to('SG'))
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
    assert_that(players_page.get_player_name(name))
    assert_that(players_page.get_player_realm().text, equal_to('NA'))
    assert_that(
        players_page.get_player_game(config.data.TEST_TITLE.CODE))  # for now it will be the code (not friendly_name)


@pytest.mark.xfail(reason='PLAT-notifications being displayed at the wrong place', raises=TimeoutException)
@pytest.allure.testcase("Ensure player won't get created if email is already taken")
def test_add_player_does_not_create_player_if_email_already_taken(config, browser, setup):
    add_player_page, players_page, _, _ = setup
    notification = Notification(browser)

    unique_id = RandomUtilities.create_unique_id_lowercase()
    email = '{}@qa.wargaming.net'.format(config.admin.username)
    password = '{}'.format(unique_id)
    name = 'test_player_{}'.format(unique_id)

    add_player_page.type_login_input(email)
    add_player_page.type_password_input(password)
    add_player_page.type_name_input(name)
    add_player_page.click_save_button()

    notification.wait_for_notification_message()
    assert_that(
        notification.get_notification_message().text,
        equal_to("\"The login '{}' already taken, creation impossible\"".format(
            email
        ))
    )

    add_player_page.click_cancel_button()
    players_page.wait_for_page_load()
    player_list = players_page.get_player_list()

    count = 0
    for player in player_list:
        if name in player.get_attribute('innerHTML'):
            count = count + 1
    assert_that(count, equal_to(1))


@pytest.mark.xfail(reason='PLAT-notifications being displayed at the wrong place', raises=TimeoutException)
@pytest.allure.testcase("Ensure player won't get created if name is already taken")
def test_add_player_does_not_create_player_if_name_already_taken(config, browser, setup):
    add_player_page, players_page, _, _ = setup
    notification = Notification(browser)

    unique_id = RandomUtilities.create_unique_id_lowercase()
    email = '{}@qa.wargaming.net'.format(unique_id)
    password = '{}'.format(unique_id)
    name = '{}'.format(config.data.TEST_PLAYER.NAME)

    add_player_page.type_login_input(email)
    add_player_page.type_password_input(password)
    add_player_page.type_name_input(name)
    add_player_page.click_save_button()

    notification.wait_for_notification_message()
    assert_that(
        notification.get_notification_message().text,
        equal_to("\"The name '{}' already taken, creation impossible\"".format(
            name
        ))
    )

    add_player_page.click_cancel_button()
    players_page.wait_for_page_load()
    player_list = players_page.get_player_list()

    count = 0
    for player in player_list:
        if name in player.get_attribute('innerHTML'):
            count = count + 1
    assert_that(count, equal_to(1))


@pytest.allure.testcase("Ensure cancel button returns the user to the players page")
def test_add_player_cancel_button_returns_to_players_page(setup):
    add_player_page, players_page, _, _ = setup

    add_player_page.click_cancel_button()

    players_page.wait_for_page_load()
    assert_that(players_page.get_player_list(), greater_than_or_equal_to(1))


@pytest.allure.testcase("Ensure page header button returns the user to the players page")
def test_add_player_header_button_returns_to_players_page(setup):
    add_player_page, players_page, _, _ = setup

    add_player_page.click_page_header()

    players_page.wait_for_page_load()
    assert_that(players_page.get_player_list(), greater_than_or_equal_to(1))


@pytest.mark.xfail(reason='PLAT-6030 and notifications being displayed at the wrong place', raises=AssertionError)
@pytest.allure.testcase("Ensure player won't get created when login input is invalid")
@pytest.mark.parametrize('invalid_email', ['bad@email', 'bad@', 'bad@.', 'bad.email', 'bad@.com', 'bad@e.c'])
def test_add_player_does_not_create_player_when_login_is_invalid(invalid_email, setup):
    add_player_page, _, _, _ = setup

    unique_id = RandomUtilities.create_unique_id_lowercase()
    password = '{}'.format(unique_id)
    name = 'test_player_{}'.format(unique_id)

    add_player_page.type_login_input(invalid_email)
    add_player_page.type_password_input(password)
    add_player_page.type_name_input(name)
    add_player_page.click_save_button()
    add_player_page.wait_for_login_invalid_message()
    assert_that(add_player_page.get_login_invalid_message().text, equal_to('Enter a valid value.'))

    assert_that(add_player_page.get_save_button().is_enabled(), equal_to(False))


@pytest.mark.xfail(reason='PLAT-6030 and notifications being displayed at the wrong place', raises=AssertionError)
@pytest.allure.testcase("Ensure player won't get created when password input is invalid")
def test_add_player_does_not_create_player_when_password_is_invalid(setup, browser):
    add_player_page, _, _, _ = setup

    unique_id = RandomUtilities.create_unique_id_lowercase()
    email = '{}@qa.wargaming.net'.format(unique_id)
    name = 'test_player_{}'.format(unique_id)

    add_player_page.type_login_input(email)
    add_player_page.type_password_input('!')
    add_player_page.type_name_input(name)
    add_player_page.click_save_button()
    add_player_page.wait_for_password_invalid_message()
    assert_that(add_player_page.get_password_invalid_message().text, equal_to('Ensure this field has at least '
                                                                              '6 characters.'))
    add_player_page.type_password_input('!!!!!!')
    add_player_page.click_save_button()

    WebDriverWait(browser, DEFAULT_PAGE_TIMEOUT).until(
        exact_text(AddPlayerLocators.PASSWORD_INVALID_MESSAGE, 'Enter a valid value.'),
        'Password invalid message did not display'
    )

    assert_that(add_player_page.get_password_invalid_message().text, equal_to('Enter a valid value.'))

    assert_that(add_player_page.get_save_button().is_enabled(), equal_to(False))


@pytest.mark.xfail(reason='PLAT-6030 and notifications being displayed at the wrong place', raises=AssertionError)
@pytest.allure.testcase("Ensure player won't get created when name input is invalid")
def test_add_player_does_not_create_player_when_name_is_invalid(setup, browser):
    add_player_page, _, _, _ = setup

    unique_id = RandomUtilities.create_unique_id_lowercase()
    email = '{}@qa.wargaming.net'.format(unique_id)
    password = '{}'.format(unique_id)

    add_player_page.type_login_input(email)
    add_player_page.type_password_input(password)
    add_player_page.type_name_input('!')
    add_player_page.click_save_button()
    add_player_page.wait_for_name_invalid_message()
    assert_that(add_player_page.get_name_invalid_message().text, equal_to('Enter a valid value.\nEnsure this value '
                                                                          'has at least 3 characters (it has 1).'))
    add_player_page.type_name_input('!!!')
    add_player_page.click_save_button()

    WebDriverWait(browser, DEFAULT_PAGE_TIMEOUT).until(
        exact_text(AddPlayerLocators.NAME_INVALID_MESSAGE, 'Enter a valid value.'),
        'Name invalid message did not display'
    )

    assert_that(add_player_page.get_name_invalid_message().text, equal_to('Enter a valid value.'))

    assert_that(add_player_page.get_save_button().is_enabled(), equal_to(False))


@pytest.mark.xfail(reason='PLAT-6030', raises=AssertionError)
@pytest.allure.testcase("Ensure the player is not being created when creating with empty input data")
@pytest.mark.parametrize('email, password, name', [(email_data, password_data, name_data)
                                                   for email_data in ['', 'admin@qa.wargaming.net']
                                                   for password_data in ['', 'password']
                                                   for name_data in ['', 'name']][:-1])
def test_add_player_does_not_create_player_when_empty_input_data(setup, email, password, name):
    add_player_page, _, _, _ = setup

    add_player_page.type_login_input(email)
    add_player_page.type_password_input(password)
    add_player_page.type_name_input(name)

    assert_that(add_player_page.get_save_button().is_enabled(), equal_to(False))
