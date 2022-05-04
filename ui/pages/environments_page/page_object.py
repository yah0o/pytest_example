from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from locators import EnvironmentsLocators
from ui.pages.base_page import BasePage
from ui.main.constants import DEFAULT_PAGE_TIMEOUT


class Environments(BasePage):
    def wait_for_page_load(self):
        """
        Wait for the page to be fully loaded
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(
                EnvironmentsLocators.ENVIRONMENTS_TITLE),
            'Environments page failed to load'
        )

    def get_environments_title(self):
        """
        Get Environments title
        :return: Environments title
        :rtype: WebElement
        """
        return self.browser.find_element(*EnvironmentsLocators.ENVIRONMENTS_TITLE)

    def get_environments_subheading(self):
        """
        Get Environments subheading
        :return: Environment subheading
        :rtype: WebElement
        """
        return self.browser.find_element(*EnvironmentsLocators.ENVIRONMENTS_SUBHEADING)

    def get_realm_box_by_name(self, name):
        """
        Get realm box
        :param name: name of the desired realm
        :type name: str
        :return: realm box
        :rtype: WebElement
        """
        return self.browser.find_element(*EnvironmentsLocators.get_realm_box_locator_by_name(name))

    def get_realm_heading_by_name(self, name):
        """
        Get realm heading
        :param name: name of the desired realm
        :type name: str
        :return: realm heading
        :rtype: WebElement
        """
        return self.browser.find_element(*EnvironmentsLocators.get_realm_heading_locator_by_name(name))

    def click_realm_heading_by_name(self, name):
        """
        Click realm heading
        """
        button = self.get_realm_heading_by_name(name)
        button.click()

    def get_realm_status_by_name(self, name):
        """
        Get realm status
        :param name: name of the desired realm
        :type name: str
        :return: realm status
        :rtype: WebElement
        """
        return self.browser.find_element(*EnvironmentsLocators.get_realm_status_locator_by_name(name))

    def get_realm_last_published_span_by_name(self, name):
        """
        Get realm last published span
        :param name: realm's name
        :type name: str
        :return: realm's last published span
        :rtype: WebElement
        """
        return self.browser.find_element(*EnvironmentsLocators.get_realm_last_published_span_locator_by_name(name))

    def get_realm_last_published_catalog_by_name(self, realm, catalog_code):
        """
        Get realm's last published catalog
        :param realm: name of the realm
        :type realm: str
        :param catalog_code: name of the catalog
        :type catalog_code: str
        :return: realm's last published catalog
        :rtype: WebElement
        """
        return self.browser.find_element(*EnvironmentsLocators.get_realm_last_published_catalog_by_name(
            realm,
            catalog_code
        ))

    def get_realm_last_published_catalog_title_by_name(self, realm, catalog_code):
        """
        Get realm's last published catalog's title
        :param realm: name of the realm
        :type realm: str
        :param catalog_code: name of the catalog
        :type catalog_code: str
        :return: realm's last published catalog's title
        :rtype: WebElement
        """
        return self.browser.find_element(*EnvironmentsLocators.get_realm_last_published_catalog_title_by_name(
            realm,
            catalog_code
        ))

    def get_realm_no_published_catalog_by_name(self, realm):
        """
        Get realm's no published catalog span
        :param realm: name of the realm
        :type realm: str
        :return: realm's no published catalog span
        :rtype: WebElement
        """
        return self.browser.find_element(*EnvironmentsLocators.get_realm_no_published_catalog_by_name(realm))

    def get_details_heading(self):
        """
        Get an appropriate heading for details table after clicking on specific realm box
        :return: details table heading
        :rtype: WebElement
        """
        return self.browser.find_element(*EnvironmentsLocators.DETAILS_HEADING)

    def get_details_status(self):
        """
        Get server status for details table
        :return: details server status
        :rtype: WebElement
        """
        return self.browser.find_element(*EnvironmentsLocators.DETAILS_STATUS)

    def get_details_catalogs_list(self):
        """
        Get an appropriate catalogs list in the details table after clicking on specific realm box
        :return: details table catalogs list
        :rtype: WebElement
        """
        return self.browser.find_elements(*EnvironmentsLocators.DETAILS_CATALOGS_LIST)

    def get_details_catalogs_header(self):
        """
        Get the catalogs header in the details table
        :return: details table catalogs header
        :rtype: WebElement
        """
        return self.browser.find_element(*EnvironmentsLocators.DETAILS_CATALOGS_HEADER)

    def get_details_last_published_button(self):
        """
        Get the last published button in the details table
        :return: details table last published button
        :rtype: WebElement
        """
        return self.browser.find_element(*EnvironmentsLocators.DETAILS_LAST_PUBLISHED_BUTTON)

    def get_details_catalog(self, catalog_code, publish_version, index):
        """
        Get a specific catalog in the details table
        :param catalog_code: name of the catalog
        :type catalog_code: str
        :param publish_version: publish version of the catalog
        :type publish_version: int
        :param index: row of the details table
        :type index: int
        :return: catalog in the details table
        :rtype: WebElement
        """
        return self.browser.find_element(*EnvironmentsLocators.get_details_catalog_by_name(
            catalog_code,
            publish_version,
            index
        ))

    def get_details_catalog_title(self, catalog_code, publish_version):
        """
        Get the title of a specific catalog in the details table
        :param catalog_code: name of the catalog
        :type catalog_code: str
        :param publish_version: publish version of the catalog
        :type publish_version: int
        :return: title of a catalog in the details table
        :rtype: WebElement
        """
        return self.browser.find_element(*EnvironmentsLocators.get_details_catalog_title_by_name(
            catalog_code,
            publish_version
        ))

    def get_details_catalog_actions_menu(self, catalog_code, publish_version, index):
        """
        Get the actions menu of a specific catalog in the details table
        :param catalog_code: name of the catalog
        :type catalog_code: str
        :param publish_version: publish version of the catalog
        :type publish_version: int
        :param index: row of the details table
        :type index: int
        :return: actions menu of a catalog in the details table
        :rtype: WebElement
        """
        return self.browser.find_element(*EnvironmentsLocators.get_details_catalog_actions_menu_by_name(
            catalog_code,
            publish_version,
            index
        ))

    def click_details_catalog_actions_menu(self, catalog_code, publish_version, index):
        """
        Click the actions menu button of a specific catalog in the details table
        :param catalog_code: name of the catalog
        :type catalog_code: str
        :param publish_version: publish version of the catalog
        :type publish_version: int
        :param index: row of the details table
        :type index: int
        """
        button = self.get_details_catalog_actions_menu(catalog_code, publish_version, index)
        button.click()

    def get_details_close_button(self):
        """
        Get the close button in the details table
        :return: details table close button
        :rtype: WebElement
        """
        return self.browser.find_element(*EnvironmentsLocators.DETAILS_CLOSE_BUTTON)

    def click_details_close_button(self):
        """
        Click the close button in the details table
        """
        button = self.get_details_close_button()
        button.click()
