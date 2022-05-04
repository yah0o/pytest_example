from selenium.webdriver.common.by import By


class StudiosLocators(object):
    STUDIOS_TITLE = (By.ID, 'studios_top_bar_heading')
    IMPORT_BUTTON = (By.ID, 'openImportStudio')
    ADD_BUTTON = (By.ID, 'openAddStudio')
    SEARCH_BOX_INPUT = (By.ID, 'studios_searchbar')
    STUDIOS_LIST = (By.ID, 'studioList')

    @staticmethod
    def get_studio_button_locator_by_name(name):
        """
        Get the locator for the studio button based on the display name
        :param name: Name shown on the button
        :type name: str
        :return: locator for the correct button
        :rtype: (By, str)
        """
        return By.XPATH, "//div[@id='{}_container']/div/div".format(name)

    @staticmethod
    def get_studio_button_settings_locator_by_name(name):
        """
        Get the locator for the settings icon on the studio button based on the display name
        :param name: Name shown on the button
        :type name: str
        :return: locator for the correct button
        :rtype: (By, str)
        """
        return By.ID, "studio_settings_button_{}".format(name)
