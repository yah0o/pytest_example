from selenium.webdriver.common.by import By


class LoginPageLocators(object):
    WARGAMING_SSO_LINK = (By.XPATH, "//div[@class='authContainer__a86344d2']//a")
    USERNAME_INPUT = (By.ID, 'userNameInput')
    PASSWORD_INPUT = (By.ID, 'passwordInput')
    SIGN_IN_BUTTON = (By.ID, 'submitButton')
