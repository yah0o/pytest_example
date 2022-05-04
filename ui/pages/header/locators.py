from selenium.webdriver.common.by import By


class HeaderLocators(object):
    HOME_BUTTON = (By.ID, 'home_button')
    TOP_BAR_HEADER = (By.ID, 'topbar_heading')
    NETWORK_STATUS = (By.ID, 'network_status')
    NOTIFICATION_ICON = (By.ID, 'notification_icon')
    SETTINGS_ICON = (By.ID, 'settings_icon_toggle_menu')
    DROP_DOWN_MENU = (By.ID, 'overlord_user_menu_toggle_menu')
    DROP_DOWN_OPTIONS = (By.XPATH, "//option")
    USER_ICON = (By.XPATH, "//div[@class='user_dropdown__userIconBox___1B2rT']")
    USER_ID = (By.XPATH, "//div[@class='user_dropdown__userIDBox___1leGr']")
    LOGOUT_BUTTON = (By.ID, 'overlord_user_menu_logout')
