from selenium.webdriver.common.by import By


class EditStorefrontLocators(object):
    EDIT_STOREFRONT_HEADER = (By.ID, 'edit_storefront_header')

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

    METADATA_HEADER = (By.ID, 'metadata_label')
    METADATA_TOGGLE = (By.ID, 'metadata_editor_toggle_toggle')
    METADATA_CHECKBOX = (By.ID, 'metadata_editor_toggle')
    METADATA_FIELD_EDITOR_LABEL = (By.ID, 'metadata_editor_toggle_labelLeft')
    METADATA_CODE_EDITOR_LABEL = (By.ID, 'metadata_editor_toggle_labelRight')

    TAGS_HEADER = (By.ID, 'tags_header')
    TAGS_INPUT = (By.ID, 'tags_drop_down')
    TAGS_DROP_DOWN_ARROW = (By.ID, 'icon_tags_drop_down')

    PRODUCTS_HEADER = (By.ID, 'products_header')
    PRODUCT_ADD_BUTTON = (By.ID, 'products_add_button')
    PRODUCT_CODE_COLUMN = (By.ID, 'column_heading_product_code')
    PRODUCT_LIST = (By.ID, 'table_body_storefront_products_list')
    PRODUCT_DISPLAY_WEIGHT_COLUMN = (By.ID, 'column_heading_displayWeight')

    SAVE_AND_CLOSE_BUTTON = (By.ID, 'edit_storefront_save_close_button')
    SAVE_BUTTON = (By.ID, 'edit_storefront_save_button')
    CANCEL_BUTTON = (By.ID, 'edit_storefront_cancel_button')

    @staticmethod
    def get_product_locator_by_name(name):
        """
        Get the locator for the product based on the name (after adding a product to the storefront)
        :param name: Name of the Product
        :type name: str
        :return: locator for the specific product
        :rtype: (By, str)
        """
        return By.ID, "{}_displayCode".format(name)

    @staticmethod
    def get_product_display_weight_input_locator_by_name(name):
        """
        Get the locator for the display weight input based on the name (after adding a product to the storefront)
        :param name: Name of the Product
        :type name: str
        :return: locator for the product's display weight input
        :rtype: (By, str)
        """
        return By.ID, "{}_display_weight".format(name)

    @staticmethod
    def get_product_remove_button_locator_by_name(name):
        """
        Get the locator for the remove button based on the name (after adding a product to the storefront)
        :param name: Name of the Product
        :type name: str
        :return: locator for the product's remove button
        :rtype: (By, str)
        """
        return By.ID, "{}_remove".format(name)
