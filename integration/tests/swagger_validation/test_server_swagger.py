import uuid

import pytest

from integration.main.helpers import AccountUtilities, PurchaseUtil
from integration.main.request import RequestBuilder
from integration.main.services import CurrencyItem, LegacyProductItem, PurchaseProductItem, WalletItem, \
    LegacyCurrencyItem
from integration.schemas import Schemas


@pytest.allure.feature('swagger')
@pytest.allure.story('server')
class TestServerSwagger(object):

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

        profile_response = config.freya.tools_gateway.player.create_title_profile(config.store.wgid,
                                                                                  config.data.TEST_TITLE,
                                                                                  config.environment['region'])
        profile_response.assert_is_success()
        config.store.profile_id = profile_response.content['profile_id']

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here

    def test_account_created(self, config):

        account_response = config.freya.server_gateway.account_created(config.store.profile_id)
        account_response.assert_is_success()
        Schemas.swagger_validate(account_response, '/api/v1/accountCreated')

    def test_begin_game_session(self, config):

        account_response = config.freya.server_gateway.account_created(config.store.profile_id, 'OK')
        account_response.assert_is_success()

        session_response = config.freya.server_gateway.begin_game_session(config.store.profile_id)
        session_response.assert_is_success()
        Schemas.swagger_validate(session_response, '/api/v1/beginGameSession')

    def test_cancel_entitlement(self, config):

        transaction_id = str(uuid.uuid4())

        grant_response = config.freya.server_gateway.grant_entitlement(config.store.profile_id,
                                                                       config.data.TEST_ENTITLEMENT.ENTITLEMENT_CODE,
                                                                       config.data.TEST_ENTITLEMENT.AMOUNT,
                                                                       tx_id=transaction_id)
        grant_response.assert_is_success()

        cancel_response = config.freya.server_gateway.cancel_entitlement(config.store.wgid, transaction_id)
        cancel_response.assert_is_success()
        Schemas.swagger_validate(cancel_response, '/api/v1/cancelEntitlement')

    def test_commit_purchase(self, config):

        bind_response = config.psa.service.bind(
            config.store.wgid,
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            PurchaseUtil.PaymentNone.PAYPAL_NONCE
        )
        bind_response.assert_is_success()

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_MONEY.PRODUCT_CODE],
            config.store.wgid,
            config.data.TEST_MONEY.COUNTRY,
            config.data.TEST_MONEY.LANGUAGE,
        )
        fetch_response.assert_is_success()
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        product_id = product_response.content["product_id"]
        cost = product_response.content['price']['real_price']

        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_MONEY.COUNTRY,
            config.data.TEST_MONEY.LANGUAGE,
            config.store.profile_id,
            config.store.account.email,
            config.store.profile_id,
            [PurchaseProductItem(product_id, 1)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(cost['code'], cost['amount']),
            2,
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL
        )
        prepare_response.assert_is_success()
        order_id = prepare_response.content['body']['order_id']
        action_data = prepare_response.content['body']['required_action']['action_data']

        commit_response = config.freya.server_gateway.commit_purchase(
            str(uuid.uuid4()),
            order_id,
            config.store.wgid,
            action_data['payment_data']['amount'],
            action_data['payment_data']['currency_code'],
            action_data['payment_data']['payment_method'],
            '123456',
            action_data['2fa']['type']
        )
        commit_response.assert_is_success()
        Schemas.swagger_validate(commit_response, '/api/v1/commitPurchase')

    def test_consume_currency(self, config):

        grant_response = config.freya.server_gateway.grant_currency(str(uuid.uuid4()), config.store.profile_id,
                                                                   config.data.TEST_CURRENCY.CURRENCY_CODE,
                                                                   config.data.TEST_CURRENCY.AMOUNT)
        grant_response.assert_is_success()

        consume_response = config.freya.server_gateway.consume_currency(str(uuid.uuid4()), config.store.profile_id,
                                                                       config.data.TEST_CURRENCY.CURRENCY_CODE,
                                                                       config.data.TEST_CURRENCY.AMOUNT)
        consume_response.assert_is_success()
        Schemas.swagger_validate(consume_response, '/api/v1/consumeCurrency')

    def test_consume_entitlement(self, config):

        grant_response = config.freya.server_gateway.grant_entitlement(config.store.profile_id,
                                                                      config.data.TEST_ENTITLEMENT.ENTITLEMENT_CODE,
                                                                      config.data.TEST_ENTITLEMENT.AMOUNT)
        grant_response.assert_is_success()

        consume_response = config.freya.server_gateway.consume_entitlement(config.store.profile_id,
                                                                          config.data.TEST_ENTITLEMENT.ENTITLEMENT_CODE,
                                                                          config.data.TEST_ENTITLEMENT.AMOUNT)
        consume_response.assert_is_success()
        Schemas.swagger_validate(consume_response, '/api/v1/consumeEntitlement')

    def test_create_auth_token(self, config):

        login_response = config.freya.auth_gateway.login_with_email(config.store.account.email,
                                                                    config.store.account.password)
        login_response.assert_is_success()

        create_response = config.freya.server_gateway.create_auth_token(config.store.wgid, config.data.TARGET_APPLICATION)
        create_response.assert_is_success()
        Schemas.swagger_validate(create_response, '/api/v1/createAuthToken')

    def test_create_ban(self, config):

        create_response = config.freya.server_gateway.create_ban(
            config.store.profile_id,
            config.data.TEST_BAN.PROJECT,
            config.data.TEST_BAN.TYPE,
            config.data.TEST_BAN.REASON,
            config.data.TEST_BAN.AUTHOR
        )
        create_response.assert_is_success()
        Schemas.swagger_validate(create_response, '/api/v1/createBan')

    def test_create_remember_me_token(self, config):

        create_response = config.freya.server_gateway.create_remember_me_token(config.store.account.email,
                                                                               config.store.account.password,
                                                                               client_ip='127.0.0.1')
        create_response.assert_is_success()
        Schemas.swagger_validate(create_response, '/api/v1/createRememberMeToken')

    def test_end_game_session(self, config):

        login_response = config.freya.auth_gateway.login_with_email(config.store.account.email,
                                                                    config.store.account.password)
        login_response.assert_is_success()

        begin_session_response = config.freya.server_gateway.begin_game_session(config.store.profile_id)
        begin_session_response.assert_is_success()

        end_session_response = config.freya.server_gateway.end_game_session(config.store.profile_id)
        end_session_response.assert_is_success()
        Schemas.swagger_validate(end_session_response, '/api/v1/endGameSession')

    def test_fetch_product_list(self, config):

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_STORE.STOREFRONT,
            config.store.wgid,
            config.data.TEST_STORE.COUNTRY,
            config.data.TEST_STORE.LANGUAGE
        )
        fetch_response.assert_is_success()
        Schemas.swagger_validate(fetch_response, '/api/v1/fetchProductList')

    def test_fetch_product_price(self, config):

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_PRODUCT.PRODUCT_CODE,
            config.data.TEST_STORE.COUNTRY,
            config.data.TEST_PRODUCT.AMOUNT
        )
        fetch_response.assert_is_success()
        Schemas.swagger_validate(fetch_response, '/api/v1/fetchProductPrice')

    def test_fetch_products(self, config):

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT.PRODUCT_CODE],
            config.store.wgid,
            config.data.TEST_PRODUCT.COUNTRY,
            config.data.TEST_PRODUCT.LANGUAGE
        )
        fetch_response.assert_is_success()
        Schemas.swagger_validate(fetch_response, '/api/v1/fetchProducts')

    def test_generate_webhook_test(self, config):

        report_response = config.freya.server_gateway.generate_webhook_test()
        report_response.assert_is_success()
        Schemas.swagger_validate(report_response, '/api/v1/generateWebhookTest')

    def test_get_accounts_by_nickname(self, config):

        get_response = config.freya.server_gateway.get_accounts_by_nickname([config.store.account.name])
        get_response.assert_is_success()
        Schemas.swagger_validate(get_response, '/api/v1/getAccountsByNickname')

    def test_get_accounts_by_profile_id(self, config):

        get_response = config.freya.server_gateway.get_accounts_by_profile_id([config.store.profile_id])
        get_response.assert_is_success()
        Schemas.swagger_validate(get_response, '/api/v1/getAccountsByProfileId')

    def test_get_accounts_by_login(self, config):

        get_response = config.freya.server_gateway.get_accounts_by_login([config.store.account.email])
        get_response.assert_is_success()
        Schemas.swagger_validate(get_response, '/api/v1/getAccountsByLogin')

    def test_get_accounts_by_wgid(self, config):

        get_response = config.freya.server_gateway.get_accounts_by_wgid([config.store.wgid])
        get_response.assert_is_success()
        Schemas.swagger_validate(get_response, '/api/v1/getAccountsByWgId')

    def test_get_account_commerce_info(self, config):
        commerce_response = config.freya.server_gateway.get_account_commerce_info(
            config.store.wgid,
            'US')
        commerce_response.assert_is_success()
        Schemas.swagger_validate(commerce_response, '/api/v1/getAccountCommerceInfo')

    def test_get_full_inventory_from_session(self, config):

        login_response = config.freya.auth_gateway.login_with_email(config.store.account.email,
                                                                    config.store.account.password)
        login_response.assert_is_success()
        client_session = login_response.content['body']['client_session']

        inventory_response = config.freya.server_gateway.get_full_inventory_from_session(client_session)
        inventory_response.assert_is_success()
        Schemas.swagger_validate(inventory_response, '/api/v1/getFullInventoryFromSession')

    def test_get_inventory(self, config):

        inventory_response = config.freya.server_gateway.get_inventory(config.store.wgid)
        inventory_response.assert_is_success()
        Schemas.swagger_validate(inventory_response, '/api/v1/getInventory')

    def test_get_purchase_status_by_order_id(self, config):

        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PURCHASE.FREE.PRODUCT_CODE,
            config.data.TEST_PURCHASE.FREE.AMOUNT,
            []
        )
        purchase_response.assert_is_success()

        status_response = config.freya.server_gateway.get_purchase_status_by_order_id(
            purchase_response.content['body']['order_id'], config.store.profile_id)
        status_response.assert_is_success()
        Schemas.swagger_validate(status_response, '/api/v1/getPurchaseStatusByOrderId')

    def test_get_webhook_audit_log(self, config):

        audit_response = config.freya.server_gateway.get_webhook_audit_log(0, 1495664424, 1, 10)
        audit_response.assert_is_success()
        Schemas.swagger_validate(audit_response, '/api/v1/getWebhookAuditLog')

    def test_grant_currency(self, config):

        grant_response = config.freya.server_gateway.grant_currency(str(uuid.uuid4()), config.store.profile_id,
                                                                   config.data.TEST_CURRENCY.CURRENCY_CODE,
                                                                   config.data.TEST_CURRENCY.AMOUNT)
        grant_response.assert_is_success()
        Schemas.swagger_validate(grant_response, '/api/v1/grantCurrency')

    def test_grant_entitlement(self, config):

        grant_response = config.freya.server_gateway.grant_entitlement(config.store.profile_id,
                                                                      config.data.TEST_ENTITLEMENT.ENTITLEMENT_CODE,
                                                                      config.data.TEST_ENTITLEMENT.AMOUNT)
        grant_response.assert_is_success()
        Schemas.swagger_validate(grant_response, '/api/v1/grantEntitlement')

    def test_grant_product(self, config):

        grant_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT.COUNTRY,
            config.data.TEST_PRODUCT.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT.PRODUCT_CODE, config.data.TEST_PRODUCT.AMOUNT)]
        )
        grant_response.assert_is_success()
        Schemas.swagger_validate(grant_response, '/api/v1/grantProduct')

    def test_move_currency(self, config):

        account_two = AccountUtilities.create_account()
        account_two_response = config.freya.tools_gateway.player.new(
            account_two.email,
            account_two.name,
            account_two.password,
            config.data.TEST_TITLE,
            config.environment['region']
        )
        account_two_response.assert_is_success()
        account_two_wgid = account_two_response.content['id']

        profile_two_response = config.freya.tools_gateway.player.create_title_profile(account_two_wgid,
                                                                                      config.data.TEST_TITLE,
                                                                                      config.environment['region'])
        profile_two_response.assert_is_success()
        profile_two_id = profile_two_response.content['profile_id']

        grant_response = config.freya.server_gateway.grant_currency(str(uuid.uuid4()), config.store.profile_id,
                                                                   config.data.TEST_CURRENCY.CURRENCY_CODE,
                                                                   config.data.TEST_CURRENCY.AMOUNT)
        grant_response.assert_is_success()

        move_response = config.freya.server_gateway.move_currency(str(uuid.uuid4()), config.store.profile_id,
                                                                 profile_two_id,
                                                                 config.data.TEST_CURRENCY.CURRENCY_CODE,
                                                                 config.data.TEST_CURRENCY.AMOUNT)
        move_response.assert_is_success()
        Schemas.swagger_validate(move_response, '/api/v1/moveCurrency')

    def test_ping(self, config):

        ping_response = config.freya.server_gateway.ping()
        ping_response.assert_is_success()
        Schemas.swagger_validate(ping_response, '/api/v1/ping')

    def test_prepare_purchase(self, config):

        bind_response = config.psa.service.bind(
            config.store.wgid,
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            PurchaseUtil.PaymentNone.PAYPAL_NONCE
        )
        bind_response.assert_is_success()

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_MONEY.PRODUCT_CODE],
            config.store.wgid,
            config.data.TEST_MONEY.COUNTRY,
            config.data.TEST_MONEY.LANGUAGE,
        )
        fetch_response.assert_is_success()
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        product_id = product_response.content["product_id"]
        cost = product_response.content['price']['real_price']

        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_MONEY.COUNTRY,
            config.data.TEST_MONEY.LANGUAGE,
            config.store.profile_id,
            config.store.account.email,
            config.store.profile_id,
            [PurchaseProductItem(product_id, 1)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(cost['code'], cost['amount']),
            2,
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL
        )
        prepare_response.assert_is_success()
        Schemas.swagger_validate(prepare_response, '/api/v1/preparePurchase')

    def test_purchase_product(self, config):

        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PRODUCT_FULL.CODE,
            config.data.TEST_PRODUCT_FULL.AMOUNT,
            [LegacyCurrencyItem(
                config.data.TEST_PRODUCT_FULL.VIRTUAL_CURRENCY.CURRENCY_CODE,
                config.data.TEST_PRODUCT_FULL.VIRTUAL_CURRENCY.AMOUNT
            )]
        )
        purchase_response.assert_is_success()
        Schemas.swagger_validate(purchase_response, '/api/v1/purchaseProduct')

    @pytest.mark.xfail(reason='Not yet implemented', raises=AssertionError)
    def test_report_user(self, config):

        report_response = config.freya.server_gateway.report_user(config.store.profile_id)
        report_response.assert_is_success()
        Schemas.swagger_validate(report_response, '/api/v1/reportUser')

    def test_reverse_entitlement(self, config):

        grant_response = config.freya.server_gateway.grant_entitlement(config.store.profile_id,
                                                                      config.data.TEST_ENTITLEMENT.ENTITLEMENT_CODE,
                                                                      config.data.TEST_ENTITLEMENT.AMOUNT)
        grant_response.assert_is_success()
        transaction_id = grant_response.content['body']['transaction_id']

        reverse_response = config.freya.server_gateway.reverse_entitlement(config.store.wgid, transaction_id,
                                                                          str(uuid.uuid4()))
        reverse_response.assert_is_success()
        Schemas.swagger_validate(reverse_response, '/api/v1/reverseEntitlement')

    def test_validate_client_session(self, config):

        login_response = config.freya.auth_gateway.login_with_email(config.store.account.email,
                                                                    config.store.account.password)
        login_response.assert_is_success()
        client_session = login_response.content['body']['client_session']

        validate_response = config.freya.server_gateway.validate_client_session(client_session, None)
        validate_response.assert_is_success()
        Schemas.swagger_validate(validate_response, '/api/v1/validateClientSession')
