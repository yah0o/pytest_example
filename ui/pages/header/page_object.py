from selenium.webdriver.remote.webelement import WebElement

from locators import HeaderLocators
from ui.pages.base_page import BasePage


class Header(BasePage):
    def get_home_button(self):
        """
        Get the home button
        :return: home button
        :rtype: WebElement
        """
        return self.browser.find_element(*HeaderLocators.HOME_BUTTON)

    def click_home_button(self):
        """
        Click the home button
        """
        button = self.get_home_button()
        button.click()

    def get_top_bar_header(self):
        """
        Get the topbar header
        :return: topbar header
        :rtype: WebElement
        """
        return self.browser.find_element(*HeaderLocators.TOP_BAR_HEADER)

    def get_network_status(self):
        """
        Get the network status
        :return: network status
        :rtype: WebElement
        """
        return self.browser.find_element(*HeaderLocators.NETWORK_STATUS)

    def get_notification_icon(self):
        """
        Get the notification icon
        :return: notification icon
        :rtype: WebElement
        """
        return self.browser.find_element(*HeaderLocators.NOTIFICATION_ICON)

    def get_settings_icon(self):
        """
        Get the settings icon
        :return: settings icon
        :rtype: WebElement
        """
        return self.browser.find_element(*HeaderLocators.SETTINGS_ICON)

    def get_drop_down_menu(self):
        """
        Get the account menu
        :return: account menu
        :rtype: WebElement
        """
        return self.browser.find_element(*HeaderLocators.DROP_DOWN_MENU)

    def get_drop_down_options(self):
        """
        Get the drop down options
        :return: drop down options
        :rtype: WebElement
        """
        return self.browser.find_elements(*HeaderLocators.DROP_DOWN_OPTIONS)

    def get_user_icon(self):
        """
        Get the user icon
        :return: user icon
        :rtype: WebElement
        """
        return self.browser.find_element(*HeaderLocators.USER_ICON)

    def get_user_id(self):
        """
        Get the user id
        :return: user id
        :rtype: WebElement
        """
        return self.browser.find_element(*HeaderLocators.USER_ID)

    def get_logout_button(self):
        """
        Get the logout button
        :return: logout button
        :rtype: WebElement
        """
        return self.browser.find_element(*HeaderLocators.LOGOUT_BUTTON)

    def click_logout_button(self):
        """
        Click the logout button
        """
        button = self.get_logout_button()
        button.click()
