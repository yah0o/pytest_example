import pytest
from selenium.common.exceptions import TimeoutException
from hamcrest import assert_that, equal_to, has_length, greater_than_or_equal_to

from ui.pages import AddTitle, Titles, Sidebar, Notification, Header
from ui.main.helpers import RandomUtilities
from ui.main.constants import CODE_INVALID_INPUT, EMAIL_INVALID_INPUT, PLATFORM_HEADER_TEXT


@pytest.allure.step('Validate elements on the add title page')
def validate_page(add_title_page):
    add_title_text = add_title_page.get_add_title_text()
    assert_that(add_title_text.text, equal_to('Create Title'))

    name_label_text = add_title_page.get_name_label()
    assert_that(name_label_text.text, equal_to('Name'))

    assert_that(add_title_page.get_name_field())

    code_label_text = add_title_page.get_code_label()
    assert_that(code_label_text.text, equal_to('Code'))

    assert_that(add_title_page.get_code_field())

    contact_label_text = add_title_page.get_contact_label()
    assert_that(contact_label_text.text, equal_to('Title Contact email'))

    assert_that(add_title_page.get_contact_field())

    save_button_text = add_title_page.get_save_button()
    assert_that(save_button_text.text, equal_to('Create'))

    cancel_button_text = add_title_page.get_cancel_button()
    assert_that(cancel_button_text.text, equal_to('Cancel'))


@pytest.allure.step('Validate elements on the add title sidebar')
def validate_add_title_sidebar_page(sidebar_page):
    # dashboard_button = sidebar_page.get_dashboard_button()
    # assert_that(dashboard_button.text, equal_to('Dashboard'))

    studios_button = sidebar_page.get_studios_button()
    assert_that(studios_button.text, equal_to('Studios'))

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


@pytest.allure.step('Validate elements on the add title header page')
def validate_add_title_header_page(header_page):
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
    add_title_page = AddTitle(browser)
    titles_page = Titles(browser)
    sidebar_page = Sidebar(browser)
    header_page = Header(browser)

    steps.login(config.admin.username, config.admin.password)
    steps.navigate_to_titles_page(config.data.TEST_STUDIO.CODE)

    config.store.titles_list = titles_page.get_titles_list()

    titles_page.click_add_title_button()
    add_title_page.wait_for_page_load()

    yield add_title_page, titles_page, sidebar_page, header_page


@pytest.allure.testcase("Validate add title page")
def test_add_title_page(setup):
    add_title_page, _, _, _ = setup
    validate_page(add_title_page)


@pytest.allure.testcase("Validate add title sidebar")
def test_add_title_sidebar_page(setup):
    _, _, sidebar_page, _ = setup
    validate_add_title_sidebar_page(sidebar_page)


@pytest.allure.testcase("Validate add title header")
def test_add_title_header_page(setup):
    _, _, _, header_page = setup
    validate_add_title_header_page(header_page)


@pytest.mark.xfail(reason='PLAT-6334', raises=TimeoutException)
@pytest.allure.testcase("Validate that a title can be added through the UI")
def test_add_title_functions(config, browser, setup):
    add_title_page, titles_page, sidebar_page, _ = setup
    notification = Notification(browser)

    unique_id = RandomUtilities.create_unique_id_lowercase()
    title_name = 'Test Title {}'.format(unique_id)
    code = 'test_title_{}'.format(unique_id)
    email = '{}@qa.wargaming.net'.format(config.admin.username)

    add_title_page.type_name_field(title_name)
    add_title_page.type_code_field(code)
    add_title_page.type_contact_field(email)
    add_title_page.click_save_button()

    notification.wait_for_notification_message()
    assert_that(notification.get_notification_message().text, equal_to('Title: {} successfully created!'.format(code)))

    titles_page.wait_for_page_load()
    assert_that(titles_page.get_title_button_by_name(code).text, equal_to(title_name))


@pytest.allure.testcase("Ensure duplicate title won't get created")
def test_add_title_does_not_create_duplicate_title(config, browser, setup):
    add_title_page, titles_page, sidebar_page, _ = setup
    notification = Notification(browser)

    add_title_page.type_name_field('Test Title')
    add_title_page.type_code_field(config.data.TEST_TITLE.CODE)
    add_title_page.type_contact_field('{}@qa.wargaming.net'.format(config.admin.username))
    add_title_page.click_save_button()

    notification.wait_for_notification_message()
    assert_that(
        notification.get_notification_message().text,
        equal_to("\"Title '{}' of studio '{}' already exists, creation impossible\"".format(
            config.data.TEST_TITLE.CODE,
            config.data.TEST_STUDIO.CODE
        ))
    )

    add_title_page.click_cancel_button()
    titles_page.wait_for_page_load()
    titles_list = titles_page.get_titles_list()

    count = 0
    for title in titles_list:
        if config.data.TEST_TITLE.CODE in title.get_attribute('innerHTML'):
            count = count + 1
    assert_that(count, equal_to(1))


@pytest.allure.testcase("Ensure cancel button returns the user to the titles page")
def test_add_title_cancel_returns_to_titles_page(setup):
    add_title_page, titles_page, _, _ = setup

    add_title_page.click_cancel_button()

    titles_page.wait_for_page_load()
    assert_that(titles_page.get_titles_list(), greater_than_or_equal_to(1))


@pytest.allure.testcase("Ensure title won't get created when code input is invalid")
@pytest.mark.parametrize('invalid_code', ['!', '@'])
def test_add_title_does_not_create_title_when_code_is_invalid(invalid_code, setup):
    add_title_page, _, _, _ = setup

    unique_id = RandomUtilities.create_unique_id_lowercase()
    title_name = 'Test UI Create Title {}'.format(unique_id)

    add_title_page.type_name_field(title_name)
    add_title_page.type_code_field(invalid_code)
    add_title_page.wait_for_code_invalid_message()
    assert_that(add_title_page.get_code_invalid_message().text, equal_to(CODE_INVALID_INPUT))

    assert_that(add_title_page.get_save_button().is_enabled(), equal_to(False))


@pytest.allure.testcase("Ensure title won't get created when email is invalid")
@pytest.mark.parametrize('invalid_email', ['bad_email', 'bad@email', 'bad@', 'bad@.', 'bad.email', 'bad@.com'])
def test_add_title_does_not_create_title_when_email_is_invalid(invalid_email, setup):
    add_title_page, _, _, _ = setup

    unique_id = RandomUtilities.create_unique_id_lowercase()
    title_name = 'Test UI Create Title {}'.format(unique_id)
    title_code = 'test_ui_create_title_{}'.format(unique_id)

    add_title_page.type_name_field(title_name)
    add_title_page.type_code_field(title_code)

    add_title_page.type_contact_field(invalid_email)
    add_title_page.wait_for_invalid_email_message()
    assert_that(add_title_page.get_invalid_email_message().text, equal_to(EMAIL_INVALID_INPUT))
    assert_that(add_title_page.get_save_button().is_enabled(), equal_to(False))


@pytest.allure.testcase("Ensure the title is not being created when saving with empty input data")
@pytest.mark.parametrize('name, code, email', [(name_data, code_data, email_data)
                                               for name_data in ['', 'name']
                                               for code_data in ['', 'code']
                                               for email_data in ['', 'admin@qa.wargaming.net']][:-1])
def test_add_title_does_not_create_title_when_empty_input_data(setup, name, code, email):
    add_title_page, _, _, _ = setup

    add_title_page.type_name_field(name)
    add_title_page.type_code_field(code)
    add_title_page.type_contact_field(email)

    assert_that(add_title_page.get_save_button().is_enabled(), equal_to(False))
