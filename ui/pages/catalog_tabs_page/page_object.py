from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from locators import CatalogTabsLocators
from ui.pages.base_page import BasePage
from ui.main.constants import DEFAULT_PAGE_TIMEOUT


class CatalogTabs(BasePage):
    def wait_for_page_load(self):
        """
        Wait for the page to be fully loaded
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(CatalogTabsLocators.STOREFRONTS_TAB),
            'Catalog tabs page failed to load'
        )

    def get_catalog_title(self):
        """
        Get catalog title
        :return: catalog title element
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogTabsLocators.CATALOG_TITLE)

    def get_secondary_heading(self):
        """
        Get secondary heading
        :return: secondary heading element
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogTabsLocators.SECONDARY_HEADING)

    def get_download_config_button(self):
        """
        Get download config button
        :return: download config button
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogTabsLocators.DOWNLOAD_CONFIG_BUTTON)

    def click_download_config_button(self):
        """
        Click download config button
        """
        button = self.get_download_config_button()
        button.click()

    def get_publish_button(self):
        """
        Get publish button
        :return: publish button
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogTabsLocators.PUBLISH_BUTTON)

    def click_publish_button(self):
        """
        Click publish button
        """
        button = self.get_publish_button()
        button.click()

    def get_overview_tab(self):
        """
        Get overview tab
        :return: overview tab
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogTabsLocators.OVERVIEW_TAB)

    def click_overview_tab(self):
        """
        Click overview tab
        """
        tab = self.get_overview_tab()
        tab.click()

    def get_storefronts_tab(self):
        """
        Get storefronts tab
        :return: storefronts tab
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogTabsLocators.STOREFRONTS_TAB)

    def click_storefronts_tab(self):
        """
        Click storefronts tab
        """
        tab = self.get_storefronts_tab()
        tab.click()

    def get_products_tab(self):
        """
        Get products tab
        :return: products tab
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogTabsLocators.PRODUCTS_TAB)

    def click_products_tab(self):
        """
        Click products tab
        """
        tab = self.get_products_tab()
        self.browser.execute_script('arguments[0].click()', tab)

    def get_entitlements_tab(self):
        """
        Get entitlements tab
        :return: entitlements tab
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogTabsLocators.ENTITLEMENTS_TAB)

    def click_entitlements_tab(self):
        """
        Click entitlements tab
        """
        tab = self.get_entitlements_tab()
        self.browser.execute_script('arguments[0].click()', tab)

    def get_currencies_tab(self):
        """
        Get currencies tab
        :return: currencies tab
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogTabsLocators.CURRENCIES_TAB)

    def click_currencies_tab(self):
        """
        Click currencies tab
        """
        tab = self.get_currencies_tab()
        self.browser.execute_script('arguments[0].click()', tab)

    def get_campaigns_tab(self):
        """
        Get campaigns tab
        :return: campaigns tab
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogTabsLocators.CAMPAIGNS_TAB)

    def click_campaigns_tab(self):
        """
        Click campaigns tab
        """
        tab = self.get_campaigns_tab()
        tab.click()

    def get_activity_tab(self):
        """
        Get activity tab
        :return: activity tab
        :rtype: WebElement
        """
        return self.browser.find_element(*CatalogTabsLocators.ACTIVITY_TAB)

    def click_activity_tab(self):
        """
        Click activity tab
        """
        tab = self.get_activity_tab()
        tab.click()

    def get_tab_list(self):
        """
        Get tabs in the tab list
        :return: tab list
        :rtype: list of WebElement
        """
        return self.browser.find_elements(*CatalogTabsLocators.TAB_LIST)
