from selenium.webdriver.common.by import By


class ActionsMenuLocators(object):

    @staticmethod
    def get_actions_menu_list_locator_by_name(name):
        """
        Get the locator for the actions menu list based on the name of the entity
        :param name: name of the entity
        :type name: str
        :return: locator for the specific actions menu list
        :rtype: (By, str)
        """
        return By.XPATH, '//ul[@id="{}_actions_menu_list"]/div'.format(name)

    @staticmethod
    def get_actions_menu_download_config_locator_by_name(name):
        """
        Get the locator for the actions menu Download Config based on the name of the entity
        :param name: name of the entity
        :type name: str
        :return: locator for the specific actions menu Download Config
        :rtype: (By, str)
        """
        return By.ID, "{}_actions_downloadConfig".format(name)

    @staticmethod
    def get_actions_menu_edit_locator_by_name(name):
        """
        Get the locator for the actions menu Edit based on the name of the entity
        :param name: name of the entity
        :type name: str
        :return: locator for the specific actions menu Edit
        :rtype: (By, str)
        """
        return By.ID, "{}_actions_edit".format(name)

    @staticmethod
    def get_actions_menu_duplicate_locator_by_name(name):
        """
        Get the locator for the actions menu Duplicate based on the name of the entity
        :param name: name of the entity
        :type name: str
        :return: locator for the specific actions menu Duplicate
        :rtype: (By, str)
        """
        return By.ID, "{}_actions_duplicate".format(name)

    @staticmethod
    def get_actions_menu_remove_locator_by_name(name):
        """
        Get the locator for the actions menu Remove based on the name of the entity
        :param name: name of the entity
        :type name: str
        :return: locator for the specific actions menu Remove
        :rtype: (By, str)
        """
        return By.ID, "{}_actions_remove".format(name)
