from selenium.webdriver.common.by import By


class CatalogsLocators(object):
    INFO_BOX = (By.ID, 'catalog_list_info_box')
    INFO_BOX_EXIT_BUTTON = (By.ID, 'catalog_list_info_box_close_button')
    INFO_BOX_STRONG = (By.ID, 'catalogs_info_box_highlight')
    INFO_BOX_STRONG_2 = (By.ID, 'entities_info_box_highlight')
    CATALOGS_TITLE = (By.ID, 'primary_heading')
    ADD_CATALOG_BUTTON = (By.ID, 'add_catalog_button')
    IMPORT_CATALOG_BUTTON = (By.ID, 'import_catalog_button')
    CHOOSE_CATALOG_TEXT = (By.ID, 'catalog_sub_header')
    SEARCH_BOX_INPUT = (By.ID, 'catalog_search_bar')
    FILTER_NAME = (By.ID, 'drop_down_filter')
    FILTER_DROPDOWN_ARROW = (By.ID, 'icon_drop_down_filter')
    FIRST_COLUMN_NAME = (By.ID, 'column_heading_friendly_name')
    SECOND_COLUMN_NAME = (By.ID, 'column_heading_actions')
    SELECT_ALL_CHECKBOX = (By.ID, 'checkbox_catalog_table_checkbox_clickable')
    CATALOGS_LIST = (By.ID, 'table_body_catalog_table')

    @staticmethod
    def get_catalog_locator_by_name(name):
        """
        Get the locator for the catalog link based on the display name
        :param name: Name shown on the button
        :type name: str
        :return: locator for the correct link
        :rtype: (By, str)
        """
        return By.ID, "table_cell_{}_friendly_name".format(name)

    @staticmethod
    def get_catalog_checkbox_locator_by_name(name):
        """
        Get the locator for the checkbox near the catalog link based on the display name
        :param name: Name shown on the button
        :type name: str
        :return: locator for the correct link
        :rtype: (By, str)
        """
        return By.ID, "row_catalog_table_{}_checkbox".format(name)

    @staticmethod
    def get_catalog_actions_button_locator_by_name(name):
        """
        Get the locator for the actions button near the catalog link based on the display name
        :param name: Name shown on the button
        :type name: str
        :return: locator for the correct link
        :rtype: (By, str)
        """
        return By.ID, "{}_actions_menu_button".format(name)
