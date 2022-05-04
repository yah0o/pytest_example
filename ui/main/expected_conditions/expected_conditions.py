from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import StaleElementReferenceException


class exact_text(object):
    """ An expectation for checking if the given text is the same in the
    specified element.
    locator, text
    """

    def __init__(self, locator, text_):
        self.locator = locator
        self.text = text_

    def __call__(self, driver):
        try:
            element_text = expected_conditions._find_element(driver, self.locator).text
            return self.text == element_text
        except StaleElementReferenceException:
            return False


class get_player_list(object):
    """ An expectation for checking if the given list has the certain length.
    list_locator, button_locator, expected_length
    """

    def __init__(self, list_locator, button_locator, expected_length):
        self.list = list_locator
        self.button = button_locator
        self.expected_length = expected_length

    def __call__(self, driver):
        button = expected_conditions._find_element(driver, self.button)
        button.click()
        import time
        time.sleep(1)
        player_list = expected_conditions._find_elements(driver, self.list)
        try:
            return len(player_list) == self.expected_length
        except StaleElementReferenceException:
            return False
