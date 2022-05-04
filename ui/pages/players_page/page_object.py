from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from locators import PlayerLocators
from ui.main.constants import DEFAULT_PAGE_TIMEOUT
from ui.pages.base_page import BasePage
from ui.main.expected_conditions.expected_conditions import get_player_list


class Players(BasePage):
    def wait_for_page_load(self):
        """
        Wait for the page to be fully loaded
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(PlayerLocators.CREATE_BUTTON),
            'Players page failed to load'
        )

    def wait_for_info_box_to_disappear(self):
        """
        Make sure the info box is not present after info box exit button was clicked
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.invisibility_of_element_located(PlayerLocators.INFO_BOX),
            'Info box exit button was clicked but info box is still present'
        )

    def wait_for_validation_box(self):
        """
        Make sure the validation box is present after the tag exit button was clicked
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(PlayerLocators.VALIDATION_BOX),
            "Validation box didn't appear"
        )

    def wait_for_validation_box_to_disappear(self):
        """
        Make sure the validation box is not present after validation box exit button was clicked
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.invisibility_of_element_located(PlayerLocators.VALIDATION_BOX),
            'Validation box exit button was clicked but validation box is still present'
        )

    def wait_for_field_list_item_to_be_clickable(self, name):
        """
        Wait for the the list item to be clickable
        :param name: Name of the item
        :type name: str
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.element_to_be_clickable(
                PlayerLocators.get_field_drop_down_list_item_locator_by_name(name)),
            "Field's list item is not clickable"
        )

    def wait_for_value_realm_item_to_be_clickable(self, name):
        """
        Wait for the the list item to be clickable
        :param name: Name of the item
        :type name: str
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.element_to_be_clickable(
                PlayerLocators.get_value_drop_down_list_realm_locator_by_name(name)),
            "Value's realm item is not clickable"
        )

    def wait_for_value_game_item_to_be_clickable(self, name):
        """
        Wait for the the list item to be clickable
        :param name: Name of the item
        :type name: str
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.element_to_be_clickable(
                PlayerLocators.get_value_drop_down_list_game_locator_by_name(name)),
            "Value's game item is not clickable"
        )

    def wait_for_player_list_load(self):
        """
        Wait for the player list to be fully loaded
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            get_player_list(PlayerLocators.PLAYER_LIST, PlayerLocators.ADD_BUTTON, 5),
            'Players were not created or not all players were created'
        )

    def get_page_header(self):
        """
        Get the page header
        :return: page header
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.PAGE_HEADER)

    def get_create_button(self):
        """
        Get the create button
        :return: create button
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.CREATE_BUTTON)

    def click_create_button(self):
        """
        Click the create button
        """
        button = self.get_create_button()
        button.click()

    def get_create_bulk_button(self):
        """
        Get the create bulk button
        :return: create bulk button
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.CREATE_BULK_BUTTON)

    def click_create_bulk_button(self):
        """
        Click the create bulk button
        """
        button = self.get_create_bulk_button()
        button.click()

    def get_info_box(self):
        """
        Get the info box
        :return: info box
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.INFO_BOX)

    def get_info_box_exit_button(self):
        """
        Get the info box exit button
        :return: info box exit button
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.INFO_BOX_EXIT_BUTTON)

    def click_info_box_exit_button(self):
        """
        Click the info box exit button
        """
        button = self.get_info_box_exit_button()
        button.click()

    def get_info_box_strong(self):
        """
        Get the info box strong element
        :return: info box strong element
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.INFO_BOX_STRONG)

    def get_validation_box(self):
        """
        Get the validation box
        :return: validation box
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.VALIDATION_BOX)

    def get_validation_box_exit_button(self):
        """
        Get the validation box exit button
        :return: validation box exit button
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.VALIDATION_BOX_EXIT_BUTTON)

    def click_validation_box_exit_button(self):
        """
        Click the validation box exit button
        """
        button = self.get_validation_box_exit_button()
        button.click()

    def get_validation_box_name_strong(self):
        """
        Get the validation box Name strong element
        :return: validation box Name strong element
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.VALIDATION_BOX_NAME_STRONG)

    def get_validation_box_realm_strong(self):
        """
        Get the validation box Realm strong element
        :return: validation box Realm strong element
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.VALIDATION_BOX_REALM_STRONG)

    def get_validation_box_game_strong(self):
        """
        Get the validation box Game strong element
        :return: validation box Game strong element
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.VALIDATION_BOX_GAME_STRONG)

    def get_field_label(self):
        """
        Get the Field label
        :return: Field label
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.FIELD_LABEL)

    def get_field_input(self):
        """
        Get the Field input
        :return: Field input
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.FIELD_INPUT)

    def click_field_input(self):
        """
        Click the Field input
        """
        input = self.get_field_input()
        input.click()

    def get_field_drop_down_list_arrow(self):
        """
        Get the Field drop down list arrow
        :return: Field drop down list arrow
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.FIELD_DROP_DOWN_LIST_ARROW)

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
        return self.browser.find_elements(*PlayerLocators.FIELD_DROP_DOWN_LIST)

    def get_field_drop_down_list_item(self, name):
        """
        Get the Field's drop down list item based on the name
        :param name: Name of the item
        :type name: str
        :return: Field's drop down list item
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.get_field_drop_down_list_item_locator_by_name(name))

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
        return self.browser.find_element(*PlayerLocators.OPERATOR_LABEL)

    def get_operator_input(self):
        """
        Get the Operator input
        :return: Operator input
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.OPERATOR_INPUT)

    def get_operator_drop_down_list_arrow(self):
        """
        Get the Operator drop down list arrow
        :return: Operator drop down list arrow
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.OPERATOR_DROP_DOWN_LIST_ARROW)

    def get_value_label(self):
        """
        Get the Value label
        :return: Value label
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.VALUE_LABEL)

    def get_value_input(self):
        """
        Get the Value input
        :return: Value input
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.VALUE_INPUT)

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
        return self.browser.find_element(*PlayerLocators.VALUE_DROP_DOWN_LIST_ARROW)

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
        return self.browser.find_elements(*PlayerLocators.VALUE_DROP_DOWN_LIST)

    def get_realm(self, name):
        """
        Get the realm based on the name (in the Value column, after selecting Realm item from the Field)
        :param name: Name of the realm
        :type name: str
        :return: realm element
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.get_value_drop_down_list_realm_locator_by_name(name))

    def click_realm(self, name):
        """
        Click the realm based on the name (in the Value column, after selecting Realm item from the Field)
        :param name: Name of the realm
        :type name: str
        """
        list_item = self.get_realm(name)
        list_item.click()

    def get_game(self, name):
        """
        Get the Game based on the name (in the Value column, after selecting Game item from the Field)
        :param name: Name of the game
        :type name: str
        :return: game element
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.get_value_drop_down_list_game_locator_by_name(name))

    def click_game(self, name):
        """
        Click the Game based on the name (in the Value column, after selecting Game item from the Field)
        :param name: Name of the game
        :type name: str
        """
        list_item = self.get_game(name)
        list_item.click()

    def get_name_tag(self):
        """
        Get the Name tag
        :return: Name tag
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.NAME_TAG)

    def get_name_tag_exit_button(self):
        """
        Get the Name tag exit button
        :return: Name tag exit button
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.NAME_TAG_EXIT_BUTTON)

    def click_name_tag_exit_button(self):
        """
        Click the Name tag exit button
        """
        button = self.get_name_tag_exit_button()
        button.click()

    def get_realm_tag(self):
        """
        Get the Realm tag
        :return: Realm tag
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.REALM_TAG)

    def get_realm_tag_exit_button(self):
        """
        Get the Realm tag exit button
        :return: Realm tag exit button
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.REALM_TAG_EXIT_BUTTON)

    def click_realm_tag_exit_button(self):
        """
        Click the Realm tag exit button
        """
        button = self.get_realm_tag_exit_button()
        button.click()

    def get_game_tag(self):
        """
        Get the Game tag
        :return: Game tag
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.GAME_TAG)

    def get_game_tag_exit_button(self):
        """
        Get the Game tag exit button
        :return: Game tag exit button
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.GAME_TAG_EXIT_BUTTON)

    def click_game_tag_exit_button(self):
        """
        Click the Game tag exit button
        """
        button = self.get_game_tag_exit_button()
        button.click()

    def get_add_button(self):
        """
        Get the Add button
        :return: Add button
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.ADD_BUTTON)

    def click_add_button(self):
        """
        Click the Add button
        """
        button = self.get_add_button()
        button.click()

    def get_filter_button(self):
        """
        Get the Filter button
        :return: Filter button
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.FILTER_BUTTON)

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
        return self.browser.find_element(*PlayerLocators.RESET_BUTTON)

    def click_reset_button(self):
        """
        Click the Reset button
        """
        button = self.get_reset_button()
        button.click()

    def get_showing_results_text(self):
        """
        Get the "Showing results" text
        :return: "Showing results" text
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.SHOWING_RESULTS_TEXT)

    def get_table_column_list(self):
        """
        Get the list of table's column headers
        :return: list of table's column headers
        :rtype: list of WebElement
        """
        return self.browser.find_elements(*PlayerLocators.TABLE_COLUMN_LIST)

    def get_table_column_header(self, name):
        """
        Get the specific table's column header based on the name
        :param name: Name of the column
        :type name: str
        :return: specific table's column header
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.get_table_column_header_locator_by_name(name))

    def get_player_list(self):
        """
        Get the list of players
        :return: list of players
        :rtype: list of WebElement
        """
        return self.browser.find_elements(*PlayerLocators.PLAYER_LIST)

    def get_no_players_found(self):
        """
        Get the 'No Players found' element (e.g. after all tags were removed)
        :return: 'No Players found' element
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.NO_PLAYERS_FOUND)

    def get_player_id(self, name):
        """
        Get the specific player's id based on the name
        :param name: name of the player
        :type name: str
        :return: specific player's id
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.get_table_id_locator_by_name(name))

    def click_player_id(self, name):
        """
        Click the specific player's id based on the name
        :param name: name of the player
        :type name: str
        """
        button = self.get_player_id(name)
        button.click()

    def get_player_name(self, name):
        """
        Get the specific player's name based on the name
        :param name: name of the player
        :type name: str
        :return: specific player's name
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.get_table_name_locator_by_name(name))

    def get_player_realm(self, name):
        """
        Get the specific player's realm based on the name
        :param name: name of the player
        :type name: str
        :return: specific player's realm
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.get_table_realm_locator_by_name(name))

    def get_player_game(self, name):
        """
        Get the specific player's game based on the name
        :param name: name of the player
        :type name: str
        :return: specific player's game
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.get_table_game_locator_by_name(name))

    def get_player_actions_button(self, name):
        """
        Get the specific player's actions button based on the name
        :param name: name of the player
        :type name: str
        :return: specific player's actions button
        :rtype: WebElement
        """
        return self.browser.find_element(*PlayerLocators.get_table_actions_button_locator_by_name(name))

    def click_player_actions_button(self, name):
        """
        Click the specific player's actions button based on the name
        :param name: name of the player
        :type name: str
        """
        button = self.get_player_actions_button(name)
        button.click()
