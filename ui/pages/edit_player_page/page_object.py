from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from locators import EditPlayerLocators
from ui.main.constants import DEFAULT_PAGE_TIMEOUT
from ui.pages.base_page import BasePage


class EditPlayer(BasePage):
    def wait_for_page_load(self):
        """
        Wait for the page to be fully loaded
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(EditPlayerLocators.CREATE_GAME_BUTTON),
            'Edit Player page failed to load'
        )

    def get_page_header(self):
        """
        Get the page header
        :return: page header
        :rtype: WebElement
        """
        return self.browser.find_element(*EditPlayerLocators.PAGE_HEADER)

    def click_page_header(self):
        """
        Click on the page header
        """
        page_title = self.get_page_header()
        page_title.click()

    def get_page_subheader(self):
        """
        Get the page subheader (player's realm and ID)
        :return: page subheader
        :rtype: WebElement
        """
        return self.browser.find_element(*EditPlayerLocators.PAGE_SUBHEADER)

    def get_id_label(self):
        """
        Get the label for the ID
        :return: label for the ID
        :rtype: WebElement
        """
        return self.browser.find_element(*EditPlayerLocators.ID_LABEL)

    def get_id_input(self):
        """
        Get ID input field
        :return: ID input field
        :rtype: WebElement
        """
        return self.browser.find_element(*EditPlayerLocators.ID_INPUT)

    def get_name_label(self):
        """
        Get the label for the Name
        :return: label for the Name
        :rtype: WebElement
        """
        return self.browser.find_element(*EditPlayerLocators.NAME_LABEL)

    def get_name_input(self):
        """
        Get Name input field
        :return: Name input field
        :rtype: WebElement
        """
        return self.browser.find_element(*EditPlayerLocators.NAME_INPUT)

    def get_realm_label(self):
        """
        Get the label for the Realm
        :return: label for the Realm
        :rtype: WebElement
        """
        return self.browser.find_element(*EditPlayerLocators.REALM_LABEL)

    def get_realm_input(self):
        """
        Get Realm input field
        :return: Realm input field
        :rtype: WebElement
        """
        return self.browser.find_element(*EditPlayerLocators.REALM_INPUT)

    def get_game_registrations_header(self):
        """
        Get the Game Registrations header
        :return: Game Registrations header
        :rtype: WebElement
        """
        return self.browser.find_element(*EditPlayerLocators.GAME_REGISTRATIONS_HEADER)

    def get_game_registrations_name_column(self):
        """
        Get the Game Registrations Name column
        :return: Game Registrations Name column
        :rtype: WebElement
        """
        return self.browser.find_element(*EditPlayerLocators.GAME_REGISTRATIONS_NAME_COLUMN)

    def get_game(self, name):
        """
        Get the registered game based on the name
        :param name: Name of the game
        :type name: str
        :return: the registered game
        :rtype: WebElement
        """
        return self.browser.find_element(*EditPlayerLocators.get_game_locator_by_name(name))

    def get_game_list(self):
        """
        Get the list of registered games
        :return: list of registered games
        :rtype: list of WebElement
        """
        return self.browser.find_elements(*EditPlayerLocators.GAME_LIST)

    def get_create_game_button(self):
        """
        Get the Create game button
        :return: Create game button
        :rtype: WebElement
        """
        return self.browser.find_element(*EditPlayerLocators.CREATE_GAME_BUTTON)

    def click_create_game_button(self):
        """
        Click the Create game button
        """
        button = self.get_create_game_button()
        button.click()

    def get_game_registrations_showing_results_text(self):
        """
        Get the "Showing results" text
        :return: "Showing results" text
        :rtype: WebElement
        """
        return self.browser.find_element(*EditPlayerLocators.GAME_REGISTRATIONS_SHOWING_RESULTS_TEXT)

    def get_bans_header(self):
        """
        Get the Bans header
        :return: Bans header
        :rtype: WebElement
        """
        return self.browser.find_element(*EditPlayerLocators.BANS_HEADER)

    def get_field_label(self):
        """
        Get the Field label
        :return: Field label
        :rtype: WebElement
        """
        return self.browser.find_element(*EditPlayerLocators.FIELD_LABEL)

    def get_field_input(self):
        """
        Get the Field input
        :return: Field input
        :rtype: WebElement
        """
        return self.browser.find_element(*EditPlayerLocators.FIELD_INPUT)

    def get_field_drop_down_list_arrow(self):
        """
        Get the Field drop down list arrow
        :return: Field drop down list arrow
        :rtype: WebElement
        """
        return self.browser.find_element(*EditPlayerLocators.FIELD_DROP_DOWN_LIST_ARROW)

    def click_field_drop_down_list_arrow(self):
        """
        Click the Field drop down list arrow
        """
        arrow = self.get_field_drop_down_list_arrow()
        arrow.click()

    def get_field_drop_down_list(self):
        """
        Get the Field drop down list
        :return: Field drop down list
        :rtype: WebElement
        """
        return self.browser.find_elements(*EditPlayerLocators.FIELD_DROP_DOWN_LIST)

    def get_field_drop_down_list_item(self, name):
        """
        Get the Field's drop down list item based on the name
        :param name: Name of the item
        :type name: str
        :return: Field's drop down list item
        :rtype: WebElement
        """
        return self.browser.find_element(*EditPlayerLocators.get_field_drop_down_list_item_locator_by_name(name))

    def click_field_drop_down_list_item(self, name):
        """
        Click the Field's drop down list item based on the name
        :param name: Name of the item
        :type name: str
        """
        list_item = self.get_field_drop_down_list_item(name)
        list_item.click()

    def get_operator_label(self):
        """
        Get the Operator label
        :return: Operator label
        :rtype: WebElement
        """
        return self.browser.find_element(*EditPlayerLocators.OPERATOR_LABEL)

    def get_operator_input(self):
        """
        Get the Operator input
        :return: Operator input
        :rtype: WebElement
        """
        return self.browser.find_element(*EditPlayerLocators.OPERATOR_INPUT)

    def get_operator_drop_down_list_arrow(self):
        """
        Get the Operator drop down list arrow
        :return: Operator drop down list arrow
        :rtype: WebElement
        """
        return self.browser.find_element(*EditPlayerLocators.OPERATOR_DROP_DOWN_LIST_ARROW)

    def get_value_label(self):
        """
        Get the Value label
        :return: Value label
        :rtype: WebElement
        """
        return self.browser.find_element(*EditPlayerLocators.VALUE_LABEL)

    def get_value_input(self):
        """
        Get the Value input
        :return: Value input
        :rtype: WebElement
        """
        return self.browser.find_element(*EditPlayerLocators.VALUE_INPUT)

    def type_value_input(self, value):
        """
        Type in the Value input
        :param value: value want to type
        :type value: str
        """
        input_field = self.get_value_input()
        input_field.send_keys(value)

    def click_value_input(self):
        """
        Click the Value input
        """
        input_field = self.get_value_input()
        input_field.click()

    def get_value_drop_down_list_arrow(self):
        """
        Get the Value drop down list arrow
        :return: Value drop down list arrow
        :rtype: WebElement
        """
        return self.browser.find_element(*EditPlayerLocators.VALUE_DROP_DOWN_LIST_ARROW)

    def click_value_drop_down_list_arrow(self):
        """
        Click the Value drop down list arrow
        """
        arrow = self.get_value_drop_down_list_arrow()
        arrow.click()

    def get_value_drop_down_list(self):
        """
        Get the Value drop down list
        :return: Value drop down list
        :rtype: WebElement
        """
        return self.browser.find_elements(*EditPlayerLocators.VALUE_DROP_DOWN_LIST)

    def get_status_value(self, name):
        """
        Get the ban status based on the name (in the Value column, after selecting Status item from the Field)
        :param name: Name of the status
        :type name: str
        :return: ban status
        :rtype: WebElement
        """
        return self.browser.find_element(*EditPlayerLocators.get_value_drop_down_list_status_locator_by_name(name))

    def click_status_value(self, name):
        """
        Click the ban status based on the name (in the Value column, after selecting Status item from the Field)
        :param name: Name of the status
        :type name: str
        """
        list_item = self.get_status_value(name)
        list_item.click()

    def get_game_value(self, name):
        """
        Get the game based on the name (in the Value column, after selecting Game item from the Field)
        :param name: Name of the game
        :type name: str
        :return: Name of the game
        :rtype: WebElement
        """
        return self.browser.find_element(*EditPlayerLocators.get_value_drop_down_list_game_locator_by_name(name))

    def click_game_value(self, name):
        """
        Click the game based on the name (in the Value column, after selecting Game item from the Field)
        :param name: Name of the game
        :type name: str
        """
        list_item = self.get_game_value(name)
        list_item.click()

    def get_create_ban_button(self):
        """
        Get the Create button (Bans table)
        :return: Create button
        :rtype: WebElement
        """
        return self.browser.find_element(*EditPlayerLocators.CREATE_BAN_BUTTON)

    def click_create_ban_button(self):
        """
        Click the Create button (Bans table)
        """
        button = self.get_create_ban_button()
        button.click()

    def get_filter_button(self):
        """
        Get the Filter button
        :return: Filter button
        :rtype: WebElement
        """
        return self.browser.find_element(*EditPlayerLocators.FILTER_BUTTON)

    def click_filter_button(self):
        """
        Click the Filter button
        """
        button = self.get_filter_button()
        button.click()

    def get_reset_button(self):
        """
        Get the Reset button
        :return: Reset button
        :rtype: WebElement
        """
        return self.browser.find_element(*EditPlayerLocators.RESET_BUTTON)

    def click_reset_button(self):
        """
        Click the Reset button
        """
        button = self.get_reset_button()
        button.click()

    def get_add_button(self):
        """
        Get the Add button
        :return: Add button
        :rtype: WebElement
        """
        return self.browser.find_element(*EditPlayerLocators.ADD_BUTTON)

    def click_add_button(self):
        """
        Click the Add button
        """
        button = self.get_add_button()
        button.click()

    def get_bans_showing_results_text(self):
        """
        Get the "Showing results" text
        :return: "Showing results" text
        :rtype: WebElement
        """
        return self.browser.find_element(*EditPlayerLocators.BANS_SHOWING_RESULTS_TEXT)

    def get_bans_table_column_list(self):
        """
        Get the list of table's column headers
        :return: list of table's column headers
        :rtype: list of WebElement
        """
        return self.browser.find_elements(*EditPlayerLocators.BANS_TABLE_COLUMN_LIST)

    def get_bans_table_column_header(self, name):
        """
        Get the specific table's column header based on the name
        :param name: Name of the column header
        :type name: str
        :return: specific column header
        :rtype: WebElement
        """
        return self.browser.find_element(*EditPlayerLocators.get_bans_table_column_header_locator_by_name(name))

    def get_no_bans_found(self):
        """
        Get the 'No Bans found' element (if no bans were created for the player)
        :return: 'No Players found' element
        :rtype: WebElement
        """
        return self.browser.find_element(*EditPlayerLocators.NO_BANS_FOUND)
