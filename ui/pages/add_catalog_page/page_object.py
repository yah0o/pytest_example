from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from locators import AddCatalogLocators
from ui.pages.base_page import BasePage
from ui.main.constants import DEFAULT_PAGE_TIMEOUT


class AddCatalog(BasePage):
    def wait_for_page_load(self):
        """
        Wait for the page to load
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(AddCatalogLocators.SAVE_BUTTON),
            '"Add catalog" page failed to load'
        )

    def get_add_catalog_header(self):
        """
        Get the header for the add catalog page
        :return: header for add catalog page
        :rtype: WebElement
        """
        return self.browser.find_element(*AddCatalogLocators.ADD_CATALOG_HEADER)

    def get_field_header(self, field):
        """
        Get the header for specific field
        :param field: field of the header
        :type field: str
        :return: header
        :rtype: WebElement
        """
        return self.browser.find_element(*AddCatalogLocators.get_header_by_name(field))

    def get_field_label(self, field):
        """
        Get the label for specific field
        :param field: field of the label
        :type field: str
        :return: label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddCatalogLocators.get_field_label_by_name(field))

    def get_field_input(self, field):
        """
        Get the input for a field
        :param field: field of the input
        :type field: str
        :return: input
        :rtype: WebElement
        """
        return self.browser.find_element(*AddCatalogLocators.get_field_input_by_name(field))

    def type_field_input(self, field, value):
        """
        Type into the input for the field
        :param field: field of the input
        :type field: str
        :param value: value to type into the input
        :type value: str
        """
        input_field = self.get_field_input(field)
        input_field.send_keys(value)

    def get_field_invalid_message(self, field):
        """
        Get field's invalid message
        :param field: field of the invalid message
        :type field: str
        :return: invalid message
        :rtype: WebElement
        """
        return self.browser.find_element(*AddCatalogLocators.get_field_invalid_message_by_name(field))

    def get_field_toggle(self, field):
        """
        Get the field's toggle
        :param field: field of the toggle
        :type field: str
        :return: toggle
        :rtype: WebElement
        """
        return self.browser.find_element(*AddCatalogLocators.get_field_toggle(field))

    def click_field_toggle(self, field):
        """
        Click the field's toggle
        :param field: field of the toggle
        :type field: str
        """
        toggle = self.get_field_toggle(field)
        toggle.click()

    def get_field_toggle_left_label(self, field):
        """
        Get the field's toggle left label
        :param field: field of the toggle
        :type field: str
        :return: toggle's left label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddCatalogLocators.get_field_toggle_left_label(field))

    def get_field_toggle_right_label(self, field):
        """
        Get the field's toggle right label
        :param field: field of the toggle
        :type field: str
        :return: toggle's right label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddCatalogLocators.get_field_toggle_right_label(field))

    def get_active_header(self):
        """
        Get the active header
        :return: active header
        :rtype: WebElement
        """
        return self.browser.find_element(*AddCatalogLocators.ACTIVE_HEADER)

    def get_tags_input(self):
        """
        Get the tags input
        :return: tags input
        :rtype: WebElement
        """
        return self.browser.find_element(*AddCatalogLocators.TAGS_INPUT)

    def type_tags_input(self, value):
        """
        Type into the tags input
        :param value: value to type into tags input
        :type value: str
        """
        input_field = self.get_tags_input()
        input_field.send_keys(value)

    def get_notification_templates_add_json_button(self):
        """
        Get notification templates add new json field button
        :return: notification templates add new json field button
        :rtype: WebElement
        """
        return self.browser.find_element(*AddCatalogLocators.ADD_JSON_BUTTON)

    def click_notification_templates_add_json_button(self):
        """
        Click notification templates add new json field button
        """
        button = self.get_notification_templates_add_json_button()
        button.click()

    def get_feature_flags_add_json_button(self):
        """
        Get feature flags add new json field button
        :return: feature flags add new json field button
        :rtype: WebElement
        """
        return self.browser.find_element(*AddCatalogLocators.ADD_JSON_BUTTON)

    def click_feature_flags_add_json_button(self):
        """
        Click feature flags add new json field button
        """
        button = self.get_feature_flags_add_json_button()
        button.click()

    def get_metadata_add_namespace_button(self):
        """
        Get metadata add new namespace button
        :return: metadata add namespace button
        :rtype: WebElement
        """
        return self.browser.find_element(*AddCatalogLocators.ADD_NAMESPACE_BUTTON)

    def click_metadata_add_namespace_button(self):
        """
        Click metadata add new json field button
        """
        button = self.get_metadata_add_namespace_button()
        button.click()

    def get_save_button(self):
        """
        Get the save button
        :return: save button
        :rtype: WebElement
        """
        return self.browser.find_element(*AddCatalogLocators.SAVE_BUTTON)

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
        return self.browser.find_element(*AddCatalogLocators.CANCEL_BUTTON)

    def click_cancel_button(self):
        """
        Click the cancel button
        """
        button = self.get_cancel_button()
        button.click()
