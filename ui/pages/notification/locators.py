from selenium.webdriver.common.by import By


class NotificationLocators(object):
    NOTIFICATION_MESSAGE = (By.XPATH, "//p[@class='notification_bar__notificationMessage___1tF50']")
    PRODUCTS_NOTIFICATION_MESSAGE = (By.XPATH,
                                     "//p[@class='notification_bar__notificationMessage___1tF50__1554314584472']")
