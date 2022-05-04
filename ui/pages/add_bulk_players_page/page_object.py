from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from locators import AddBulkPlayersLocators
from ui.pages.base_page import BasePage
from ui.main.patterns.waiters import wait_for_non_empty_text
from ui.main.constants import DEFAULT_PAGE_TIMEOUT


class AddBulkPlayers(BasePage):
    def wait_for_page_load(self):
        """
        Wait for the page to be fully loaded
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(AddBulkPlayersLocators.SAVE_BUTTON),
            '"Add bulk players" page failed to load'
        )

    def wait_for_login_invalid_message(self):
        """
        Wait for the error message to appear after entering not allowed characters in the Login
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            wait_for_non_empty_text(AddBulkPlayersLocators.LOGIN_INVALID_MESSAGE),
            'Login invalid message did not display'
        )

    def wait_for_password_invalid_message(self):
        """
        Wait for the error message to appear after entering not allowed characters in the Password
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            wait_for_non_empty_text(AddBulkPlayersLocators.PASSWORD_INVALID_MESSAGE),
            'Password invalid message did not display'
        )

    def wait_for_name_invalid_message(self):
        """
        Wait for the error message to appear after entering not allowed characters in the Name
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            wait_for_non_empty_text(AddBulkPlayersLocators.NAME_INVALID_MESSAGE),
            'Name invalid message did not display'
        )

    def wait_for_ip_invalid_message(self):
        """
        Wait for the error message to appear after entering not allowed characters in the IP
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            wait_for_non_empty_text(AddBulkPlayersLocators.IP_INVALID_MESSAGE),
            'IP invalid message did not display'
        )

    def wait_for_realm_list_item_to_be_clickable(self, name):
        """
        Wait for the the list item to be clickable
        :param name: Name of the realm
        :type name: str
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.element_to_be_clickable(
                AddBulkPlayersLocators.get_realm_drop_down_list_item_locator_by_name(name)),
            "Realm's list item is not clickable"
        )

    def get_page_header(self):
        """
        Get page header text
        :return: page header text
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.PAGE_HEADER)

    def click_page_header(self):
        """
        Click on the page header
        """
        page_header = self.get_page_header()
        page_header.click()

    def get_page_subheader(self):
        """
        Get the page subheader
        :return: page subheader
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.PAGE_SUBHEADER)

    def get_context_text(self):
        """
        Get Context text
        :return: Context text
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.CONTEXT_TEXT)

    def get_iterations_label(self):
        """
        Get the label for the Iterations
        :return: label for the Iterations
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.ITERATIONS_LABEL)

    def get_iterations_input(self):
        """
        Get Iterations input field
        :return: Iterations input field
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.ITERATIONS_INPUT)

    def type_iterations_input(self, value):
        """
        Type in the Iterations input
        :param value: value want to type
        :type value: int
        """
        input_field = self.get_iterations_input()
        input_field.clear()
        input_field.send_keys(value)

    def get_realm_label(self):
        """
        Get the label for the Realm
        :return: label for the Realm
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.REALM_LABEL)

    def get_realm_input(self):
        """
        Get Realm input field
        :return: Realm input field
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.REALM_INPUT)

    def click_realm_input(self):
        """
        Click on the Realm input field
        """
        input_field = self.get_realm_input()
        input_field.click()

    def get_realm_drop_down_arrow(self):
        """
        Get Realm drop down list arrow
        :return: Realm drop down list arrow
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.REALM_DROP_DOWN_LIST_ARROW)

    def click_realm_drop_down_arrow(self):
        """
        Click on the Realm drop down list arrow
        """
        arrow = self.get_realm_drop_down_arrow()
        arrow.click()

    def get_realm_drop_down_list(self):
        """
        Get the Realm drop down list
        :return: Realm drop down list
        :rtype: WebElement
        """
        return self.browser.find_elements(*AddBulkPlayersLocators.REALM_DROP_DOWN_LIST)

    def get_realm_drop_down_list_item(self, name):
        """
        Get the Realm's drop down list item based on the name
        :param name: Name of the realm
        :type name: str
        :return: Realm's drop down list item
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.get_realm_drop_down_list_item_locator_by_name(name))

    def click_realm_drop_down_list_item(self, name):
        """
        Click the Realm's drop down list item based on the name
        :param name: Name of the realm
        :type name: str
        """
        list_item = self.get_realm_drop_down_list_item(name)
        list_item.click()

    def get_games_label(self):
        """
        Get the label for the Games
        :return: label for the Games
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.GAMES_LABEL)

    def get_games_input(self):
        """
        Get Games input field
        :return: Games input field
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.GAMES_INPUT)

    def type_games_input(self, value):
        """
        Type in the Games input
        :param value: value want to type
        :type value: str
        """
        input_field = self.get_games_input()
        input_field.send_keys(value)

    def click_games_input(self):
        """
        Click on the Games input field
        """
        input_field = self.get_games_input()
        input_field.click()

    def get_games_drop_down_arrow(self):
        """
        Get Games drop down list arrow
        :return: Games drop down list arrow
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.GAMES_DROP_DOWN_LIST_ARROW)

    def click_games_drop_down_arrow(self):
        """
        Click on the Games drop down list arrow
        """
        arrow = self.get_games_drop_down_arrow()
        arrow.click()

    def get_games_drop_down_list(self):
        """
        Get the Games drop down list
        :return: Games drop down list
        :rtype: WebElement
        """
        return self.browser.find_elements(*AddBulkPlayersLocators.GAMES_DROP_DOWN_LIST)

    def get_games_drop_down_list_item(self, name):
        """
        Get the Games's drop down list item based on the name
        :param name: Name of the game
        :type name: str
        :return: Games's drop down list item
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.get_games_drop_down_list_item_locator_by_name(name))

    def click_games_drop_down_list_item(self, name):
        """
        Click the Games's drop down list item based on the name
        :param name: Name of the game
        :type name: str
        """
        list_item = self.get_games_drop_down_list_item(name)
        list_item.click()

    def get_game_tag(self):
        """
        Get the game tag
        :return: game tag
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.GAME_TAG)

    def get_game_tag_exit_button(self):
        """
        Get the game tag exit button
        :return: game tag exit button
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.GAME_TAG_EXIT_BUTTON)

    def click_game_tag_exit_button(self):
        """
        Click the game tag exit button
        """
        button = self.get_game_tag_exit_button()
        button.click()

    def get_template_text(self):
        """
        Get Template text
        :return: Template text
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.TEMPLATE_TEXT)

    def get_info_box(self):
        """
        Get the info box
        :return: info box
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.INFO_BOX)

    def get_info_box_button(self):
        """
        Get the info box button
        :return: info box button
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.INFO_BOX_BUTTON)

    def click_info_box_button(self):
        """
        Click the info box button
        """
        button = self.get_info_box_button()
        button.click()

    def get_info_box_strong(self):
        """
        Get the info box's 'Info' strong element
        :return: info box's strong element
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.INFO_BOX_STRONG)

    def get_login_label(self):
        """
        Get the label for the Login
        :return: label for the Login
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.LOGIN_LABEL)

    def get_login_input(self):
        """
        Get Login input field
        :return: Login input field
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.LOGIN_INPUT)

    def type_login_input(self, value):
        """
        Type in the Login input
        :param value: value want to type
        :type value: str
        """
        input_field = self.get_login_input()
        input_field.send_keys(value)

    def get_login_invalid_message(self):
        """
        Get 'Login invalid message' after entering characters that aren't allowed in that field
        :return: Login invalid message
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.LOGIN_INVALID_MESSAGE)

    def get_password_label(self):
        """
        Get the label for the Password
        :return: label for the Password
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.PASSWORD_LABEL)

    def get_password_input(self):
        """
        Get Password input field
        :return: Password input field
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.PASSWORD_INPUT)

    def type_password_input(self, value):
        """
        Type in the Password input
        :param value: value want to type
        :type value: str
        """
        input_field = self.get_password_input()
        input_field.send_keys(value)

    def get_password_invalid_message(self):
        """
        Get 'Password invalid message' after entering characters that aren't allowed in that field
        :return: Password invalid message
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.PASSWORD_INVALID_MESSAGE)

    def get_name_label(self):
        """
        Get the label for the Name
        :return: label for the Name
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.NAME_LABEL)

    def get_name_input(self):
        """
        Get Name input field
        :return: Name input field
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.NAME_INPUT)

    def type_name_input(self, value):
        """
        Type in the Name input
        :param value: value want to type
        :type value: str
        """
        input_field = self.get_name_input()
        input_field.send_keys(value)

    def get_name_invalid_message(self):
        """
        Get 'Name invalid message' after entering characters that aren't allowed in that field
        :return: Name invalid message
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.NAME_INVALID_MESSAGE)

    def get_authentication_method_label(self):
        """
        Get the label for the Authentication Method
        :return: label for the Authentication Method
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.AUTHENTICATION_METHOD_LABEL)

    def get_authentication_method_input(self):
        """
        Get Authentication Method input field
        :return: Authentication Method input field
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.AUTHENTICATION_METHOD_INPUT)

    def click_authentication_method_input(self):
        """
        Click on the Authentication Method input field
        """
        input_field = self.get_authentication_method_input()
        input_field.click()

    def get_authentication_method_drop_down_arrow(self):
        """
        Get Authentication Method drop down list arrow
        :return: Authentication Method drop down list arrow
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.AUTHENTICATION_METHOD_DROP_DOWN_LIST_ARROW)

    def click_authentication_method_drop_down_arrow(self):
        """
        Click on the Authentication Method drop down list arrow
        """
        arrow = self.get_authentication_method_drop_down_arrow()
        arrow.click()

    def get_authentication_method_drop_down_list(self):
        """
        Get the Authentication Method drop down list
        :return: Authentication Method drop down list
        :rtype: WebElement
        """
        return self.browser.find_elements(*AddBulkPlayersLocators.AUTHENTICATION_METHOD_DROP_DOWN_LIST)

    def get_authentication_method_drop_down_list_item(self, name):
        """
        Get the Authentication Method's drop down list item based on the name
        :param name: Name of the method
        :type name: str
        :return: Authentication Method's drop down list item
        :rtype: WebElement
        """
        return self.browser.find_element(
            *AddBulkPlayersLocators.get_authentication_method_drop_down_list_item_locator_by_name(name))

    def click_authentication_method_drop_down_list_item(self, name):
        """
        Click the Authentication Method's drop down list item based on the name
        :param name: Name of the method
        :type name: str
        """
        list_item = self.get_authentication_method_drop_down_list_item(name)
        list_item.click()

    def get_ip_label(self):
        """
        Get the label for the IP
        :return: label for the IP
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.IP_LABEL)

    def get_ip_input(self):
        """
        Get IP input field
        :return: IP input field
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.IP_INPUT)

    def type_ip_input(self, value):
        """
        Type in the IP input
        :param value: value want to type
        :type value: str
        """
        input_field = self.get_ip_input()
        input_field.send_keys(value)

    def get_ip_invalid_message(self):
        """
        Get 'IP invalid message' after entering characters that aren't allowed in that field
        :return: IP invalid message
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.IP_INVALID_MESSAGE)

    def get_save_button(self):
        """
        Get the save button
        :return: save button
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.SAVE_BUTTON)

    def click_save_button(self):
        """
        Click the save button
        """
        button = self.get_save_button()
        button.click()

    def get_cancel_button(self):
        """
        Get the cancel button
        :return: cancel button
        :rtype: WebElement
        """
        return self.browser.find_element(*AddBulkPlayersLocators.CANCEL_BUTTON)

    def click_cancel_button(self):
        """
        Click the cancel button
        """
        button = self.get_cancel_button()
        button.click()
