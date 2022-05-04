from selenium.webdriver.common.by import By


class CatalogOverviewLocators(object):
    RECENT_ACTIVITY_TEXT = (By.ID, 'recent_activity_main_heading_text')
    RECENT_ACTIVITY_SUBHEADING_TEXT = (By.ID, 'recent_activity_sub_heading_text')
    SEE_ALL_ACTIVITY_LINK = (By.ID, 'see_all_activity_link')
    RECENT_ACTIVITY_DATE_COLUMN = (By.ID, 'column_heading_date')
    RECENT_ACTIVITY_NAME_COLUMN = (By.ID, 'column_heading_user_name')
    RECENT_ACTIVITY_ACTIVITY_COLUMN = (By.ID, 'column_heading_activity')
    ACTIVITY_LIST = (By.ID, 'table_body_recent_activity_table')

    STATUS_ACROSS_ENVIRONMENTS_TEXT = (By.ID, 'environments_status_main_heading_text')
    STATUS_SUBHEADING_TEXT = (By.ID, 'environments_status_sub_heading_text')
    SEE_ALL_CATALOGS_LINK = (By.ID, 'see_all_catalogs')
    STATUS_NAME_COLUMN = (By.ID, 'column_heading_environment_name')
    STATUS_LAST_PROMOTION_DATE_COLUMN = (By.ID, 'column_heading_last_promotion_date')
    STATUS_LIST = (By.ID, 'table_body_environments_status_table')
