import uuid

import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities
from integration.main.services import LegacyProductItem


@pytest.mark.skip_for_regions('trie', 'nps11')
@pytest.allure.feature('functional')
@pytest.allure.story('spa access')
class TestSpaAccess(object):

    @pytest.fixture(autouse=True)
    def setup(self, config):
        ###
        # Test setup

        config.store.account = AccountUtilities.create_account(attrs='user_stated_country=ZZ')

        account_created = config.spa.http.create_account(config.store.account.__dict__)
        account_created.assert_is_success()
        update_account = config.spa.http.update(account_created.content['id'],
                                                game=config.environment['test_title_pgn'])
        update_account.assert_is_success()

        config.store.profile_id = account_created.content['id']
        config.store.wgid = account_created.content['id']

        title_response = config.freya.title_config.get_titles(config.environment['no_access_1_title'])

        config.store.api_key = next((tv['server_api_key'] for tv in title_response[0]['title_versions'] if
                                     tv['active'] is True and tv['default'] is True), None)

        assert_that(config.store.api_key, not_none())

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(config.store.wgid)
        delete_response.assert_is_success()

    @pytest.mark.skip_for_regions('wgt1', 'trie', 'wgs11', 'nps11')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_spa_access_should_fail_when_granting_access_product_with_missed_game(self, config):
        # Should be failed cause no spa access on that product
        first_auth_response = config.freya.auth_gateway(config.store.api_key).login_with_email(
            config.store.account.email,
            config.store.account.password)
        first_auth_response.assert_is_success()

        assert_that(first_auth_response.content['body']['allowed'], equal_to(False))

        grant_product_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_SPA_PRODUCT.COUNTRY,
            config.data.TEST_SPA_PRODUCT.LANGUAGE,
            config.store.wgid,
            [LegacyProductItem(config.data.TEST_SPA_PRODUCT.CODE, config.data.TEST_SPA_PRODUCT.AMOUNT)]
        )
        grant_product_response.assert_is_success()

        second_auth_response = config.freya.auth_gateway(config.store.api_key).login_with_email(
            config.store.account.email,
            config.store.account.password)
        second_auth_response.assert_is_success()

        assert_that(second_auth_response.content['body']['allowed'], equal_to(False))

    @pytest.mark.skip_for_regions('wgt1', 'trie', 'wgs11', 'nps1', 'nps11')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_spa_access_should_succeed_when_granting_access_product_to_user_who_already_has_this_access_product(
            self,
            config
    ):
        # Should be failed cause no spa access on that product
        first_auth_response = config.freya.auth_gateway.login_with_email(
            config.store.account.email,
            config.store.account.password)
        first_auth_response.assert_is_success()

        assert_that(first_auth_response.content['body']['allowed'], equal_to(True))

        grant_product_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_SPA_PRODUCT.COUNTRY,
            config.data.TEST_SPA_PRODUCT.LANGUAGE,
            config.store.wgid,
            [LegacyProductItem(config.data.TEST_SPA_PRODUCT.CODE, config.data.TEST_SPA_PRODUCT.AMOUNT)]
        )
        grant_product_response.assert_is_success()

        second_auth_response = config.freya.auth_gateway(config.store.api_key).login_with_email(
            config.store.account.email,
            config.store.account.password)
        second_auth_response.assert_is_success()

        assert_that(second_auth_response.content['body']['allowed'], equal_to(False))

    @pytest.mark.skip(reason='spa-ordo issue')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_spa_access_to_not_allowed_title_should_not_change_when_granting_access_to_different_title(self, config):
        title_response_2 = config.freya.title_config.get_titles(config.environment['no_access_2_title'])

        api_key_2 = next((tv['server_api_key'] for tv in title_response_2[0]['title_versions'] if
                          tv['active'] is True and tv['default'] is True), None)

        assert_that(api_key_2, not_none())

        first_auth_response = config.freya.auth_gateway(api_key_2).login_with_email(
            config.store.account.email,
            config.store.account.password)
        first_auth_response.assert_is_success()

        assert_that(first_auth_response.content['body']['allowed'], equal_to(False))

        grant_product_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_SPA_PRODUCT.COUNTRY,
            config.data.TEST_SPA_PRODUCT.LANGUAGE,
            config.store.wgid,
            [LegacyProductItem(config.data.TEST_SPA_PRODUCT.CODE, config.data.TEST_SPA_PRODUCT.AMOUNT)]
        )
        grant_product_response.assert_is_success()

        second_auth_response = config.freya.auth_gateway(api_key_2).login_with_email(
            config.store.account.email,
            config.store.account.password)
        second_auth_response.assert_is_success()

        assert_that(second_auth_response.content['body']['allowed'], equal_to(False))
