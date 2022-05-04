from selenium.webdriver.common.by import By


class AddTitleLocators(object):
    ADD_TITLE_TEXT = (By.ID, 'create_title_heading')
    NAME_LABEL = (By.ID, 'title_name_input_label')
    NAME_INPUT = (By.ID, 'title_name_input')
    CODE_LABEL = (By.ID, 'title_code_input_label')
    CODE_INPUT = (By.ID, 'title_code_input')
    CODE_INVALID_MESSAGE = (By.ID, 'title_code_input_invalid')
    CONTACT_LABEL = (By.ID, 'title_contact_input_label')
    CONTACT_INPUT = (By.ID, 'title_contact_input')
    SAVE_BUTTON = (By.ID, 'create_title_save')
    CANCEL_BUTTON = (By.ID, 'create_title_cancel')
    INVALID_EMAIL_MESSAGE = (By.ID, 'title_contact_input_invalid')
