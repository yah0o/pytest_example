import time

import pytest
from hamcrest import *


class TestUserFlow(object):
    CODES = {
        'sg': {'JP': 'ja'},
        'ru': {'BY': 'be'},
        'us': {'US': 'en'},
        'eu': {'IT': 'it'}
    }

    @pytest.allure.feature('functional')
    @pytest.allure.story('monitoring')
    @pytest.mark.smoke
    @pytest.mark.skip(reason="Need to investigate failures but not actively being used")
    @pytest.mark.parametrize('title', ['twa'])
    def test_titles(self, config, title):
        login_response = config.freya.tools_gateway.login.auth_adfs_login(config.admin.username, config.admin.password)
        login_response.assert_is_success()

        # get title
        title_response = config.freya.tools_gateway.title.get_title('{}.{}'.format(config.environment['region'], title))
        title_response.assert_is_success()

        # get active catalog
        assert_that(title_response.content['title_versions'], not_(empty()))
        default_version = next((data for data in title_response.content['title_versions']['data'] if data['default']),
                               None)
        assert_that(default_version, not_none())
        assert_that(default_version['catalogs_activations'], not_(empty()))
        config.log.info('___catalog_activations___')
        config.log.info(default_version['catalogs_activations'])

        server_api_key = default_version['server_api_key']
        assert_that(server_api_key, not_none())
        config.log.info('___server_api_key___')
        config.log.info(server_api_key)

        activated_version = next((activation for activation in default_version['catalogs_activations'] if
                                  float(activation['active_at']) <= time.time()), None)
        assert_that(activated_version, not_none())
        active_catalog = activated_version['catalog']
        config.log.info('___active_catalog___')
        config.log.info(active_catalog)

        # get branch
        branch_response = config.freya.tools_gateway.title.branch('{}.{}'.format(config.environment['region'], title))
        branch_response.assert_is_success()
        branch_code = branch_response.content['data'][0]['branch_code']
        assert_that(branch_code, not_none())
        config.log.info('___branch_code___')
        config.log.info(branch_code)

        # get working catalog
        catalog_response = config.freya.tools_gateway.working_catalog.get_catalog(
            '{}.{}'.format(config.environment['region'], title), 'MAIN')
        catalog_response.assert_is_success()
        pub_version = catalog_response.content['pub_version']
        assert_that(pub_version, not_none())
        config.log.info('___pub_version___')
        config.log.info(pub_version)

        # get published catalog
        published_response = config.freya.tools_gateway.publish_catalog.get_published_version(
            '{}.{}'.format(config.environment['region'], title), 'MAIN', pub_version - 1)
        published_response.assert_is_success()

        # fetch product list
        fetch_response = config.freya.server_gateway(server_api_key).fetch_product_list('STOREFRONT_PSS', 0,
                                                                                        TestUserFlow.CODES.get(
                                                                                          config.environment[
                                                                                              'region']).keys(
                                                                                        )[0], TestUserFlow.CODES.get(
                config.environment['region']).values()[0], None, server_api_key)
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body'], has_key('uriList'))
        uri_list = fetch_response.content['body']['uriList']
        assert_that(len(uri_list) > 0)
        config.log.info('___uri_list___')
        config.log.info(uri_list)
