from selenium.webdriver.common.by import By


class TitlesPageLocators(object):
    STUDIO_CODE_SPAN = (By.ID, 'titles_top_bar_sub_heading_top')
    PAGE_TITLE = (By.ID, 'titles_top_bar_heading')
    ADD_TITLE_BUTTON = (By.ID, 'add_title_button')
    SEARCH_BOX_INPUT = (By.ID, 'titles_list_search_input')
    TITLES_LIST = (By.XPATH, "//div[@class='titles__mainBody___3s8ME']")

    @staticmethod
    def get_title_button_locator_by_name(name):
        """
        Get the locator for the title button based on the display name
        :param name: Name shown on the button
        :type name: str
        :return: locator for the correct button
        :rtype: (By, str)
        """
        return By.ID, '{}_name'.format(name)

    @staticmethod
    def get_title_button_edit_button_locator_by_name(name):
        """
        Get the locator for the settings icon on the title button based on the display name
        :param name: Name shown on the button
        :type name: str
        :return: locator for the correct button
        :rtype: (By, str)
        """
        return By.ID, '{}_title_edit_button'.format(name)

    @staticmethod
    def get_title_button_image_locator_by_name(name):
        """
        Get the locator for the image on the title button based on the display name
        :param name: Name shown on the button
        :type name: str
        :return: locator for the correct button
        :rtype: (By, str)
        """
        return By.ID, '{}_img'.format(name)
