from selenium.webdriver.common.by import By


class EditPlayerLocators(object):
    PAGE_HEADER = (By.XPATH, "//h1[@class='header__title___1itKA']//a")
    PAGE_SUBHEADER = (By.XPATH, "//h1[@class='header__title___1itKA']/span[2]")

    ID_LABEL = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirColumn___3Qma0']/div[1]/label")
    ID_INPUT = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirColumn___3Qma0']/div[1]/label/span/input")

    NAME_LABEL = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirColumn___3Qma0']/div[2]/label")
    NAME_INPUT = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirColumn___3Qma0']/div[2]/label/span/input")

    REALM_LABEL = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirColumn___3Qma0']/div[3]/label")
    REALM_INPUT = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirColumn___3Qma0']/div[3]/label/span/input")

    GAME_REGISTRATIONS_HEADER = (By.XPATH, "//h2[@class='header__title___1itKA']/span[text()='Game Registrations']")
    GAME_REGISTRATIONS_NAME_COLUMN = (By.XPATH, "//th[@id='column_heading_game' and text()='Name']")
    GAME_LIST = (By.XPATH, "//div[@id='wgptx']/section[2]//tbody/tr")
    CREATE_GAME_BUTTON = (By.XPATH, "//div[@id='wgptx']/section[2]//div//button")
    GAME_REGISTRATIONS_SHOWING_RESULTS_TEXT = (By.XPATH, "//div[@id='wgptx']/section[2]//p")

    BANS_HEADER = (By.XPATH, "//h2[@class='header__title___1itKA']/span[text()='Bans']")

    FIELD_LABEL = (By.XPATH, "//span[@class='drop_down__basicLabel___1R5CD' and text()='Field']")
    FIELD_INPUT = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirRow___29rUw components__flexAIFlexStart___2jEak']/div[1]/div/span/div/span[1]")
    FIELD_DROP_DOWN_LIST_ARROW = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirRow___29rUw components__flexAIFlexStart___2jEak']/div[1]/div/span/div/span[2]")
    FIELD_DROP_DOWN_LIST = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirRow___29rUw components__flexAIFlexStart___2jEak']/div[1]/div/span/div/ul/li")

    OPERATOR_LABEL = (By.XPATH, "//span[@class='drop_down__basicLabelDisabled___39o_t' and text()='Operator']")
    OPERATOR_INPUT = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirRow___29rUw components__flexAIFlexStart___2jEak']/div[2]/div/span/div/span[1]")
    OPERATOR_DROP_DOWN_LIST_ARROW = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirRow___29rUw components__flexAIFlexStart___2jEak']/div[2]/div/span/div/span[2]")

    VALUE_LABEL = (By.XPATH, "//span[@class='drop_down__basicLabel___1R5CD' and text()='Value']")
    VALUE_INPUT = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirRow___29rUw components__flexAIFlexStart___2jEak']/div[3]//span/div/span[1]")
    VALUE_DROP_DOWN_LIST_ARROW = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirRow___29rUw components__flexAIFlexStart___2jEak']/div[3]/div/span/div/span[2]")
    VALUE_DROP_DOWN_LIST = (By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirRow___29rUw components__flexAIFlexStart___2jEak']/div[3]/div/span/div/ul/li")

    CREATE_BAN_BUTTON = (By.XPATH, "//div[@id='wgptx']/section[3]//div//button[@label='Create']")
    FILTER_BUTTON = (By.XPATH, "//div[@id='wgptx']/section[3]//div//button[@label='Filter']")
    RESET_BUTTON = (By.XPATH, "//div[@id='wgptx']/section[3]//div//button[@label='Reset']")
    ADD_BUTTON = (By.XPATH, "//div[@id='wgptx']/section[3]//div//button[@label='Add']")

    BANS_SHOWING_RESULTS_TEXT = (By.XPATH, "//div[@id='wgptx']/section[3]/main/div/div/div[3]/div/p")

    BANS_TABLE_COLUMN_LIST = (By.XPATH, "//div[@id='wgptx']/section[3]//tr/th")
    NO_BANS_FOUND = (By.XPATH, "//td[@class='table__noDataCell___3pyjm']")

    @staticmethod
    def get_game_locator_by_name(name):
        """
        Get the locator for the player's game based on the name (Game Registrations table)
        :param name: Name of the game
        :type name: str
        :return: locator for the specific player's game
        :rtype: (By, str)
        """
        return By.ID, "table_cell_{}_game".format(name)

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
    def get_value_drop_down_list_status_locator_by_name(name):
        """
        Get the locator for the Status based on the name (in the Value column, after selecting Status from the Field)
        :param name: Name of the status
        :type name: str
        :return: locator for the status
        :rtype: (By, str)
        """
        return By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirRow___29rUw components__flexAIFlexStart___2jEak']/div[3]/div/span/div/ul/li/div/p[text()='{}']".format(
            name)

    @staticmethod
    def get_value_drop_down_list_game_locator_by_name(name):
        """
        Get the locator for the Game based on the name (in the Value column, after selecting Game from the Field)
        :param name: Name of the game
        :type name: str
        :return: locator for the game
        :rtype: (By, str)
        """
        return By.XPATH, "//div[@class='components__flex___3GCvy components__flexDirRow___29rUw components__flexAIFlexStart___2jEak']/div[3]/div/span/div/ul/li/div/p[text()='{}']".format(name)

    @staticmethod
    def get_bans_table_column_header_locator_by_name(name):
        """
        Get the locator for the specific table's column header based on the name
        :param name: Name of the column
        :type name: str
        :return: locator for the specific table's column header
        :rtype: (By, str)
        """
        return By.ID, 'column_heading_{}'.format(name)
