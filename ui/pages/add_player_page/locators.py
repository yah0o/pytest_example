from selenium.webdriver.common.by import By


class AddPlayerLocators(object):
    PAGE_HEADER = (By.XPATH, "//h1[@class='header__title___1itKA']//a")
    PAGE_SUBHEADER = (By.XPATH, "//h1[@class='header__title___1itKA']/span[2]")

    REALM_LABEL = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirColumn___3Qma0']/div[1]/div/div/span")
    REALM_INPUT = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirColumn___3Qma0']/div[1]/div/span/div/span[1]")
    REALM_DROP_DOWN_LIST_ARROW = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirColumn___3Qma0']/div[1]/div/span/div/span[2]")
    REALM_DROP_DOWN_LIST = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirColumn___3Qma0']/div[1]/div/span/div/ul/li")

    GAMES_LABEL = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirColumn___3Qma0']/div[2]/div/div/span")
    GAMES_INPUT = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirColumn___3Qma0']/div[2]/div/span//input")
    GAMES_DROP_DOWN_LIST_ARROW = (By.ID, 'icon_undefined_drop_down')
    GAMES_DROP_DOWN_LIST = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirColumn___3Qma0']/div[2]/div/span/div/ul/li")

    GAME_TAG = (By.ID, 'undefined_wot_chip')
    GAME_TAG_EXIT_BUTTON = (By.XPATH, "//span[@class='chip__cancelIcon___10Jl6']")

    LOGIN_LABEL = (By.XPATH, "//label[@class='text_field__textFieldLabel___2LncU']/div[text()='Login']")
    LOGIN_INPUT = (
        By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirColumn___3Qma0']/div[3]/label/span/input")
    LOGIN_INVALID_MESSAGE = (By.XPATH, "//div[@class='message_box__messageBox___2avRn message_box__danger___17B8G']//tr/td[2]")

    PASSWORD_LABEL = (By.XPATH, "//label[@class='text_field__textFieldLabel___2LncU']/div[text()='Password']")
    PASSWORD_INPUT = (
        By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirColumn___3Qma0']/div[4]/label/span/input")
    PASSWORD_INVALID_MESSAGE = (By.XPATH, "//div[@class='message_box__messageBox___2avRn message_box__danger___17B8G']//tr/td[2]")

    NAME_LABEL = (By.XPATH, "//label[@class='text_field__textFieldLabel___2LncU']/div[text()='Name']")
    NAME_INPUT = (
        By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirColumn___3Qma0']/div[5]/label/span/input")
    NAME_INVALID_MESSAGE = (By.XPATH, "//div[@class='message_box__messageBox___2avRn message_box__danger___17B8G']//tr/td[2]")

    AUTHENTICATION_METHOD_LABEL = (
        By.XPATH, "//span[@class='drop_down__basicLabel___1R5CD' and text()='Authentication Method']")
    AUTHENTICATION_METHOD_INPUT = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirColumn___3Qma0']/div[6]/div/span/div/span[1]")
    AUTHENTICATION_METHOD_DROP_DOWN_LIST_ARROW = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirColumn___3Qma0']/div[6]/div/span/div/span[2]")
    AUTHENTICATION_METHOD_DROP_DOWN_LIST = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirColumn___3Qma0']/div[6]/div/span/div/ul/li")

    IP_LABEL = (By.XPATH, "//label[@class='text_field__textFieldLabel___2LncU']/div[text()='IP']")
    IP_INPUT = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirColumn___3Qma0']/div[7]/label/span/input")
    IP_INVALID_MESSAGE = (By.XPATH, "//div[@class='message_box__messageBox___2avRn message_box__danger___17B8G']//tr/td[2]")

    SAVE_BUTTON = (By.XPATH, "//button[@class='button__textButton___30NFq' and text()='Save']")
    CANCEL_BUTTON = (By.XPATH, "//button[@class='button__textButton___30NFq' and text()='Cancel']")

    @staticmethod
    def get_realm_drop_down_list_item_locator_by_name(name):
        """
        Get the locator for the Realm's drop down list item based on the name
        :param name: Name of the realm
        :type name: str
        :return: locator for the Realm's drop down list item
        :rtype: (By, str)
        """
        return By.XPATH, \
        "//div[@class='components__flex___3GCvy components__flexDirColumn___3Qma0']/div[1]/div/span[2]/div/ul/li/div/p[text()='{}']".format(name)

    @staticmethod
    def get_games_drop_down_list_item_locator_by_name(name):
        """
        Get the locator for the Games's drop down list item based on the name
        :param name: Name of the game
        :type name: str
        :return: locator for the Games's drop down list item
        :rtype: (By, str)
        """
        return By.XPATH, \
        "//div[@class='components__flex___3GCvy components__flexDirColumn___3Qma0']/div[2]/div[1]/span[2]/div/ul/li/div/p[text()='{}']".format(name)

    @staticmethod
    def get_authentication_method_drop_down_list_item_locator_by_name(name):
        """
        Get the locator for the Authentication Method's drop down list item based on the name
        :param name: Name of the method
        :type name: str
        :return: locator for the Authentication Method's drop down list item
        :rtype: (By, str)
        """
        return By.XPATH, \
        "//div[@class='components__flex___3GCvy components__flexDirColumn___3Qma0']/div[6]/div/span[2]/div/ul/li/div/p[text()='{}']".format(name)
