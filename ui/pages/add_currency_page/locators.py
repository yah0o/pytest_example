from selenium.webdriver.common.by import By


class AddCurrencyLocators(object):
    ADD_CURRENCY_HEADER = (By.ID, 'add_currency_header')
    FRIENDLY_NAME_LABEL = (By.ID, 'friendly_name_input_label')
    FRIENDLY_NAME_INPUT = (By.ID, 'friendly_name_input')
    FRIENDLY_NAME_INVALID_MESSAGE = (By.ID, 'friendly_name_input_invalid')
    CODE_LABEL = (By.ID, 'code_input_label')
    CODE_INPUT = (By.ID, 'code_input')
    CODE_INVALID_MESSAGE = (By.ID, 'code_input_invalid')
    ACTIVE_HEADER = (By.ID, 'active_header')
    ACTIVE_TOGGLE = (By.ID, 'active_toggle')
    METADATA_HEADER = (By.ID, 'metadata_label')
    METADATA_TOGGLE = (By.ID, 'metadata_editor_toggle_toggle')
    METADATA_CHECKBOX = (By.ID, 'metadata_editor_toggle')
    METADATA_FIELD_EDITOR_LABEL = (By.ID, 'metadata_editor_toggle_labelLeft')
    METADATA_CODE_EDITOR_LABEL = (By.ID, 'metadata_editor_toggle_labelRight')
    TAGS_HEADER = (By.ID, 'tags_header')
    TAGS_INPUT = (By.ID, 'tags_drop_down')
    TAGS_DROP_DOWN_ARROW = (By.ID, 'icon_tags_drop_down')
    INCLUDE_CURRENCY_FIN_RPT_LABEL = (By.ID, 'reported_header')
    INCLUDE_CURRENCY_FIN_RPT_TOGGLE = (By.ID, 'reported_toggle')
    DECIMAL_REPORTED_FIN_RPT_LABEL = (By.ID, 'fraction_digit_count_input_label')
    DECIMAL_REPORTED_FIN_RPT_INPUT = (By.ID, 'fraction_digit_count_input')
    SAVE_BUTTON = (By.ID, 'add_currency_save_button')
    CANCEL_BUTTON = (By.ID, 'add_currency_cancel_button')