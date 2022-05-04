from selenium.webdriver.common.by import By


class AddBulkPlayersLocators(object):
    PAGE_HEADER = (By.XPATH, "//h1[@class='header__title___1itKA']/span/a")
    PAGE_SUBHEADER = (By.XPATH, "//h1[@class='header__title___1itKA']/span[2]")
    CONTEXT_TEXT = (By.XPATH, "//h2[@class='header__title___1itKA']/span[text()='Context']")

    ITERATIONS_LABEL = (By.XPATH, "//div[@class='text_field__header___biqb4' and text()='Iterations']")
    ITERATIONS_INPUT = (By.XPATH, "//div[@id='wgptx']/section/main/div[3]/div/label/span/input")

    REALM_LABEL = (By.XPATH, "//span[@class='drop_down__basicLabel___1R5CD' and text()='Realm']")
    REALM_INPUT = (By.XPATH, "//div[@id='wgptx']/section/main/div[3]/div[2]/div//span/div/span[1]")
    REALM_DROP_DOWN_LIST_ARROW = (By.XPATH, "//div[@id='wgptx']/section/main/div[3]/div[2]/div//span/div/span[2]")
    REALM_DROP_DOWN_LIST = (By.XPATH, "//div[@id='wgptx']/section/main/div[3]/div[2]/div//span/div/ul/li")

    GAMES_LABEL = (By.XPATH, "//span[@class='drop_down__basicLabel___1R5CD' and text()='Games']")
    GAMES_INPUT = (By.ID, 'undefined_drop_down')
    GAMES_DROP_DOWN_LIST_ARROW = (By.ID, 'icon_undefined_drop_down')
    GAMES_DROP_DOWN_LIST = (By.XPATH, "//div[@id='wgptx']/section/main/div[3]/div[3]/div//span/div/ul/li")

    GAME_TAG = (By.ID, 'undefined_wot_chip')
    GAME_TAG_EXIT_BUTTON = (By.XPATH, "//span[@class='chip__cancelIcon___10Jl6']")

    TEMPLATE_TEXT = (By.XPATH, "//h2[@class='header__title___1itKA']/span[text()='Template']")

    INFO_BOX = (By.XPATH, "//div[@class='message_box__messageBox___2avRn message_box__info___3paCe']")
    INFO_BOX_BUTTON = (By.XPATH, "//button[@class='collapsible_row__iconButton___3iAAV']")
    INFO_BOX_STRONG = (By.XPATH, "//div[@class='collapsible_row__headerElement___2t9lY']/strong")

    LOGIN_LABEL = (By.XPATH, "//div[@class='text_field__header___biqb4' and text()='Login']")
    LOGIN_INPUT = (By.XPATH, "//div[@id='wgptx']/section/main/div[6]/div[1]/label/span//input")
    LOGIN_INVALID_MESSAGE = (By.XPATH, "//div[@class='message_box__messageBox___2avRn message_box__danger___17B8G']//tr/td[2]/span")

    PASSWORD_LABEL = (By.XPATH, "//div[@class='text_field__header___biqb4' and text()='Password']")
    PASSWORD_INPUT = (By.XPATH, "//div[@id='wgptx']/section/main/div[6]/div[2]/label/span//input")
    PASSWORD_INVALID_MESSAGE = (By.XPATH, "//div[@class='message_box__messageBox___2avRn message_box__danger___17B8G']//tr/td[2]/span")

    NAME_LABEL = (By.XPATH, "//div[@class='text_field__header___biqb4' and text()='Name']")
    NAME_INPUT = (By.XPATH, "//div[@id='wgptx']/section/main/div[6]/div[3]/label/span//input")
    NAME_INVALID_MESSAGE = (By.XPATH, "//div[@class='message_box__messageBox___2avRn message_box__danger___17B8G']//tr/td[2]/span")

    AUTHENTICATION_METHOD_LABEL = (By.XPATH, "//span[@class='drop_down__basicLabel___1R5CD' and text()='Authentication Method']")
    AUTHENTICATION_METHOD_INPUT = (By.XPATH, "//div[@id='wgptx']/section/main/div[6]/div[4]/div/span/div/span[1]")
    AUTHENTICATION_METHOD_DROP_DOWN_LIST_ARROW = (By.XPATH, "//div[@id='wgptx']/section/main/div[6]/div[4]/div/span/div/span[2]")
    AUTHENTICATION_METHOD_DROP_DOWN_LIST = (By.XPATH, "//div[@id='wgptx']/section/main/div[6]/div[4]/div/span/div/ul/li")

    IP_LABEL = (By.XPATH, "//div[@class='text_field__header___biqb4' and text()='IP']")
    IP_INPUT = (By.XPATH, "//div[@id='wgptx']/section/main/div[6]/div[5]/label/span/input")
    IP_INVALID_MESSAGE = (By.XPATH, "//div[@class='message_box__messageBox___2avRn message_box__danger___17B8G']//tr/td[2]/span")

    SAVE_BUTTON = (By.XPATH, "//button[@label='Save']")
    CANCEL_BUTTON = (By.XPATH, "//button[@label='Cancel']")

    @staticmethod
    def get_realm_drop_down_list_item_locator_by_name(name):
        """
        Get the locator for the Realm's drop down list item based on the name
        :param name: Name of the realm
        :type name: str
        :return: locator for the Realm's drop down list item
        :rtype: (By, str)
        """
        return By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirColumn___3Qma0']/div[2]/div/span/div/ul/li/div/p[text()='{}']".format(name)

    @staticmethod
    def get_games_drop_down_list_item_locator_by_name(name):
        """
        Get the locator for the Games's drop down list item based on the name
        :param name: Name of the game
        :type name: str
        :return: locator for the Games's drop down list item
        :rtype: (By, str)
        """
        return By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirColumn___3Qma0']/div[3]/div/span/div/ul/li/div/p[text()='{}']".format(name)

    @staticmethod
    def get_authentication_method_drop_down_list_item_locator_by_name(name):
        """
        Get the locator for the Authentication Method's drop down list item based on the name
        :param name: Name of the method
        :type name: str
        :return: locator for the Authentication Method's drop down list item
        :rtype: (By, str)
        """
        return By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirColumn___3Qma0']/div[4]/div/span/div/ul/li/div/p[text()='{}']".format(name)
