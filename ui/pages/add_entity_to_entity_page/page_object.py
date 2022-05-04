from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from locators import AddEntityToEntityLocators
from ui.pages.base_page import BasePage
from ui.main.constants import DEFAULT_PAGE_TIMEOUT


class AddEntityToEntity(BasePage):
    def wait_for_page_load(self, entity_type):
        """
        Wait for the page to be fully loaded
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(
                AddEntityToEntityLocators.get_entity_list_locator_by_entity_type(entity_type)),
            "'Add entity to entity picker page' failed to load"
        )

    def get_entity_header(self):
        """
        Get the entity header
        :return: entity header
        :rtype: WebElement
        """
        return self.browser.find_element(*AddEntityToEntityLocators.ENTITY_HEADER)

    def get_add_button(self):
        """
        Get the add button (after selecting at least two products from the list)
        :return: add button
        :rtype: WebElement
        """
        return self.browser.find_element(*AddEntityToEntityLocators.ADD_BUTTON)

    def click_add_button(self):
        """
        Click the add button
        """
        button = self.get_add_button()
        button.click()

    def get_search_box(self):
        """
        Get the search box
        :return: search box element
        :rtype: WebElement
        """
        return self.browser.find_element(*AddEntityToEntityLocators.SEARCH_BOX_INPUT)

    def type_search_box(self, value):
        """
        Type into search box
        :param value: value to search for
        :type value: str
        """
        input_field = self.get_search_box()
        input_field.send_keys(value)

    def get_drop_down_list(self):
        """
        Get the drop down list
        :return: drop down list
        :rtype: WebElement
        """
        return self.browser.find_element(*AddEntityToEntityLocators.DROP_DOWN_LIST)

    def get_drop_down_list_arrow(self):
        """
        Get the drop down list arrow
        :return: drop down list arrow
        :rtype: WebElement
        """
        return self.browser.find_element(*AddEntityToEntityLocators.DROP_DOWN_LIST_ARROW)

    def click_drop_down_list_arrow(self):
        """
        Click the drop down list arrow
        """
        arrow = self.get_drop_down_list_arrow()
        arrow.click()

    def get_code_column(self):
        """
        Get Code column
        :return: Code column
        :rtype: WebElement
        """
        return self.browser.find_element(*AddEntityToEntityLocators.CODE_COLUMN)

    def get_friendly_name_column(self):
        """
        Get Friendly Name column
        :return: Friendly Name column
        :rtype: WebElement
        """
        return self.browser.find_element(*AddEntityToEntityLocators.FRIENDLY_NAME_COLUMN)

    def get_entity_by_name(self, name):
        """
        Get an entity by its name
        :param name: Name of the entity
        :type name: str
        :return: Entity button
        :rtype: WebElement
        """
        return WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(
                AddEntityToEntityLocators.get_entity_locator_by_name(name)
            ),
            '{} could not be found'.format(name)
        )

    def click_entity_button(self, name):
        """
        Click the specified entity button
        :param name: Name of the entity
        :type name: str
        """
        button = self.get_entity_by_name(name)
        button.click()

    def get_entity_checkbox(self, name):
        """
        Get checkbox for the specific entity
        :param name: Name of the entity
        :type name: str
        :return: checkbox for the specific entity
        :rtype: WebElement
        """
        return self.browser.find_element(*AddEntityToEntityLocators.get_entity_checkbox_locator_by_name(name))

    def click_entity_checkbox(self, name):
        """
        Check the entity's checkbox
        :param name: Name of the entity
        :type name: str
        """
        checkbox = self.get_entity_checkbox(name)
        self.browser.execute_script('arguments[0].click()', checkbox)

    def get_entity_plus_button_by_name(self, name):
        """
        Get the entity plus button
        :param name: Name of the entity
        :type name: str
        :return: specific entity's plus button
        :rtype: WebElement
        """
        return self.browser.find_element(*AddEntityToEntityLocators.get_entity_plus_button_locator_by_name(name))

    def click_entity_plus_button(self, name):
        """
        Click the entity's plus button
        :param name: Name of the entity
        :type name: str
        """
        button = self.get_entity_plus_button_by_name(name)
        button.click()

    def get_entity_select_all_checkbox_by_entity_type(self, entity_type):
        """
        Get the table's select all checkbox
        :param entity_type: Type of the entity
        :type entity_type: str
        :return: table's select all checkbox
        :rtype: WebElement
        """
        return self.browser.find_element(
            *AddEntityToEntityLocators.get_entity_select_all_checkbox_locator_by_entity_type(entity_type))

    def click_entity_select_all_checkbox(self, entity_type):
        """
        Click the table's select all checkbox
        :param entity_type: Type of the entity
        :type entity_type: str
        """
        checkbox = self.get_entity_select_all_checkbox_by_entity_type(entity_type)
        self.browser.execute_script('arguments[0].click()', checkbox)

    def get_entity_list_by_entity_type(self, entity_type):
        """
        Get the list of entities
        :param entity_type: Type of the entity
        :type entity_type: str
        :return: list of entities
        :rtype: list of WebElement
        """
        return self.browser.find_elements(
            *AddEntityToEntityLocators.get_entity_list_locator_by_entity_type(entity_type))

    def get_close_button(self):
        """
        Get the close button
        :return: close button
        :rtype: WebElement
        """
        return self.browser.find_element(*AddEntityToEntityLocators.CLOSE_BUTTON)

    def click_close_button(self):
        """
        Click the close button
        """
        button = self.get_close_button()
        button.click()
