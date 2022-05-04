from selenium.webdriver.common.by import By


class EditCurrencyLocators(object):
    EDIT_CURRENCY_HEADER = (By.ID, 'edit_currency_header')
    INFO_BOX = (By.ID, 'edit_currency_info_msg')

    BASIC_INFO = (By.XPATH, "//header[text()='Basic Information']")
    FRIENDLY_NAME_LABEL = (By.ID, 'friendly_name_label_div')
    FRIENDLY_NAME_INPUT = (By.ID, 'friendly_name_input')
    FRIENDLY_NAME_INVALID_MESSAGE = (By.ID, 'friendly_name_invalid')
    ACTIVE_HEADER = (By.ID, 'active_header')
    ACTIVE_TOGGLE = (By.ID, 'active_toggle')
    ACTIVE_CHECKBOX = (By.ID, 'active')
    INACTIVE_LABEL = (By.ID, 'active_labelLeft')
    ACTIVE_LABEL = (By.ID, 'active_labelRight')
    TAGS_HEADER = (By.ID, 'tags_header')
    TAGS_INPUT = (By.ID, 'tags_drop_down')

    PLATFORM_INFO = (By.XPATH, "//header[text()='Platform Information']")
    CODE_LABEL = (By.ID, 'code_label_div')
    CODE_INPUT = (By.ID, 'code_input')
    VERSION_LABEL = (By.ID, 'version_label_div')
    VERSION_INPUT = (By.ID, 'version_input')

    CURRENCY_SETTINGS = (By.XPATH, "//header[text()='Currency Settings']")
    REPORTED_HEADER = (By.ID, 'reported_header')
    REPORTED_TOGGLE = (By.ID, 'reported_toggle')
    REPORTED_CHECKBOX = (By.ID, 'reported')
    NOT_INCLUDED_LABEL = (By.ID, 'reported_labelLeft')
    INCLUDED_LABEL = (By.ID, 'reported_labelRight')
    PRICE_PRECISION_LABEL = (By.ID, 'fraction_digit_count_label_div')
    PRICE_PRECISION_INPUT = (By.ID, 'fraction_digit_count_input')
    PRICE_PRECISION_INVALID_MESSAGE = (By.ID, 'fraction_digit_count_invalid')

    CUSTOM_DATA = (By.XPATH, "//header[text()='Custom Data']")
    METADATA_LABEL = (By.ID, 'metadata_label')
    METADATA_TOGGLE = (By.ID, 'metadata_editor_toggle_toggle')
    METADATA_CHECKBOX = (By.ID, 'metadata_editor_toggle')
    FIELD_EDITOR_LABEL = (By.ID, 'metadata_editor_toggle_labelLeft')
    CODE_EDITOR_LABEL = (By.ID, 'metadata_editor_toggle_labelRight')

    SAVE_AND_CLOSE_BUTTON = (By.ID, 'edit_currency_save_close_button')
    SAVE_BUTTON = (By.ID, 'edit_currency_save_button')
    CANCEL_BUTTON = (By.ID, 'edit_currency_cancel_button')
