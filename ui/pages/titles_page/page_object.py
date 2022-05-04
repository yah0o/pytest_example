from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from locators import TitlesPageLocators
from ui.main.constants import DEFAULT_PAGE_TIMEOUT
from ui.pages.base_page import BasePage


class Titles(BasePage):
    def wait_for_page_load(self):
        """
        Wait for the page to be fully loaded with titles
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(TitlesPageLocators.TITLES_LIST),
            'Titles page failed to load'
        )

    def get_studio_code_span(self):
        """
        Get studio code span
        :return: studio code span
        :rtype: WebElement
        """
        return self.browser.find_element(*TitlesPageLocators.STUDIO_CODE_SPAN)

    def get_page_title(self):
        """
        Retrieves page title element
        :return: Page title element
        :rtype: WebElement
        """
        return self.browser.find_element(*TitlesPageLocators.PAGE_TITLE)

    def get_add_title_button(self):
        """
        Retrieves add title button
        :return: Add title button
        :rtype: WebElement
        """
        return self.browser.find_element(*TitlesPageLocators.ADD_TITLE_BUTTON)

    def click_add_title_button(self):
        """
        Mouse click action on the add title button
        """
        button = self.get_add_title_button()
        button.click()

    def get_search_box(self):
        """
        Retrieves the title search box element from the titles page
        :return: Title search box
        :rtype: WebElement
        """
        return self.browser.find_element(*TitlesPageLocators.SEARCH_BOX_INPUT)

    def type_search_box(self, value):
        """
        Keyboard type action in the titles search box
        :param value: String input for the titles search box
        :type value: str
        """
        input_field = self.get_search_box()
        input_field.send_keys(value)

    def get_titles_list(self):
        """
        Retrieves the title list element
        :return: Title list element
        :rtype: list of WebElement
        """
        return self.browser.find_elements(*TitlesPageLocators.TITLES_LIST)

    def get_title_button_by_name(self, name):
        """
        Get the button for a given title
        :param name: name of the desired title
        :type name: str
        :return: title button
        :rtype: WebElement
        """
        return WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(
                TitlesPageLocators.get_title_button_locator_by_name(name)
            ),
            'Button for {} could not be found'.format(name)
        )

    def click_title_button_by_name(self, name):
        """
        Click the button for the given title
        :param name: name of the desired title
        :type name: str
        """
        button = self.get_title_button_by_name(name)
        button.click()

    def get_title_edit_button_by_name(self, name):
        """
        Get edit button on title button
        :param name: name of the desired title
        :type name: str
        :return: edit button
        :rtype: WebElement
        """
        return self.browser.find_element(*TitlesPageLocators.get_title_button_edit_button_locator_by_name(name))

    def click_title_edit_button_by_name(self, name):
        """
        Click edit button on title button
        :param name: name of the desired title
        :type name: str
        """
        button = self.get_title_edit_button_by_name(name)
        button.click()

    def get_title_image_by_name(self, name):
        """
        Get image on title button
        :param name: name of the desired title
        :type name: str
        :return: title button
        :rtype: WebElement
        """
        return self.browser.find_element(*TitlesPageLocators.get_title_button_image_locator_by_name(name))
