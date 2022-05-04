import time
import uuid

import pytest

from integration.main.helpers import AccountUtilities
from integration.main.services import LegacyCurrencyItem
from integration.schemas import Schemas


@pytest.allure.feature('swagger')
@pytest.allure.story('tools')
class TestPlayerSwagger(object):

    @pytest.fixture(autouse=True)
    def setup(self, config):
        ###
        # Test setup
        login_response = config.freya.tools_gateway.login.auth_adfs_login(config.admin.username, config.admin.password)
        login_response.assert_is_success()

        config.store.account = AccountUtilities.create_account()
        account_response = config.freya.tools_gateway.player.new(
            config.store.account.email,
            config.store.account.name,
            config.store.account.password,
            config.data.TEST_TITLE,
            config.environment['region']
        )
        account_response.assert_is_success()
        config.store.wgid = account_response.content['id']

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here

    def test_player_consume_currency(self, config):
        grant_response = config.freya.tools_gateway.player.grant_currency(
            config.data.TEST_TITLE,
            config.store.wgid,
            config.data.TEST_CURRENCY.CURRENCY_CODE,
            config.data.TEST_CURRENCY.AMOUNT,
            str(uuid.uuid4())
        )
        grant_response.assert_is_success()
        currency = grant_response.content['body']['currency']

        consume_response = config.freya.tools_gateway.player.consume_currency(
            config.data.TEST_TITLE,
            config.store.wgid,
            currency['code'],
            currency['amount'],
            str(uuid.uuid4())
        )
        consume_response.assert_is_success()
        Schemas.swagger_validate(consume_response, '/api/v1/player/{title_code}/consumeCurrency')

    def test_player_consume_entitlement(self, config):
        grant_response = config.freya.tools_gateway.player.grant_entitlement(
            config.data.TEST_TITLE,
            config.store.wgid,
            config.data.TEST_ENTITLEMENT.ENTITLEMENT_CODE,
            config.data.TEST_ENTITLEMENT.AMOUNT
        )
        grant_response.assert_is_success()
        entitlement = grant_response.content['body']['entitlement']

        consume_response = config.freya.tools_gateway.player.consume_entitlement(
            config.data.TEST_TITLE,
            config.store.wgid,
            entitlement['code'],
            entitlement['amount']
        )
        consume_response.assert_is_success()
        Schemas.swagger_validate(consume_response, '/api/v1/player/{title_code}/consumeEntitlement')

    def test_player_create(self, config):
        new_response = config.freya.tools_gateway.player.new(
            "test_{0}@wargaming.net".format(int(time.time())),
            "test_{0}".format(int(time.time())),
            "111111",
            config.data.TEST_TITLE
        )
        new_response.assert_is_success()
        Schemas.swagger_validate(new_response, '/api/v1/player')

    def test_player_createBan(self, config):
        profile = config.freya.tools_gateway.player.create_title_profile(config.store.wgid, config.data.TEST_TITLE)
        profile.assert_is_success()

        ban_response = config.freya.tools_gateway.player.create_ban(
            config.store.wgid,
            config.data.TEST_BAN.REASON,
            config.data.TEST_BAN.AUTHOR,
            config.data.TEST_BAN.GAME,
            config.data.TEST_BAN.PROJECT.lower(),
            config.data.TEST_BAN.EXPIRES
        )
        ban_response.assert_is_success()
        Schemas.swagger_validate(ban_response, '/api/v1/player/create-ban')

    def test_player_createTitleProfile(self, config):
        profile_response = config.freya.tools_gateway.player.create_title_profile(config.store.wgid,
                                                                                  config.data.TEST_TITLE)
        profile_response.assert_is_success()
        Schemas.swagger_validate(profile_response, '/api/v1/player/id/{id}/profile/{title_code}')

    def test_player_deleteBan(self, config):
        ban_response = config.freya.tools_gateway.player.create_ban(
            config.store.wgid,
            config.data.TEST_BAN.REASON,
            config.data.TEST_BAN.AUTHOR,
            config.data.TEST_BAN.GAME,
            config.data.TEST_BAN.PROJECT.lower(),
            config.data.TEST_BAN.EXPIRES
        )
        ban_response.assert_is_success()
        ban_id = ban_response.content['ban_id']

        delete_response = config.freya.tools_gateway.player.delete_ban(ban_id)
        delete_response.assert_is_success()
        Schemas.swagger_validate(delete_response, '/api/v1/player/delete-ban')

    def test_player_getBans(self, config):
        get_response = config.freya.tools_gateway.player.get_bans(config.store.wgid)
        get_response.assert_is_success()
        Schemas.swagger_validate(get_response, '/api/v1/player/get-bans')

    def test_player_getById(self, config):
        player_response = config.freya.tools_gateway.player.get_player_by_id(config.store.wgid)
        player_response.assert_is_success()
        Schemas.swagger_validate(player_response, '/api/v1/player/id/{id}')

    def test_player_getByLogin(self, config):
        player_response = config.freya.tools_gateway.player.get_player_by_login(config.store.account.email)
        player_response.assert_is_success()
        Schemas.swagger_validate(player_response, '/api/v1/player/login/{login}')

    def test_player_getByName(self, config):
        player_response = config.freya.tools_gateway.player.get_player_by_name(config.store.account.name)
        player_response.assert_is_success()
        Schemas.swagger_validate(player_response, '/api/v1/player/name/{name}')

    def test_player_get_full_inventory(self, config):
        profile_response = config.freya.tools_gateway.player.create_title_profile(config.store.wgid,
                                                                                  config.data.TEST_TITLE)
        profile_response.assert_is_success()

        inventory_response = config.freya.tools_gateway.player.get_full_inventory(config.data.TEST_TITLE,
                                                                                  config.store.wgid)
        inventory_response.assert_is_success()
        Schemas.swagger_validate(inventory_response, '/api/v1/player/{title_code}/getFullInventory')

    def test_player_grant_currency(self, config):
        profile_response = config.freya.tools_gateway.player.create_title_profile(config.store.wgid,
                                                                                  config.data.TEST_TITLE)
        profile_response.assert_is_success()

        grant_response = config.freya.tools_gateway.player.grant_currency(
            config.data.TEST_TITLE,
            config.store.wgid,
            config.data.TEST_CURRENCY.CURRENCY_CODE,
            config.data.TEST_CURRENCY.AMOUNT,
            str(uuid.uuid4())
        )
        grant_response.assert_is_success()
        Schemas.swagger_validate(grant_response, '/api/v1/player/{title_code}/grantCurrency')

    def test_player_grant_entitlement(self, config):
        profile_response = config.freya.tools_gateway.player.create_title_profile(config.store.wgid,
                                                                                  config.data.TEST_TITLE)
        profile_response.assert_is_success()

        grant_response = config.freya.tools_gateway.player.grant_entitlement(
            config.data.TEST_TITLE,
            config.store.wgid,
            config.data.TEST_ENTITLEMENT.ENTITLEMENT_CODE,
            config.data.TEST_ENTITLEMENT.AMOUNT
        )
        grant_response.assert_is_success()
        Schemas.swagger_validate(grant_response, '/api/v1/player/{title_code}/grantEntitlement')

    def test_player_kickByTitleAndProfileId(self, config):
        create_title_response = config.freya.tools_gateway.player.create_title_profile(config.store.wgid,
                                                                                       config.data.TEST_TITLE)
        create_title_response.assert_is_success()
        profile_id = create_title_response.content['profile_id']

        login_response = config.freya.auth_gateway.login_with_email(config.store.account.email,
                                                                    config.store.account.password)
        login_response.assert_is_success()

        kick_response = config.freya.tools_gateway.player.kick_by_title_and_profile_id(config.data.TEST_TITLE,
                                                                                       profile_id)
        kick_response.assert_is_success()
        Schemas.swagger_validate(kick_response, '/api/v1/player/kick/{titleCode}/profile/{profileId}')

    def test_player_kickByTitleAndWgId(self, config):

        login_response = config.freya.auth_gateway.login_with_email(config.store.account.email,
                                                                    config.store.account.password)
        login_response.assert_is_success()

        kick_response = config.freya.tools_gateway.player.kick_by_wgid_and_title(config.data.TEST_TITLE,
                                                                                 config.store.wgid)
        kick_response.assert_is_success()
        Schemas.swagger_validate(kick_response, '/api/v1/player/kick/{titleCode}/wg/{wgId}')

    @pytest.mark.xfail(reason='PLAT-4252', raises=AssertionError)
    def test_player_kickByWgId(self, config):

        login_response = config.freya.auth_gateway.login_with_email(config.store.account.email,
                                                                    config.store.account.password)
        login_response.assert_is_success()

        kick_response = config.freya.tools_gateway.player.kick_by_wgid(config.store.wgid)
        kick_response.assert_is_success()
        Schemas.swagger_validate(kick_response, '/api/v1/player/kick/wg/{wgId}')

    @pytest.allure.feature('swagger')
    @pytest.allure.story('tools')
    def test_player_name(self, config):
        player_response = config.freya.tools_gateway.player.get_player_list()
        player_response.assert_is_success()
        Schemas.swagger_validate(player_response, '/api/v1/player/name/{name}')

    def test_player_profile(self, config):
        profile_response = config.freya.tools_gateway.player.create_title_profile(config.store.wgid,
                                                                                  config.data.TEST_TITLE)
        profile_response.assert_is_success()
        profile_id = profile_response.content['profile_id']

        player_response = config.freya.tools_gateway.player.get_player_profile(profile_id, config.data.TEST_TITLE)
        player_response.assert_is_success()
        Schemas.swagger_validate(player_response, '/api/v1/player/id/{id}/profile/{title_code}')

    def test_player_purchase_product(self, config):
        player_response = config.freya.tools_gateway.player.create_title_profile(config.store.wgid,
                                                                                 config.data.TEST_TITLE)
        player_response.assert_is_success()

        grant_reponse = config.freya.tools_gateway.player.grant_currency(
            config.data.TEST_TITLE,
            config.store.wgid,
            config.data.TEST_PRODUCT_FULL.VIRTUAL_CURRENCY.CURRENCY_CODE,
            config.data.TEST_PRODUCT_FULL.VIRTUAL_CURRENCY.AMOUNT,
        )
        grant_reponse.assert_is_success()

        purchase_response = config.freya.tools_gateway.player.purchase_product(
            config.data.TEST_TITLE,
            config.store.wgid,
            config.store.wgid,
            config.data.TEST_PRODUCT_FULL.CODE,
            config.data.TEST_PRODUCT_FULL.AMOUNT,
            [LegacyCurrencyItem(
                config.data.TEST_PRODUCT_FULL.VIRTUAL_CURRENCY.CURRENCY_CODE,
                config.data.TEST_PRODUCT_FULL.VIRTUAL_CURRENCY.AMOUNT
            )],
            str(uuid.uuid4())
        )
        purchase_response.assert_is_success()
        Schemas.swagger_validate(purchase_response, '/api/v1/player/{title_code}/purchaseProduct')

    def test_player_regions(self, config):
        # No schema
        pass
