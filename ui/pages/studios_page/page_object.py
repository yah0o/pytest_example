from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from locators import StudiosLocators
from ui.pages.base_page import BasePage
from ui.main.constants import DEFAULT_PAGE_TIMEOUT


class Studios(BasePage):
    def wait_for_page_load(self):
        """
        Wait for the page to be fully loaded
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(StudiosLocators.STUDIOS_LIST),
            'Studios page failed to load'
        )

    def get_studios_title(self):
        """
        Get studios title
        :return: studios title element
        :rtype: WebElement
        """
        return self.browser.find_element(*StudiosLocators.STUDIOS_TITLE)

    def get_import_button(self):
        """
        Get import studio button
        :return: import studio button
        :rtype: WebElement
        """
        return self.browser.find_element(*StudiosLocators.IMPORT_BUTTON)

    def click_import_button(self):
        """
        Click import studio button
        """
        button = self.get_import_button()
        button.click()

    def get_add_button(self):
        """
        Get add studio button
        :return: add studio button
        :rtype: WebElement
        """
        return self.browser.find_element(*StudiosLocators.ADD_BUTTON)

    def click_add_button(self):
        """
        Click add studio button
        """
        button = self.get_add_button()
        button.click()

    def get_search_box(self):
        """
        Get search box
        :return: search box element
        :rtype: WebElement
        """
        return self.browser.find_element(*StudiosLocators.SEARCH_BOX_INPUT)

    def type_search_box(self, value):
        """
        Type into search box
        :param value: value to search for
        :type value: str
        """
        input_field = self.get_search_box()
        input_field.send_keys(value)

    def get_studios_list(self):
        """
        Get list of studios
        :return: list of studios
        :rtype: list of WebElement
        """
        return self.browser.find_elements(*StudiosLocators.STUDIOS_LIST)

    def get_studio_button_by_name(self, name):
        """
        Get the button for a given studio
        :param name: name of the desired studio
        :type name: str
        :return: studio button
        :rtype: WebElement
        """
        return WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(
                StudiosLocators.get_studio_button_locator_by_name(name)
            ),
            'Button for {} could not be found'.format(name)
        )

    def click_studio_button_by_name(self, name):
        """
        Click the button for the given studio
        :param name: name of the desired studio
        :type name: str
        """
        button = self.get_studio_button_by_name(name)
        button.click()

    def get_studio_settings_icon_by_name(self, name):
        """
        Get settings icon on studio button
        :param name: name of the desired studio
        :type name: str
        :return: studio button
        :rtype: WebElement
        """
        return self.browser.find_element(*StudiosLocators.get_studio_button_settings_locator_by_name(name))

    def click_studio_settings_icon_by_name(self, name):
        """
        Click settings icon on studio button
        :param name: name of the desired studio
        :type name: str
        """
        button = self.get_studio_settings_icon_by_name(name)
        button.click()
