from selenium.webdriver.remote.webdriver import WebDriver


class BasePage(object):
    def __init__(self, browser):
        """
        Initialize a base page
        :param browser: browser to be used in testing
        :type browser: WebDriver
        """
        self.browser = browser
