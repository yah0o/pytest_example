from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from locators import AddGameRegistrationLocators
from ui.pages.base_page import BasePage
from ui.main.constants import DEFAULT_PAGE_TIMEOUT


class AddGameRegistration(BasePage):
    def wait_for_page_load(self):
        """
        Wait for the page to be fully loaded
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(AddGameRegistrationLocators.SAVE_BUTTON),
            '"Add game registration" page failed to load'
        )

    def wait_for_game_list_item_to_be_clickable(self, name):
        """
        Wait for the the list item to be clickable
        :param name: Name of the game
        :type name: str
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.element_to_be_clickable(
                AddGameRegistrationLocators.get_game_drop_down_list_item_locator_by_name(name)),
            "Game's list item is not clickable"
        )

    def wait_for_game_list_item_to_be_clickable_by_index(self, index):
        """
        Wait for the the list item to be clickable by index
        :param index: item index
        :type index: int
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.element_to_be_clickable(
                AddGameRegistrationLocators.GAME_DROP_DOWN_LIST.select_by_index(index)),
            "Game's list item is not clickable by index"
        )

    def get_page_header(self):
        """
        Get page header text
        :return: page header text
        :rtype: WebElement
        """
        return self.browser.find_element(*AddGameRegistrationLocators.PAGE_HEADER)

    def click_page_header(self):
        """
        Click on the page header
        """
        page_header = self.get_page_header()
        page_header.click()

    def get_page_subheader_1(self):
        """
        Get the page subheader (player's realm and ID)
        :return: page subheader
        :rtype: WebElement
        """
        return self.browser.find_element(*AddGameRegistrationLocators.PAGE_SUBHEADER_1)

    def click_page_subheader_1(self):
        """
        Click on the page subheader
        """
        page_header = self.get_page_subheader_1()
        page_header.click()

    def get_page_subheader_2(self):
        """
        Get the page subheader ('Create Game Registration' text)
        :return: page subheader
        :rtype: WebElement
        """
        return self.browser.find_element(*AddGameRegistrationLocators.PAGE_SUBHEADER_2)

    def get_wgid_label(self):
        """
        Get the label for the WGID
        :return: label for the WGID
        :rtype: WebElement
        """
        return self.browser.find_element(*AddGameRegistrationLocators.WGID_LABEL)

    def get_wgid_input(self):
        """
        Get WGID input field
        :return: WGID input field
        :rtype: WebElement
        """
        return self.browser.find_element(*AddGameRegistrationLocators.WGID_INPUT)

    def get_realm_label(self):
        """
        Get the label for the Realm
        :return: label for the Realm
        :rtype: WebElement
        """
        return self.browser.find_element(*AddGameRegistrationLocators.REALM_LABEL)

    def get_realm_input(self):
        """
        Get Realm input field
        :return: Realm input field
        :rtype: WebElement
        """
        return self.browser.find_element(*AddGameRegistrationLocators.REALM_INPUT)

    def get_realm_drop_down_arrow(self):
        """
        Get Realm drop down list arrow
        :return: Realm drop down list arrow
        :rtype: WebElement
        """
        return self.browser.find_element(*AddGameRegistrationLocators.REALM_DROP_DOWN_LIST_ARROW)

    def get_game_label(self):
        """
        Get the label for the Game
        :return: label for the Game
        :rtype: WebElement
        """
        return self.browser.find_element(*AddGameRegistrationLocators.GAME_LABEL)

    def get_game_input(self):
        """
        Get Game input field
        :return: Game input field
        :rtype: WebElement
        """
        return self.browser.find_element(*AddGameRegistrationLocators.GAME_INPUT)

    def click_game_input(self):
        """
        Click on the Game input field
        """
        input_field = self.get_game_input()
        input_field.click()

    def get_game_drop_down_arrow(self):
        """
        Get Game drop down list arrow
        :return: Game drop down list arrow
        :rtype: WebElement
        """
        return self.browser.find_element(*AddGameRegistrationLocators.GAME_DROP_DOWN_LIST_ARROW)

    def click_game_drop_down_arrow(self):
        """
        Click on the Game drop down list arrow
        """
        arrow = self.get_game_drop_down_arrow()
        arrow.click()

    def get_game_drop_down_list(self):
        """
        Get the Game drop down list
        :return: Game drop down list
        :rtype: WebElement
        """
        return self.browser.find_elements(*AddGameRegistrationLocators.GAME_DROP_DOWN_LIST)

    def get_game_drop_down_list_item(self, name):
        """
        Get the Game's drop down list item based on the name
        :param name: Name of the game
        :type name: str
        :return: Game's drop down list item
        :rtype: WebElement
        """
        return self.browser.find_element(
            *AddGameRegistrationLocators.get_game_drop_down_list_item_locator_by_name(name))

    def click_game_drop_down_list_item(self, name):
        """
        Click the Game's drop down list item based on the name
        :param name: Name of the game
        :type name: str
        """
        list_item = self.get_game_drop_down_list_item(name)
        list_item.click()

    def get_game_drop_down_list_item_by_index(self, index):
        """
        Get the Game's drop down list item based on the index
        :param index: item index
        :type index: int
        :return: Game's drop down list item
        :rtype: WebElement
        """
        return self.browser.find_element(*AddGameRegistrationLocators.GAME_DROP_DOWN_LIST.select_by_index(index))

    def click_game_drop_down_list_item_by_index(self, index):
        """
        Click the Game's drop down list item based on the index
        :param index: item index
        :type index: int
        """
        list_item = self.get_game_drop_down_list_item_by_index(index)
        list_item.click()

    def get_save_button(self):
        """
        Get the save button
        :return: save button
        :rtype: WebElement
        """
        return self.browser.find_element(*AddGameRegistrationLocators.SAVE_BUTTON)

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
        return self.browser.find_element(*AddGameRegistrationLocators.CANCEL_BUTTON)

    def click_cancel_button(self):
        """
        Click the cancel button
        """
        button = self.get_cancel_button()
        button.click()
