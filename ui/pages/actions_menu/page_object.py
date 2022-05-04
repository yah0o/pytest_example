from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from locators import ActionsMenuLocators
from ui.pages.base_page import BasePage
from ui.main.constants import DEFAULT_PAGE_TIMEOUT


class ActionsMenu(BasePage):
    def wait_for_actions_menu_load(self, name):
        """
        Wait for the Actions menu to be fully loaded
        :param name: name of the desired entity
        :type name: str
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(
                ActionsMenuLocators.get_actions_menu_list_locator_by_name(name)
            ),
            "Actions menu for {} didn't load".format(name)
        )

    def get_actions_menu_list_by_name(self, name):
        """
        Get the Actions menu list after clicking on Actions button
        :param name: name of the desired entity
        :type name: str
        :return: Actions menu list
        :rtype: list of WebElement
        """
        return self.browser.find_elements(*ActionsMenuLocators.get_actions_menu_list_locator_by_name(name))

    def get_actions_download_config_by_name(self, name):
        """
        Get the Download Config option after clicking on Actions button
        :param name: name of the desired entity
        :type name: str
        :return: Download Config option
        :rtype: WebElement
        """
        return self.browser.find_element(*ActionsMenuLocators.get_actions_menu_download_config_locator_by_name(name))

    def click_actions_download_config(self, name):
        """
        Click the Download Config
        :param name: name of the desired entity
        :type name: str
        """
        button = self.get_actions_download_config_by_name(name)
        button.click()

    def get_actions_edit_by_name(self, name):
        """
        Get the Edit option after clicking on Actions button
        :param name: name of the desired entity
        :type name: str
        :return: Edit option
        :rtype: WebElement
        """
        return self.browser.find_element(*ActionsMenuLocators.get_actions_menu_edit_locator_by_name(name))

    def click_actions_edit(self, name):
        """
        Click the Edit
        :param name: name of the desired entity
        :type name: str
        """
        button = self.get_actions_edit_by_name(name)
        button.click()

    def get_actions_duplicate_by_name(self, name):
        """
        Get the Duplicate option after clicking on Actions button
        :param name: name of the desired entity
        :type name: str
        :return: Duplicate option
        :rtype: WebElement
        """
        return self.browser.find_element(*ActionsMenuLocators.get_actions_menu_duplicate_locator_by_name(name))

    def click_actions_duplicate(self, name):
        """
        Click the Duplicate
        :param name: name of the desired entity
        :type name: str
        """
        button = self.get_actions_duplicate_by_name(name)
        button.click()

    def get_actions_remove_by_name(self, name):
        """
        Get the Remove option after clicking on Actions button
        :param name: name of the desired entity
        :type name: str
        :return: Remove option
        :rtype: WebElement
        """
        return self.browser.find_element(*ActionsMenuLocators.get_actions_menu_remove_locator_by_name(name))

    def click_actions_remove(self, name):
        """
        Click the Remove
        :param name: name of the desired entity
        :type name: str
        """
        button = self.get_actions_remove_by_name(name)
        button.click()
