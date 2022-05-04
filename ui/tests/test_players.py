import pytest
from hamcrest import assert_that, equal_to, greater_than_or_equal_to, has_length, empty, none, contains_string
from selenium.common.exceptions import NoSuchElementException

from ui.pages import Players, Sidebar, Header, AddPlayer, AddBulkPlayers, EditPlayer, ActionsMenu, Notification
from ui.main.constants import PLATFORM_HEADER_TEXT
from ui.main.helpers import RandomUtilities


@pytest.allure.step('Validate elements on the players page')
def validate_page(players_page, config):
    assert_that(players_page.get_page_header().text, equal_to('Players'))
    assert_that(players_page.get_create_button().text, equal_to('Create'))
    assert_that(players_page.get_create_bulk_button().text, equal_to('Create Bulk'))

    assert_that(players_page.get_info_box())
    assert_that(players_page.get_info_box_exit_button())
    assert_that(players_page.get_info_box_strong().text, equal_to('Players'))

    assert_that(players_page.get_field_label().text, equal_to('Field'))
    assert_that(players_page.get_field_input().text, equal_to('Name'))  # this is a default value for now
    assert_that(players_page.get_field_drop_down_list_arrow())
    assert_that(players_page.get_field_drop_down_list(), has_length(3))  # the list will change with contracts API
    assert_that(players_page.get_operator_label().text, equal_to('Operator'))
    assert_that(players_page.get_operator_input().text, equal_to('starts with (.*)'))
    assert_that(players_page.get_operator_drop_down_list_arrow())
    assert_that(players_page.get_value_label().text, equal_to('Value'))
    assert_that(players_page.get_value_input().text, empty())
    assert_that(players_page.get_add_button().is_enabled(), equal_to(False))

    players_page.click_field_drop_down_list_arrow()
    players_page.wait_for_field_list_item_to_be_clickable('Realm')
    players_page.click_field_drop_down_list_item('Realm')
    assert_that(players_page.get_field_label().text, equal_to('Field'))
    assert_that(players_page.get_field_input().text, equal_to('Realm'))
    assert_that(players_page.get_operator_label().text, equal_to('Operator'))
    assert_that(players_page.get_operator_input().text, equal_to('equal (=)'))
    assert_that(players_page.get_operator_drop_down_list_arrow())
    assert_that(players_page.get_value_label().text, equal_to('Value'))
    assert_that(players_page.get_value_input().text, equal_to('EU'))  # this is a default value for now
    assert_that(players_page.get_value_drop_down_list_arrow())
    assert_that(players_page.get_value_drop_down_list(), has_length(4))
    assert_that(players_page.get_add_button().is_enabled(), equal_to(True))

    players_page.click_field_drop_down_list_arrow()
    players_page.wait_for_field_list_item_to_be_clickable('Game')
    players_page.click_field_drop_down_list_item('Game')
    assert_that(players_page.get_field_label().text, equal_to('Field'))
    assert_that(players_page.get_field_input().text, equal_to('Game'))
    assert_that(players_page.get_operator_label().text, equal_to('Operator'))
    assert_that(players_page.get_operator_input().text, equal_to('in (in)'))
    assert_that(players_page.get_operator_drop_down_list_arrow())
    assert_that(players_page.get_value_label().text, equal_to('List'))
    assert_that(players_page.get_value_input().text, empty())
    assert_that(players_page.get_value_drop_down_list_arrow())
    assert_that(players_page.get_value_drop_down_list(), greater_than_or_equal_to(1))  # check this list contains
    # profiles for games in selected studio only (when permissions are in)
    assert_that(players_page.get_add_button().is_enabled(), equal_to(False))

    assert_that(players_page.get_name_tag().text, contains_string("Name"))
    assert_that(players_page.get_name_tag_exit_button())
    assert_that(players_page.get_realm_tag().text, contains_string("Realm"))
    assert_that(players_page.get_realm_tag_exit_button())
    assert_that(players_page.get_game_tag().text, contains_string("Game"))  # game tags appear in two places right now
    # which will be fixed
    assert_that(players_page.get_game_tag_exit_button())

    assert_that(players_page.get_filter_button().text, equal_to('Filter'))
    assert_that(players_page.get_reset_button().text, equal_to('Reset'))

    assert_that(players_page.get_showing_results_text().text, equal_to('Showing Results'))  # the text might include
    # the count in the future

    assert_that(players_page.get_table_column_header('id').text, equal_to('ID'))
    assert_that(players_page.get_table_column_header('name').text, equal_to('Name'))
    assert_that(players_page.get_table_column_header('realm').text, equal_to('Realm'))
    assert_that(players_page.get_table_column_header('games').text, equal_to('Games'))
    assert_that(players_page.get_table_column_header('actions').text, equal_to('Actions'))
    assert_that(players_page.get_table_column_list(), has_length(5))

    assert_that(players_page.get_player_id(config.data.TEST_PLAYER.NAME))
    assert_that(players_page.get_player_name(config.data.TEST_PLAYER.NAME))
    assert_that(players_page.get_player_realm(config.data.TEST_PLAYER.NAME))
    assert_that(players_page.get_player_game(config.data.TEST_PLAYER.NAME))
    assert_that(players_page.get_player_actions_button(config.data.TEST_PLAYER.NAME))
    assert_that(players_page.get_player_list(), greater_than_or_equal_to(1))


@pytest.allure.step('Validate elements on the players sidebar page')
def validate_players_sidebar_page(sidebar_page):
    assert_that(sidebar_page.get_studios_button().text, equal_to('Studios'))
    assert_that(sidebar_page.get_titles_button().text, equal_to('Titles'))
    assert_that(sidebar_page.get_players_button().text, equal_to('Players'))
    assert_that(sidebar_page.get_panel(), has_length(3))


@pytest.allure.step('Validate elements on the players header page')
def validate_players_header_page(header_page):
    assert_that(header_page.get_home_button())
    assert_that(header_page.get_top_bar_header().text, equal_to(PLATFORM_HEADER_TEXT))
    assert_that(header_page.get_settings_icon())
    assert_that(header_page.get_drop_down_menu())
    assert_that(header_page.get_drop_down_options(), has_length(2))


@pytest.allure.step('Validate elements on the players actions menu')
def validate_players_actions_menu(actions_menu, config):
    assert_that(actions_menu.get_actions_remove_by_name(config.data.TEST_PLAYER.NAME).text, equal_to('Delete'))
    assert_that(actions_menu.get_actions_menu_list_by_name(config.data.TEST_PLAYER.NAME), has_length(1))


@pytest.fixture
def setup(config, browser, steps):
    players_page = Players(browser)
    sidebar_page = Sidebar(browser)
    header_page = Header(browser)
    actions_menu = ActionsMenu(browser)

    steps.login(config.admin.username, config.admin.password)
    steps.navigate_to_titles_page(config.data.TEST_STUDIO.CODE)
    sidebar_page.click_players_button()
    players_page.wait_for_page_load()

    yield players_page, sidebar_page, header_page, actions_menu


@pytest.fixture
def clean_up(setup, browser, config):
    yield
    players_page, _, _, actions_menu = setup
    add_player_page = AddPlayer(browser)
    notification = Notification(browser)
    edit_player_page = EditPlayer(browser)

    players_page.click_create_button()
    add_player_page.wait_for_page_load()

    unique_id = RandomUtilities.create_unique_id_lowercase()

    add_player_page.type_login_input('test_player@qa.wargaming.net')
    add_player_page.type_password_input('{}'.format(unique_id))
    add_player_page.type_name_input('test_player')
    add_player_page.click_save_button()

    notification.wait_for_notification_message()
    assert_that(notification.get_notification_message().text, equal_to('Player: test_player successfully created!'))

    edit_player_page.wait_for_page_load()
    assert_that(edit_player_page.get_name_input().get_attribute('value'), equal_to('test_player'))

    edit_player_page.click_page_header()
    players_page.wait_for_page_load()
    assert_that(players_page.get_player_name('test_player'))


@pytest.mark.xfail(reason='PLAT-6212, PLAT-6229, PLAT-6305', raises=NoSuchElementException)
@pytest.allure.testcase('Validate players page')
def test_players_page(setup, config):
    players_page, _, _, _ = setup
    validate_page(players_page, config)


@pytest.allure.testcase('Validate players sidebar page')
def test_players_sidebar_page(setup):
    _, sidebar_page, _, _ = setup
    validate_players_sidebar_page(sidebar_page)


@pytest.allure.testcase('Validate players header page')
def test_players_header_page(setup):
    _, _, header_page, _ = setup
    validate_players_header_page(header_page)


@pytest.mark.xfail(reason='PLAT-6305', raises=NoSuchElementException)
@pytest.allure.testcase('Validate players actions menu')
def test_players_actions_menu(setup, config):
    players_page, _, _, actions_menu = setup

    players_page.click_player_actions_button(config.data.TEST_PLAYER.NAME)
    actions_menu.wait_for_actions_menu_load(config.data.TEST_PLAYER.NAME)
    validate_players_actions_menu(actions_menu, config)


@pytest.allure.testcase("Validate create button leads the user to the create player page")
def test_players_add_button_leads_to_add_player_page(setup, browser):
    players_page, _, _, _ = setup
    add_player_page = AddPlayer(browser)

    players_page.click_create_button()

    add_player_page.wait_for_page_load()
    assert_that(add_player_page.get_save_button())


@pytest.allure.testcase("Validate create bulk button leads the user to the create bulk players page")
def test_players_add_bulk_button_leads_to_add_bulk_players_page(setup, browser):
    players_page, _, _, _ = setup
    add_bulk_players_page = AddBulkPlayers(browser)

    players_page.click_create_bulk_button()

    add_bulk_players_page.wait_for_page_load()
    assert_that(add_bulk_players_page.get_save_button())


@pytest.mark.xfail(reason='PLAT-6305', raises=NoSuchElementException)
@pytest.allure.testcase("Validate add button is working properly when selecting Name from the Field")
def test_players_add_button_for_name(setup, config):
    players_page, _, _, _ = setup

    players_page.type_value_input('test')
    players_page.click_add_button()
    assert_that(players_page.get_player_list(), greater_than_or_equal_to(1))
    assert_that(players_page.get_player_name(config.data.TEST_PLAYER.NAME))


@pytest.mark.xfail(reason='PLAT-6305', raises=NoSuchElementException)
@pytest.allure.testcase("Validate add button is working properly when selecting Realm from the Field")
def test_players_add_button_for_realm(setup, config):
    players_page, _, _, _ = setup

    players_page.click_field_drop_down_list_arrow()
    players_page.click_field_drop_down_list_item('Realm')
    players_page.click_value_drop_down_list_arrow()
    players_page.click_realm('RU')
    players_page.click_add_button()
    assert_that(players_page.get_player_list(), greater_than_or_equal_to(1))
    assert_that(players_page.get_player_realm(config.data.TEST_PLAYER.NAME), equal_to('RU'))


@pytest.mark.xfail(reason='PLAT-6305, WGPTX-126', raises=NoSuchElementException)
@pytest.allure.testcase("Validate add button is working properly when selecting Game from the Field")
def test_players_add_button_for_game(setup, config):
    players_page, _, _, _ = setup

    players_page.click_field_drop_down_list_arrow()
    players_page.click_field_drop_down_list_item('Game')
    players_page.click_value_drop_down_list_arrow()
    players_page.click_game(config.data.TEST_TITLE.CODE)
    players_page.click_add_button()
    assert_that(players_page.get_player_list(), greater_than_or_equal_to(1))
    assert_that(players_page.get_player_game(config.data.TEST_PLAYER.NAME), equal_to(config.data.TEST_TITLE.CODE))


@pytest.allure.testcase("Make sure validation messages show up when removing tags")
def test_players_validation_messages_show_up_when_removing_tags(setup, config):
    players_page, _, _, _ = setup

    players_page.click_name_tag_exit_button()
    players_page.click_realm_tag_exit_button()
    players_page.click_game_tag_exit_button()
    players_page.wait_for_validation_box()
    assert_that(players_page.get_validation_box().text, contains_string('This field is required.'))
    assert_that(players_page.get_validation_box_name_strong().text, equal_to('Name'))
    assert_that(players_page.get_validation_box_realm_strong().text, equal_to('Realm'))
    # assert_that(players_page.get_validation_box_game_strong().text, equal_to('Game'))  # this isn't showing up;
    # Cyprus is waiting for Contract API to manage error messages better

    players_page.click_validation_box_exit_button()
    players_page.wait_for_validation_box_to_disappear()
    assert_that(players_page.get_no_players_found().text, equal_to('No Players found.'))


@pytest.allure.testcase("Test reset button removes all selections made, plus tags")
def test_players_reset_button_resets_everything_to_default(setup, config):
    players_page, _, _, _ = setup

    players_page.click_reset_button()
    players_page.wait_for_validation_box()
    assert_that(players_page.get_validation_box())
    assert_that(players_page.get_no_players_found().text, equal_to('No Players found.'))

    assert_that(players_page.get_field_input().text, equal_to('Name'))
    assert_that(players_page.get_operator_input().text, equal_to('starts with (.*)'))
    assert_that(players_page.get_value_input().text, empty())
    assert_that(players_page.get_add_button().is_enabled(), equal_to(False))


@pytest.mark.xfail(reason='PLAT-6229', raises=NoSuchElementException)
@pytest.allure.testcase("Validate info box exit button closes the info box")
def test_players_info_box_exit_button_closes_the_box(setup):
    players_page, _, _, _ = setup

    players_page.click_info_box_exit_button()
    players_page.wait_for_info_box_to_disappear()


@pytest.mark.xfail(reason='PLAT-6305', raises=NoSuchElementException)
@pytest.allure.testcase("Validate clicking on the player id leads the user to the player account page")
def test_players_click_on_player_id_leads_to_edit_player_page(setup, browser, config):
    players_page, _, _, _ = setup
    edit_player_page = EditPlayer(browser)

    players_page.click_player_id(config.data.TEST_PLAYER.NAME)

    edit_player_page.wait_for_page_load()
    assert_that(edit_player_page.get_create_game_button())


@pytest.mark.xfail(reason='PLAT-6305, Notifications', raises=NoSuchElementException)
@pytest.allure.testcase("Validate the player can be removed")
def test_players_can_remove_player(setup, browser, config, clean_up):
    players_page, _, _, actions_menu = setup
    notification = Notification(browser)

    players_page.click_player_actions_button(config.data.TEST_PLAYER.NAME)
    actions_menu.wait_for_actions_menu_load(config.data.TEST_PLAYER.NAME)
    actions_menu.click_actions_remove(config.data.TEST_PLAYER.NAME)

    notification.wait_for_notification_message()
    assert_that(notification.get_notification_message().text, equal_to('Player: test_player successfully deleted!'))

    player_list = players_page.get_player_list()
    player = next((player for player in player_list
                   if player == config.data.TEST_PLAYER.NAME), None)
    assert_that(player, none(), 'The player that was removed is still present')
