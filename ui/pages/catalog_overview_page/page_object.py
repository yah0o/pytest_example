from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from locators import CatalogOverviewLocators
from ui.pages.base_page import BasePage
from ui.main.constants import DEFAULT_PAGE_TIMEOUT


class CatalogOverview(BasePage):
    def wait_for_page_load(self):
        """
        Wait for the page to be fully loaded
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(CatalogOverviewLocators.ACTIVITY_LIST),
            'Catatog overview page failed to load'
        )

    def get_recent_activity_text(self):
        """
        Get "Recent activity" text
        :return: "Recent activity" text element
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogOverviewLocators.RECENT_ACTIVITY_TEXT)

    def get_recent_activity_subheading_text(self):
        """
        Get "Latest changes to the catalog" text
        :return: "Latest changes to the catalog" text element
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogOverviewLocators.RECENT_ACTIVITY_SUBHEADING_TEXT)

    def get_see_all_activity_link(self):
        """
        Get "See all activity" link
        :return: "See all activity" link
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogOverviewLocators.SEE_ALL_ACTIVITY_LINK)

    def click_see_all_activity_link(self):
        """
        Click "See all activity" link
        """
        tab = self.get_see_all_activity_link()
        tab.click()

    def get_recent_activity_date_column(self):
        """
        Get the name of 'Recent activity' table's Date column
        :return: Date column text
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogOverviewLocators.RECENT_ACTIVITY_DATE_COLUMN)

    def get_recent_activity_name_column(self):
        """
        Get the name of 'Recent activity' table's Name column
        :return: Name column text
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogOverviewLocators.RECENT_ACTIVITY_NAME_COLUMN)

    def get_recent_activity_activity_column(self):
        """
        Get the name of 'Recent activity' table's Activity column
        :return: Activity column text
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogOverviewLocators.RECENT_ACTIVITY_ACTIVITY_COLUMN)

    def get_activity_list(self):
        """
        Get list of activities
        :return: list of activities
        :rtype: list of WebElement
        """
        return self.browser.find_elements(*CatalogOverviewLocators.ACTIVITY_LIST)

    def get_status_text(self):
        """
        Get "Status across environments" text
        :return: "Status across environments" text element
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogOverviewLocators.STATUS_ACROSS_ENVIRONMENTS_TEXT)

    def get_status_subheading_text(self):
        """
        Get "Environments where the catalog has been promoted" text
        :return: "Environments where the catalog has been promoted" text element
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogOverviewLocators.STATUS_SUBHEADING_TEXT)

    def get_see_all_catalogs_link(self):
        """
        Get "See all catalogs" link
        :return: "See all catalogs" link
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogOverviewLocators.SEE_ALL_CATALOGS_LINK)

    def click_see_all_catalogs_link(self):
        """
        Click "See all catalogs" link
        """
        tab = self.get_see_all_catalogs_link()
        tab.click()

    def get_status_name_column(self):
        """
        Get the name of 'Status across environments' table's Name column
        :return: Name column text
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogOverviewLocators.STATUS_NAME_COLUMN)

    def get_status_last_promotion_date_column(self):
        """
        Get the name of 'Status across environments' table's 'Last promotion date' column
        :return: 'Last promotion date' column text
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogOverviewLocators.STATUS_LAST_PROMOTION_DATE_COLUMN)

    def get_status_list(self):
        """
        Get list of statuses
        :return: list of statuses
        :rtype: list of WebElement
        """
        return self.browser.find_elements(*CatalogOverviewLocators.STATUS_LIST)
