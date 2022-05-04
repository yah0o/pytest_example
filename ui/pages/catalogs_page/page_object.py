from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from locators import CatalogsLocators
from ui.pages.base_page import BasePage
from ui.main.constants import DEFAULT_PAGE_TIMEOUT


class Catalogs(BasePage):
    def wait_for_page_load(self):
        """
        Wait for the page to be fully loaded
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(CatalogsLocators.CATALOGS_LIST),
            'Catatogs page failed to load'
        )

    def wait_for_info_box_to_disappear(self):
        """
        Make sure the info box is not present after info box exit button was clicked
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.invisibility_of_element_located(CatalogsLocators.INFO_BOX),
            'Info box exit button was clicked but info box is still present'
        )

    def get_catalogs_title(self):
        """
        Get catalogs title on the catalogs page
        :return: catalogs title element
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogsLocators.CATALOGS_TITLE)

    def get_info_box(self):
        """
        Get the info box
        :return: info box
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogsLocators.INFO_BOX)

    def get_info_box_exit_button(self):
        """
        Get the info box's exit button
        :return: info box's exit button
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogsLocators.INFO_BOX_EXIT_BUTTON)

    def click_info_box_exit_button(self):
        """
        Click the info box's exit button
        """
        button = self.get_info_box_exit_button()
        button.click()

    def get_info_box_strong(self):
        """
        Get the info box's 'catalogs' strong element
        :return: info box's strong element
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogsLocators.INFO_BOX_STRONG)

    def get_info_box_strong2(self):
        """
        Get the info box's 'Entities' strong element
        :return: info box's strong element
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogsLocators.INFO_BOX_STRONG_2)

    def get_import_catalog_button(self):
        """
        Get import catalog button on the catalogs page
        :return: import catalog button
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogsLocators.IMPORT_CATALOG_BUTTON)

    def click_import_catalog_button(self):
        """
        Click import catalog button on the catalogs page
        """
        button = self.get_import_catalog_button()
        button.click()

    def get_add_catalog_button(self):
        """
        Get add catalog button on the catalogs page
        :return: add catalog button
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogsLocators.ADD_CATALOG_BUTTON)

    def click_add_catalog_button(self):
        """
        Click add catalog button on the catalogs page
        """
        button = self.get_add_catalog_button()
        button.click()

    def get_choose_catalog_text(self):
        """
        Get "choose a catalog" text on the catalogs page
        :return: "choose a catalog" text element
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogsLocators.CHOOSE_CATALOG_TEXT)

    def get_search_box(self):
        """
        Get search box on the catalogs page
        :return: search box element
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogsLocators.SEARCH_BOX_INPUT)

    def type_search_box(self, value):
        """
        Type into search box on the catalogs page
        :param value: value to search for
        :type value: str
        """
        input_field = self.get_search_box()
        input_field.send_keys(value)

    def get_filter_name(self):
        """
        Get filter name near the dropdown arrow
        :return: filter name
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogsLocators.FILTER_NAME)

    def get_filter_dropdown_arrow(self):
        """
        Get filter dropdown arrow on the catalogs page
        :return: filter dropdown arrow
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogsLocators.FILTER_DROPDOWN_ARROW)

    def click_filter_dropdown_arrow(self):
        """
        Click filter dropdown arrow on the catalogs page
        """
        button = self.get_filter_dropdown_arrow()
        button.click()

    def get_first_column_name(self):
        """
        Get table's first column name on the catalogs page
        :return: first column name
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogsLocators.FIRST_COLUMN_NAME)

    def get_second_column_name(self):
        """
        Get table's second column name on the catalogs page
        :return: second column name
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogsLocators.SECOND_COLUMN_NAME)

    def get_select_all_checkbox(self):
        """
        Get "select all" checkbox on the catalogs page
        :return: "select all" checkbox
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogsLocators.SELECT_ALL_CHECKBOX)

    def check_select_all_checkbox(self):
        """
        Check "select all" checkbox on the catalogs page
        """
        checkbox = self.get_select_all_checkbox()
        self.browser.execute_script('arguments[0].click()', checkbox)

    def get_catalogs_list(self):
        """
        Get list of catalogs on the catalogs page
        :return: list of catalogs
        :rtype: list of WebElement
        """
        return self.browser.find_elements(*CatalogsLocators.CATALOGS_LIST)

    def get_catalog_by_name(self, name):
        """
        Get the link to a given catalog
        :param name: name of the desired catalog
        :type name: str
        :return: catalog link
        :rtype: WebElement
        """
        return WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(
                CatalogsLocators.get_catalog_locator_by_name(name)
            ),
            'Link to {} could not be found'.format(name)
        )

    def click_catalog_by_name(self, name):
        """
        Click the link to a given catalog
        :param name: name of the desired catalog
        :type name: str
        """
        button = self.get_catalog_by_name(name)
        button.click()

    def get_catalog_checkbox_by_name(self, name):
        """
        Get the checkbox near a given catalog
        :param name: name of the desired catalog
        :type name: str
        :return: checkbox
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogsLocators.get_catalog_checkbox_locator_by_name(name))

    def click_catalog_checkbox_by_name(self, name):
        """
        Click the checkbox near a given catalog
        :param name: name of the desired catalog
        :type name: str
        """
        button = self.get_catalog_checkbox_by_name(name)
        button.click()

    def get_catalog_actions_button_by_name(self, name):
        """
        Get the actions button near a given catalog
        :param name: name of the desired catalog
        :type name: str
        :return: actions button
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogsLocators.get_catalog_actions_button_locator_by_name(name))

    def click_catalog_actions_button_by_name(self, name):
        """
        Click the actions button near a given catalog
        :param name: name of the desired catalog
        :type name: str
        """
        button = self.get_catalog_actions_button_by_name(name)
        button.click()
