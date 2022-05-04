from selenium.webdriver.common.by import By


class ProductLocators(object):
    IMPORT_BUTTON = (By.ID, 'importButton')
    ADD_BUTTON = (By.ID, 'add_product')
    SEARCH_BOX_INPUT = (By.ID, 'product_search_bar')
    DROP_DOWN_LIST = (By.ID, 'product_drop_down')
    DROP_DOWN_LIST_ARROW = (By.ID, 'icon_product_drop_down')
    INFO_BOX = (By.ID, 'products_info_box')
    INFO_BOX_EXIT_BUTTON = (By.ID, 'products_info_box_close_button')
    INFO_BOX_STRONG = (By.ID, 'products_info_box_highlight')
    TABLE_NAME_COLUMN = (By.ID, 'column_heading_friendly_name')
    TABLE_ACTIONS_COLUMN = (By.ID, 'column_heading_action')
    TABLE_SELECT_ALL_CHECKBOX = (By.ID, 'checkbox_table_product_checkbox_clickable')
    PRODUCT_LIST = (By.ID, 'table_body_table_product')

    @staticmethod
    def get_product_locator_by_name(name):
        """
        Get the locator for the product based on the name
        :param name: Name of the Product
        :type name: str
        :return: locator for the specific Product
        :rtype: (By, str)
        """
        return By.ID, "table_cell_{}_friendly_name".format(name)

    @staticmethod
    def get_product_checkbox_locator_by_name(name):
        """
        Get the locator for the product checkbox based on the name
        :param name: Name of the product
        :type name: str
        :return: locator for the specific product's checkbox
        :rtype: (By, str)
        """
        return By.ID, "row_table_product_{}_checkbox".format(name)

    @staticmethod
    def get_product_actions_button_locator_by_name(name):
        """
        Get the locator for the product actions button based on the name
        :param name: Name of the product
        :type name: str
        :return: locator for the specific product's actions button
        :rtype: (By, str)
        """
        return By.ID, "{}_actions_menu_button".format(name)
