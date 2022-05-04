from selenium.webdriver.common.by import By


class AddPricesToProductLocators(object):
    PRICES_HEADER = (By.ID, 'prices_header')
    MONEY_HEADER = (By.ID, 'prices_real_money_header')
    MONEY_TOGGLE = (By.ID, 'prices_type_toggle')
    VIRTUAL_MONEY_LABEL = (By.ID, 'prices_real_money_labelLeft')
    REAL_MONEY_LABEL = (By.ID, 'prices_real_money_labelRight')
    CURRENCY_CODE_LABEL = (By.XPATH, "prices_code_header")
    VM_CURRENCY_CODE_DROP_DOWN = (By.ID, 'prices_code')
    VM_CURRENCY_CODE_DROP_DOWN_LIST = (By.XPATH, "//ul[@class='drop_down__hidden___1utMy__1555095325341 drop_down__list___2aGdv__1555095325341 drop_down__bottom___3cEOL__1555095325341']")
    VM_CURRENCY_CODE_DROP_DOWN_ARROW = (By.ID, 'icon_prices_code')
    RM_CURRENCY_CODE_INPUT = (By.ID, 'prices_code_input')
    PRICING_TYPE_LABEL = (By.XPATH, "//div[@class='create_entity_form__pricingType___3nuwY' and text()='Pricing type:']")
    PRICING_TYPE_DROP_DOWN = (By.ID, 'prices_qty_pricing_type')
    AMOUNT_LABEL = (By.XPATH, "prices_amount_label_div")
    AMOUNT_INPUT = (By.ID, 'prices_amount_input')
    ADD_BUTTON = (By.XPATH, "//button[@label='Add']")
    CLOSE_BUTTON = (By.XPATH, "//button[@label='Close']")

    @staticmethod
    def get_drop_down_option_locator_by_name(name):
        """
        Get the locator of the drop down option in the drop down list
        :param name: name of the option
        :type name: str
        :return: locator for the specific option in the drop down menu
        :rtype: (By, str)
        """
        return By.ID, "{}_option".format(name)
