from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from locators import AddStudioLocators
from ui.pages.base_page import BasePage
from ui.main.constants import DEFAULT_PAGE_TIMEOUT
from ui.main.patterns.waiters import wait_for_non_empty_text


class AddStudio(BasePage):
    def wait_for_page_load(self):
        """
        Wait for the page to be fully loaded
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(AddStudioLocators.SAVE_BUTTON),
            '"Add studio" page failed to load'
        )

    def wait_for_code_invalid_message(self):
        """
        Wait for the error message to appear after entering not allowed characters into code
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            wait_for_non_empty_text(AddStudioLocators.CODE_INVALID_MESSAGE),
            'Code invalid message did not display'
        )

    def wait_for_studio_contact_invalid_message(self):
        """
        Wait for the error message to appear after entering not allowed characters into 'studio contact email'
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            wait_for_non_empty_text(AddStudioLocators.STUDIO_CONTACT_INVALID_MESSAGE),
            'Studio Contact invalid message did not display'
        )

    def wait_for_wg_contact_invalid_message(self):
        """
        Wait for the error message to appear after entering not allowed characters into 'wg contact email'
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            wait_for_non_empty_text(AddStudioLocators.WG_CONTACT_INVALID_MESSAGE),
            'WG Contact invalid message did not display'
        )

    def get_studios_title(self):
        """
        Get Studios title on the Add Studio page
        :return: studios title element
        :rtype: WebElement
        """
        return self.browser.find_element(*AddStudioLocators.STUDIOS_TITLE)

    def get_import_button(self):
        """
        Get Import Studio button on the Add Studio page
        :return: import studio button
        :rtype: WebElement
        """
        return self.browser.find_element(*AddStudioLocators.IMPORT_BUTTON)

    def click_import_button(self):
        """
        Click Import Studio button on the Add Studio page
        """
        button = self.get_import_button()
        button.click()

    def get_add_button(self):
        """
        Get Add Studio button on the Add Studio page
        :return: add studio button
        :rtype: WebElement
        """
        return self.browser.find_element(*AddStudioLocators.ADD_BUTTON)

    def click_add_button(self):
        """
        Click Add Studio button on the Add Studio page
        """
        button = self.get_add_button()
        button.click()

    def get_add_studio_title(self):
        """
        Get Add studio title on the Add Studio page
        :return: add studio title element
        :rtype: WebElement
        """
        return self.browser.find_element(*AddStudioLocators.ADD_STUDIO_TITLE)

    def get_name_label(self):
        """
        Get the label for the name input field element
        :return: Label for the name input field element
        :rtype: WebElement
        """
        return self.browser.find_element(*AddStudioLocators.NAME_LABEL)

    def get_name_field(self):
        """
        Get name input field element
        :return: name input field element
        :rtype: WebElement
        """
        return self.browser.find_element(*AddStudioLocators.NAME_INPUT)

    def type_name_field(self, value):
        """
        Type studio name into input field
        :param value: studio name
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
        return self.browser.find_element(*AddStudioLocators.CODE_LABEL)

    def get_code_field(self):
        """
        Get code input field element
        :return: code input field element
        :rtype: WebElement
        """
        return self.browser.find_element(*AddStudioLocators.CODE_INPUT)

    def type_code_field(self, value):
        """
        Type studio code into input field
        :param value: studio code
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
        return self.browser.find_element(*AddStudioLocators.CODE_INVALID_MESSAGE)

    def get_studio_contact_label(self):
        """
        Get the label for the 'studio contact email' field
        :return: Label for the 'studio contact email' field
        :rtype: WebElement
        """
        return self.browser.find_element(*AddStudioLocators.STUDIO_CONTACT_LABEL)

    def get_studio_contact_input(self):
        """
        Get 'studio contact email' input field
        :return: 'studio contact email' input field
        :rtype: WebElement
        """
        return self.browser.find_element(*AddStudioLocators.STUDIO_CONTACT_INPUT)

    def type_studio_contact_input(self, value):
        """
        Type studio contact email into input field
        :param value: studio contact email
        :type value: str
        """
        input_field = self.get_studio_contact_input()
        input_field.send_keys(value)

    def get_studio_contact_invalid_message(self):
        """
        Get the error message after entering characters that aren't allowed in the 'studio contact email' field
        :return: studio contact email invalid message
        :rtype: WebElement
        """
        return self.browser.find_element(*AddStudioLocators.STUDIO_CONTACT_INVALID_MESSAGE)

    def get_wg_contact_label(self):
        """
        Get the label for the 'wg contact email' field
        :return: Label for the 'wg contact email' field
        :rtype: WebElement
        """
        return self.browser.find_element(*AddStudioLocators.WG_CONTACT_LABEL)

    def get_wg_contact_input(self):
        """
        Get 'wg contact email' input field
        :return: 'wg contact email' input field
        :rtype: WebElement
        """
        return self.browser.find_element(*AddStudioLocators.WG_CONTACT_INPUT)

    def type_wg_contact_input(self, value):
        """
        Type wg contact email into input field
        :param value: wg contact email
        :type value: str
        """
        input_field = self.get_wg_contact_input()
        input_field.send_keys(value)

    def get_wg_contact_invalid_message(self):
        """
        Get the error message after entering characters that aren't allowed in the 'wg contact email' field
        :return: wg contact email invalid message
        :rtype: WebElement
        """
        return self.browser.find_element(*AddStudioLocators.WG_CONTACT_INVALID_MESSAGE)

    def get_save_button(self):
        """
        Get the save button
        :return: save button
        :rtype: WebElement
        """
        return self.browser.find_element(*AddStudioLocators.SAVE_BUTTON)

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
        return self.browser.find_element(*AddStudioLocators.CANCEL_BUTTON)

    def click_cancel_button(self):
        """
        Click the cancel button to cancel operation
        """
        button = self.get_cancel_button()
        button.click()
