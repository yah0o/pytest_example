from selenium.webdriver.common.by import By


class EditProductLocators(object):
    EDIT_PRODUCT_HEADER = (By.ID, 'edit_product_header')
    FRIENDLY_NAME_LABEL = (By.ID, 'friendly_name_label_div')
    FRIENDLY_NAME_INPUT = (By.ID, 'friendly_name_input')
    FRIENDLY_NAME_INVALID_MESSAGE = (By.ID, 'friendly_name_input_invalid')
    CODE_LABEL = (By.ID, 'code_label_div')
    CODE_INPUT = (By.ID, 'code_input')
    VERSION_LABEL = (By.ID, 'version_label_div')
    VERSION_INPUT = (By.ID, 'version_input')

    ACTIVE_HEADER = (By.ID, 'active_header')
    ACTIVE_TOGGLE = (By.ID, 'active_toggle')
    ACTIVE_CHECKBOX = (By.ID, 'active')

    METADATA_HEADER = (By.ID, 'metadata_label')
    METADATA_TOGGLE = (By.ID, 'metadata_editor_toggle_toggle')
    METADATA_CHECKBOX = (By.ID, 'metadata_editor_toggle')
    METADATA_FIELD_EDITOR_LABEL = (By.ID, 'metadata_editor_toggle_labelLeft')
    METADATA_CODE_EDITOR_LABEL = (By.ID, 'metadata_editor_toggle_labelRight')

    TAGS_HEADER = (By.ID, 'tags_header')
    TAGS_INPUT = (By.ID, 'tags_drop_down')
    TAGS_DROP_DOWN_ARROW = (By.ID, 'icon_tags_drop_down')

    NAME_HEADER = (By.ID, 'name_header')
    NAME_KEY_LABEL = (By.ID, 'name_keyInput_label')
    NAME_KEY_INPUT = (By.ID, 'name_keyInput')
    NAME_VALUE_LABEL = (By.ID, 'name_valueInput_label')
    NAME_VALUE_INPUT = (By.ID, 'name_valueInput')
    NAME_ADD_BUTTON = (By.ID, 'name_add_button')

    DESCRIPTION_HEADER = (By.ID, 'description_header')
    DESCRIPTION_KEY_LABEL = (By.ID, 'description_keyInput_label')
    DESCRIPTION_KEY_INPUT = (By.ID, 'description_keyInput')
    DESCRIPTION_VALUE_LABEL = (By.ID, 'description_valueInput_label')
    DESCRIPTION_VALUE_INPUT = (By.ID, 'description_valueInput')
    DESCRIPTION_ADD_BUTTON = (By.ID, 'description_add_button')

    PURCHASABLE_LEFT = (By.ID, 'purchasable_labelLeft')
    PURCHASABLE_RIGHT = (By.ID, 'purchasable_labelRight')
    PURCHASABLE_TOGGLE = (By.ID, 'purchasable_toggle')
    PURCHASABLE_CHECKBOX = (By.ID, 'purchasable')

    VISIBLE_LEFT = (By.ID, 'visible_labelLeft')
    VISIBLE_RIGHT = (By.ID, 'visible_labelRight')
    VISIBLE_TOGGLE = (By.ID, 'visible_toggle')
    VISIBLE_CHECKBOX = (By.ID, 'visible')

    RESTRICTED_COUNTRIES_HEADER = (By.ID, 'restricted_countries_header')
    RESTRICTED_COUNTRIES_INPUT = (By.ID, 'restricted_countries_drop_down')
    RESTRICTED_COUNTRIES_DROP_DOWN_ARROW = (By.ID, 'icon_restricted_countries_drop_down')

    SPA_ACCESS_HEADER = (By.ID, 'spa_access_header')
    SPA_ACCESS_INPUT = (By.ID, 'spa_access_drop_down')
    SPA_ACCESS_DROP_DOWN_ARROW = (By.ID, 'icon_spa_access_drop_down')

    PRICES_LIST = (By.XPATH, "//tbody[@id='table_body_price_reference']/tr")
    PRICES_RM_HEADER = (By.ID, 'column_heading_price_reference_realMoney')
    PRICES_CURRENCY_CODE_HEADER = (By.ID, 'column_heading_price_reference_displayCode')
    PRICES_AMOUNT_HEADER = (By.ID, 'column_heading_price_reference_amount')

    SAVE_AND_CLOSE_BUTTON = (By.ID, 'edit_product_save_close_button')
    SAVE_BUTTON = (By.ID, 'edit_product_save_button')
    CANCEL_BUTTON = (By.ID, 'edit_product_cancel_button')

    @staticmethod
    def get_entity_heading_by_entity_type_locator(entity_type):
        """
        Get the heading locator based on the entity type
        :param entity_type: entity type whose header want
        :type entity_type: str
        :return: locator for the entity heading
        :rtype: (By, str)
        """
        return By.ID, "{}_header".format(entity_type)

    @staticmethod
    def get_entity_add_button_by_entity_type_locator(entity_type):
        """
        Get the add button locator based on the entity type
        :param entity_type: entity type whose add button want
        :type entity_type: str
        :return: locator for the add button
        :rtype: (By, str)
        """
        return By.ID, "{}_add_button".format(entity_type)

    @staticmethod
    def get_entity_table_code_column_locator_by_entity_type(entity_type):
        """
        Get the table's Code column locator based on the entity type
        :param entity_type: entity type whose Code column want
        :type entity_type: str
        :return: locator for the table's Code column
        :rtype: (By, str)
        """
        return By.ID, "column_heading_{}_table_displayCode".format(entity_type)

    @staticmethod
    def get_entity_table_amount_column_locator_by_entity_type(entity_type):
        """
        Get the table's Amount column locator based on the entity type
        :param entity_type: entity type whose Amount column want
        :type entity_type: str
        :return: locator for the table's Amount column
        :rtype: (By, str)
        """
        return By.ID, "column_heading_{}_table_amountColumn".format(entity_type)

    @staticmethod
    def get_entity_table_pct_value_column_locator_by_entity_type(entity_type):
        """
        Get the table's PCT Value column locator based on the entity type
        :param entity_type: entity type whose PCT Value column want
        :type entity_type: str
        :return: locator for the table's PCT Value column
        :rtype: (By, str)
        """
        return By.ID, "column_heading_{}_table_pct_valueColumn".format(entity_type)

    @staticmethod
    def get_entity_locator_by_name(name):
        """
        Get the locator for the entity based on the name (after adding an entity to the product)
        :param name: Name of the entity
        :type name: str
        :return: locator for the specific entity
        :rtype: (By, str)
        """
        return By.ID, "{}_displayCode".format(name)

    @staticmethod
    def get_entity_list_locator_by_entity_type(entity_type):
        """
        Get the locator for the entity list based on the entity type (after adding an entity to the product)
        :param entity_type: entity type whose list want
        :type entity_type: str
        :return: locator for the entity list
        :rtype: (By, str)
        """
        return By.XPATH, "//tbody[@id='table_body_{}_table']/tr".format(entity_type)

    @staticmethod
    def get_entity_amount_input_locator_by_name(name):
        """
        Get the locator for the Amount input based on the name (after adding an entity to the product)
        :param name: Name of the entity
        :type name: str
        :return: locator for the entity's amount input
        :rtype: (By, str)
        """
        return By.ID, "{}_amount_input".format(name)

    @staticmethod
    def get_entity_pct_value_input_locator_by_name(name):
        """
        Get the locator for the PCT Value input based on the name (after adding an entity to the product)
        :param name: Name of the entity
        :type name: str
        :return: locator for the entity's amount input
        :rtype: (By, str)
        """
        return By.ID, "{}_percent_input".format(name)

    @staticmethod
    def get_entity_remove_button_locator_by_name(name):
        """
        Get the locator for the remove button based on the name (after adding an entity to the product)
        :param name: Name of the entity
        :type name: str
        :return: locator for the entity's remove button
        :rtype: (By, str)
        """
        return By.ID, "{}_remove".format(name)

    @staticmethod
    def get_prices_toggle_locator_by_currency(currency_code):
        """
        Get locator for the toggle for a specific Currency
        :param currency_code: Code of the Currency
        :type currency_code: str
        :return: locator of the toggle for the Currency
        :rtype: (By, str)
        """
        return By.ID, 'prices_{}_real_money_toggle'.format(currency_code)

    @staticmethod
    def get_prices_vc_currency_code_locator_by_currency(currency_code):
        """
        Get the locator of the VC Currency Code for a specific Currency
        :param currency_code: Code of the Currency
        :type currency_code: str
        :return: locator of the VC Currency Code for the Currency
        :rtype: (By, str)
        """
        return By.ID, '{}_code'.format(currency_code)

    @staticmethod
    def get_prices_rm_currency_code_locator_by_currency(currency_code):
        """
        Get the locator of the RM Currency Code for a specific Currency
        :param currency_code: Code of the Currency
        :type currency_code: str
        :return: locator of the RM Currency Code for the Currency
        :rtype: (By, str)
        """
        return By.ID, 'table_cell_{}_displayCode'.format(currency_code)

    @staticmethod
    def get_prices_pricing_type_locator_by_currency(currency_code):
        """
        Get the locator of the Pricing Type for a specific Currency
        :param currency_code: Code of the Currency
        :type currency_code: str
        :return: locator of the Pricing Type for the Currency
        :rtype: (By, str)
        """
        return By.ID, 'table_cell_{}_qtyPricingType'.format(currency_code)

    @staticmethod
    def get_prices_amount_locator_by_currency(currency_code):
        """
        Get the locator of the Amount for a specific Currency
        :param currency_code: Code of the Currency
        :type currency_code: str
        :return: locator of the Amount for the Currency
        :rtype: (By, str)
        """
        return By.ID, 'prices_amount_{}_input'.format(currency_code)

    @staticmethod
    def get_prices_delete_button_locator_by_currency(currency_code):
        """
        Get the locator of the Delete button for a specific Currency
        :param currency_code: Code of the Currency
        :type currency_code: str
        :return: locator of the Delete button for the Currency
        :rtype: (By, str)
        """
        return By.ID, 'prices_{}_delete_button'.format(currency_code)
