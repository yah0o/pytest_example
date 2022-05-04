from selenium.webdriver.common.by import By


class EntitlementLocators(object):
    IMPORT_BUTTON = (By.ID, 'importButton')
    ADD_BUTTON = (By.ID, 'add_entitlement')
    SEARCH_BOX_INPUT = (By.ID, 'entitlement_search_bar')
    DROP_DOWN_LIST = (By.ID, 'entitlement_drop_down')
    DROP_DOWN_LIST_ARROW = (By.ID, 'icon_entitlement_drop_down')
    INFO_BOX = (By.ID, 'entitlements_info_box')
    INFO_BOX_EXIT_BUTTON = (By.ID, 'entitlements_info_box_close_button')
    INFO_BOX_STRONG = (By.ID, 'entitlements_info_box_highlight')
    TABLE_HEADER_NAME_COLUMN = (By.ID, 'column_heading_friendly_name')
    TABLE_HEADER_ACTIONS_COLUMN = (By.ID, 'column_heading_action')
    TABLE_SELECT_ALL_CHECKBOX = (By.ID, 'checkbox_table_entitlement_checkbox_clickable')
    ENTITLEMENT_LIST = (By.ID, 'table_entitlement')

    @staticmethod
    def get_entitlement_locator_by_name(name):
        """
        Get the locator for the entitlement based on the name
        :param name: Name of the entitlement
        :type name: str
        :return: locator for the specific entitlement
        :rtype: (By, str)
        """
        return By.ID, "table_cell_{}_friendly_name".format(name)

    @staticmethod
    def get_entitlement_checkbox_locator_by_name(name):
        """
        Get the locator for the entitlement checkbox based on the name
        :param name: Name of the entitlement
        :type name: str
        :return: locator for the specific entitlement's checkbox
        :rtype: (By, str)
        """
        return By.ID, "row_table_entitlement_{}_checkbox".format(name)

    @staticmethod
    def get_entitlement_actions_button_locator_by_name(name):
        """
        Get the locator for the entitlement actions button based on the name
        :param name: Name of the entitlement
        :type name: str
        :return: locator for the specific entitlement's actions button
        :rtype: (By, str)
        """
        return By.ID, "{}_actions_menu_button".format(name)
