from selenium.webdriver.common.by import By


class AddCatalogLocators(object):
    ADD_CATALOG_HEADER = (By.ID, 'modify_catalog_header')
    ACTIVE_HEADER = (By.ID, 'active_header')
    TAGS_INPUT = (By.ID, 'tags_drop_down')
    SAVE_BUTTON = (By.ID, 'save_close_button')
    CANCEL_BUTTON = (By.ID, 'cancel_button')
    ADD_JSON_BUTTON = (By.XPATH, "//button[text()='Add New JSON Field']")
    NAMESPACES_LABEL = (By.XPATH, "//div[text()='Namespaces']")
    ADD_NAMESPACE_BUTTON = (By.XPATH, "//button[text()='+ Add Namespace']")

    @staticmethod
    def get_header_by_name(name):
        """
        Get the header locators with specific name
        :param name: name of header
        :type name: str
        :return: locator for header
        :rtype: {By, str)
        """
        return By.XPATH, "//header[text()='{}']".format(name)

    @staticmethod
    def get_field_label_by_name(field_name):
        """
        Get the label locator for the specific field
        :param field_name: field of the label
        :type field_name: str
        :return: locator for label of the field
        :rtype: (By, str)
        """
        return By.ID, '{}_label'.format(field_name)

    @staticmethod
    def get_field_input_by_name(field_name):
        """
        Get the input locator for the specific field
        :param field_name: field of the input
        :type field_name: str
        :return: locator for input of the field
        :rtype: (By, str)
        """
        return By.ID, '{}_input'.format(field_name)

    @staticmethod
    def get_field_invalid_message_by_name(field_name):
        """
        Get the invalid message locator for the specific field
        :param field_name: field of the invalid message
        :type field_name: str
        :return: locator for invalid message of the field
        :rtype: (By, str)
        """
        return By.ID, '{}_invalid'.format(field_name)

    @staticmethod
    def get_field_toggle(field_name):
        """
        Get the toggle for the field
        :param field_name: field of the toggle
        :type field_name: str
        :return: toggle of the field
        :rtype: (By, str)
        """
        return By.ID, '{}_toggle'.format(field_name)

    @staticmethod
    def get_field_toggle_left_label(field_name):
        """
        Get the label to the left of the toggle
        :param field_name: field of the label
        :type field_name: str
        :return: label on left of toggle
        :rtype: (By, str)
        """
        return By.ID, '{}_labelLeft'.format(field_name)

    @staticmethod
    def get_field_toggle_right_label(field_name):
        """
        Get the label to the right of the toggle
        :param field_name: field of the label
        :type field_name: str
        :return: label on right of toggle
        :rtype: (By, str)
        """
        return By.ID, '{}_labelRight'.format(field_name)
