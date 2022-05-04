from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from locators import StorefrontLocators
from ui.pages.base_page import BasePage
from ui.main.constants import DEFAULT_PAGE_TIMEOUT


class Storefronts(BasePage):
    def wait_for_page_load(self):
        """
        Wait for the page to be fully loaded
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(StorefrontLocators.STOREFRONT_LIST),
            'Catalog Storefront page failed to load'
        )

    def wait_for_info_box_to_disappear(self):
        """
        Make sure the info box is not present after info box exit button was clicked
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.invisibility_of_element_located(StorefrontLocators.INFO_BOX),
            'Info box exit button was clicked but info box is still present'
        )

    def get_import_button(self):
        """
        Get import storefront button
        :return: import storefront button
        :rtype: WebElement
        """
        return self.browser.find_element(*StorefrontLocators.IMPORT_BUTTON)

    def click_import_button(self):
        """
        Click import storefront button
        """
        button = self.get_import_button()
        button.click()

    def get_add_button(self):
        """
        Get add storefront button
        :return: add storefront button
        :rtype: WebElement
        """
        return self.browser.find_element(*StorefrontLocators.ADD_BUTTON)

    def click_add_button(self):
        """
        Click add storefront button
        """
        button = self.get_add_button()
        button.click()

    def get_search_box(self):
        """
        Get search box on the storefronts page
        :return: search box element
        :rtype: WebElement
        """
        return self.browser.find_element(*StorefrontLocators.SEARCH_BOX_INPUT)

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
        return self.browser.find_element(*StorefrontLocators.DROP_DOWN_LIST)

    def get_drop_down_list_arrow(self):
        """
        Get the drop down list arrow
        :return: drop down list arrow
        :rtype: WebElement
        """
        return self.browser.find_element(*StorefrontLocators.DROP_DOWN_LIST_ARROW)

    def click_drop_down_list_arrow(self):
        """
        Click the drop down list arrow
        """
        span = self.get_drop_down_list_arrow()
        span.click()

    def get_info_box(self):
        """
        Get the info box
        :return: info box
        :rtype: WebElement
        """
        return self.browser.find_element(*StorefrontLocators.INFO_BOX)

    def get_info_box_exit_button(self):
        """
        Get the info box's exit button
        :return: info box's exit button
        :rtype: WebElement
        """
        return self.browser.find_element(*StorefrontLocators.INFO_BOX_EXIT_BUTTON)

    def click_info_box_exit_button(self):
        """
        Click the info box's exit button
        """
        span = self.get_info_box_exit_button()
        span.click()

    def get_info_box_strong(self):
        """
        Get the info box's strong element
        :return: info box's strong element
        :rtype: WebElement
        """
        return self.browser.find_element(*StorefrontLocators.INFO_BOX_STRONG)

    def get_table_name_column(self):
        """
        Get the table's name column
        :return: table's name column
        :rtype: WebElement
        """
        return self.browser.find_element(*StorefrontLocators.TABLE_NAME_COLUMN)

    def get_table_actions_column(self):
        """
        Get the table's actions column
        :return: table's actions column
        :rtype: WebElement
        """
        return self.browser.find_element(*StorefrontLocators.TABLE_ACTIONS_COLUMN)

    def get_table_select_all_checkbox(self):
        """
        Get the table's select all checkbox
        :return: table's select all checkbox
        :rtype: WebElement
        """
        return self.browser.find_element(*StorefrontLocators.TABLE_SELECT_ALL_CHECKBOX)

    def click_table_select_all_checkbox(self):
        """
        Click the table's select all chechbox
        """
        checkbox = self.get_table_select_all_checkbox()
        self.browser.execute_script('arguments[0].click()', checkbox)

    def get_storefronts_list(self):
        """
        Get a list of storefronts
        :return: list of storefronts
        :rtype: list of WebElement
        """
        return self.browser.find_elements(*StorefrontLocators.STOREFRONT_LIST)

    def get_storefront_by_name(self, name):
        """
        Get a storefront by its name
        :param name: Name of the desired Storefront
        :type name: str
        :return: storefront button
        :rtype: WebElement
        """
        return WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(
                StorefrontLocators.get_storefront_locator_by_name(name)
            ),
            '{} could not be found'.format(name)
        )

    def click_storefront_button(self, name):
        """
        Click the specified storefront button
        :param name: Name of the desired Storefront
        :type name: str
        """
        button = self.get_storefront_by_name(name)
        button.click()

    def get_storefront_checkbox_by_name(self, name):
        """
        Get checkbox for the specific storefront
        :param name: Name of the desired Storefront
        :type name: str
        :return: specific storefront's checkbox
        :rtype: WebElement
        """
        return self.browser.find_element(*StorefrontLocators.get_storefront_checkbox_locator_by_name(name))

    def check_storefront_checkbox_by_name(self, name):
        """
        Check the storefront checkbox
        :param name: Name of the desired Storefront
        :type name: str
        """
        span = self.get_storefront_checkbox_by_name(name)
        span.click()

    def get_storefront_actions_button_by_name(self, name):
        """
        Get the storefront actions button
        :param name: Name of the desired Storefront
        :type name: str
        :return: storefront's actions button
        :rtype: WebElement
        """
        return self.browser.find_element(*StorefrontLocators.get_storefront_actions_button_locator_by_name(name))

    def click_storefront_actions_button(self, name):
        """
        Click the storefront actions button
        :param name: Name of the desired Storefront
        :type name: str
        """
        button = self.get_storefront_actions_button_by_name(name)
        button.click()
