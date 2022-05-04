from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from locators import AddTitleLocators
from ui.pages.base_page import BasePage
from ui.main.patterns.waiters import wait_for_non_empty_text
from ui.main.constants import DEFAULT_PAGE_TIMEOUT


class AddTitle(BasePage):
    def wait_for_page_load(self):
        """
        Wait for the page to be fully loaded
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(AddTitleLocators.SAVE_BUTTON),
            '"Add title" page failed to load'
        )

    def wait_for_invalid_email_message(self):
        """
        Wait for the error message to appear after entering invalid email
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            wait_for_non_empty_text(AddTitleLocators.INVALID_EMAIL_MESSAGE),
            'Invalid email error message did not display'
        )

    def wait_for_code_invalid_message(self):
        """
        Wait for the error message to appear after entering not allowed characters into code
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            wait_for_non_empty_text(AddTitleLocators.CODE_INVALID_MESSAGE),
            'Code invalid message did not display'
        )

    def get_add_title_text(self):
        """
        Get Add title text on the Add Title page
        :return: add title element
        :rtype: WebElement
        """
        return self.browser.find_element(*AddTitleLocators.ADD_TITLE_TEXT)

    def get_name_label(self):
        """
        Get the label for the name input field element
        :return: Label for the name input field element
        :rtype: WebElement
        """
        return self.browser.find_element(*AddTitleLocators.NAME_LABEL)

    def get_name_field(self):
        """
        Get name input field element
        :return: name input field element
        :rtype: WebElement
        """
        return self.browser.find_element(*AddTitleLocators.NAME_INPUT)

    def type_name_field(self, value):
        """
        Type title name into input field
        :param value: title name
        :type value: str
        """
        input_field = self.get_name_field()
        input_field.send_keys(value)

    def get_code_label(self):
        """
        Get the label for the code input field element
        :return: Label for the code input field element
        :rtype: WebElement
        """
        return self.browser.find_element(*AddTitleLocators.CODE_LABEL)

    def get_code_field(self):
        """
        Get code input field element
        :return: code input field element
        :rtype: WebElement
        """
        return self.browser.find_element(*AddTitleLocators.CODE_INPUT)

    def type_code_field(self, value):
        """
        Type title code into input field
        :param value: title code
        :type value: str
        """
        input_field = self.get_code_field()
        input_field.send_keys(value)

    def get_code_invalid_message(self):
        """
        Get 'code invalid message' after entering characters that aren't allowed in the code
        :return: code invalid message
        :rtype: WebElement
        """
        return self.browser.find_element(*AddTitleLocators.CODE_INVALID_MESSAGE)

    def get_contact_label(self):
        """
        Get the label for the contact email input field element
        :return: Label for the contact email input field element
        :rtype: WebElement
        """
        return self.browser.find_element(*AddTitleLocators.CONTACT_LABEL)

    def get_contact_field(self):
        """
        Get contact email input field element
        :return: contact email input field element
        :rtype: WebElement
        """
        return self.browser.find_element(*AddTitleLocators.CONTACT_INPUT)

    def type_contact_field(self, value):
        """
        Type contact email into input field
        :param value: contact email
        :type value: str
        """
        input_field = self.get_contact_field()
        input_field.send_keys(value)

    def get_save_button(self):
        """
        Get the save button
        :return: save button
        :rtype: WebElement
        """
        return self.browser.find_element(*AddTitleLocators.SAVE_BUTTON)

    def click_save_button(self):
        """
        Click the save button to initiate saving
        """
        button = self.get_save_button()
        button.click()

    def get_cancel_button(self):
        """
        Get the cancel button
        :return: cancel button
        :rtype: WebElement
        """
        return self.browser.find_element(*AddTitleLocators.CANCEL_BUTTON)

    def click_cancel_button(self):
        """
        Click the cancel button to cancel operation
        """
        button = self.get_cancel_button()
        button.click()

    def get_invalid_email_message(self):
        """
        Get 'invalid email message' after entering invalid email
        :return: invalid email message
        :rtype: WebElement
        """
        return self.browser.find_element(*AddTitleLocators.INVALID_EMAIL_MESSAGE)
