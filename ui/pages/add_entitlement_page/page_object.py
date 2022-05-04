from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from locators import AddEntitlementLocators
from ui.main.constants import DEFAULT_PAGE_TIMEOUT
from ui.pages.base_page import BasePage
from ui.main.patterns.waiters import wait_for_non_empty_text


class AddEntitlement(BasePage):
    def wait_for_page_load(self):
        """
        Wait for the page to be fully loaded
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(AddEntitlementLocators.SAVE_BUTTON),
            '"Add Entitlement" page failed to load'
        )

    def wait_for_friendly_name_invalid_message(self):
        """
        Wait for the error message to appear after entering not allowed characters into friendly name field
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            wait_for_non_empty_text(AddEntitlementLocators.FRIENDLY_NAME_INVALID_MESSAGE),
            'Friendly name invalid message did not display'
        )

    def wait_for_code_invalid_message(self):
        """
        Wait for the error message to appear after entering not allowed characters into code
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            wait_for_non_empty_text(AddEntitlementLocators.CODE_INVALID_MESSAGE),
            'Code invalid message did not display'
        )

    def get_add_entitlement_header(self):
        """
        Get the add entitlement page header
        :return: add entitlement page header
        :rtype: WebElement
        """
        return self.browser.find_element(*AddEntitlementLocators.ADD_ENTITLEMENT_HEADER)

    def get_friendly_name_label(self):
        """
        Get the friendly name label
        :return: friendly name label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddEntitlementLocators.FRIENDLY_NAME_LABEL)

    def get_friendly_name_input(self):
        """
        Get the friendly name input
        :return: friendly name input
        :rtype: WebElement
        """
        return self.browser.find_element(*AddEntitlementLocators.FRIENDLY_NAME_INPUT)

    def type_friendly_name_input(self, value):
        """
        Type in the friendly name input
        :param value: value want to type
        :type value: str
        """
        input_field = self.get_friendly_name_input()
        input_field.send_keys(value)

    def get_friendly_name_invalid_message(self):
        """
        Get 'friendly name invalid message' after entering characters that aren't allowed in the friendly name
        :return: friendly name invalid message
        :rtype: WebElement
        """
        return self.browser.find_element(*AddEntitlementLocators.FRIENDLY_NAME_INVALID_MESSAGE)

    def get_code_label(self):
        """
        Get the code label
        :return: code label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddEntitlementLocators.CODE_LABEL)

    def get_code_input(self):
        """
        Get the code input
        :return: code input
        :rtype: WebElement
        """
        return self.browser.find_element(*AddEntitlementLocators.CODE_INPUT)

    def type_code_input(self, value):
        """
        Type in the code input
        :param value: value want to type
        :type value: str
        """
        input_field = self.get_code_input()
        input_field.send_keys(value)

    def get_code_invalid_message(self):
        """
        Get 'code invalid message' after entering characters that aren't allowed in the code
        :return: code invalid message
        :rtype: WebElement
        """
        return self.browser.find_element(*AddEntitlementLocators.CODE_INVALID_MESSAGE)

    def get_active_header(self):
        """
        Get the active header
        :return: active header
        :rtype: WebElement
        """
        return self.browser.find_element(*AddEntitlementLocators.ACTIVE_HEADER)

    def get_active_toggle(self):
        """
        Get the active toggle
        :return: active toggle
        :rtype: WebElement
        """
        return self.browser.find_element(*AddEntitlementLocators.ACTIVE_TOGGLE)

    def click_active_toggle(self):
        """
        Click the active toggle
        """
        toggle = self.get_active_toggle()
        toggle.click()

    def get_active_checkbox(self):
        """
        Get the active checkbox
        :return: active checkbox
        :rtype: WebElement
        """
        return self.browser.find_element(*AddEntitlementLocators.ACTIVE_CHECKBOX)

    def get_inactive_label(self):
        """
        Get the inactive label
        :return: inactive label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddEntitlementLocators.INACTIVE_LABEL)

    def get_active_label(self):
        """
        Get the active label
        :return: active label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddEntitlementLocators.ACTIVE_LABEL)

    def get_metadata_header(self):
        """
        Get the metadata header
        :return: metadata header
        :rtype: WebElement
        """
        return self.browser.find_element(*AddEntitlementLocators.METADATA_HEADER)

    def get_metadata_toggle(self):
        """
        Get the metadata toggle
        :return: metadata toggle
        :rtype: WebElement
        """
        return self.browser.find_element(*AddEntitlementLocators.METADATA_TOGGLE)

    def click_metadata_toggle(self):
        """
        Click the metadata toggle
        """
        toggle = self.get_metadata_toggle()
        toggle.click()

    def get_metadata_checkbox(self):
        """
        Get the metadata checkbox
        :return: metadata checkbox
        :rtype: WebElement
        """
        return self.browser.find_element(*AddEntitlementLocators.METADATA_CHECKBOX)

    def get_metadata_field_editor_label(self):
        """
        Get the metadata field editor label
        :return: metadata field editor label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddEntitlementLocators.METADATA_FIELD_EDITOR_LABEL)

    def get_metadata_code_editor_label(self):
        """
        Get the metadata code editor label
        :return: metadata code editor label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddEntitlementLocators.METADATA_CODE_EDITOR_LABEL)

    def get_tags_header(self):
        """
        Get the tags header
        :return: tags header
        :rtype: WebElement
        """
        return self.browser.find_element(*AddEntitlementLocators.TAGS_HEADER)

    def get_tags_input(self):
        """
        Get the tags input
        :return: tags input
        :rtype: WebElement
        """
        return self.browser.find_element(*AddEntitlementLocators.TAGS_INPUT)

    def type_tags_input(self, value):
        """
        Type in the tags input
        :param value: value want to type
        :type value: str
        """
        input_field = self.get_tags_input()
        input_field.send_keys(value)

    def get_tags_drop_down_arrow(self):
        """
        Get tags drop down arrow
        :return: tags drop down arrow
        :rtype: WebElement
        """
        return self.browser.find_element(*AddEntitlementLocators.TAGS_DROP_DOWN_ARROW)

    def click_tags_drop_down_arrow(self):
        """
        Click the tags drop down arrow
        """
        arrow = self.get_tags_drop_down_arrow()
        arrow.click()

    def get_save_button(self):
        """
        Get the save button
        :return: save button
        :rtype: WebElement
        """
        return self.browser.find_element(*AddEntitlementLocators.SAVE_BUTTON)

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
        return self.browser.find_element(*AddEntitlementLocators.CANCEL_BUTTON)

    def click_cancel_button(self):
        """
        Click the cancel button
        """
        button = self.get_cancel_button()
        button.click()
