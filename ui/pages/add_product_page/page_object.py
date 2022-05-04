from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from locators import AddProductLocators
from ui.main.constants import DEFAULT_PAGE_TIMEOUT
from ui.pages.base_page import BasePage
from ui.main.patterns.waiters import wait_for_non_empty_text


class AddProduct(BasePage):
    def wait_for_page_load(self):
        """
        Wait for the page to be fully loaded
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(AddProductLocators.SAVE_BUTTON),
            '"Add Product" page failed to load'
        )

    def wait_for_friendly_name_invalid_message(self):
        """
        Wait for the error message to appear after entering not allowed characters into friendly name field
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            wait_for_non_empty_text(AddProductLocators.FRIENDLY_NAME_INVALID_MESSAGE),
            'Friendly name invalid message did not display'
        )

    def wait_for_code_invalid_message(self):
        """
        Wait for the error message to appear after entering not allowed characters into code
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            wait_for_non_empty_text(AddProductLocators.CODE_INVALID_MESSAGE),
            'Code invalid message did not display'
        )

    def get_add_product_header(self):
        """
        Get the add product page header
        :return: add product page header
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.ADD_PRODUCT_HEADER)

    def get_friendly_name_label(self):
        """
        Get the friendly name label
        :return: friendly name label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.FRIENDLY_NAME_LABEL)

    def get_friendly_name_input(self):
        """
        Get the friendly name input
        :return: friendly name input
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.FRIENDLY_NAME_INPUT)

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
        return self.browser.find_element(*AddProductLocators.FRIENDLY_NAME_INVALID_MESSAGE)

    def get_code_label(self):
        """
        Get the code label
        :return: code label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.CODE_LABEL)

    def get_code_input(self):
        """
        Get the code input
        :return: code input
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.CODE_INPUT)

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
        return self.browser.find_element(*AddProductLocators.CODE_INVALID_MESSAGE)

    def get_active_header(self):
        """
        Get the active header
        :return: active header
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.ACTIVE_HEADER)

    def get_active_toggle(self):
        """
        Get the active toggle
        :return: active toggle
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.ACTIVE_TOGGLE)

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
        return self.browser.find_element(*AddProductLocators.ACTIVE_CHECKBOX)

    def get_inactive_label(self):
        """
        Get the inactive label
        :return: inactive label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.INACTIVE_LABEL)

    def get_active_label(self):
        """
        Get the active label
        :return: active label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.ACTIVE_LABEL)

    def get_metadata_header(self):
        """
        Get the metadata header
        :return: metadata header
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.METADATA_HEADER)

    def get_metadata_toggle(self):
        """
        Get the metadata toggle
        :return: metadata toggle
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.METADATA_TOGGLE)

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
        return self.browser.find_element(*AddProductLocators.METADATA_CHECKBOX)

    def get_field_editor_label(self):
        """
        Get the field editor label
        :return: field editor label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.FIELD_EDITOR_LABEL)

    def get_code_editor_label(self):
        """
        Get the code editor label
        :return: code editor label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.CODE_EDITOR_LABEL)

    def get_tags_header(self):
        """
        Get the tags header
        :return: tags header
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.TAGS_HEADER)

    def get_tags_input(self):
        """
        Get the tags input
        :return: tags input
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.TAGS_INPUT)

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
        return self.browser.find_element(*AddProductLocators.TAGS_DROP_DOWN_ARROW)

    def click_tags_drop_down_arrow(self):
        """
        Click tags drop down arrow
        """
        button = self.get_tags_drop_down_arrow()
        button.click()

    def get_name_header(self):
        """
        Get the name header
        :return: name header
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.NAME_HEADER)

    def get_name_key_label(self):
        """
        Get the name key label
        :return: name key label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.NAME_KEY_LABEL)

    def get_name_key_input(self):
        """
        Get the name key input
        :return: name key input
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.NAME_KEY_INPUT)

    def type_name_key_input(self, value):
        """
        Type in the name key input
        :param value: value want to type
        :type value: str
        """
        input_field = self.get_name_key_input()
        input_field.send_keys(value)

    def get_name_value_label(self):
        """
        Get the name value label
        :return: name value label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.NAME_VALUE_LABEL)

    def get_name_value_input(self):
        """
        Get the name value input
        :return: name value input
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.NAME_VALUE_INPUT)

    def type_name_value_input(self, value):
        """
        Type in the name value input
        :param value: value want to type
        :type value: str
        """
        input_field = self.get_name_value_input()
        input_field.send_keys(value)

    def get_name_add_button(self):
        """
        Get the name add button
        :return: name add button
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.NAME_ADD_BUTTON)

    def click_name_add_button(self):
        """
        Click the name add button
        """
        button = self.get_name_add_button()
        button.click()

    def get_description_header(self):
        """
        Get the description header
        :return: description header
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.DESCRIPTION_HEADER)

    def get_description_key_label(self):
        """
        Get the description key label
        :return: description key label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.DESCRIPTION_KEY_LABEL)

    def get_description_key_input(self):
        """
        Get the description key input
        :return: description key input
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.DESCRIPTION_KEY_INPUT)

    def type_description_key_input(self, value):
        """
        Type in the description key input
        :param value: value want to type
        :type value: str
        """
        input_field = self.get_description_key_input()
        input_field.send_keys(value)

    def get_description_value_label(self):
        """
        Get the description value label
        :return: description value label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.DESCRIPTION_VALUE_LABEL)

    def get_description_value_input(self):
        """
        Get the description value input
        :return: description value input
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.DESCRIPTION_VALUE_INPUT)

    def type_description_value_input(self, value):
        """
        Type in the description value input
        :param value: value want to type
        :type value: str
        """
        input_field = self.get_description_value_input()
        input_field.send_keys(value)

    def get_description_add_button(self):
        """
        Get the description add button
        :return: description add button
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.DESCRIPTION_ADD_BUTTON)

    def click_description_add_button(self):
        """
        Click the description add button
        """
        button = self.get_description_add_button()
        button.click()

    def get_purchasable_header(self):
        """
        Get the purchasable header
        :return: purchasable header
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.PURCHASABLE_HEADER)

    def get_purchasable_toggle(self):
        """
        Get the purchasable toggle
        :return: purchasable toggle
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.PURCHASABLE_TOGGLE)

    def click_purchasable_toggle(self):
        """
        Click the purchasable toggle
        """
        toggle = self.get_purchasable_toggle()
        self.browser.execute_script('arguments[0].click()', toggle)

    def get_purchasable_checkbox(self):
        """
        Get the purchasable checkbox
        :return: purchasable checkbox
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.PURCHASABLE_CHECKBOX)

    def get_not_purchasable_label(self):
        """
        Get the not purchasable label
        :return: not purchasable label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.NOT_PURCHASABLE_LABEL)

    def get_purchasable_label(self):
        """
        Get the purchasable label
        :return: purchasable label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.PURCHASABLE_LABEL)

    def get_visible_header(self):
        """
        Get the visible header
        :return: visible header
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.VISIBLE_HEADER)

    def get_visible_toggle(self):
        """
        Get the visible toggle
        :return: visible toggle
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.VISIBLE_TOGGLE)

    def click_visible_toggle(self):
        """
        Click the visible toggle
        """
        toggle = self.get_visible_toggle()
        toggle.click()

    def get_visible_checkbox(self):
        """
        Get the visible checkbox
        :return: visible checkbox
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.VISIBLE_CHECKBOX)

    def get_invisible_label(self):
        """
        Get the invisible label
        :return: invisible label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.INVISIBLE_LABEL)

    def get_visible_label(self):
        """
        Get the visible label
        :return: visible label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.VISIBLE_LABEL)

    def get_restricted_countries_header(self):
        """
        Get the Restricted Countries header
        :return: Restricted Countries header
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.RESTRICTED_COUNTRIES_HEADER)

    def get_restricted_countries_input(self):
        """
        Get the Restricted Countries input
        :return: Restricted Countries  input
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.RESTRICTED_COUNTRIES_INPUT)

    def type_restricted_countries_input(self, value):
        """
        Type in the Restricted Countries input
        :param value: value want to type
        :type value: str
        """
        input_field = self.get_restricted_countries_input()
        input_field.send_keys(value)

    def get_restricted_countries_drop_down_arrow(self):
        """
        Get Restricted Countries drop down arrow
        :return: Restricted Countries drop down arrow
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.RESTRICTED_COUNTRIES_DROP_DOWN_ARROW)

    def click_restricted_countries_drop_down_arrow(self):
        """
        Click Restricted Countries drop down arrow
        """
        button = self.get_restricted_countries_drop_down_arrow()
        button.click()

    def get_spa_access_header(self):
        """
        Get the SPA Access header
        :return: SPA Access header
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.SPA_ACCESS_HEADER)

    def get_spa_access_input(self):
        """
        Get the SPA Access input
        :return: SPA Access input
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.SPA_ACCESS_INPUT)

    def type_spa_access_input(self, value):
        """
        Type in the SPA Access input
        :param value: value want to type
        :type value: str
        """
        input_field = self.get_spa_access_input()
        input_field.send_keys(value)

    def get_spa_access_drop_down_arrow(self):
        """
        Get SPA Access drop down arrow
        :return: SPA Access drop down arrow
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.SPA_ACCESS_DROP_DOWN_ARROW)

    def click_spa_access_drop_down_arrow(self):
        """
        Click SPA Access drop down arrow
        """
        button = self.get_spa_access_drop_down_arrow()
        button.click()

    def get_prices_list(self):
        """
        Get a list of Prices
        :return: list of Prices
        :rtype: list of WebElement
        """
        return self.browser.find_elements(*AddProductLocators.PRICES_LIST)

    def get_prices_rm_header(self):
        """
        Get Prices real money header
        :return: Prices real money header
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.PRICES_RM_HEADER)

    def get_prices_currency_code_header(self):
        """
        Get Prices currency code header
        :return: Prices currency code header
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.PRICES_CURRENCY_CODE_HEADER)

    def get_prices_amount_header(self):
        """
        Get Prices amount header
        :return: Prices amount header
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.PRICES_AMOUNT_HEADER)

    def get_save_button(self):
        """
        Get the save button
        :return: save button
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.SAVE_BUTTON)

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
        return self.browser.find_element(*AddProductLocators.CANCEL_BUTTON)

    def click_cancel_button(self):
        """
        Click the cancel button
        """
        button = self.get_cancel_button()
        button.click()

    def get_entity_heading(self, entity_type):
        """
        Get the heading of the entity type
        :param entity_type: entity type whose header want
        :type entity_type: str
        :return: heading for the entity type
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.get_entity_heading_by_entity_type_locator(entity_type))

    def get_entity_add_button(self, entity_type):
        """
        Get the add button of the entity type
        :param entity_type: entity type whose add button want
        :type entity_type: str
        :return: add button for the entity type
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.get_entity_add_button_by_entity_type_locator(entity_type))

    def click_entity_add_button(self, entity_type):
        """
        Click the add button of the entity type
        :param entity_type: entity type whose add button want to click
        :type entity_type: str
        """
        button = self.get_entity_add_button(entity_type)
        button.click()

    def get_entity_table_code_column(self, entity_type):
        """
        Get the table's Code column based on the entity type (after adding a currency to the product)
        :param entity_type: entity type whose Code column want
        :type entity_type: str
        :return: table's Code column for the entity type
        :rtype: WebElement
        """
        return self.browser.find_element(
            *AddProductLocators.get_entity_table_code_column_locator_by_entity_type(entity_type))

    def get_entity_table_amount_column(self, entity_type):
        """
        Get the table's Amount column based on the entity type (after adding a currency to the product)
        :param entity_type: entity type whose Amount column want
        :type entity_type: str
        :return: table's Amount column for the entity type
        :rtype: WebElement
        """
        return self.browser.find_element(
            *AddProductLocators.get_entity_table_amount_column_locator_by_entity_type(entity_type))

    def get_entity_table_pct_value_column(self, entity_type):
        """
        Get the table's PCT Value column based on the entity type (after adding a currency to the product)
        :param entity_type: entity type whose PCT Value column want
        :type entity_type: str
        :return: table's PCT Value column for the entity type
        :rtype: WebElement
        """
        return self.browser.find_element(
            *AddProductLocators.get_entity_table_pct_value_column_locator_by_entity_type(entity_type))

    def get_entity_by_name(self, name):
        """
        Get an entity based on the name (after adding a currency to the product)
        :param name: Name of the entity
        :type name: str
        :return: specific entity
        :rtype: WebElement
        """
        return WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(
                AddProductLocators.get_entity_locator_by_name(name)
            ),
            '{} could not be found'.format(name)
        )

    def get_entity_list(self, entity_type):
        """
        Get a list of entities (after adding at least one entity to the product)
        :param entity_type: entity type whose list want
        :type entity_type: str
        :return: list of entities for the entity type
        :rtype: list of WebElement
        """
        return self.browser.find_elements(*AddProductLocators.get_entity_list_locator_by_entity_type(entity_type))

    def get_entity_amount_input(self, name):
        """
        Get the entity's amount input based on the name (after adding a currency to the product)
        :param name: Name of the entity
        :type name: str
        :return: amount input
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.get_entity_amount_input_locator_by_name(name))

    def type_entity_amount_input(self, value, name):
        """
        Type in the amount input
        :param value: value want to type
        :type value: str
        :param name: Name of the entity
        :type name: str
        """
        input_field = self.get_entity_amount_input(name)
        input_field.send_keys(value)

    def get_entity_pct_value_input(self, name):
        """
        Get the entity's pct value input based on the name (after adding a currency to the product)
        :param name: Name of the entity
        :type name: str
        :return: pct value input
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.get_entity_pct_value_input_locator_by_name(name))

    def type_entity_pct_value_input(self, value, name):
        """
        Type in the pct value input
        :param value: value want to type
        :type value: str
        :param name: Name of the entity
        :type name: str
        """
        input_field = self.get_entity_pct_value_input(name)
        input_field.send_keys(value)

    def get_entity_remove_button(self, name):
        """
        Get the entity's remove button based on the name (after adding a currency to the product)
        :param name: Name of the entity
        :type name: str
        :return: remove button
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.get_entity_remove_button_locator_by_name(name))

    def click_entity_remove_button(self, name):
        """
        Click the entity's remove button based on the name
        :param name: Name of the entity
        :type name: str
        """
        button = self.get_entity_remove_button(name)
        button.click()

    def get_prices_toggle(self, currency_code):
        """
        Get the toggle of a specific Currency
        :param currency_code: Code of the Currency
        :type currency_code: str
        :return: toggle of the Currency
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.get_prices_toggle_locator_by_currency(currency_code))

    def get_prices_vc_currency_code(self, currency_code):
        """
        Get the VC Currency Code
        :param currency_code: Code of the Currency
        :type currency_code: Str
        :return: VC Currency Code
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.get_prices_vc_currency_code_locator_by_currency(
            currency_code
        ))

    def get_prices_rm_currency_code(self, currency_code):
        """
        Get the RM Currency Code
        :param currency_code: Code of the Currency
        :type currency_code: Str
        :return: RM Currency Code
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.get_prices_rm_currency_code_locator_by_currency(
            currency_code
        ))

    def get_prices_pricing_type(self, currency_code):
        """
        Get the Pricing Type of a specific Currency
        :param currency_code: Code of the Currency
        :type currency_code: str
        :return: Pricing Type of the Currency
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.get_prices_pricing_type_locator_by_currency(currency_code))

    def click_prices_pricing_type(self, currency_code):
        """
        Click the Pricing Type of a specific Currency
        :param currency_code: Code of the Currency
        :type currency_code: str
        """
        pricing_type = self.get_prices_pricing_type(currency_code)
        pricing_type.click()

    def get_prices_amount(self, currency_code):
        """
        Get the Amount of a specific Currency
        :param currency_code: Code of the Currency
        :type currency_code: str
        :return: Amount of the Currency
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.get_prices_amount_locator_by_currency(currency_code))

    def type_prices_amount(self, currency_code, value):
        """
        Type into Amount of a specific Currency
        :param currency_code: Code of the Currency
        :type currency_code: str
        :param value: Value want to type
        :type value: str
        """
        input_field = self.get_prices_amount(currency_code)
        input_field.send_keys(value)

    def get_prices_delete_button(self, currency_code):
        """
        Get Delete button of a specific Currency
        :param currency_code: Code of the Currency
        :type currency_code: str
        :return: Delete button of the Currency
        :rtype: WebElement
        """
        return self.browser.find_element(*AddProductLocators.get_prices_delete_button_locator_by_currency(
            currency_code
        ))

    def click_prices_delete_button(self, currency_code):
        """
        Click the Delete button of a specific Currency
        :param currency_code: Code of the Currency
        :type currency_code: str
        """
        button = self.get_prices_delete_button(currency_code)
        button.click()
