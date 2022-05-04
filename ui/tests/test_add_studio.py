import pytest
from selenium.common.exceptions import TimeoutException
from hamcrest import assert_that, equal_to, has_length, greater_than_or_equal_to

from ui.pages import AddStudio, Studios, Sidebar, Header, Notification
from ui.main.helpers import RandomUtilities
from ui.main.constants import PLATFORM_HEADER_TEXT, CODE_INVALID_INPUT, EMAIL_INVALID_INPUT


@pytest.allure.step('Validate elements on the add studio page')
def validate_page(add_studio_page):
    assert_that(add_studio_page.get_studios_title().text, equal_to('Studios'))
    # assert_that(add_studio_page.get_import_button().text, equal_to('IMPORT STUDIO'))
    assert_that(add_studio_page.get_add_button().text, equal_to('CREATE STUDIO'))
    assert_that(add_studio_page.get_add_studio_title().text, equal_to('Create studio'))
    assert_that(add_studio_page.get_name_label().text, equal_to('Name'))
    assert_that(add_studio_page.get_name_field())
    assert_that(add_studio_page.get_code_label().text, equal_to('Code'))
    assert_that(add_studio_page.get_code_field())
    assert_that(add_studio_page.get_studio_contact_label().text, equal_to('Studio Contact email'))
    assert_that(add_studio_page.get_studio_contact_input())
    assert_that(add_studio_page.get_wg_contact_label().text, equal_to('WG Contact email'))
    assert_that(add_studio_page.get_wg_contact_input())
    assert_that(add_studio_page.get_save_button().text, equal_to('Create'))
    assert_that(add_studio_page.get_cancel_button().text, equal_to('Cancel'))


@pytest.allure.step('Validate elements on the studios sidebar page')
def validate_add_studio_sidebar_page(sidebar_page):
    studios_button = sidebar_page.get_studios_button()
    assert_that(studios_button.text, equal_to('Studios'))

    # reports_button = sidebar_page.get_reports_button()
    # assert_that(reports_button.text, equal_to('Reports'))

    sidebar_panel = sidebar_page.get_panel()
    assert_that(sidebar_panel, has_length(1))


@pytest.allure.step('Validate elements on the add studio header page')
def validate_add_studio_header_page(header_page):
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
    add_studio_page = AddStudio(browser)
    studios_page = Studios(browser)
    sidebar_page = Sidebar(browser)
    header_page = Header(browser)

    steps.login(config.admin.username, config.admin.password)

    studios_page.click_add_button()

    add_studio_page.wait_for_page_load()

    yield add_studio_page, studios_page, sidebar_page, header_page


@pytest.allure.testcase("Validate add studio page")
def test_add_studio_page(setup):
    add_studio_page, _, _, _ = setup
    validate_page(add_studio_page)


@pytest.allure.testcase("Validate add studio sidebar page")
def test_add_studio_sidebar_page(setup):
    _, _, sidebar_page, _ = setup
    validate_add_studio_sidebar_page(sidebar_page)


@pytest.allure.testcase("Validate add studio header page")
def test_add_studio_header_page(setup):
    _, _, _, header_page = setup
    validate_add_studio_header_page(header_page)


@pytest.mark.xfail(reason='PLAT-6334', raises=TimeoutException)
@pytest.allure.testcase("Validate that a studio can be added through the UI")
def test_add_studio_functions(config, browser, setup):
    add_studio_page, studios_page, _, _ = setup
    notification = Notification(browser)

    unique_id = RandomUtilities.create_unique_id_lowercase()
    studio_name = 'Test UI Create Studio {}'.format(unique_id)
    studio_code = 'test_ui_create_studio_{}'.format(unique_id)
    studio_contact_email = '{}@qa.wargaming.net'.format(config.admin.username)
    wg_contact_email = '{}@qa.wargaming.net'.format(config.admin.username)

    add_studio_page.type_name_field(studio_name)
    add_studio_page.type_code_field(studio_code)
    add_studio_page.type_studio_contact_input(studio_contact_email)
    add_studio_page.type_wg_contact_input(wg_contact_email)
    add_studio_page.click_save_button()

    notification.wait_for_notification_message()
    assert_that(notification.get_notification_message().text,
                equal_to('Studio: {} successfully created!'.format(studio_code)))

    studios_page.wait_for_page_load()
    assert_that(studios_page.get_studio_button_by_name(studio_code).text, equal_to(studio_name))


@pytest.allure.testcase("Ensure duplicate studio won't get created")
def test_add_studio_does_not_create_duplicate_studio(config, browser, setup):
    add_studio_page, studios_page, _, _ = setup
    notification = Notification(browser)

    add_studio_page.type_name_field(config.data.TEST_STUDIO.FRIENDLY_NAME)
    add_studio_page.type_code_field(config.data.TEST_STUDIO.CODE)
    add_studio_page.type_studio_contact_input('{}@qa.wargaming.net'.format(config.admin.username))
    add_studio_page.type_wg_contact_input('{}@qa.wargaming.net'.format(config.admin.username))
    add_studio_page.click_save_button()

    notification.wait_for_notification_message()
    assert_that(
        notification.get_notification_message().text,
        equal_to("Studio '{}' already exists, creation impossible".format(config.data.TEST_STUDIO.CODE))
    )

    add_studio_page.click_cancel_button()
    studios_page.wait_for_page_load()
    studios_list = studios_page.get_studios_list()

    count = 0
    for studio in studios_list:
        if config.data.TEST_STUDIO.CODE in studio.get_attribute('innerHTML'):
            count = count + 1
    assert_that(count, equal_to(1))


@pytest.allure.testcase("Ensure cancel button returns the user to the studios page")
def test_add_studio_cancel_returns_to_studios_page(setup, browser):
    add_studio_page, studios_page, _, _ = setup

    add_studio_page.click_cancel_button()

    studios_page.wait_for_page_load()
    assert_that(studios_page.get_studios_list(), greater_than_or_equal_to(1))


@pytest.allure.testcase("Ensure studio won't get created when code input is invalid")
@pytest.mark.parametrize('invalid_code', ['!', '@'])
def test_add_studio_does_not_create_studio_when_code_is_invalid(invalid_code, setup):
    add_studio_page, _, _, _ = setup

    unique_id = RandomUtilities.create_unique_id_lowercase()
    studio_name = 'Test UI Create Studio {}'.format(unique_id)

    add_studio_page.type_name_field(studio_name)
    add_studio_page.type_code_field(invalid_code)
    add_studio_page.wait_for_code_invalid_message()
    assert_that(add_studio_page.get_code_invalid_message().text, equal_to(CODE_INVALID_INPUT))

    assert_that(add_studio_page.get_save_button().is_enabled(), equal_to(False))


@pytest.allure.testcase("Ensure studio won't get created when studio contact email is invalid")
@pytest.mark.parametrize('invalid_email', ['bad_email', 'bad@email', 'bad@', 'bad@.', 'bad.email', 'bad@.com'])
def test_add_studio_does_not_create_studio_when_studio_contact_email_is_invalid(invalid_email, setup, config):
    add_studio_page, _, _, _ = setup

    unique_id = RandomUtilities.create_unique_id_lowercase()
    studio_name = 'Test UI Create Studio {}'.format(unique_id)
    studio_code = 'test_ui_create_studio_{}'.format(unique_id)
    wg_contact_email = '{}@qa.wargaming.net'.format(config.admin.username)

    add_studio_page.type_name_field(studio_name)
    add_studio_page.type_code_field(studio_code)
    add_studio_page.type_wg_contact_input(wg_contact_email)

    add_studio_page.type_studio_contact_input(invalid_email)
    add_studio_page.wait_for_studio_contact_invalid_message()
    assert_that(add_studio_page.get_studio_contact_invalid_message().text, equal_to(EMAIL_INVALID_INPUT))

    assert_that(add_studio_page.get_save_button().is_enabled(), equal_to(False))


@pytest.allure.testcase("Ensure studio won't get created when wg contact email is invalid")
@pytest.mark.parametrize('invalid_email', ['bad_email', 'bad@email', 'bad@', 'bad@.', 'bad.email', 'bad@.com'])
def test_add_studio_does_not_create_studio_when_wg_contact_email_is_invalid(invalid_email, setup, config):
    add_studio_page, _, _, _ = setup

    unique_id = RandomUtilities.create_unique_id_lowercase()
    studio_name = 'Test UI Create Studio {}'.format(unique_id)
    studio_code = 'test_ui_create_studio_{}'.format(unique_id)
    studio_contact_email = '{}@qa.wargaming.net'.format(config.admin.username)

    add_studio_page.type_name_field(studio_name)
    add_studio_page.type_code_field(studio_code)
    add_studio_page.type_studio_contact_input(studio_contact_email)

    add_studio_page.type_wg_contact_input(invalid_email)
    add_studio_page.wait_for_wg_contact_invalid_message()
    assert_that(add_studio_page.get_wg_contact_invalid_message().text, equal_to(EMAIL_INVALID_INPUT))

    assert_that(add_studio_page.get_save_button().is_enabled(), equal_to(False))


@pytest.allure.testcase("Ensure the studio won't get created when saving with empty input data")
@pytest.mark.parametrize('name, code, studio_email, wg_email', [(name_data, code_data, studio_email_data, wg_email_data)
                                                            for name_data in ['', 'name']
                                                            for code_data in ['', 'code']
                                                            for studio_email_data in ['', 'admin@qa.wargaming.net']
                                                            for wg_email_data in ['', 'admin@qa.wargaming.net']][:-1])
def test_add_studio_does_not_create_studio_when_empty_input_data(setup, name, code, studio_email, wg_email):
    add_studio_page, _, _, _ = setup

    add_studio_page.type_name_field(name)
    add_studio_page.type_code_field(code)
    add_studio_page.type_studio_contact_input(studio_email)
    add_studio_page.type_wg_contact_input(wg_email)

    assert_that(add_studio_page.get_save_button().is_enabled(), equal_to(False))
