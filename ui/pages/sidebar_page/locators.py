from selenium.webdriver.common.by import By


class SidebarLocators(object):
    ACTIVITY_BUTTON = (By.ID, 'sidemenu_Activity')
    CATALOGS_BUTTON = (By.ID, 'sidemenu_Catalogs')
    DASHBOARD_BUTTON = (By.ID, 'sidemenu_Dashboard')
    PLAYERS_BUTTON = (By.ID, 'sidemenu_Players')
    REPORTS_BUTTON = (By.ID, 'sidemenu_Reports')
    SETTINGS_BUTTON = (By.ID, 'sidemenu_Settings')
    PANEL = (By.XPATH, "//div[@id='side_menu']//li")
    STUDIOS_BUTTON = (By.ID, 'sidemenu_Studios')
    TITLES_BUTTON = (By.ID, 'sidemenu_Titles')
    USERS_BUTTON = (By.ID, 'sidemenu_Users')
    ENVIRONMENTS_BUTTON = (By.ID, 'sidemenu_Environments')
    TITLE_COMPONENTS_BUTTON = (By.ID, 'sidemenu_Components')
    BACK_TO_TITLES_BUTTON = (By.ID, 'sidemenu_< Back to Titles')
    DATA_BUTTON = (By.ID, 'sidemenu_Data')
