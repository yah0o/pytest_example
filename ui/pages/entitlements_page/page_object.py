from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from locators import EntitlementLocators
from ui.main.constants import DEFAULT_PAGE_TIMEOUT
from ui.pages.base_page import BasePage


class Entitlements(BasePage):
    def wait_for_page_load(self):
        """
        Wait for the page to be fully loaded
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(EntitlementLocators.ENTITLEMENT_LIST),
            'Catalog Entitlement page failed to load'
        )

    def wait_for_info_box_to_disappear(self):
        """
        Make sure the info box is not present after info box exit button was clicked
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.invisibility_of_element_located(EntitlementLocators.INFO_BOX),
            'Info box exit button was clicked but info box is still present'
        )

    def get_import_button(self):
        """
        Get the import button
        :return: import button
        :rtype: WebElement
        """
        return self.browser.find_element(*EntitlementLocators.IMPORT_BUTTON)

    def click_import_button(self):
        """
        Click the import button
        """
        button = self.get_import_button()
        button.click()

    def get_add_button(self):
        """
        Get the add button
        :return: add button
        :rtype: WebElement
        """
        return self.browser.find_element(*EntitlementLocators.ADD_BUTTON)

    def click_add_button(self):
        """
        Click the add button
        """
        button = self.get_add_button()
        button.click()

    def get_search_box(self):
        """
        Get the search box
        :return: search box
        :rtype: WebElement
        """
        return self.browser.find_element(*EntitlementLocators.SEARCH_BOX_INPUT)

    def type_search_box(self, value):
        """
        Type into the search box
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
        return self.browser.find_element(*EntitlementLocators.DROP_DOWN_LIST)

    def get_drop_down_list_arrow(self):
        """
        Get the drop down list arrow
        :return: drop down list arrow
        :rtype: WebElement
        """
        return self.browser.find_element(*EntitlementLocators.DROP_DOWN_LIST_ARROW)

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
        return self.browser.find_element(*EntitlementLocators.INFO_BOX)

    def get_info_box_exit_button(self):
        """
        Get the info box exit button
        :return: info box exit button
        :rtype: WebElement
        """
        return self.browser.find_element(*EntitlementLocators.INFO_BOX_EXIT_BUTTON)

    def click_info_box_exit_button(self):
        """
        Click the info box exit button
        """
        button = self.get_info_box_exit_button()
        button.click()

    def get_info_box_strong(self):
        """
        Get the info box strong element
        :return: info box strong element
        :rtype: WebElement
        """
        return self.browser.find_element(*EntitlementLocators.INFO_BOX_STRONG)

    def get_table_header_name_column(self):
        """
        Get the header for the table's name column
        :return: header of table's name column
        :rtype: WebElement
        """
        return self.browser.find_element(*EntitlementLocators.TABLE_HEADER_NAME_COLUMN)

    def get_table_header_actions_column(self):
        """
        Get the header for the table's actions column
        :return: header of table's actions column
        :rtype: WebElement
        """
        return self.browser.find_element(*EntitlementLocators.TABLE_HEADER_ACTIONS_COLUMN)

    def get_table_select_all_checkbox(self):
        """
        Get the checkbox that selects all entitlements in the table
        :return: select all checkbox
        :rtype: WebElement
        """
        return self.browser.find_element(*EntitlementLocators.TABLE_SELECT_ALL_CHECKBOX)

    def click_table_select_all_checkbox(self):
        """
        Click the select all checkbox
        """
        checkbox = self.get_table_select_all_checkbox()
        self.browser.execute_script('arguments[0].click()', checkbox)

    def get_entitlements_list(self):
        """
        Get the list of entitlements
        :return: list of entitlements
        :rtype: list of WebElement
        """
        return self.browser.find_elements(*EntitlementLocators.ENTITLEMENT_LIST)

    def get_entitlement_by_name(self, name):
        """
        Get the specified entitlement
        :param name: name of the entitlement
        :type name: str
        :return: entitlement with the specified name
        :rtype: WebElement
        """
        return WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(
                EntitlementLocators.get_entitlement_locator_by_name(name)
            ),
            '{} could not be found'.format(name)
        )

    def click_entitlement_by_name(self, name):
        """
        Click the specific entitlement
        :param name: name of the entitlement
        :type name: str
        """
        button = self.get_entitlement_by_name(name)
        button.click()

    def get_entitlement_checkbox_by_name(self, name):
        """
        Get a specific entitlement's checkbox
        :param name: name of the entitlement
        :type name: str
        :return: checkbox of the specified entitlement
        :rtype: WebElement
        """
        return self.browser.find_element(*EntitlementLocators.get_entitlement_checkbox_locator_by_name(name))

    def click_entitlement_checkbox_by_name(self, name):
        """
        Click a specific entitlement's checkbox
        :param name: name of the entitlement
        :type name: str
        """
        checkbox = self.get_entitlement_checkbox_by_name(name)
        checkbox.click()

    def get_entitlement_actions_button_by_name(self, name):
        """
        Get a specific entitlement's actions button
        :param name: name of the entitlement
        :type name: str
        :return: actions button of the specified entitlement
        :rtype: WebElement
        """
        return self.browser.find_element(*EntitlementLocators.get_entitlement_actions_button_locator_by_name(name))

    def click_entitlement_actions_button_by_name(self, name):
        """
        Click a specific entitlement's actions button
        :param name: name of the entitlement
        :type name: str
        """
        button = self.get_entitlement_actions_button_by_name(name)
        button.click()
