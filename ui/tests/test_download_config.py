import json
import os.path
import time

import pytest
from hamcrest import assert_that, equal_to, has_key

from ui.pages import CatalogTabs


@pytest.fixture
def setup(config, browser, steps):
    if config.store.headless or config.store.browser_name == 'safari':
        pytest.skip('Cannot download when Headless is True or browser is Safari')

    catalog_tabs_page = CatalogTabs(browser)

    steps.login(config.admin.username, config.admin.password)
    steps.navigate_to_titles_page(config.data.TEST_STUDIO.CODE)
    steps.navigate_to_catalogs_page(config.data.TEST_TITLE.CODE)
    steps.navigate_to_catalog_tabs_page(config.data.TEST_CATALOG.CODE)
    catalog_tabs_page.wait_for_page_load()

    config.store.path = '{}/WGPlatformCatalogConfig.json'.format(os.getcwd())

    yield catalog_tabs_page

    os.remove(config.store.path)


@pytest.allure.testcase("Validate that can download config")
def test_download_config(setup, config):
    catalog_tabs_page = setup

    catalog_tabs_page.click_download_config_button()

    if not os.path.exists(config.store.path):
        time.sleep(1)

    assert_that(os.path.isfile(config.store.path))

    with open(config.store.path, 'r') as download_file:
        data = json.load(download_file)

        assert_that(data, has_key('PlatformServerAPIKey'))
        assert_that(data['PlatformServerAPIKey'], equal_to(config.environment['api_key']))

        assert_that(data, has_key('PlatformGateway'))
        assert_that(
            data['PlatformGateway'],
            equal_to('http://platform-{}.sv4s.wgcrowd.io/'.format(config.environment['region']))
        )
