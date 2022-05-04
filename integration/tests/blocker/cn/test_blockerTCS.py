import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers.matchers import has_keys


@pytest.allure.feature('TCS')
@pytest.allure.story('title registry')
@pytest.allure.severity(severity_level.BLOCKER)
class TestTR(object):

    def test_get_title(self, config):
        title_response = config.freya.title_registry.get_titles()
        title_response.assert_is_success()

        assert_that(title_response.content, has_key('titles'))
        assert_that(title_response.content['titles'], not_none())

        titles = title_response.content['titles']
        test_title = next((title for title in titles if title['code'] == config.environment['integration_title']), None)
        assert_that(test_title, not_none())
        assert_that(test_title['code'], equal_to(config.environment['integration_title']))

    def test_get_currencies(self, config):
        currencies_response = config.freya.title_registry.get_currencies()
        currencies_response.assert_is_success()

        assert_that(currencies_response.content, has_key('data'))
        assert_that(currencies_response.content['data'], not_none())

        currencies = currencies_response.content['data']
        test_currency = next((currency for currency in currencies if
                              currency['code'] == '{}.{}'.format(
                                  config.environment['integration_title'],
                                  config.data.PREMIUM_BLOCKER_VC.VIRTUAL_CURRENCIES.TEST_CURRENCY.CODE
                              )), None)

        assert_that(test_currency, not_none())
        assert_that(test_currency, has_key('title'))
        assert_that(test_currency['title'], equal_to(config.environment['integration_title']))
        assert_that(test_currency, has_key('code'))
        assert_that(test_currency['code'], equal_to('{}.{}'.format(
            config.environment['integration_title'],
            config.data.PREMIUM_BLOCKER_VC.VIRTUAL_CURRENCIES.TEST_CURRENCY.CODE
        )))

    def test_get_namespaces(self, config):
        namespaces_response = config.freya.title_registry.get_namespaces()
        namespaces_response.assert_is_success()

        assert_that(namespaces_response.content, has_key('namespaces'))
        assert_that(namespaces_response.content['namespaces'], not_none())
        assert_that(namespaces_response.content, has_key('updated_at'))
        assert_that(namespaces_response.content['updated_at'], not_none())

    def test_get_components(self, config):
        components_response = config.freya.title_registry.get_components()
        components_response.assert_is_success()

        assert_that(components_response.content, has_key('resources'))
        assert_that(components_response.content['resources'], not_none())

        resources = components_response.content['resources']
        chat_resource = next((resource for resource in resources if
                              resource['component'] == 'chat'), None)

        assert_that(chat_resource, not_none())
        assert_that(chat_resource['component'], equal_to('chat'))
        assert_that(chat_resource, has_key('title'))
        assert_that(chat_resource, has_key('pgn'))
        assert_that(chat_resource, has_key('autospawn'))
        assert_that(chat_resource, has_key('bantypes'))

        game_resource = next((resource for resource in resources if
                              resource['component'] == 'game'), None)

        assert_that(game_resource, not_none())
        assert_that(game_resource['component'], equal_to('game'))
        assert_that(game_resource, has_key('title'))
        assert_that(game_resource, has_key('pgn'))
        assert_that(chat_resource, has_key('bantypes'))

    def test_get_entitlements_map(self, config):
        title_response = config.freya.title_registry.get_entitlements_map()
        title_response.assert_is_success()

        assert_that(title_response.content, has_key('data'))
        assert_that(title_response.content['data'], not_none())

        data = title_response.content['data']
        shared_entitlement = next((entitlement for entitlement in data
                                   if entitlement['title'] == config.environment['shared_entitlement']), None)
        assert_that(shared_entitlement, not_none())
        assert_that(shared_entitlement['title'], equal_to(config.environment['shared_entitlement']))

        entitlements = shared_entitlement['entitlements']
        shared_premium = next((entitlement for entitlement in entitlements if
                               entitlement['owner_title'] == config.environment['shared_entitlement']), None)
        assert_that(shared_premium, not_none())

    def test_get_entitlements(self, config):
        entitlements_response = config.freya.title_registry.get_entitlements()
        entitlements_response.assert_is_success()

        assert_that(entitlements_response.content, has_key('entitlements'))
        assert_that(entitlements_response.content['entitlements'], not_none())

        entitlements = entitlements_response.content['entitlements']
        test_entitlement = next((entitlement for entitlement in entitlements if
                                 entitlement['title_code'] == config.environment['shared_entitlement']), None)

        assert_that(test_entitlement, not_none())

    def test_get_currencies_map(self, config):
        currencies_response = config.freya.title_registry.get_currencies_virtual()
        currencies_response.assert_is_success()

        assert_that(currencies_response.content, has_key('data'))
        assert_that(currencies_response.content['data'], not_none())

        data = currencies_response.content['data']
        test_title = next((title for title in data if
                           title['title'] == config.environment['integration_title']), None)

        assert_that(test_title, has_key('currencies'))
        assert_that(test_title, has_key('title'))
        assert_that(test_title['title'], equal_to(config.environment['integration_title']))

        assert_that(test_title['currencies'], not_none())
        test_title_currencies = test_title['currencies']
        test_currency = next((currency for currency in test_title_currencies if
                              currency[
                                  'local_code'] == config.data.PREMIUM_BLOCKER_VC.VIRTUAL_CURRENCIES.TEST_CURRENCY.CODE),
                             None)

        assert_that(test_currency, not_none())
        assert_that(test_currency['local_code'],
                    equal_to(config.data.PREMIUM_BLOCKER_VC.VIRTUAL_CURRENCIES.TEST_CURRENCY.CODE))
        assert_that(test_currency, has_key('platform_code'))
        assert_that(test_currency['platform_code'], equal_to('{}.{}'.format(
            config.environment['integration_title'],
            config.data.PREMIUM_BLOCKER_VC.VIRTUAL_CURRENCIES.TEST_CURRENCY.CODE
        )))
        assert_that(test_currency, has_key('owner_title'))
        assert_that(test_currency['owner_title'], equal_to(config.environment['integration_title']))

    def test_get_currencies_real(self, config):
        currencies_response = config.freya.title_registry.get_currencies_real()
        currencies_response.assert_is_success()

        assert_that(currencies_response.content, has_key('data'))
        assert_that(currencies_response.content['data'], not_none())

        real_currencies = currencies_response.content['data']
        usd_currency = next((currency for currency in real_currencies if
                             currency['code'] == config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.CURRENCY_CODE), None)

        assert_that(usd_currency, not_none())
        assert_that(usd_currency['code'], equal_to(config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.CURRENCY_CODE))
        assert_that(usd_currency, has_key('decimal_places'))
        assert_that(usd_currency['decimal_places'], equal_to(2))
        assert_that(usd_currency, has_key('is_real'))
        assert_that(usd_currency, has_key('is_reported'))
        assert_that(usd_currency, has_key('title'))


@pytest.allure.feature('TCS')
@pytest.allure.story('title config service')
@pytest.allure.severity(severity_level.BLOCKER)
class TestTCS(object):

    def test_get_title(self, config):
        title_code = config.environment['integration_title']
        title_response = config.freya.title_config.get_titles(title_id_or_code=title_code)
        assert_that(title_response, not_none(), 'Title is empty')
        assert_that(title_response[0], has_keys('access', 'state', 'id', 'title_id',
                                                'friendly_name', 'pgn', 'pop', 'code',
                                                'created_at', 'updated_at', 'webhook_endpoint',
                                                'ggapi_discovery', 'ggapi_method', 'ggapi', 'webhook_gzip_accepted',
                                                'automatic_registration', 'internal', 'external_product_cdn',
                                                'enforce_prerequisites', 'event_schemas', 'document_schemas',
                                                'namespaces', 'title_versions', 'permitting_titles',
                                                'permitting_titles', 'type', 'public'))

    def test_get_titles(self, config):
        title_response = config.freya.title_config.get_all_titles()
        title_response.assert_is_success()
        assert_that(title_response.content['titles'], not_none(), 'Empty list of titles')

    def test_get_active_titles(self, config):
        title_response = config.freya.title_config.get_active_titles()
        title_response.assert_is_success()
        titles = title_response.content['titles']
        is_active = next((title for title in titles if title['title_versions'][0]['active'] is True), None)
        assert_that(is_active['title_versions'][0]['active'], equal_to(True), 'There are inactive titles in response')
