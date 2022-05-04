import uuid

import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities, InventoryUtilities, PurchaseUtil, ReturnValue, WaitOn
from integration.main.services import CurrencyItem, PurchaseProductItem


@pytest.mark.skip_for_regions('trie', 'wgt1')
@pytest.allure.feature('functional')
@pytest.allure.story('purchase flow')
@pytest.mark.notprodsafe
@pytest.mark.notpreprodsafe
class TestPurchaseFlow(object):

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

        login_response = config.freya.auth_gateway.login_with_email(
            config.store.account.email,
            config.store.account.password
        )
        login_response.assert_is_success()

        config.store.profile_id = login_response.content['body']['profile_id']

        config.log.info('Initial inventory check')

        waiter = WaitOn(lambda: InventoryUtilities.inventory_empty(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            check_currencies=True,
            check_entitlements=True
        )).until(ReturnValue.EQUAL_TO(True), 30)

        waiter.wait('Should have empty inventory\n{}'.format(
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

        config.log.info('Fetch products from {} storefront'.format(config.data.TEST_STORE_FULL.STOREFRONT))
        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_STORE_FULL.STOREFRONT,
            config.store.profile_id,
            config.data.TEST_STORE_FULL.COUNTRY,
            config.data.TEST_STORE_FULL.LANGUAGE
        )
        fetch_response.assert_is_success()
        config.store.product_uriList = fetch_response.content['body']['uriList']

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(config.store.wgid)
        delete_response.assert_is_success()

    @pytest.fixture
    def bind_account(self, config):
        config.log.info('Binding braintree_paypal payment method')
        bind_response = config.psa.service.bind(config.store.wgid,
                                                PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
                                                PurchaseUtil.PaymentNone.PAYPAL_NONCE)
        bind_response.assert_is_success()

    @pytest.allure.severity(severity_level.NORMAL)
    def test_purchase_flow_should_ensure_test_currency_from_purchased_product_is_in_inventory(
            self,
            config,
            bind_account
    ):
        config.log.info('Saved Product ID of {}'.format(config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE))
        product_info = next((info for info in PurchaseUtil.get_product_infos(config.store.product_uriList) if
                             info['product_code'] == config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE),
                            None)

        assert_that(product_info, not_none())
        assert_that(product_info, has_key('product_id'))
        product_id = product_info['product_id']

        assert_that(product_info, has_key('currencies'))
        assert_that(product_info['currencies'], has_length(1))
        product_currencies = int(product_info['currencies'][0]['amount'])

        config.log.info(
            'Fetch price for {} quantity of {}'.format(1, config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE))
        fetch_price_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            1,
            config.data.TEST_STORE_FULL.STOREFRONT
        )
        fetch_price_response.assert_is_success()

        fetch_info = fetch_price_response.content['body']['price']

        assert_that(fetch_info, has_key('real_price'))
        cost = fetch_info['real_price']

        config.log.info('Prepare purchase for {}'.format(config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE))
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.wgid,
            config.store.wgid,
            [PurchaseProductItem(product_id, 1)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(cost['code'], cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            storefront=config.data.TEST_PRODUCT_VARIABLE.STOREFRONT
        )
        prepare_response.assert_is_success()

        order_id = prepare_response.content['body']['order_id']
        action_data = prepare_response.content['body']['required_action']['action_data']

        config.log.info('Commit purchase for {}'.format(config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE))
        tx_id = str(uuid.uuid4())

        commit_response = config.freya.server_gateway.commit_purchase(
            tx_id,
            order_id,
            config.store.wgid,
            action_data['payment_data']['amount'],
            action_data['payment_data']['currency_code'],
            action_data['payment_data']['payment_method'],
            '123456',
            action_data['2fa']['type']
        )
        commit_response.assert_is_success()
        assert_that(commit_response.content['body']['transaction_id'], equal_to(tx_id))
        assert_that(commit_response.content['body']['order_id'], equal_to(order_id))

        final_product_currencies = (product_currencies * 1)

        waiter = WaitOn(
            lambda: InventoryUtilities.inventory_has(
                config.freya.server_gateway,
                config.log,
                config.store.profile_id,
                {config.data.TEST_PRODUCT_VARIABLE.CURRENCIES.CODE: final_product_currencies},
                {}
            )
        ).until(ReturnValue.EQUAL_TO(True), timeout=30)

    @pytest.allure.severity(severity_level.NORMAL)
    def test_purchase_flow_should_ensure_entitlement_from_purchased_product_is_in_inventory(
            self,
            config,
            bind_account
    ):
        config.log.info('Saved Product ID of {}'.format(config.data.TEST_PRODUCT_REAL_PRICE.CODE))
        product_info = next((info for info in PurchaseUtil.get_product_infos(config.store.product_uriList) if
                             info['product_code'] == config.data.TEST_PRODUCT_REAL_PRICE.CODE),
                            None)

        assert_that(product_info, not_none())
        assert_that(product_info, has_key('product_id'))
        product_id = product_info['product_id']

        config.log.info(
            'Fetch price for {} quantity of {}'.format(1, config.data.TEST_PRODUCT_REAL_PRICE.CODE))
        fetch_price_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_PRODUCT_REAL_PRICE.CODE,
            config.data.TEST_PRODUCT_REAL_PRICE.COUNTRY,
            1,
            config.data.TEST_STORE_FULL.STOREFRONT
        )
        fetch_price_response.assert_is_success()

        fetch_info = fetch_price_response.content['body']['price']

        assert_that(fetch_info, has_key('real_price'))
        cost = fetch_info['real_price']

        config.log.info('Prepare purchase for {}'.format(config.data.TEST_PRODUCT_REAL_PRICE.CODE))
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_REAL_PRICE.COUNTRY,
            config.data.TEST_PRODUCT_REAL_PRICE.LANGUAGE,
            config.store.wgid,
            config.store.wgid,
            [PurchaseProductItem(product_id, 1)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(cost['code'], cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            storefront=config.data.TEST_PRODUCT_REAL_PRICE.STOREFRONT
        )
        prepare_response.assert_is_success()

        order_id = prepare_response.content['body']['order_id']
        action_data = prepare_response.content['body']['required_action']['action_data']

        config.log.info('Commit purchase for {}'.format(config.data.TEST_PRODUCT_REAL_PRICE.CODE))
        tx_id = str(uuid.uuid4())

        commit_response = config.freya.server_gateway.commit_purchase(
            tx_id,
            order_id,
            config.store.wgid,
            action_data['payment_data']['amount'],
            action_data['payment_data']['currency_code'],
            action_data['payment_data']['payment_method'],
            '123456',
            action_data['2fa']['type']
        )
        commit_response.assert_is_success()
        assert_that(commit_response.content['body']['transaction_id'], equal_to(tx_id))
        assert_that(commit_response.content['body']['order_id'], equal_to(order_id))

        waiter = WaitOn(
            lambda: InventoryUtilities.inventory_has(
                config.freya.server_gateway,
                config.log,
                config.store.profile_id,
                {},
                {config.data.TEST_PRODUCT_REAL_PRICE.ENTITLEMENTS.CODE: 1}
            )
        ).until(ReturnValue.EQUAL_TO(True), timeout=30)

    @pytest.allure.severity(severity_level.NORMAL)
    def test_purchase_flow_should_ensure_test_currency_and_entitlement_from_purchased_product_is_in_inventory(
            self,
            config,
            bind_account
    ):
        config.log.info('Saved Product ID of {}'.format(config.data.TEST_PRODUCT_FULL_REAL_PRICE.CODE))
        product_info = next((info for info in PurchaseUtil.get_product_infos(config.store.product_uriList) if
                             info['product_code'] == config.data.TEST_PRODUCT_FULL_REAL_PRICE.CODE),
                            None)

        assert_that(product_info, not_none())
        assert_that(product_info, has_key('product_id'))
        product_id = product_info['product_id']

        assert_that(product_info, has_key('currencies'))
        assert_that(product_info['currencies'], has_length(1))
        product_currencies = int(product_info['currencies'][0]['amount'])

        config.log.info(
            'Fetch price for {} quantity of {}'.format(1, config.data.TEST_PRODUCT_FULL_REAL_PRICE.CODE))
        fetch_price_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_PRODUCT_FULL_REAL_PRICE.CODE,
            config.data.TEST_PRODUCT_FULL_REAL_PRICE.COUNTRY,
            1,
            config.data.TEST_STORE_FULL.STOREFRONT
        )
        fetch_price_response.assert_is_success()

        fetch_info = fetch_price_response.content['body']['price']

        assert_that(fetch_info, has_key('real_price'))
        cost = fetch_info['real_price']

        config.log.info('Prepare purchase for {}'.format(config.data.TEST_PRODUCT_FULL_REAL_PRICE.CODE))
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_FULL_REAL_PRICE.COUNTRY,
            config.data.TEST_PRODUCT_FULL_REAL_PRICE.LANGUAGE,
            config.store.wgid,
            config.store.wgid,
            [PurchaseProductItem(product_id, 1)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(cost['code'], cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            storefront=config.data.TEST_PRODUCT_FULL_REAL_PRICE.STOREFRONT
        )
        prepare_response.assert_is_success()

        order_id = prepare_response.content['body']['order_id']
        action_data = prepare_response.content['body']['required_action']['action_data']

        config.log.info('Commit purchase for {}'.format(config.data.TEST_PRODUCT_FULL_REAL_PRICE.CODE))
        tx_id = str(uuid.uuid4())

        commit_response = config.freya.server_gateway.commit_purchase(
            tx_id,
            order_id,
            config.store.wgid,
            action_data['payment_data']['amount'],
            action_data['payment_data']['currency_code'],
            action_data['payment_data']['payment_method'],
            '123456',
            action_data['2fa']['type']
        )
        commit_response.assert_is_success()
        assert_that(commit_response.content['body']['transaction_id'], equal_to(tx_id))
        assert_that(commit_response.content['body']['order_id'], equal_to(order_id))

        final_product_currencies = (product_currencies * 1)

        waiter = WaitOn(
            lambda: InventoryUtilities.inventory_has(
                config.freya.server_gateway,
                config.log,
                config.store.profile_id,
                {config.data.TEST_PRODUCT_FULL_REAL_PRICE.CURRENCIES.CODE: final_product_currencies},
                {config.data.TEST_PRODUCT_FULL_REAL_PRICE.ENTITLEMENTS.CODE: 1}
            )
        ).until(ReturnValue.EQUAL_TO(True), timeout=30)
