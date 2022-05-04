from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from locators import NotificationLocators
from ui.pages.base_page import BasePage
from ui.main.constants import DEFAULT_PAGE_TIMEOUT


class Notification(BasePage):
    def wait_for_notification_message(self):
        """
        Wait for the notification message to appear
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(NotificationLocators.NOTIFICATION_MESSAGE),
            'Notification message did not display'
        )

    def wait_for_notification_message_to_disappear(self):
        """
        Wait for the notification message to disappear
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.invisibility_of_element_located(NotificationLocators.NOTIFICATION_MESSAGE),
            'Notification message is still there'
        )

    def get_notification_message(self):
        """
        Get the notification message after an action is taken
        :return: message element in the notification bar
        :rtype: WebElement
        """
        return self.browser.find_element(*NotificationLocators.NOTIFICATION_MESSAGE)
