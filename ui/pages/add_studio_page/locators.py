from selenium.webdriver.common.by import By


class AddStudioLocators(object):
    STUDIOS_TITLE = (By.ID, 'add_studio_heading')
    IMPORT_BUTTON = (By.ID, 'openImportStudio')
    ADD_BUTTON = (By.ID, 'openAddStudio')
    ADD_STUDIO_TITLE = (By.ID, 'add_studio_heading')
    NAME_LABEL = (By.ID, 'friendly_name_field_label')
    NAME_INPUT = (By.ID, 'friendly_name_field')
    CODE_LABEL = (By.ID, 'code_field_label')
    CODE_INPUT = (By.ID, 'code_field')
    CODE_INVALID_MESSAGE = (By.ID, 'code_field_invalid')
    STUDIO_CONTACT_LABEL = (By.ID, 'studio_contact_field_label')
    STUDIO_CONTACT_INPUT = (By.ID, 'studio_contact_field')
    STUDIO_CONTACT_INVALID_MESSAGE = (By.ID, 'studio_contact_field_invalid')
    WG_CONTACT_LABEL = (By.ID, 'wg_contact_field_label')
    WG_CONTACT_INPUT = (By.ID, 'wg_contact_field')
    WG_CONTACT_INVALID_MESSAGE = (By.ID, 'wg_contact_field_invalid')
    SAVE_BUTTON = (By.ID, 'add_studio_save_button')
    CANCEL_BUTTON = (By.ID, 'add_studio_cancel_button')
