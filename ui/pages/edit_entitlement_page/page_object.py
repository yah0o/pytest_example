from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from locators import EditEntitlementLocators
from ui.main.constants import DEFAULT_PAGE_TIMEOUT
from ui.pages.base_page import BasePage
from ui.main.patterns.waiters import wait_for_non_empty_text


class EditEntitlement(BasePage):
    def wait_for_page_load(self):
        """
        Wait for the page to be fully loaded
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(EditEntitlementLocators.SAVE_BUTTON),
            '"Edit Entitlement" page failed to load'
        )

    def wait_for_friendly_name_invalid_message(self):
        """
        Wait for the error message to appear after entering not allowed characters into friendly name field
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            wait_for_non_empty_text(EditEntitlementLocators.FRIENDLY_NAME_INVALID_MESSAGE),
            'Invalid friendly name message did not display'
        )

    def get_edit_entitlement_header(self):
        """
        Get the edit entitlement header
        :return: edit entitlement header
        :rtype: WebElement
        """
        return self.browser.find_element(*EditEntitlementLocators.EDIT_ENTITLEMENT_HEADER)

    def get_friendly_name_label(self):
        """
        Get the friendly name label
        :return: friendly name label
        :rtype: WebElement
        """
        return self.browser.find_element(*EditEntitlementLocators.FRIENDLY_NAME_LABEL)

    def get_friendly_name_input(self):
        """
        Get the friendly name input
        :return: friendly name input
        :rtype: WebElement
        """
        return self.browser.find_element(*EditEntitlementLocators.FRIENDLY_NAME_INPUT)

    def type_friendly_name_input(self, value):
        """
        Type in the friendly name input
        :param value: value want to type
        :type value: str
        """
        input_field = self.get_friendly_name_input()
        input_field.clear()
        input_field.send_keys(value)

    def get_friendly_name_invalid_message(self):
        """
        Get 'invalid friendly name message' after entering characters that aren't allowed in the friendly name
        :return: invalid friendly name message
        :rtype: WebElement
        """
        return self.browser.find_element(*EditEntitlementLocators.FRIENDLY_NAME_INVALID_MESSAGE)

    def get_code_label(self):
        """
        Get the code label
        :return: code label
        :rtype: WebElement
        """
        return self.browser.find_element(*EditEntitlementLocators.CODE_LABEL)

    def get_code_input(self):
        """
        Get the code input
        :return: code input
        :rtype: WebElement
        """
        return self.browser.find_element(*EditEntitlementLocators.CODE_INPUT)

    def get_version_label(self):
        """
        Get the version label
        :return: version label
        :rtype: WebElement
        """
        return self.browser.find_element(*EditEntitlementLocators.VERSION_LABEL)

    def get_version_input(self):
        """
        Get the version input
        :return: version input
        :rtype: WebElement
        """
        return self.browser.find_element(*EditEntitlementLocators.VERSION_INPUT)

    def get_active_header(self):
        """
        Get the active header
        :return: active header
        :rtype: WebElement
        """
        return self.browser.find_element(*EditEntitlementLocators.ACTIVE_HEADER)

    def get_active_toggle(self):
        """
        Get the active toggle
        :return: active toggle
        :rtype: WebElement
        """
        return self.browser.find_element(*EditEntitlementLocators.ACTIVE_TOGGLE)

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
        return self.browser.find_element(*EditEntitlementLocators.ACTIVE_CHECKBOX)

    def get_inactive_label(self):
        """
        Get the inactive label
        :return: inactive label
        :rtype: WebElement
        """
        return self.browser.find_element(*EditEntitlementLocators.INACTIVE_LABEL)

    def get_active_label(self):
        """
        Get the active label
        :return: active label
        :rtype: WebElement
        """
        return self.browser.find_element(*EditEntitlementLocators.ACTIVE_LABEL)

    def get_metadata_header(self):
        """
        Get the metadata header
        :return: metadata header
        :rtype: WebElement
        """
        return self.browser.find_element(*EditEntitlementLocators.METADATA_HEADER)

    def get_metadata_toggle(self):
        """
        Get the metadata toggle
        :return: metadata toggle
        :rtype: WebElement
        """
        return self.browser.find_element(*EditEntitlementLocators.METADATA_TOGGLE)

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
        return self.browser.find_element(*EditEntitlementLocators.METADATA_CHECKBOX)

    def get_metadata_field_editor_label(self):
        """
        Get the metadata field editor label
        :return: metadata field editor label
        :rtype: WebElement
        """
        return self.browser.find_element(*EditEntitlementLocators.METADATA_FIELD_EDITOR_LABEL)

    def get_metadata_code_editor_label(self):
        """
        Get the metadata code editor label
        :return: metadata code editor label
        :rtype: WebElement
        """
        return self.browser.find_element(*EditEntitlementLocators.METADATA_CODE_EDITOR_LABEL)

    def get_tags_header(self):
        """
        Get the tags header
        :return: tags header
        :rtype: WebElement
        """
        return self.browser.find_element(*EditEntitlementLocators.TAGS_HEADER)

    def get_tags_input(self):
        """
        Get the tags input
        :return: tags input
        :rtype: WebElement
        """
        return self.browser.find_element(*EditEntitlementLocators.TAGS_INPUT)

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
        Get the tags drop down arrow
        :return: tags drop down arrow
        :rtype: WebElement
        """
        return self.browser.find_element(*EditEntitlementLocators.TAGS_DROP_DOWN_ARROW)

    def click_tags_drop_down_arrow(self):
        """
        Click the tags drop down arrow
        """
        arrow = self.get_tags_drop_down_arrow()
        arrow.click()

    def get_save_and_close_button(self):
        """
        Get the 'save and close' button
        :return: 'save and close' button
        :rtype: WebElement
        """
        return self.browser.find_element(*EditEntitlementLocators.SAVE_AND_CLOSE_BUTTON)

    def click_save_and_close_button(self):
        """
        Click the 'save and close' button
        """
        button = self.get_save_and_close_button()
        button.click()

    def get_save_button(self):
        """
        Get the save button
        :return: save button
        :rtype: WebElement
        """
        return self.browser.find_element(*EditEntitlementLocators.SAVE_BUTTON)

    def click_save_button(self):
        """
        Click the save button
        """
        button = self.get_save_button()
        self.browser.execute_script('arguments[0].click()', button)

    def get_cancel_button(self):
        """
        Get the cancel button
        :return: cancel button
        :rtype: WebElement
        """
        return self.browser.find_element(*EditEntitlementLocators.CANCEL_BUTTON)

    def click_cancel_button(self):
        """
        Click the cancel button
        """
        button = self.get_cancel_button()
        button.click()
