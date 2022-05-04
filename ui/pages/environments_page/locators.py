from selenium.webdriver.common.by import By


class EnvironmentsLocators(object):
    ENVIRONMENTS_TITLE = (By.ID, 'environments_top_bar_heading')
    ENVIRONMENTS_SUBHEADING = (By.ID, 'environments_top_bar_sub_heading_top')
    DETAILS_HEADING = (By.ID, 'details_header')
    DETAILS_STATUS = (By.ID, 'details_sub_header')
    DETAILS_CATALOGS_LIST = (By.ID, 'details_list')
    DETAILS_CATALOGS_HEADER = (By.ID, 'details_catalog_list_header')
    DETAILS_LAST_PUBLISHED_BUTTON = (By.XPATH, "//button[@class='diagram__orderButton___1VIoW']")
    DETAILS_CLOSE_BUTTON = (By.XPATH, "//button[@class='diagram__closeButton___3gQpB']")

    @staticmethod
    def get_realm_box_locator_by_name(name):
        """
        Get the locator for the realm box based on the display name
        :param name: realm name shown on the box
        :type name: str
        :return: locator for the realm's box
        :rtype: (By, str)
        """
        return By.ID, "box_{}".format(name)

    @staticmethod
    def get_realm_heading_locator_by_name(name):
        """
        Get the locator for the realm heading based on the display name
        :param name: realm name shown on the box
        :type name: str
        :return: locator for the realm's heading on the box
        :rtype: (By, str)
        """
        return By.ID, "heading_span_{}".format(name)

    @staticmethod
    def get_realm_status_locator_by_name(name):
        """
        Get the locator for the realm status based on the display name
        :param name: realm name shown on the box
        :type name: str
        :return: locator for the realm's status on the box
        :rtype: (By, str)
        """
        return By.ID, "subheading_server_status_{}".format(name)

    @staticmethod
    def get_realm_last_published_span_locator_by_name(name):
        """
        Get the locator for the realm last published span
        :param name: realm name
        :type name: str
        :return: locator for the realm's last published span on the box
        :rtype: (By, str)
        """
        return By.ID, 'subheading_span_last_published_{}'.format(name)

    @staticmethod
    def get_realm_last_published_catalog_by_name(realm, catalog_code):
        """
        Get the locator for the realm last published catalog
        :param realm: realm name
        :type realm: str
        :param catalog_code: name of the catalog
        :type catalog_code: str
        :return: locator of the last published catalog for the realm
        :rtype: (By, str)
        """
        return By.ID, 'subheading_code_{}_{}'.format(catalog_code, realm)

    @staticmethod
    def get_realm_last_published_catalog_title_by_name(realm, catalog_code):
        """
        Get the locator for the realm last published catalog's title
        :param realm: realm name
        :type realm: str
        :param catalog_code: name of the catalog
        :type catalog_code: str
        :return: locator of the last published catalog's title for the realm
        :rtype: (By, str)
        """
        return By.ID, 'subheading_title_{}_{}'.format(catalog_code, realm)

    @staticmethod
    def get_realm_no_published_catalog_by_name(realm):
        """
        Get the locator for the realm no published catalog span
        :param realm: realm name
        :type realm: str
        :return: locator of the no published catalog span
        :rtype: (By, str)
        """
        return By.ID, 'subheading_span_no_catalogs_{}'.format(realm)

    @staticmethod
    def get_details_catalog_by_name(catalog_code, publish_version, index):
        """
        Get the locator for a specific details table catalog
        :param catalog_code: name of the catalog
        :type catalog_code: str
        :param publish_version: publish version of the catalog
        :type publish_version: int
        :param index: row of the details table
        :type index: int
        :return: locator of a catalog in the details table list
        :rtype: (By, str)
        """
        return By.ID, 'subheading_code_{}_{}_{}'.format(catalog_code, index, publish_version)

    @staticmethod
    def get_details_catalog_title_by_name(catalog_code, publish_version):
        """
        Get locator for a specific details table catalog's table
        :param catalog_code: name of the catalog
        :type catalog_code: str
        :param publish_version: publish version of the catalog
        :type publish_version: int
        :return: locator of a catalog's title in the details table list
        :rtype: (By, str)
        """
        return By.ID, 'subheading_title_{}_{}'.format(catalog_code, publish_version)

    @staticmethod
    def get_details_catalog_actions_menu_by_name(catalog_code, publish_version, index):
        """
        Get the locator for a specific details table catalog's actions menu
        :param catalog_code: name of the catalog
        :type catalog_code: str
        :param publish_version: publish version of the catalog
        :type publish_version: int
        :param index: row of the details table
        :type index: int
        :return: locator of a catalog's actions menu in the details table list
        :rtype: (By, str)
        """
        return By.ID, 'menu_catalog_{}_{}_{}_toggle_menu'.format(catalog_code, index, publish_version)
