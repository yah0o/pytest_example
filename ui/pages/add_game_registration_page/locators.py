from selenium.webdriver.common.by import By


class AddGameRegistrationLocators(object):
    PAGE_HEADER = (By.XPATH, "//h1[@class='header__title___1itKA']/span[1]/a")
    PAGE_SUBHEADER_1 = (By.XPATH, "//h1[@class='header__title___1itKA']/span[2]/a")
    PAGE_SUBHEADER_2 = (By.XPATH, "//h1[@class='header__title___1itKA']/span[3]/span")

    WGID_LABEL = (By.XPATH, "//div[@class='text_field__header___biqb4']")
    WGID_INPUT = (By.XPATH, "//label[@class='text_field__textFieldLabel___2LncU']/span/input")

    REALM_LABEL = (By.XPATH, "//span[@class='drop_down__basicLabelDisabled___39o_t']")
    REALM_INPUT = (By.XPATH, "//div[@id='wgptx']//main/div[2]/div[2]/div/div/span/div/span[1]")
    REALM_DROP_DOWN_LIST_ARROW = (By.XPATH, "//div[@id='wgptx']//main/div[2]/div[2]/div/div/span/div/span[2]")

    GAME_LABEL = (By.XPATH, "//div[@id='wgptx']//main/div[2]/div[3]/div/div/div/span")
    GAME_INPUT = (By.XPATH, "//div[@id='wgptx']//main/div[2]/div[3]/div/div/span/div/span[1]")
    GAME_DROP_DOWN_LIST_ARROW = (By.XPATH, "//div[@id='wgptx']//main/div[2]/div[3]/div/div/span/div/span[2]")
    GAME_DROP_DOWN_LIST = (By.XPATH, "//div[@id='wgptx']//main/div[2]/div[3]/div/div/span/div/ul/li")

    SAVE_BUTTON = (By.XPATH, "//button[@label='Save']")
    CANCEL_BUTTON = (By.XPATH, "//button[@label='Cancel']")

    @staticmethod
    def get_game_drop_down_list_item_locator_by_name(name):
        """
        Get the locator for the Games's drop down list item based on the name
        :param name: Name of the game
        :type name: str
        :return: locator for the Games's drop down list item
        :rtype: (By, str)
        """
        return By.XPATH, "//div[@id='wgptx']//main/div[2]/div[3]/div/div/span/div/ul/li/div/p[text()='{}']".format(name)
