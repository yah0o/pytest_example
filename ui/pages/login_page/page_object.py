from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from locators import LoginPageLocators
from ui.pages.base_page import BasePage
from ui.main.constants import DEFAULT_PAGE_TIMEOUT


class LoginPage(BasePage):
    def wait_for_page_load(self):
        """
        Wait for the page to be fully loaded
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(LoginPageLocators.WARGAMING_SSO_LINK),
            'Login page failed to load'
        )

    def wait_for_credentials_page_load(self):
        """
        Wait for the credentials page to be fully loaded
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(LoginPageLocators.USERNAME_INPUT),
            'Credentials page failed to load'
        )

    def get_username_field(self):
        """
        Get the username field element
        :return: username field element
        :rtype: WebElement
        """
        return self.browser.find_element(*LoginPageLocators.USERNAME_INPUT)

    def set_username_field(self, value):
        """
        Set the username to use when logging in
        :param value: Username to use during authentication
        :type value: str
        """
        input_field = self.get_username_field()
        input_field.send_keys(value)

    def get_password_field(self):
        """
        Get the password field element
        :return: password field element
        :rtype: WebElement
        """
        return self.browser.find_element(*LoginPageLocators.PASSWORD_INPUT)

    def set_password_field(self, value):
        """
        Set the password to use when logging in
        :param value: password to use during authentication
        :type value: str
        """
        input_field = self.get_password_field()
        input_field.send_keys(value)

    def get_sign_in_button(self):
        """
        Get the sign in button
        :return: sign in button
        :rtype: WebElement
        """
        return self.browser.find_element(*LoginPageLocators.SIGN_IN_BUTTON)

    def click_sign_in_button(self):
        """
        Click the sign in button to initiate logging in
        """
        button = self.get_sign_in_button()
        button.click()

    def get_sso_link(self):
        """
        Get Wargaming SSO link
        :return: link
        :rtype: WebElement
        """
        return self.browser.find_element(*LoginPageLocators.WARGAMING_SSO_LINK)

    def click_sso_link(self):
        """
        Click Wargaming SSO link to initiate logging in
        """
        link = self.get_sso_link()
        link.click()