from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions


class wait_for_non_empty_text(object):
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            element_text = expected_conditions._find_element(driver, self.locator).text.strip()
            return element_text != ""
        except StaleElementReferenceException:
            return False
