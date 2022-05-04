import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select
from ui.pages import LoginPage, Header, Sidebar, Studios, Titles, Catalogs, Storefronts, Products, AddTitle, \
    CatalogTabs, Entitlements, Currencies, Environments


class UISteps(object):
    def __init__(self, browser):
        """
        Initialize the ui steps
        :param browser: browser to be used during testing
        :type browser: WebDriver
        """
        self.browser = browser
        self.login_page = LoginPage(self.browser)
        self.header = Header(self.browser)
        self.sidebar_page = Sidebar(self.browser)
        self.studios_page = Studios(self.browser)
        self.titles_page = Titles(self.browser)
        self.catalogs_page = Catalogs(self.browser)
        self.add_title_page = AddTitle(self.browser)
        self.storefronts_page = Storefronts(self.browser)
        self.catalog_tabs_page = CatalogTabs(self.browser)
        self.products_page = Products(self.browser)
        self.entitlements_page = Entitlements(self.browser)
        self.currencies_page = Currencies(self.browser)
        self.environments_page = Environments(self.browser)

    @pytest.allure.step('Navigate to a url')
    def navigate(self, url):
        """
        Navigate the browser to the specified url
        :param url: url to which you want to navigate
        :type url: str
        """
        self.browser.get(url)

    @pytest.allure.step('Login to tools ui')
    def login(self, username, password):
        """
        Login to the tools ui
        :param username: Username to use for authentication
        :type username: str
        :param password: Password to use for authentication
        :type password: str
        """
        self.login_page.wait_for_page_load()

        self.login_page.click_sso_link()

        self.login_page.wait_for_credentials_page_load()

        self.login_page.set_username_field(username)
        self.login_page.set_password_field(password)
        self.login_page.click_sign_in_button()
        self.studios_page.wait_for_page_load()

    @pytest.allure.step('Logout of tools ui')
    def logout(self):
        """
        Logout of the tools ui
        """
        logout_option = Select(self.header.get_drop_down_menu())
        logout_option.select_by_value('logout')

    @pytest.allure.step('Navigate to titles page for a given studio')
    def navigate_to_titles_page(self, name):
        """
        Navigate the browser to the Titles page
        :param name: name of the studio for which you want the titles
        :type name: str
        """
        self.studios_page.click_studio_button_by_name(name)
        self.titles_page.wait_for_page_load()

    @pytest.allure.step('Navigate to the Catalogs page within the Test Title')
    def navigate_to_catalogs_page(self, name):
        """
        Navigate the browser to the Catalogs page
        """
        self.titles_page.click_title_button_by_name(name)
        self.catalogs_page.wait_for_page_load()

    @pytest.allure.step('Navigate to the Environments page within the Test Title')
    def navigate_to_environments_page(self):
        """
        Navigate the browser to the Environments page
        """
        self.sidebar_page.wait_for_page_load()
        self.sidebar_page.click_environments_button()
        self.environments_page.wait_for_page_load()

    @pytest.allure.step('Navigate to the Catalog Tabs/Overview page within the Test Catalog')
    def navigate_to_catalog_tabs_page(self, name):
        """
        Navigate the browser to the Catalog Tabs/Overview page
        """
        self.catalogs_page.click_catalog_by_name(name)
        self.catalog_tabs_page.wait_for_page_load()

    @pytest.allure.step('Navigate to Storefronts page')
    def navigate_to_storefronts_page(self):
        """
        Navigate the browser to the Storefronts page
        """
        self.storefronts_page.wait_for_page_load()

    @pytest.allure.step('Navigate to Products tab')
    def navigate_to_products_tab(self):
        """
        Navigate the browser to the Products tab
        """
        self.catalog_tabs_page.click_products_tab()
        self.products_page.wait_for_page_load()

    @pytest.allure.step('Navigate to Entitlements page')
    def navigate_to_entitlements_page(self):
        """
        Navigate the browser to the Entitlements page
        """
        self.catalog_tabs_page.click_entitlements_tab()
        self.entitlements_page.wait_for_page_load()

    @pytest.allure.step('Navigate to Currencies page')
    def navigate_to_currencies_page(self):
        """
        Navigate the browser to the Currencies page
        """
        self.catalog_tabs_page.click_currencies_tab()
        self.currencies_page.wait_for_page_load()
