from selenium.webdriver.common.by import By


class StorefrontLocators(object):
    IMPORT_BUTTON = (By.ID, 'importButton')
    ADD_BUTTON = (By.ID, 'add_storefront')
    SEARCH_BOX_INPUT = (By.ID, 'storefront_search_bar')
    DROP_DOWN_LIST = (By.ID, 'storefront_drop_down')
    DROP_DOWN_LIST_ARROW = (By.ID, 'storefronts_info_box_close_button')
    INFO_BOX = (By.ID, 'storefronts_info_box')
    INFO_BOX_EXIT_BUTTON = (By.ID, 'storefronts_info_box_close_button')
    INFO_BOX_STRONG = (By.ID, 'storefronts_info_box_highlight')
    TABLE_NAME_COLUMN = (By.ID, 'column_heading_friendly_name')
    TABLE_ACTIONS_COLUMN = (By.ID, 'column_heading_action')
    TABLE_SELECT_ALL_CHECKBOX = (By.ID, 'checkbox_table_storefront_checkbox_clickable')
    STOREFRONT_LIST = (By.ID, 'table_body_table_storefront')

    @staticmethod
    def get_storefront_locator_by_name(name):
        """
        Get the locator for the storefront based on the name
        :param name: Name of the storefront
        :type name: str
        :return: locator for the specific storefront
        :rtype: (By, str)
        """
        return By.ID, "table_cell_{}_friendly_name".format(name)

    @staticmethod
    def get_storefront_checkbox_locator_by_name(name):
        """
        Get the locator for the storefront checkbox based on the name
        :param name: Name of the storefront
        :type name: str
        :return: locator for the specific storefront's checkbox
        :rtype: (By, str)
        """
        return By.ID, "row_table_storefront_{}_checkbox".format(name)

    @staticmethod
    def get_storefront_actions_button_locator_by_name(name):
        """
        Get the locator for the storefront actions button based on the name
        :param name: Name of the storefront
        :type name: str
        :return: locator for the specific storefront's actions button
        :rtype: (By, str)
        """
        return By.ID, "{}_actions_menu_button".format(name)
