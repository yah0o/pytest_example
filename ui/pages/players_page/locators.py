from selenium.webdriver.common.by import By


class PlayerLocators(object):
    PAGE_HEADER = (By.XPATH, "//h1[@class='header__title___1itKA']")
    CREATE_BUTTON = (By.XPATH, "//button[@class='button__textButton___30NFq' and text()='Create']")
    CREATE_BULK_BUTTON = (By.XPATH, "//button[@class='button__textButton___30NFq' and text()='Create Bulk']")

    INFO_BOX = (By.XPATH, "//div[@class='message_box__messageBox___2avRn message_box__info___3paCe']")
    INFO_BOX_EXIT_BUTTON = (By.XPATH, "//div[@class='message_box__messageBox___2avRn message_box__info___3paCe']/span")
    INFO_BOX_STRONG = (By.XPATH, "//div[@class='message_box__messageBox___2avRn message_box__info___3paCe']/strong")

    VALIDATION_BOX = (By.XPATH, "//div[@class='message_box__messageBox___2avRn message_box__danger___17B8G']")
    VALIDATION_BOX_EXIT_BUTTON = (
        By.XPATH, "//span[@class='message_box__exitButton___3m4CN components__userSelectNone___2qhzr']")
    VALIDATION_BOX_NAME_STRONG = (By.XPATH, "//div[@class='message_box__messageBox___2avRn message_box__danger___17B8G']/table/tbody/tr[1]/td[1]")
    VALIDATION_BOX_REALM_STRONG = (By.XPATH, "//div[@class='message_box__messageBox___2avRn message_box__danger___17B8G']/table/tbody/tr[2]/td[1]")
    VALIDATION_BOX_GAME_STRONG = ()

    FIELD_LABEL = (By.XPATH, "//span[@class='drop_down__basicLabel___1R5CD' and text()='Field']")
    FIELD_INPUT = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirRow___29rUw components__flexAIFlexStart___2jEak']/div[1]/div/span/div/span[1]")
    FIELD_DROP_DOWN_LIST_ARROW = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirRow___29rUw components__flexAIFlexStart___2jEak']/div[1]/div/span/div/span[2]")
    FIELD_DROP_DOWN_LIST = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirRow___29rUw components__flexAIFlexStart___2jEak']/div[1]/div/span/div/ul/li")

    OPERATOR_LABEL = (By.XPATH, "//span[@class='drop_down__basicLabelDisabled___39o_t' and text()='Operator']")
    OPERATOR_INPUT = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirRow___29rUw components__flexAIFlexStart___2jEak']/div[2]/div/span/div/span[1]")
    OPERATOR_DROP_DOWN_LIST_ARROW = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirRow___29rUw components__flexAIFlexStart___2jEak']/div[2]/div/span/div/span[2]")

    VALUE_LABEL = (By.XPATH, "//label[@class='text_field__textFieldLabel___2LncU']/div[text()='Value']")
    VALUE_INPUT = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirRow___29rUw components__flexAIFlexStart___2jEak']/div[3]/label/span/input")
    VALUE_DROP_DOWN_LIST_ARROW = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirRow___29rUw components__flexAIFlexStart___2jEak']/div[3]/div/span/div/span[2]")
    VALUE_DROP_DOWN_LIST = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirRow___29rUw components__flexAIFlexStart___2jEak']/div[3]/div/span/div/ul/li")

    NAME_TAG = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirRow___29rUw']/span[1]")
    NAME_TAG_EXIT_BUTTON = (By.XPATH, "//span[@class='chip__chip___1f2ZZ' and text()='Name']/span")

    REALM_TAG = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirRow___29rUw']/span[2]")
    REALM_TAG_EXIT_BUTTON = (By.XPATH, "//span[@class='chip__chip___1f2ZZ' and text()='Realm']/span")

    GAME_TAG = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirRow___29rUw']/span[3]")
    GAME_TAG_EXIT_BUTTON = (By.XPATH, "//span[@class='chip__chip___1f2ZZ' and text()='Game']/span")

    ADD_BUTTON = (By.XPATH, "//button[@class='button__textButton___30NFq' and text()='Add']")
    FILTER_BUTTON = (By.XPATH, "//button[@class='button__textButton___30NFq' and text()='Filter']")
    RESET_BUTTON = (By.XPATH, "//button[@class='button__textButton___30NFq' and text()='Reset']")

    SHOWING_RESULTS_TEXT = (By.XPATH, "//p[@class='caption table__results___2_97_']")

    TABLE_COLUMN_LIST = (By.XPATH, "//thead[@class='table__tableHeader___r3k__']/tr/th")
    PLAYER_LIST = (By.XPATH, "//tbody[@class='table__tableBody____j4Uc']/tr")
    NO_PLAYERS_FOUND = (By.XPATH, "//td[@class='table__noDataCell___3pyjm']")

    @staticmethod
    def get_field_drop_down_list_item_locator_by_name(name):
        """
        Get the locator for the Field's drop down list item based on the name
        :param name: Name of the item
        :type name: str
        :return: locator for the Field's drop down list item
        :rtype: (By, str)
        """
        return By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirRow___29rUw components__flexAIFlexStart___2jEak']/div[1]/div/span/div/ul/li/div/p[text()='{}']".format(name)

    @staticmethod
    def get_value_drop_down_list_realm_locator_by_name(name):
        """
        Get the locator for the Realm based on the name (in the Value column, after selecting Realm item from the Field)
        :param name: Name of the realm
        :type name: str
        :return: locator for the realm
        :rtype: (By, str)
        """
        return By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirRow___29rUw components__flexAIFlexStart___2jEak']/div[3]/div/span/div/ul/li/div/p[text()='{}']".format(name)

    @staticmethod
    def get_value_drop_down_list_game_locator_by_name(name):
        """
        Get the locator for the Game based on the name (in the Value column, after selecting Game item from the Field)
        :param name: Name of the game
        :type name: str
        :return: locator for the game
        :rtype: (By, str)
        """
        return By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirRow___29rUw components__flexAIFlexStart___2jEak']/div[3]/div/span[2]/div/ul/li/div/p[text()='{}']".format(name)

    @staticmethod
    def get_table_column_header_locator_by_name(name):
        """
        Get the locator for the specific table's column header based on the name
        :param name: Name of the column
        :type name: str
        :return: locator for the specific table's column header
        :rtype: (By, str)
        """
        return By.ID, 'column_heading_{}'.format(name)

    @staticmethod
    def get_table_id_locator_by_name(name):
        """
        Get the locator for the player's id based on the name
        :param name: Name of the player
        :type name: str
        :return: locator for the specific player's id
        :rtype: (By, str)
        """
        return By.ID, "table_cell_{}_id".format(name)

    @staticmethod
    def get_table_name_locator_by_name(name):
        """
        Get the locator for the player's name based on the name
        :param name: Name of the player
        :type name: str
        :return: locator for the specific player's name
        :rtype: (By, str)
        """
        return By.ID, "table_cell_{}_name".format(name)

    @staticmethod
    def get_table_realm_locator_by_name(name):
        """
        Get the locator for the player's realm based on the name
        :param name: Name of the player
        :type name: str
        :return: locator for the specific player's realm
        :rtype: (By, str)
        """
        return By.ID, "table_cell_{}_realm".format(name)

    @staticmethod
    def get_table_game_locator_by_name(name):
        """
        Get the locator for the player's game based on the name
        :param name: Name of the player
        :type name: str
        :return: locator for the specific player's game
        :rtype: (By, str)
        """
        return By.ID, "table_cell_{}_games".format(name)

    @staticmethod
    def get_table_actions_button_locator_by_name(name):
        """
        Get the locator for the player's actions button based on the name
        :param name: Name of the player
        :type name: str
        :return: locator for the specific player's actions button
        :rtype: (By, str)
        """
        return By.ID, "{}_toggle_menu".format(name)
