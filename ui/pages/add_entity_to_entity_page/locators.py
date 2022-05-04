from selenium.webdriver.common.by import By


class AddEntityToEntityLocators(object):
    ENTITY_HEADER = (By.ID, 'undefined_header')
    SEARCH_BOX_INPUT = (By.XPATH, "//input[@class='search_bar__searchInput___XvYtd']")
    DROP_DOWN_LIST = (By.XPATH, "//span[@class='drop_down__input___25vcC drop_down__readOnly___WEJAb']")
    DROP_DOWN_LIST_ARROW = (
        By.XPATH, "//div[@class='drop_down__wrapBlur___3F1cZ drop_down__readOnly___WEJAb drop_down__wrap___sZs-D']")
    CODE_COLUMN = (By.ID, 'column_heading_entity_picker_table_currencies_displayCode')
    FRIENDLY_NAME_COLUMN = (By.ID, 'column_heading_entity_picker_table_currencies_friendly_name')
    ADD_BUTTON = (By.XPATH, "//button[@label='Add']")
    CLOSE_BUTTON = (By.XPATH, "//button[@label='Close']")

    @staticmethod
    def get_entity_locator_by_name(name):
        """
        Get the locator for the entity based on the name
        :param name: Name of the entity
        :type name: str
        :return: locator for the specific entity
        :rtype: (By, str)
        """
        return By.ID, "table_cell_{}_displayCode".format(name)

    @staticmethod
    def get_entity_checkbox_locator_by_name(name):
        """
        Get the locator for the entity checkbox based on the name
        :param name: Name of the entity
        :type name: str
        :return: locator for the specific entity checkbox
        :rtype: (By, str)
        """
        return By.ID, '{}_checkbox'.format(name)

    @staticmethod
    def get_entity_plus_button_locator_by_name(name):
        """
        Get the locator for the entity plus button based on the name
        :param name: Name of the entity
        :type name: str
        :return: locator for the specific entity plus button
        :rtype: (By, str)
        """
        return By.ID, "table_cell_{}_add_button".format(name)

    @staticmethod
    def get_entity_select_all_checkbox_locator_by_entity_type(entity_type):
        """
        Get the locator for the 'select all' checkbox based on the entity type
        :param entity_type: Type of the entity
        :type entity_type: str
        :return: locator for the specific 'select all' checkbox
        :rtype: (By, str)
        """
        return By.ID, "checkbox_entity_picker_table_{}_checkbox_clickable".format(entity_type)

    @staticmethod
    def get_entity_list_locator_by_entity_type(entity_type):
        """
        Get the locator for the entity list based on the entity type
        :param entity_type: Type of the entity
        :type entity_type: str
        :return: locator for the specific entity list
        :rtype: (By, str)
        """
        return By.XPATH, "//tbody[@id='table_body_entity_picker_table_{}']/tr".format(entity_type)
