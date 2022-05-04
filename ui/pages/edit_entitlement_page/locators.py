from selenium.webdriver.common.by import By


class EditEntitlementLocators(object):
    EDIT_ENTITLEMENT_HEADER = (By.ID, 'edit_entitlement_header')
    FRIENDLY_NAME_LABEL = (By.ID, 'friendly_name_input_label')
    FRIENDLY_NAME_INPUT = (By.ID, 'friendly_name_input')
    FRIENDLY_NAME_INVALID_MESSAGE = (By.ID, 'friendly_name_input_invalid')
    CODE_LABEL = (By.ID, 'code_input_label')
    CODE_INPUT = (By.ID, 'code_input')
    VERSION_LABEL = (By.ID, 'version_input_label')
    VERSION_INPUT = (By.ID, 'version_input')
    ACTIVE_HEADER = (By.ID, 'active_header')
    ACTIVE_TOGGLE = (By.ID, 'active_toggle')
    ACTIVE_CHECKBOX = (By.ID, 'active')
    INACTIVE_LABEL = (By.ID, 'active_labelLeft')
    ACTIVE_LABEL = (By.ID, 'active_labelRight')
    METADATA_HEADER = (By.ID, 'metadata_label')
    METADATA_TOGGLE = (By.ID, 'metadata_editor_toggle_toggle')
    METADATA_CHECKBOX = (By.ID, 'metadata_editor_toggle')
    METADATA_FIELD_EDITOR_LABEL = (By.ID, 'metadata_editor_toggle_labelLeft')
    METADATA_CODE_EDITOR_LABEL = (By.ID, 'metadata_editor_toggle_labelRight')
    TAGS_HEADER = (By.ID, 'tags_header')
    TAGS_INPUT = (By.ID, 'tags_drop_down')
    TAGS_DROP_DOWN_ARROW = (By.ID, 'icon_tags_drop_down')
    SAVE_AND_CLOSE_BUTTON = (By.ID, 'edit_entitlement_save_close_button')
    SAVE_BUTTON = (By.ID, 'edit_entitlement_save_button')
    CANCEL_BUTTON = (By.ID, 'edit_entitlement_cancel_button')
