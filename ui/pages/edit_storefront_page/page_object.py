from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from locators import EditStorefrontLocators
from ui.main.constants import DEFAULT_PAGE_TIMEOUT
from ui.pages.base_page import BasePage
from ui.main.patterns.waiters import wait_for_non_empty_text


class EditStorefront(BasePage):
    def wait_for_page_load(self):
        """
        Wait for the page to be fully loaded
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(EditStorefrontLocators.SAVE_BUTTON),
            '"Edit Storefront" page failed to load'
        )

    def wait_for_friendly_name_invalid_message(self):
        """
        Wait for the error message to appear after entering not allowed characters into friendly name field
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            wait_for_non_empty_text(EditStorefrontLocators.FRIENDLY_NAME_INVALID_MESSAGE),
            'Invalid friendly name message did not display'
        )

    def get_edit_storefront_header(self):
        """
        Get the edit storefront header
        :return: edit storefront header
        :rtype: WebElement
        """
        return self.browser.find_element(*EditStorefrontLocators.EDIT_STOREFRONT_HEADER)

    def get_friendly_name_label(self):
        """
        Get the friendly name label
        :return: friendly name label
        :rtype: WebElement
        """
        return self.browser.find_element(*EditStorefrontLocators.FRIENDLY_NAME_LABEL)

    def get_friendly_name_input(self):
        """
        Get the friendly name input
        :return: friendly name input
        :rtype: WebElement
        """
        return self.browser.find_element(*EditStorefrontLocators.FRIENDLY_NAME_INPUT)

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
        return self.browser.find_element(*EditStorefrontLocators.FRIENDLY_NAME_INVALID_MESSAGE)

    def get_code_label(self):
        """
        Get the code label
        :return: code label
        :rtype: WebElement
        """
        return self.browser.find_element(*EditStorefrontLocators.CODE_LABEL)

    def get_code_input(self):
        """
        Get the code input
        :return: code input
        :rtype: WebElement
        """
        return self.browser.find_element(*EditStorefrontLocators.CODE_INPUT)

    def get_version_label(self):
        """
        Get the version label
        :return: version label
        :rtype: WebElement
        """
        return self.browser.find_element(*EditStorefrontLocators.VERSION_LABEL)

    def get_version_input(self):
        """
        Get the version input
        :return: version input
        :rtype: WebElement
        """
        return self.browser.find_element(*EditStorefrontLocators.VERSION_INPUT)

    def get_active_header(self):
        """
        Get the active header
        :return: active header
        :rtype: WebElement
        """
        return self.browser.find_element(*EditStorefrontLocators.ACTIVE_HEADER)

    def get_active_toggle(self):
        """
        Get the active toggle
        :return: active toggle
        :rtype: WebElement
        """
        return self.browser.find_element(*EditStorefrontLocators.ACTIVE_TOGGLE)

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
        return self.browser.find_element(*EditStorefrontLocators.ACTIVE_CHECKBOX)

    def get_metadata_header(self):
        """
        Get the metadata header
        :return: metadata header
        :rtype: WebElement
        """
        return self.browser.find_element(*EditStorefrontLocators.METADATA_HEADER)

    def get_metadata_toggle(self):
        """
        Get the metadata toggle
        :return: metadata toggle
        :rtype: WebElement
        """
        return self.browser.find_element(*EditStorefrontLocators.METADATA_TOGGLE)

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
        return self.browser.find_element(*EditStorefrontLocators.METADATA_CHECKBOX)

    def get_metadata_field_editor_label(self):
        """
        Get the metadata field editor label
        :return: metadata field editor label
        :rtype: WebElement
        """
        return self.browser.find_element(*EditStorefrontLocators.METADATA_FIELD_EDITOR_LABEL)

    def get_metadata_code_editor_label(self):
        """
        Get the metadata code editor label
        :return: metadata code editor label
        :rtype: WebElement
        """
        return self.browser.find_element(*EditStorefrontLocators.METADATA_CODE_EDITOR_LABEL)

    def get_tags_header(self):
        """
        Get the tags header
        :return: tags header
        :rtype: WebElement
        """
        return self.browser.find_element(*EditStorefrontLocators.TAGS_HEADER)

    def get_tags_input(self):
        """
        Get the tags input
        :return: tags input
        :rtype: WebElement
        """
        return self.browser.find_element(*EditStorefrontLocators.TAGS_INPUT)

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
        return self.browser.find_element(*EditStorefrontLocators.TAGS_DROP_DOWN_ARROW)

    def click_tags_drop_down_arrow(self):
        """
        Click the tags drop down arrow
        """
        arrow = self.get_tags_drop_down_arrow()
        arrow.click()

    def get_products_header(self):
        """
        Get the products header
        :return: products header
        :rtype: WebElement
        """
        return self.browser.find_element(*EditStorefrontLocators.PRODUCTS_HEADER)

    def get_product_add_button(self):
        """
        Get the product add button
        :return: product add button
        :rtype: WebElement
        """
        return self.browser.find_element(*EditStorefrontLocators.PRODUCT_ADD_BUTTON)

    def click_product_add_button(self):
        """
        Click the product add button
        """
        button = self.get_product_add_button()
        button.click()

    def get_product_table_code_column(self):
        """
        Get the product table code column (after adding a product to the storefront)
        :return: table's code column
        :rtype: WebElement
        """
        return self.browser.find_element(*EditStorefrontLocators.PRODUCT_CODE_COLUMN)

    def get_product_by_name(self, name):
        """
        Get a product by its name (after adding a product to the storefront)
        :param name: Name of the desired product
        :type name: str
        :return: product button
        :rtype: WebElement
        """
        return WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(
                EditStorefrontLocators.get_product_locator_by_name(name)
            ),
            '{} could not be found'.format(name)
        )

    def get_product_list(self):
        """
        Get a list of products (after adding at least one product to the storefront)
        :return: list of products
        :rtype: list of WebElement
        """
        return self.browser.find_elements(*EditStorefrontLocators.PRODUCT_LIST)

    def get_product_table_display_weight_column(self):
        """
        Get the product table display weight column (after adding a product to the storefront)
        :return: table's display weight column
        :rtype: WebElement
        """
        return self.browser.find_element(*EditStorefrontLocators.PRODUCT_DISPLAY_WEIGHT_COLUMN)

    def get_product_display_weight_input(self, name):
        """
        Get the product's display weight input (after adding a product to the storefront)
        :param name: Name of the Product
        :type name: str
        :return: display weight input
        :rtype: WebElement
        """
        return self.browser.find_element(
            *EditStorefrontLocators.get_product_display_weight_input_locator_by_name(name))

    def type_product_display_weight_input(self, value, name):
        """
        Type in the display weight input
        :param value: value want to type
        :type value: str
        :param name: Name of the Product
        :type name: str
        """
        input_field = self.get_product_display_weight_input(name)
        input_field.send_keys(value)

    def get_product_remove_button(self, name):
        """
        Get the product's remove button (after adding a product to the storefront)
        :param name: Name of the Product
        :type name: str
        :return: product's remove button
        :rtype: WebElement
        """
        return self.browser.find_element(*EditStorefrontLocators.get_product_remove_button_locator_by_name(name))

    def click_product_remove_button(self, name):
        """
        Click the product's remove button
        :param name: Name of the Product
        :type name: str
        """
        button = self.get_product_remove_button(name)
        button.click()

    def get_save_and_close_button(self):
        """
        Get the 'save and close' button
        :return: 'save and close' button
        :rtype: WebElement
        """
        return self.browser.find_element(*EditStorefrontLocators.SAVE_AND_CLOSE_BUTTON)

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
        return self.browser.find_element(*EditStorefrontLocators.SAVE_BUTTON)

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
        return self.browser.find_element(*EditStorefrontLocators.CANCEL_BUTTON)

    def click_cancel_button(self):
        """
        Click the cancel button
        """
        button = self.get_cancel_button()
        button.click()
