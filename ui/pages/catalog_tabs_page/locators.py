from selenium.webdriver.common.by import By


class CatalogTabsLocators(object):
    CATALOG_TITLE = (By.ID, 'catalog_top_bar_heading')
    SECONDARY_HEADING = (By.ID, 'catalog_top_bar_sub_heading')
    DOWNLOAD_CONFIG_BUTTON = (By.ID, 'download_config_button')
    PUBLISH_BUTTON = (By.ID, 'publish_button')

    OVERVIEW_TAB = (By.ID, 'tab_Overview')
    STOREFRONTS_TAB = (By.ID, 'tab_Storefronts')
    PRODUCTS_TAB = (By.ID, 'tab_Products')
    ENTITLEMENTS_TAB = (By.ID, 'tab_Entitlements')
    CURRENCIES_TAB = (By.ID, 'tab_Currencies')
    CAMPAIGNS_TAB = (By.ID, 'tab_Campaigns')
    ACTIVITY_TAB = (By.ID, 'tab_Activity')
    TAB_LIST = (By.XPATH, "//div[@id='tab_tab_list']/div")
