from selenium.webdriver.common.by import By


class CurrencyLocators(object):
    IMPORT_BUTTON = (By.ID, 'importButton')
    ADD_BUTTON = (By.ID, 'add_currency')
    SEARCH_BOX_INPUT = (By.ID, 'currency_search_bar')
    DROP_DOWN_LIST = (By.ID, 'currency_drop_down')
    DROP_DOWN_LIST_ARROW = (By.ID, 'icon_currency_drop_down')
    INFO_BOX = (By.ID, 'currencies_info_box')
    INFO_BOX_EXIT_BUTTON = (By.ID, 'currencies_info_box_close_button')
    INFO_BOX_STRONG = (By.ID, 'currencies_info_box_highlight')
    TABLE_HEADER_NAME_COLUMN = (By.ID, 'column_heading_friendly_name')
    TABLE_HEADER_ACTIONS_COLUMN = (By.ID, 'column_heading_action')
    TABLE_SELECT_ALL_CHECKBOX = (By.ID, 'checkbox_table_currency_checkbox_clickable')
    CURRENCY_LIST = (By.ID, 'table_body_table_currency')

    @staticmethod
    def get_currency_code_locator_by_name(name):
        """
        Get the locator for the currency based on the name
        :param name: Name of the Currency
        :type name: str
        :return: locator for the code of the specific Currency
        :rtype: (By, str)
        """
        return By.ID, 'table_cell_{}_code'.format(name)

    @staticmethod
    def get_currency_friendly_name_locator_by_name(name):
        """
        Get the locator for the currency based on the name
        :param name: Name of the Currency
        :type name: str
        :return: locator for the friendly name of specific Currency
        :rtype: (By, str)
        """
        return By.ID, 'table_cell_{}_friendly_name'.format(name)

    @staticmethod
    def get_currency_checkbox_locator_by_name(name):
        """
        Get the locator for the currency checkbox based on the name
        :param name: Name of the currency
        :type name: str
        :return: locator for the specific currency's checkbox
        :rtype: (By, str)
        """
        return By.ID, "row_table_currency_{}_checkbox".format(name)

    @staticmethod
    def get_currency_actions_button_locator_by_name(name):
        """
        Get the locator for the currency actions button based on the name
        :param name: Name of the currency
        :type name: str
        :return: locator for the specific currency's actions button
        :rtype: (By, str)
        """
        return By.ID, "{}_actions_menu_button".format(name)
