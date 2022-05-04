from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from locators import AddPricesToProductLocators
from ui.pages.base_page import BasePage
from ui.main.constants import DEFAULT_PAGE_TIMEOUT


class AddPricesToProduct(BasePage):
    def wait_for_page_load(self):
        """
        Wait for the page to load
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.presence_of_element_located(AddPricesToProductLocators.ADD_BUTTON),
            "'Add Prices to Product page' failed to load"
        )

    def get_prices_header(self):
        """
        Get the header for prices
        :return: Prices header
        :rtype: WebElement
        """
        return self.browser.find_element(*AddPricesToProductLocators.PRICES_HEADER)

    def get_money_header(self):
        """
        Get the header for the money
        :return: Money header
        :rtype: WebElement
        """
        return self.browser.find_element(*AddPricesToProductLocators.MONEY_HEADER)

    def get_money_toggle(self):
        """
        Get the toggle for the money
        :return: Money toggle
        :rtype: WebElement
        """
        return self.browser.find_element(*AddPricesToProductLocators.MONEY_TOGGLE)

    def click_money_toggle(self):
        """
        Click the money toggle
        """
        toggle = self.get_money_toggle()
        toggle.click()

    def get_virtual_money_label(self):
        """
        Get the label for Virtual Money
        :return: Virtual Money label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddPricesToProductLocators.VIRTUAL_MONEY_LABEL)

    def get_real_money_label(self):
        """
        Get the label for Real Money
        :return: Real Money label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddPricesToProductLocators.REAL_MONEY_LABEL)

    def get_currency_label(self):
        """
        Get the label for Currency Code
        :return: Currency Code label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddPricesToProductLocators.CURRENCY_CODE_LABEL)

    def get_currency_code_drop_down(self):
        """
        Get drop down for VC Currency Code
        :return: Currency Code drop down
        :rtype: WebElement
        """
        return self.browser.find_element(*AddPricesToProductLocators.VM_CURRENCY_CODE_DROP_DOWN)

    def get_currency_code_drop_down_list(self):
        """
        Get drop down list for VC Currency Code
        :return: Currency Code drop down list
        :rtype: WebElement
        """
        return self.browser.find_element(*AddPricesToProductLocators.VM_CURRENCY_CODE_DROP_DOWN_LIST)

    def get_currency_code_drop_down_arrow(self):
        """
        Get drop down arrow for VC Currency Code
        :return: Currency Code drop down arrow
        :rtype: WebElement
        """
        return self.browser.find_element(*AddPricesToProductLocators.VM_CURRENCY_CODE_DROP_DOWN_ARROW)

    def click_currency_code_drop_down(self):
        """
        Click the drop down menu for Currency Code
        """
        drop_down = self.get_currency_code_drop_down()
        drop_down.click()

    def get_currency_code_input(self):
        """
        Get input for RM Currency Code
        :return: Currency Code input
        :rtype: WebElement
        """
        return self.browser.find_element(*AddPricesToProductLocators.VM_CURRENCY_CODE_DROP_DOWN)

    def type_currency_code(self, value):
        """
        Type into Currency Code input
        :param value: Value want to type
        :type value: str
        """
        input_field = self.get_currency_code_input()
        input_field.send_keys(value)

    def get_pricing_type_label(self):
        """
        Get the label for Pricing Type
        :return: Pricing Type label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddPricesToProductLocators.PRICING_TYPE_LABEL)

    def get_pricing_type_drop_down(self):
        """
        Get the drop down menu for Pricing Type
        :return: Pricing Type drop down menu
        :rtype: WebElement
        """
        return self.browser.find_element(*AddPricesToProductLocators.PRICING_TYPE_DROP_DOWN)

    def click_pricing_type_drop_down(self):
        """
        Click the drop down menu for Pricing Type
        """
        drop_down = self.get_pricing_type_drop_down()
        drop_down.click()

    def wait_for_drop_down_option_load(self, name):
        """
        Wait for the Drop Down menu option to load
        :param name: Name of the option
        :type name: str
        """
        WebDriverWait(self.browser, DEFAULT_PAGE_TIMEOUT).until(
            expected_conditions.element_to_be_clickable(
                AddPricesToProductLocators.get_drop_down_option_locator_by_name(name)
            ),
            "'Drop Down menu' failed to load"
        )

    def get_drop_down_option_by_name(self, name):
        """
        Get the drop down option by its name
        :param name: Name of the option
        :type name: str
        :return: Drop Down option
        :rtype: WebElement
        """
        return self.browser.find_element(*AddPricesToProductLocators.get_drop_down_option_locator_by_name(name))

    def click_drop_down_option_by_name(self, name):
        """
        Click the drop down option
        :param name: Name of the option
        :type name: str
        """
        drop_down_option = self.get_drop_down_option_by_name(name)
        drop_down_option.click()

    def get_amount_label(self):
        """
        Get the label for Amount
        :return: Amount label
        :rtype: WebElement
        """
        return self.browser.find_element(*AddPricesToProductLocators.AMOUNT_LABEL)

    def get_amount_input(self):
        """
        Get the input for Amount
        :return: Amount input
        :rtype: WebElement
        """
        return self.browser.find_element(*AddPricesToProductLocators.AMOUNT_INPUT)

    def type_amount_input(self, value):
        """
        Type into the Amount input
        :param value: Value want to type into the iput
        :type value: str
        """
        input_field = self.get_amount_input()
        input_field.send_keys(value)

    def get_add_button(self):
        """
        Get the Add button
        :return: Add button
        :rtype: WebElement
        """
        return self.browser.find_element(*AddPricesToProductLocators.ADD_BUTTON)

    def click_add_button(self):
        """
        Click the Add button
        """
        button = self.get_add_button()
        button.click()

    def get_close_button(self):
        """
        Get the Close button
        :return:
        :rtype:
        """
        return self.browser.find_element(*AddPricesToProductLocators.CLOSE_BUTTON)

    def click_close_button(self):
        """
        Click the Close button
        """
        button = self.get_close_button()
        button.click()
