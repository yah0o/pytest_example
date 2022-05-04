from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from locators import EditCurrencyLocators
from ui.main.constants import DEFAULT_PAGE_TIMEOUT
from ui.pages.base_page import BasePage
from ui.main.patterns.waiters import wait_for_non_empty_text


class EditCurrency(BasePage):
    def wait_for_page_load(self):
        """
        Wait for the page to be fully loaded
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(EditCurrencyLocators.SAVE_AND_CLOSE_BUTTON),
            '"Edit Currency" page failed to load'
        )

    def wait_for_friendly_name_invalid_message(self):
        """
        Wait for the error message to appear after entering not allowed characters into friendly name field
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            wait_for_non_empty_text(EditCurrencyLocators.FRIENDLY_NAME_INVALID_MESSAGE),
            'Invalid friendly name message did not display'
        )

    def get_edit_currency_header(self):
        """
        Get the edit currency header
        :return: edit currency header
        :rtype: WebElement
        """
        return self.browser.find_element(*EditCurrencyLocators.EDIT_CURRENCY_HEADER)

    def get_info_box(self):
        """
        Get the info box
        :return: info box
        :rtype: WebElement
        """
        return self.browser.find_element(*EditCurrencyLocators.INFO_BOX)

    def get_basic_info_header(self):
        """
        Get the basic info header
        :return: basic info header
        :rtype: WebElement
        """
        return self.browser.find_element(*EditCurrencyLocators.BASIC_INFO)

    def get_friendly_name_label(self):
        """
        Get the friendly name label
        :return: friendly name label
        :rtype: WebElement
        """
        return self.browser.find_element(*EditCurrencyLocators.FRIENDLY_NAME_LABEL)

    def get_friendly_name_input(self):
        """
        Get the friendly name input
        :return: friendly name input
        :rtype: WebElement
        """
        return self.browser.find_element(*EditCurrencyLocators.FRIENDLY_NAME_INPUT)

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
        return self.browser.find_element(*EditCurrencyLocators.FRIENDLY_NAME_INVALID_MESSAGE)

    def get_active_header(self):
        """
        Get the active header
        :return: active header
        :rtype: WebElement
        """
        return self.browser.find_element(*EditCurrencyLocators.ACTIVE_HEADER)

    def get_active_toggle(self):
        """
        Get the active toggle
        :return: active toggle
        :rtype: WebElement
        """
        return self.browser.find_element(*EditCurrencyLocators.ACTIVE_TOGGLE)

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
        return self.browser.find_element(*EditCurrencyLocators.ACTIVE_CHECKBOX)

    def get_inactive_label(self):
        """
        Get the inactive label
        :return: inactive label
        :rtype: WebElement
        """
        return self.browser.find_element(*EditCurrencyLocators.INACTIVE_LABEL)

    def get_active_label(self):
        """
        Get the active label
        :return: active label
        :rtype: WebElement
        """
        return self.browser.find_element(*EditCurrencyLocators.ACTIVE_LABEL)

    def get_tags_header(self):
        """
        Get the tags header
        :return: tags header
        :rtype: WebElement
        """
        return self.browser.find_element(*EditCurrencyLocators.TAGS_HEADER)

    def get_tags_input(self):
        """
        Get the tags input
        :return: tags input
        :rtype: WebElement
        """
        return self.browser.find_element(*EditCurrencyLocators.TAGS_INPUT)

    def type_tags_input(self, value):
        """
        Type in the tags input
        :param value: value want to type
        :type value: str
        """
        input_field = self.get_tags_input()
        input_field.send_keys(value)

    def get_platform_info_header(self):
        """
        Get the platform info header
        :return: platform info header
        :rtype: WebElement
        """
        return self.browser.find_element(*EditCurrencyLocators.PLATFORM_INFO)

    def get_code_label(self):
        """
        Get the code label
        :return: code label
        :rtype: WebElement
        """
        return self.browser.find_element(*EditCurrencyLocators.CODE_LABEL)

    def get_code_input(self):
        """
        Get the code input
        :return: code input
        :rtype: WebElement
        """
        return self.browser.find_element(*EditCurrencyLocators.CODE_INPUT)

    def get_version_label(self):
        """
        Get the version label
        :return: version label
        :rtype: WebElement
        """
        return self.browser.find_element(*EditCurrencyLocators.VERSION_LABEL)

    def get_version_input(self):
        """
        Get the version input
        :return: version input
        :rtype: WebElement
        """
        return self.browser.find_element(*EditCurrencyLocators.VERSION_INPUT)

    def get_currency_settings_header(self):
        """
        Get the currency settings header
        :return: currency settings header
        :rtype: WebElement
        """
        return self.browser.find_element(*EditCurrencyLocators.CURRENCY_SETTINGS)

    def get_reported_header(self):
        """
        Get the reported header
        :return: reported header
        :rtype: WebElement
        """
        return self.browser.find_element(*EditCurrencyLocators.REPORTED_HEADER)

    def get_reported_toggle(self):
        """
        Get the reported toggle
        :return: reported toggle
        :rtype: WebElement
        """
        return self.browser.find_element(*EditCurrencyLocators.REPORTED_TOGGLE)

    def click_reported_toggle(self):
        """
        Click the reported toggle
        """
        toggle = self.get_reported_toggle()
        self.browser.execute_script('arguments[0].click()', toggle)

    def get_reported_checkbox(self):
        """
        Get the reported checkbox
        :return: reported checkbox
        :rtype: WebElement
        """
        return self.browser.find_element(*EditCurrencyLocators.REPORTED_CHECKBOX)

    def get_not_included_label(self):
        """
        Get the not included label
        :return: not included label
        :rtype: WebElement
        """
        return self.browser.find_element(*EditCurrencyLocators.NOT_INCLUDED_LABEL)

    def get_included_label(self):
        """
        Get the included label
        :return: included label
        :rtype: WebElement
        """
        return self.browser.find_element(*EditCurrencyLocators.INCLUDED_LABEL)

    def get_price_precision_label(self):
        """
        Get the price precision label
        :return: price precision label
        :rtype: WebElement
        """
        return self.browser.find_element(*EditCurrencyLocators.PRICE_PRECISION_LABEL)

    def get_price_precision_input(self):
        """
        Get the price precision input
        :return: price precision input
        :rtype: WebElement
        """
        return self.browser.find_element(*EditCurrencyLocators.PRICE_PRECISION_INPUT)

    def type_price_precision_input(self, value):
        """
        Type into the price precision input
        :param value: Value want to type into price precision input
        :type value: str
        """
        input_field = self.get_price_precision_input()
        input_field.send_keys(value)

    def get_price_precision_invalid_message(self):
        """
        Get the price precision invalid message
        :return: price precision invalid message
        :rtype: WebElement
        """
        return self.browser.find_element(*EditCurrencyLocators.PRICE_PRECISION_INVALID_MESSAGE)

    def get_custom_data_header(self):
        """
        Get the currency settings header
        :return: currency settings header
        :rtype: WebElement
        """
        return self.browser.find_element(*EditCurrencyLocators.CUSTOM_DATA)

    def get_metadata_label(self):
        """
        Get the metadata label
        :return: metadata label
        :rtype: WebElement
        """
        return self.browser.find_element(*EditCurrencyLocators.METADATA_LABEL)

    def get_metadata_toggle(self):
        """
        Get the metadata toggle
        :return: metadata toggle
        :rtype: WebElement
        """
        return self.browser.find_element(*EditCurrencyLocators.METADATA_TOGGLE)

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
        return self.browser.find_element(*EditCurrencyLocators.METADATA_CHECKBOX)

    def get_field_editor_label(self):
        """
        Get the field editor label
        :return: field editor label
        :rtype: WebElement
        """
        return self.browser.find_element(*EditCurrencyLocators.FIELD_EDITOR_LABEL)

    def get_code_editor_label(self):
        """
        Get the code editor label
        :return: code editor label
        :rtype: WebElement
        """
        return self.browser.find_element(*EditCurrencyLocators.CODE_EDITOR_LABEL)

    def get_save_and_close_button(self):
        """
        Get the save and close button
        :return: save and close button
        :rtype: WebElement
        """
        return self.browser.find_element(*EditCurrencyLocators.SAVE_AND_CLOSE_BUTTON)

    def click_save_and_close_button(self):
        """
        Click the save and close button
        """
        button = self.get_save_and_close_button()
        button.click()

    def get_save_button(self):
        """
        Get the save button
        :return: save button
        :rtype: WebElement
        """
        return self.browser.find_element(*EditCurrencyLocators.SAVE_BUTTON)

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
        return self.browser.find_element(*EditCurrencyLocators.CANCEL_BUTTON)

    def click_cancel_button(self):
        """
        Click the cancel button
        """
        button = self.get_cancel_button()
        button.click()
