from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from locators import AddCurrencyLocators
from ui.main.constants import DEFAULT_PAGE_TIMEOUT
from ui.pages.base_page import BasePage
from ui.main.patterns.waiters import wait_for_non_empty_text


class AddCurrency(BasePage):
    def wait_for_page_load(self):
        """
        Wait for the page to be fully loaded
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(AddCurrencyLocators.SAVE_BUTTON),
            '"Add Currency" page failed to load'
        )

    def wait_for_friendly_name_invalid_message(self):
        """
        Wait for the error message to appear after entering not allowed characters into friendly name field
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            wait_for_non_empty_text(AddCurrencyLocators.FRIENDLY_NAME_INVALID_MESSAGE),
            'Friendly name invalid message did not display'
        )

    def wait_for_code_invalid_message(self):
        """
        Wait for the error message to appear after entering not allowed characters into code
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            wait_for_non_empty_text(AddCurrencyLocators.CODE_INVALID_MESSAGE),
            'Code invalid message did not display'
        )

    def get_add_currency_header(self):
        """
        Get the add currency page header
        :return: add currency page header
        :rtype: WebElement
        """
        return self.browser.find_element(*AddCurrencyLocators.ADD_CURRENCY_HEADER)

    def get_friendly_name_label(self):
        """
        Get the friendly name label
        :return: friendly name label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddCurrencyLocators.FRIENDLY_NAME_LABEL)

    def get_friendly_name_input(self):
        """
        Get the friendly name input
        :return: friendly name input
        :rtype: WebElement
        """
        return self.browser.find_element(*AddCurrencyLocators.FRIENDLY_NAME_INPUT)

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
        return self.browser.find_element(*AddCurrencyLocators.FRIENDLY_NAME_INVALID_MESSAGE)

    def get_code_label(self):
        """
        Get the code label
        :return: code label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddCurrencyLocators.CODE_LABEL)

    def get_code_input(self):
        """
        Get the code input
        :return: code input
        :rtype: WebElement
        """
        return self.browser.find_element(*AddCurrencyLocators.CODE_INPUT)

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
        return self.browser.find_element(*AddCurrencyLocators.CODE_INVALID_MESSAGE)

    def get_active_header(self):
        """
        Get the active header
        :return: active header
        :rtype: WebElement
        """
        return self.browser.find_element(*AddCurrencyLocators.ACTIVE_HEADER)

    def get_active_toggle(self):
        """
        Get the active toggle
        :return: active toggle
        :rtype: WebElement
        """
        return self.browser.find_element(*AddCurrencyLocators.ACTIVE_TOGGLE)

    def click_active_toggle(self):
        """
        Click the active toggle
        """
        toggle = self.get_active_toggle()
        toggle.click()

    def get_metadata_header(self):
        """
        Get the metadata header
        :return: metadata header
        :rtype: WebElement
        """
        return self.browser.find_element(*AddCurrencyLocators.METADATA_HEADER)

    def get_metadata_toggle(self):
        """
        Get the metadata toggle
        :return: metadata toggle
        :rtype: WebElement
        """
        return self.browser.find_element(*AddCurrencyLocators.METADATA_TOGGLE)

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
        return self.browser.find_element(*AddCurrencyLocators.METADATA_CHECKBOX)

    def get_metadata_field_editor_label(self):
        """
        Get the metadata field editor label
        :return: metadata field editor label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddCurrencyLocators.METADATA_FIELD_EDITOR_LABEL)

    def get_metadata_code_editor_label(self):
        """
        Get the metadata code editor label
        :return: metadata code editor label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddCurrencyLocators.METADATA_CODE_EDITOR_LABEL)

    def get_tags_header(self):
        """
        Get the tags header
        :return: tags header
        :rtype: WebElement
        """
        return self.browser.find_element(*AddCurrencyLocators.TAGS_HEADER)

    def get_tags_input(self):
        """
        Get the tags input
        :return: tags input
        :rtype: WebElement
        """
        return self.browser.find_element(*AddCurrencyLocators.TAGS_INPUT)

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
        return self.browser.find_element(*AddCurrencyLocators.TAGS_DROP_DOWN_ARROW)

    def click_tags_drop_down_arrow(self):
        """
        Click tags drop down arrow
        """
        button = self.get_tags_drop_down_arrow()
        button.click()

    def get_include_currency_fin_report_label(self):
        """
        Get the Include Currency in Finance Reports label
        :return: Include Currency in Finance Reports label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddCurrencyLocators.INCLUDE_CURRENCY_FIN_RPT_LABEL)

    def get_include_currency_fin_report_toggle(self):
        """
        Get the Include Currency in Finance Reports toggle
        :return: Include Currency in Finance Reports toggle
        :rtype: WebElement
        """
        return self.browser.find_element(*AddCurrencyLocators.INCLUDE_CURRENCY_FIN_RPT_TOGGLE)

    def click_include_currency_fin_report_toggle(self):
        """
        Click the Include Currency in Finance Reports toggle
        """
        toggle = self.get_include_currency_fin_report_toggle()
        toggle.click()

    def get_decimal_reported_fin_report_label(self):
        """
        Get the Decimal Reported to Finance Report label
        :return: Decimal Reported to Finance Report label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddCurrencyLocators.DECIMAL_REPORTED_FIN_RPT_LABEL)

    def get_decimal_reported_fin_report_input(self):
        """
        Get the Decimal Reported to Finance Report input
        :return: Decimal Reported to Finance Report input
        :rtype: WebElement
        """
        return self.browser.find_element(*AddCurrencyLocators.DECIMAL_REPORTED_FIN_RPT_INPUT)

    def type_decimal_reported_fin_report_input(self, value):
        """
        Type in the Decimal Reported to Finance Report input
        :param value: value want to type
        :type value: str
        """
        input_field = self.get_decimal_reported_fin_report_label()
        input_field.send_keys(value)

    def get_save_button(self):
        """
        Get the save button
        :return: save button
        :rtype: WebElement
        """
        return self.browser.find_element(*AddCurrencyLocators.SAVE_BUTTON)

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
        return self.browser.find_element(*AddCurrencyLocators.CANCEL_BUTTON)

    def click_cancel_button(self):
        """
        Click the cancel button
        """
        button = self.get_cancel_button()
        button.click()
