from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from locators import SidebarLocators
from ui.main.constants import DEFAULT_PAGE_TIMEOUT
from ui.pages.base_page import BasePage


class Sidebar(BasePage):
    def wait_for_page_load(self):
        """
        Wait for the page to be fully loaded
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(SidebarLocators.PANEL),
            'Sidebar page failed to load'
        )

    def get_activity_button(self):
        """
        Get activity sidebar button on the sidebar page
        :return: activity sidebar button
        :rtype: WebElement
        """
        return self.browser.find_element(*SidebarLocators.ACTIVITY_BUTTON)

    def click_activity_button(self):
        """
        Click activity sidebar button on the sidebar page
        """
        button = self.get_activity_button()
        button.click()

    def get_catalogs_button(self):
        """
        Get catalogs sidebar button on the sidebar page
        :return: catalogs sidebar button
        :rtype: WebElement
        """
        return self.browser.find_element(*SidebarLocators.CATALOGS_BUTTON)

    def click_catalogs_button(self):
        """
        Click catalogs sidebar button on the sidebar page
        """
        button = self.get_catalogs_button()
        button.click()

    def get_dashboard_button(self):
        """
        Get dashboard sidebar button on the sidebar page
        :return: dashboard sidebar button
        :rtype: WebElement
        """
        return self.browser.find_element(*SidebarLocators.DASHBOARD_BUTTON)

    def click_dashboard_button(self):
        """
        Click dashboard sidebar button on the sidebar page
        """
        button = self.get_dashboard_button()
        button.click()

    def get_players_button(self):
        """
        Get players sidebar button on the sidebar page
        :return: players sidebar button
        :rtype: WebElement
        """
        return self.browser.find_element(*SidebarLocators.PLAYERS_BUTTON)

    def click_players_button(self):
        """
        Click players sidebar button on the sidebar page
        """
        button = self.get_players_button()
        button.click()

    def get_reports_button(self):
        """
        Get reports sidebar button on the sidebar page
        :return: reports sidebar button
        :rtype: WebElement
        """
        return self.browser.find_element(*SidebarLocators.REPORTS_BUTTON)

    def click_reports_button(self):
        """
        Click reports sidebar button on the sidebar page
        """
        button = self.get_reports_button()
        button.click()

    def get_settings_button(self):
        """
        Get settings sidebar button on the sidebar page
        :return: settings sidebar button
        :rtype: WebElement
        """
        return self.browser.find_element(*SidebarLocators.SETTINGS_BUTTON)

    def click_settings_button(self):
        """
        Click settings sidebar button on the sidebar page
        """
        button = self.get_settings_button()
        button.click()

    def get_panel(self):
        """
        Get elements in the sidebar panel
        :return: sidebar panel elements
        :rtype: list of WebElement
        """
        return self.browser.find_elements(*SidebarLocators.PANEL)

    def get_studios_button(self):
        """
        Get studios sidebar button on the sidebar page
        :return: studios sidebar button
        :rtype: WebElement
        """
        return self.browser.find_element(*SidebarLocators.STUDIOS_BUTTON)

    def click_studios_button(self):
        """
        Click studios sidebar button on the sidebar page
        """
        button = self.get_studios_button()
        button.click()

    def get_titles_button(self):
        """
        Get titles sidebar button on the sidebar page
        :return: titles sidebar button
        :rtype: WebElement
        """
        return self.browser.find_element(*SidebarLocators.TITLES_BUTTON)

    def click_titles_button(self):
        """
        Click titles sidebar button on the sidebar page
        """
        button = self.get_titles_button()
        button.click()

    def get_users_button(self):
        """
        Get users sidebar button on the sidebar page
        :return: users sidebar button
        :rtype: WebElement
        """
        return self.browser.find_element(*SidebarLocators.USERS_BUTTON)

    def click_users_button(self):
        """
        Click users sidebar button on the sidebar page
        """
        button = self.get_users_button()
        button.click()

    def get_environments_button(self):
        """
        Get environments sidebar button on the sidebar page
        :return: environments sidebar button
        :rtype: WebElement
        """
        return self.browser.find_element(*SidebarLocators.ENVIRONMENTS_BUTTON)

    def click_environments_button(self):
        """
        Click environments sidebar button on the sidebar page
        """
        button = self.get_environments_button()
        button.click()

    def get_title_components_button(self):
        """
        Get Title Components sidebar button on the sidebar page
        :return: Title Components sidebar button
        :rtype: WebElement
        """
        return self.browser.find_element(*SidebarLocators.TITLE_COMPONENTS_BUTTON)

    def click_title_components_button(self):
        """
        Click Title Components sidebar button on the sidebar page
        """
        button = self.get_title_components_button()
        button.click()

    def get_back_to_titles_button(self):
        """
        Get the Back to Title button on the sidebar page
        :return: Back to Title button
        :rtype: WebElement
        """
        return self.browser.find_element(*SidebarLocators.BACK_TO_TITLES_BUTTON)

    def click_back_to_titles_button(self):
        """
        Click the Back to Title button
        """
        button = self.get_back_to_titles_button()
        button.click()

    def get_data_button(self):
        """
        Get the Data button on the sidebar page
        :return: Data button
        :rtype: WebElement
        """
        return self.browser.find_element(*SidebarLocators.DATA_BUTTON)

    def click_data_button(self):
        """
        Click the Data button
        """
        button = self.get_data_button()
        button.click()
