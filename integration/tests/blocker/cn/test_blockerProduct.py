import uuid

import pytest
from allure import severity_level
from hamcrest import assert_that, has_key, has_length, not_none, equal_to, none, \
    greater_than, is_not, empty

from integration.main.helpers import WaitOn, InventoryUtilities, TitleUtilities, ReturnValue, PurchaseUtil, \
    RequestBuilder
from integration.main.services import LegacyProductItem, CurrencyItem, PurchaseProductItem


@pytest.allure.feature('functional')
@pytest.allure.severity(severity_level.BLOCKER)
class TestBlockerProduct(object):

    @pytest.fixture
    def clean_up_inventory(self, config):
        yield

        get_inventory_response = config.freya.server_gateway.get_full_inventory(config.environment['us_wgid'])

        for currency in get_inventory_response.content['body']['profile']['currencies']:
            consume_currency_response = config.freya.server_gateway.consume_currency(
                str(uuid.uuid4()),
                config.environment['us_wgid'],
                currency['code'],
                currency['amount']
            )
            consume_currency_response.assert_is_success()

        for entitlement in get_inventory_response.content['body']['profile']['entitlements']:
            # decrease premium amount to prevent insufficient_funds error
            if entitlement['code'] == config.data.PREMIUM_BLOCKER_RM.PREMIUM_ENTITLEMENT.CODE:
                pass
            else:
                consume_entitlement_response = config.freya.server_gateway.consume_entitlement(
                    config.environment['us_wgid'],
                    entitlement['code'],
                    entitlement['amount'],
                    tx_id=str(uuid.uuid4())
                )
                consume_entitlement_response.assert_is_success()

        # CN360 does not have sharred currency for now. Uncomment if will be added

        # shared_currency_api = TitleUtilities.get_api_key(
        #     config.freya.tools_gateway,
        #     config.environment['shared_currency']
        # )

        # get_shared_currency_inventory_response = config.freya.server_gateway(shared_currency_api).get_full_inventory(
        #     config.environment['us_wgid']
        # )
        #
        # for currency in get_shared_currency_inventory_response.content['body']['profile']['currencies']:
        #     consume_currency_response = config.freya.server_gateway(shared_currency_api).consume_currency(
        #         str(uuid.uuid4()),
        #         config.environment['us_wgid'],
        #         currency['code'],
        #         currency['amount']
        #     )
        #     consume_currency_response.assert_is_success()

    @pytest.allure.story('fetch products')
    def test_fetch_products_should_succeed_when_premium_product_have_vc_price_and_compensation(self, config):
        fetch_product = config.freya.server_gateway.fetch_products(
            [config.data.PREMIUM_BLOCKER_VC.CODE],
            config.environment['us_wgid'],
            config.data.PREMIUM_BLOCKER_VC.COUNTRY,
            config.data.PREMIUM_BLOCKER_VC.LANGUAGE
        )
        fetch_product.assert_is_success()

        assert_that(fetch_product.content['body'], has_key('uriList'))
        assert_that(fetch_product.content['body']['uriList'], has_length(1))
        uri = fetch_product.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        assert_that(product_response.content, has_key('entitlements'))

        entitlement = next(
            (
                entitlement for entitlement in product_response.content['entitlements']
                if entitlement['code'] == config.data.PREMIUM_BLOCKER_VC.ENTITLEMENTS.CODE
            ),
            None
        )
        assert_that(entitlement, not_none())

        assert_that(entitlement, has_key('compensation'))
        compensation = entitlement['compensation']

        assert_that(compensation, has_key('code'))
        assert_that(compensation['code'], equal_to(config.data.PREMIUM_BLOCKER_VC.COMPENSATION.CODE))
        assert_that(compensation, has_key('amount'))
        assert_that(compensation['amount'], equal_to(config.data.PREMIUM_BLOCKER_VC.COMPENSATION.AMOUNT))

    @pytest.allure.story('fetch product list')
    def test_fetch_product_list_should_succeed_when_premium_product_have_vc_price_and_comp_with_pct_pro_disc(
            self,
            config
    ):
        fetch_product = config.freya.server_gateway.fetch_product_list(
            config.data.PREMIUM_BLOCKER_VC.STOREFRONT,
            config.environment['us_wgid'],
            config.data.PREMIUM_BLOCKER_VC.COUNTRY,
            config.data.PREMIUM_BLOCKER_VC.LANGUAGE
        )
        fetch_product.assert_is_success()

        assert_that(fetch_product.content['body'], has_key('uriList'))
        assert_that(fetch_product.content['body']['uriList'], not_none())
        uri_list = fetch_product.content['body']['uriList']

        product = next(
            (
                product for product in PurchaseUtil.get_product_infos(uri_list)
                if product['product_code'] == config.data.PREMIUM_BLOCKER_VC.CODE
            ),
            None
        )
        assert_that(product, not_none())

        assert_that(product, has_key('entitlements'))

        entitlement = next(
            (
                entitlement for entitlement in product['entitlements']
                if entitlement['code'] == config.data.PREMIUM_BLOCKER_VC.ENTITLEMENTS.CODE
            ),
            None
        )
        assert_that(entitlement, not_none())

        assert_that(entitlement, has_key('compensation'))
        compensation = entitlement['compensation']

        assert_that(compensation, has_key('code'))
        assert_that(compensation['code'], equal_to(config.data.PREMIUM_BLOCKER_VC.COMPENSATION.CODE))
        assert_that(compensation, has_key('amount'))
        assert_that(compensation['amount'], equal_to(config.data.PREMIUM_BLOCKER_VC.COMPENSATION.DISCOUNTED_AMOUNT))

    @pytest.allure.story('fetch products')
    def test_fetch_products_should_succeed_when_premium_product_have_rm_price_and_compensation(self, config):
        fetch_product = config.freya.server_gateway.fetch_products(
            [config.data.PREMIUM_BLOCKER_RM.CODE],
            config.environment['us_wgid'],
            config.data.PREMIUM_BLOCKER_RM.US.COUNTRY,
            config.data.PREMIUM_BLOCKER_RM.LANGUAGE
        )
        fetch_product.assert_is_success()

        assert_that(fetch_product.content['body'], has_key('uriList'))
        assert_that(fetch_product.content['body']['uriList'], has_length(1))
        uri = fetch_product.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        assert_that(product_response.content, has_key('entitlements'))

        entitlement = next(
            (
                entitlement for entitlement in product_response.content['entitlements']
                if entitlement['code'] == config.data.PREMIUM_BLOCKER_RM.ENTITLEMENTS.CODE
            ),
            None
        )
        assert_that(entitlement, not_none())

        assert_that(entitlement, has_key('compensation'))
        compensation = entitlement['compensation']

        assert_that(compensation, has_key('code'))
        assert_that(compensation['code'], equal_to(config.data.PREMIUM_BLOCKER_RM.COMPENSATION.CODE))
        assert_that(compensation, has_key('amount'))
        assert_that(compensation['amount'], equal_to(config.data.PREMIUM_BLOCKER_RM.COMPENSATION.AMOUNT))

    @pytest.allure.story('fetch product list')
    def test_fetch_product_list_should_succeed_when_premium_product_have_rm_price_and_comp_with_pct_pro_disc(
            self,
            config
    ):
        fetch_product = config.freya.server_gateway.fetch_product_list(
            config.data.PREMIUM_BLOCKER_RM.STOREFRONT,
            config.environment['us_wgid'],
            config.data.PREMIUM_BLOCKER_RM.US.COUNTRY,
            config.data.PREMIUM_BLOCKER_RM.LANGUAGE
        )
        fetch_product.assert_is_success()

        assert_that(fetch_product.content['body'], has_key('uriList'))
        assert_that(fetch_product.content['body']['uriList'], not_none())
        uri_list = fetch_product.content['body']['uriList']

        product = next(
            (
                product for product in PurchaseUtil.get_product_infos(uri_list)
                if product['product_code'] == config.data.PREMIUM_BLOCKER_RM.CODE
            ),
            None
        )
        assert_that(product, not_none())

        assert_that(product, has_key('entitlements'))

        entitlement = next(
            (
                entitlement for entitlement in product['entitlements']
                if entitlement['code'] == config.data.PREMIUM_BLOCKER_RM.ENTITLEMENTS.CODE
            ),
            None
        )
        assert_that(entitlement, not_none())

        assert_that(entitlement, has_key('compensation'))
        compensation = entitlement['compensation']

        assert_that(compensation, has_key('code'))
        assert_that(compensation['code'], equal_to(config.data.PREMIUM_BLOCKER_RM.COMPENSATION.CODE))
        assert_that(compensation, has_key('amount'))
        assert_that(compensation['amount'], equal_to(config.data.PREMIUM_BLOCKER_RM.COMPENSATION.DISCOUNTED_AMOUNT))

    @pytest.allure.story('fetch products')
    def test_fetch_products_should_succeed_when_premium_product_have_variable_price(self, config):
        fetch_product = config.freya.server_gateway.fetch_products(
            [config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.CODE],
            config.environment['us_wgid'],
            config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.COUNTRY,
            config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.LANGUAGE
        )
        fetch_product.assert_is_success()

        assert_that(fetch_product.content['body'], has_key('uriList'))
        assert_that(fetch_product.content['body']['uriList'], has_length(1))
        uri = fetch_product.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        assert_that(product_response.content, has_key('currencies'))
        assert_that(product_response.content['currencies'], has_length(greater_than(0)))

        currency = next(
            (
                currency for currency in product_response.content['currencies']
                if currency['code'] == config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.VIRTUAL_CURRENCIES.GOLD.CODE
            ),
            None
        )
        assert_that(currency, not_none())
        assert_that(currency, has_key('amount'))
        assert_that(
            currency['amount'],
            equal_to(str(config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.VIRTUAL_CURRENCIES.GOLD.AMOUNT))
        )

    @pytest.mark.skip(reason='FREYA-1166')
    @pytest.allure.story('grant product')
    @pytest.mark.notthreadsafe
    def test_grant_product_should_succeed_when_premium_product_have_vc_price(self, config, clean_up_inventory):
        grant_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.PREMIUM_BLOCKER_VC.COUNTRY,
            config.data.PREMIUM_BLOCKER_VC.LANGUAGE,
            config.environment['us_wgid'],
            [LegacyProductItem(
                config.data.PREMIUM_BLOCKER_VC.CODE,
                config.data.PREMIUM_BLOCKER_VC.AMOUNT
            )]
        )
        grant_response.assert_is_success()
        get_inventory_response = config.freya.server_gateway.get_full_inventory(config.environment['us_wgid'])
        entitlement = next(
            (
                entitlement for entitlement in get_inventory_response.content['body']['profile']['entitlements']
                if entitlement['code'] == config.data.PREMIUM_BLOCKER_VC.PREMIUM_ENTITLEMENT.CODE
            ),
            None
        )
        assert_that(entitlement, not_none())

    @pytest.mark.skip(reason='FREYA-1166')
    @pytest.allure.story('grant product')
    @pytest.mark.notthreadsafe
    def test_grant_product_should_succeed_when_premium_product_have_rm_price(self, config, clean_up_inventory):
        grant_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.PREMIUM_BLOCKER_RM.US.COUNTRY,
            config.data.PREMIUM_BLOCKER_RM.LANGUAGE,
            config.environment['us_wgid'],
            [LegacyProductItem(
                config.data.PREMIUM_BLOCKER_RM.CODE,
                config.data.PREMIUM_BLOCKER_RM.AMOUNT
            )]
        )
        grant_response.assert_is_success()
        get_inventory_response = config.freya.server_gateway.get_full_inventory(config.environment['us_wgid'])
        entitlement = next(
            (
                entitlement for entitlement in get_inventory_response.content['body']['profile']['entitlements']
                if entitlement['code'] == config.data.PREMIUM_BLOCKER_RM.PREMIUM_ENTITLEMENT.CODE
            ),
            None
        )
        assert_that(entitlement, not_none())

    @pytest.mark.skip(reason='FREYA-1166')
    @pytest.allure.story('grant product')
    @pytest.mark.notthreadsafe
    def test_grant_product_should_succeed_when_premium_product_cost_variable_price(self, config, clean_up_inventory):
        grant_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.COUNTRY,
            config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.LANGUAGE,
            config.environment['us_wgid'],
            [LegacyProductItem(
                config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.CODE,
                config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.AMOUNT
            )]
        )
        grant_response.assert_is_success()

    @pytest.mark.skip_for_regions('cn360')
    # Union: ORDO Error
    @pytest.allure.story('purchase product')
    @pytest.mark.notthreadsafe
    def test_purchase_product_should_succeed_when_premium_product_have_vc_price(self, config, clean_up_inventory):
        config.log.info('Grant {} {} to purchase {}'.format(
            config.data.PREMIUM_BLOCKER_VC.ORIGINAL_COST.AMOUNT,
            config.data.PREMIUM_BLOCKER_VC.ORIGINAL_COST.CODE,
            config.data.PREMIUM_BLOCKER_VC.CODE
        ))

        grant_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.COUNTRY,
            config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.LANGUAGE,
            config.environment['us_wgid'],
            [LegacyProductItem(
                config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.CODE,
                config.data.PREMIUM_BLOCKER_VC.ORIGINAL_COST.AMOUNT
            )]
        )
        grant_response.assert_is_success()

        config.log.info('Purchase {}'.format(config.data.PREMIUM_BLOCKER_VC.CODE))

        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.environment['us_wgid'],
            config.environment['us_wgid'],
            config.data.PREMIUM_BLOCKER_VC.CODE,
            config.data.PREMIUM_BLOCKER_VC.AMOUNT,
            [CurrencyItem(
                config.data.PREMIUM_BLOCKER_VC.ORIGINAL_COST.CODE,
                str(config.data.PREMIUM_BLOCKER_VC.DISCOUNTED_COST.AMOUNT)
            )],
            storefront=config.data.PREMIUM_BLOCKER_VC.STOREFRONT
        )
        purchase_response.assert_is_success()

        get_inventory_response = config.freya.server_gateway.get_full_inventory(config.environment['us_wgid'])
        entitlement = next(
            (
                entitlement for entitlement in get_inventory_response.content['body']['profile']['entitlements']
                if entitlement['code'] == config.data.PREMIUM_BLOCKER_VC.PREMIUM_ENTITLEMENT.CODE
            ),
            None
        )
        assert_that(entitlement, not_none())

    @pytest.mark.skip_for_regions('cn360')
    # Union: ORDO Error
    @pytest.allure.story('purchase product')
    @pytest.mark.notthreadsafe
    def test_purchase_product_should_succeed_when_premium_product_have_discount_on_vc_price(
            self,
            config,
            clean_up_inventory
    ):
        config.log.info('Grant {} {} to purchase {}'.format(
            config.data.PREMIUM_BLOCKER_VC.DISCOUNTED_COST.AMOUNT,
            config.data.PREMIUM_BLOCKER_VC.DISCOUNTED_COST.CODE,
            config.data.PREMIUM_BLOCKER_VC.CODE
        ))

        grant_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.COUNTRY,
            config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.LANGUAGE,
            config.environment['us_wgid'],
            [LegacyProductItem(
                config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.CODE,
                config.data.PREMIUM_BLOCKER_VC.DISCOUNTED_COST.AMOUNT
            )]
        )
        grant_response.assert_is_success()

        config.log.info('Purchase {}'.format(config.data.PREMIUM_BLOCKER_VC.CODE))

        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.environment['us_wgid'],
            config.environment['us_wgid'],
            config.data.PREMIUM_BLOCKER_VC.CODE,
            config.data.PREMIUM_BLOCKER_VC.AMOUNT,
            [CurrencyItem(
                config.data.PREMIUM_BLOCKER_VC.DISCOUNTED_COST.CODE,
                str(config.data.PREMIUM_BLOCKER_VC.DISCOUNTED_COST.AMOUNT)
            )],
            storefront=config.data.PREMIUM_BLOCKER_VC.STOREFRONT
        )
        purchase_response.assert_is_success()

        config.log.info('Check inventory')

        waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.environment['us_wgid'],
            to_check_currencies={
                config.data.PREMIUM_BLOCKER_VC.VIRTUAL_CURRENCIES.TEST_CURRENCY.CODE:
                    config.data.PREMIUM_BLOCKER_VC.VIRTUAL_CURRENCIES.TEST_CURRENCY.AMOUNT
            },
            to_check_entitlements={
                config.data.PREMIUM_BLOCKER_VC.ENTITLEMENTS.CODE:
                    config.data.PREMIUM_BLOCKER_VC.ENTITLEMENTS.AMOUNT
            }
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)

        waiter.wait('Did not get {} {} or {} {}\n{}'.format(
            config.data.PREMIUM_BLOCKER_VC.VIRTUAL_CURRENCIES.TEST_CURRENCY.AMOUNT,
            config.data.PREMIUM_BLOCKER_VC.VIRTUAL_CURRENCIES.TEST_CURRENCY.CODE,
            config.data.PREMIUM_BLOCKER_VC.ENTITLEMENTS.AMOUNT,
            config.data.PREMIUM_BLOCKER_VC.ENTITLEMENTS.CODE,
            config.freya.server_gateway.get_full_inventory(config.environment['us_wgid']).details
        ))

        title_response = config.freya.title_config.get_titles(config.environment['shared_currency'])
        shared_currency_api = str(title_response[0]['title_versions'][0]['server_api_key'])

        shared_currency_waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway(shared_currency_api),
            config.log,
            config.environment['us_wgid'],
            to_check_currencies={
                config.data.PREMIUM_BLOCKER_VC.VIRTUAL_CURRENCIES.GOLD.CODE:
                    config.data.PREMIUM_BLOCKER_VC.VIRTUAL_CURRENCIES.GOLD.AMOUNT,
                config.data.PREMIUM_BLOCKER_VC.VIRTUAL_CURRENCIES.FREE_XP.CODE:
                    config.data.PREMIUM_BLOCKER_VC.VIRTUAL_CURRENCIES.FREE_XP.AMOUNT
            },
            to_check_entitlements={}
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)

        shared_currency_waiter.wait('Did not get {} {}, or {} {}\n{}'.format(
            config.data.PREMIUM_BLOCKER_VC.VIRTUAL_CURRENCIES.GOLD.AMOUNT,
            config.data.PREMIUM_BLOCKER_VC.VIRTUAL_CURRENCIES.GOLD.CODE,
            config.data.PREMIUM_BLOCKER_VC.VIRTUAL_CURRENCIES.FREE_XP.AMOUNT,
            config.data.PREMIUM_BLOCKER_VC.VIRTUAL_CURRENCIES.FREE_XP.CODE,
            config.freya.server_gateway(shared_currency_api).get_full_inventory(config.environment['us_wgid']).details
        ))

        get_inventory_response = config.freya.server_gateway.get_full_inventory(config.environment['us_wgid'])
        entitlement = next(
            (
                entitlement for entitlement in get_inventory_response.content['body']['profile']['entitlements']
                if entitlement['code'] == config.data.PREMIUM_BLOCKER_VC.PREMIUM_ENTITLEMENT.CODE
            ),
            None
        )
        assert_that(entitlement, not_none())

    @pytest.mark.skip_for_regions('cn360')
    # CN360: ORDO Error (need check from ordo team)
    @pytest.allure.story('prepare purchase')
    def test_prepare_purchase_should_succeed_when_premium_product_have_rm_price(self, config):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.PREMIUM_BLOCKER_RM.CODE],
            config.environment['us_wgid'],
            config.data.PREMIUM_BLOCKER_RM.US.COUNTRY,
            config.data.PREMIUM_BLOCKER_RM.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        assert_that(product_response.content, has_key('product_id'))
        product_id = product_response.content['product_id']

        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.PREMIUM_BLOCKER_RM.US.COUNTRY,
            config.data.PREMIUM_BLOCKER_RM.LANGUAGE,
            config.environment['us_wgid'],
            config.environment['us_wgid'],
            [PurchaseProductItem(product_id, config.data.PREMIUM_BLOCKER_RM.AMOUNT)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(
                config.data.PREMIUM_BLOCKER_RM.US.CODE,
                '{0:.2f}'.format(config.data.PREMIUM_BLOCKER_RM.US.DISCOUNTED_AMOUNT)
            ),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            storefront=config.data.PREMIUM_BLOCKER_RM.STOREFRONT
        )
        prepare_response.assert_is_success()

    @pytest.mark.skip_for_regions('cn360')
    # CN360: ORDO Error (need check from ordo team)
    @pytest.allure.story('prepare purchase')
    def test_prepare_purchase_should_succeed_when_premium_product_have_discount_on_rm_price(
            self,
            config
    ):
        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.PREMIUM_BLOCKER_RM.STOREFRONT,
            config.environment['us_wgid'],
            config.data.PREMIUM_BLOCKER_RM.US.COUNTRY,
            config.data.PREMIUM_BLOCKER_RM.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri_list = fetch_response.content['body']['uriList']

        product = next(
            (
                product for product in PurchaseUtil.get_product_infos(uri_list)
                if product['product_code'] == config.data.PREMIUM_BLOCKER_RM.CODE
            ),
            None
        )
        assert_that(product, not_none())

        assert_that(product, has_key('product_id'))
        product_id = product['product_id']

        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.PREMIUM_BLOCKER_RM.US.COUNTRY,
            config.data.PREMIUM_BLOCKER_RM.LANGUAGE,
            config.environment['us_wgid'],
            config.environment['us_wgid'],
            [PurchaseProductItem(product_id, config.data.PREMIUM_BLOCKER_RM.AMOUNT)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(
                config.data.PREMIUM_BLOCKER_RM.US.CODE,
                '{0:.2f}'.format(config.data.PREMIUM_BLOCKER_RM.US.DISCOUNTED_AMOUNT)
            ),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            storefront=config.data.PREMIUM_BLOCKER_RM.STOREFRONT
        )
        prepare_response.assert_is_success()

    @pytest.mark.skip_for_regions('cn360')
    # Delete when ordo get valid cpid for cn360
    @pytest.allure.story('purchase product with money v2')
    def test_purchase_product_with_rm_v2_should_succeed_when_premium_product_have_rm_price(self, config):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.PREMIUM_BLOCKER_RM.CODE],
            config.environment['us_wgid'],
            config.data.PREMIUM_BLOCKER_RM.US.COUNTRY,
            config.data.PREMIUM_BLOCKER_RM.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        assert_that(product_response.content, has_key('product_id'))
        product_id = product_response.content['product_id']

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.PREMIUM_BLOCKER_RM.US.COUNTRY,
            config.data.PREMIUM_BLOCKER_RM.LANGUAGE,
            config.environment['us_wgid'],
            'blocker_test@qa.wargaming.net',
            config.environment['us_wgid'],
            [PurchaseProductItem(product_id, config.data.PREMIUM_BLOCKER_RM.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(
                config.data.PREMIUM_BLOCKER_RM.US.CODE,
                '{0:.2f}'.format(config.data.PREMIUM_BLOCKER_RM.US.DISCOUNTED_AMOUNT)
            ),
            payer_current_ip='127.0.0.1',
            storefront=config.data.PREMIUM_BLOCKER_RM.STOREFRONT,
            client_payment_method_id=config.environment['client_payment_id']
        )
        purchase_response.assert_is_success()

        assert_that(purchase_response.content['body'], has_key('required_action'))
        assert_that(purchase_response.content['body']['required_action'], has_key('action_code'))

        url = purchase_response.content['body']['required_action']['action_data']['payment_url']
        config.log.info('commerce url: {0}'.format(url))
        money_request = RequestBuilder(url).get(verify=False)
        money_request.assert_is_success()
        assert_that(money_request.is_html)

    @pytest.mark.skip_for_regions('cn360')
    # Delete when ordo get valid cpid for cn360
    @pytest.allure.story('purchase product with money v2')
    def test_purchase_product_with_rm_v2_should_succeed_when_premium_product_have_discount_on_rm_price(self, config):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.PREMIUM_BLOCKER_RM.CODE],
            config.environment['us_wgid'],
            config.data.PREMIUM_BLOCKER_RM.US.COUNTRY,
            config.data.PREMIUM_BLOCKER_RM.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        assert_that(product_response.content, has_key('product_id'))
        product_id = product_response.content['product_id']

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.PREMIUM_BLOCKER_RM.US.COUNTRY,
            config.data.PREMIUM_BLOCKER_RM.LANGUAGE,
            config.environment['us_wgid'],
            'blocker_test@qa.wargaming.net',
            config.environment['us_wgid'],
            [PurchaseProductItem(product_id, config.data.PREMIUM_BLOCKER_RM.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(
                config.data.PREMIUM_BLOCKER_RM.US.CODE,
                '{0:.2f}'.format(config.data.PREMIUM_BLOCKER_RM.US.DISCOUNTED_AMOUNT)
            ),
            payer_current_ip='127.0.0.1',
            storefront=config.data.PREMIUM_BLOCKER_RM.STOREFRONT,
            client_payment_method_id=config.environment['client_payment_id']
        )
        purchase_response.assert_is_success()

        assert_that(purchase_response.content['body'], has_key('required_action'))
        assert_that(purchase_response.content['body']['required_action'], has_key('action_code'))

        url = purchase_response.content['body']['required_action']['action_data']['payment_url']
        config.log.info('commerce url: {0}'.format(url))
        money_request = RequestBuilder(url).get(verify=False)
        money_request.assert_is_success()
        assert_that(money_request.is_html)

    @pytest.mark.skip_for_regions('cn360')
    # CN360: ORDO Error (need check from ordo team)
    @pytest.allure.story('prepare purchase')
    def test_prepare_purchase_should_succeed_when_premium_product_have_rm_price_in_ru(
            self,
            config
    ):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.PREMIUM_BLOCKER_RM.CODE],
            config.environment['ru_wgid'],
            config.data.PREMIUM_BLOCKER_RM.RU.COUNTRY,
            config.data.PREMIUM_BLOCKER_RM.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        assert_that(product_response.content, has_key('product_id'))
        product_id = product_response.content['product_id']

        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.PREMIUM_BLOCKER_RM.RU.COUNTRY,
            config.data.PREMIUM_BLOCKER_RM.LANGUAGE,
            config.environment['ru_wgid'],
            config.environment['ru_wgid'],
            [PurchaseProductItem(product_id, config.data.PREMIUM_BLOCKER_RM.AMOUNT)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(
                config.data.PREMIUM_BLOCKER_RM.RU.CODE,
                '{0:.2f}'.format(config.data.PREMIUM_BLOCKER_RM.RU.DISCOUNTED_AMOUNT)
            ),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            storefront=config.data.PREMIUM_BLOCKER_RM.STOREFRONT
        )
        prepare_response.assert_is_success()

    @pytest.mark.skip_for_regions('cn360')
    # CN360: ORDO Error (need check from ordo team)
    @pytest.allure.story('prepare purchase')
    def test_prepare_purchase_should_succeed_when_premium_product_have_discount_on_rm_price_in_ru(
            self,
            config
    ):
        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.PREMIUM_BLOCKER_RM.STOREFRONT,
            config.environment['ru_wgid'],
            config.data.PREMIUM_BLOCKER_RM.RU.COUNTRY,
            config.data.PREMIUM_BLOCKER_RM.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri_list = fetch_response.content['body']['uriList']

        product = next(
            (
                product for product in PurchaseUtil.get_product_infos(uri_list)
                if product['product_code'] == config.data.PREMIUM_BLOCKER_RM.CODE
            ),
            None
        )
        assert_that(product, not_none())

        assert_that(product, has_key('product_id'))
        product_id = product['product_id']

        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.PREMIUM_BLOCKER_RM.RU.COUNTRY,
            config.data.PREMIUM_BLOCKER_RM.LANGUAGE,
            config.environment['ru_wgid'],
            config.environment['ru_wgid'],
            [PurchaseProductItem(product_id, config.data.PREMIUM_BLOCKER_RM.AMOUNT)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(
                config.data.PREMIUM_BLOCKER_RM.RU.CODE,
                '{0:.2f}'.format(config.data.PREMIUM_BLOCKER_RM.RU.DISCOUNTED_AMOUNT)
            ),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            storefront=config.data.PREMIUM_BLOCKER_RM.STOREFRONT
        )
        prepare_response.assert_is_success()

    @pytest.mark.skip_for_regions('cn360')
    # Delete when ordo get valid cpid for cn360
    @pytest.allure.story('purchase product with money v2')
    def test_purchase_product_with_rm_v2_should_succeed_when_premium_product_have_rm_price_in_ru(self, config):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.PREMIUM_BLOCKER_RM.CODE],
            config.environment['ru_wgid'],
            config.data.PREMIUM_BLOCKER_RM.RU.COUNTRY,
            config.data.PREMIUM_BLOCKER_RM.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        assert_that(product_response.content, has_key('product_id'))
        product_id = product_response.content['product_id']

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.PREMIUM_BLOCKER_RM.RU.COUNTRY,
            config.data.PREMIUM_BLOCKER_RM.LANGUAGE,
            config.environment['ru_wgid'],
            'test_blocker_ru@qa.wargaming.net',
            config.environment['ru_wgid'],
            [PurchaseProductItem(product_id, config.data.PREMIUM_BLOCKER_RM.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(
                config.data.PREMIUM_BLOCKER_RM.RU.CODE,
                '{0:.2f}'.format(config.data.PREMIUM_BLOCKER_RM.RU.DISCOUNTED_AMOUNT)
            ),
            payer_current_ip='127.0.0.1',
            storefront=config.data.PREMIUM_BLOCKER_RM.STOREFRONT,
            client_payment_method_id=config.environment['client_payment_id']
        )
        purchase_response.assert_is_success()

        assert_that(purchase_response.content['body'], has_key('required_action'))
        assert_that(purchase_response.content['body']['required_action'], has_key('action_code'))

        url = purchase_response.content['body']['required_action']['action_data']['payment_url']
        config.log.info('commerce url: {0}'.format(url))
        money_request = RequestBuilder(url).get(verify=False)
        money_request.assert_is_success()
        assert_that(money_request.is_html)

    @pytest.mark.skip_for_regions('cn360')
    # Delete when ordo get valid cpid for cn360
    @pytest.allure.story('purchase product with money v2')
    def test_purchase_product_with_rm_should_succeed_when_premium_product_have_discount_on_rm_price_in_ru(self, config):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.PREMIUM_BLOCKER_RM.CODE],
            config.environment['ru_wgid'],
            config.data.PREMIUM_BLOCKER_RM.RU.COUNTRY,
            config.data.PREMIUM_BLOCKER_RM.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        assert_that(product_response.content, has_key('product_id'))
        product_id = product_response.content['product_id']

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.PREMIUM_BLOCKER_RM.RU.COUNTRY,
            config.data.PREMIUM_BLOCKER_RM.LANGUAGE,
            config.environment['ru_wgid'],
            'test_blocker_ru@qa.wargaming.net',
            config.environment['ru_wgid'],
            [PurchaseProductItem(product_id, config.data.PREMIUM_BLOCKER_RM.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(
                config.data.PREMIUM_BLOCKER_RM.RU.CODE,
                '{0:.2f}'.format(config.data.PREMIUM_BLOCKER_RM.RU.DISCOUNTED_AMOUNT)
            ),
            payer_current_ip='127.0.0.1',
            storefront=config.data.PREMIUM_BLOCKER_RM.STOREFRONT,
            client_payment_method_id=config.environment['client_payment_id']
        )
        purchase_response.assert_is_success()

        assert_that(purchase_response.content['body'], has_key('required_action'))
        assert_that(purchase_response.content['body']['required_action'], has_key('action_code'))

        url = purchase_response.content['body']['required_action']['action_data']['payment_url']
        config.log.info('commerce url: {0}'.format(url))
        money_request = RequestBuilder(url).get(verify=False)
        money_request.assert_is_success()
        assert_that(money_request.is_html)

    @pytest.mark.skip_for_regions('cn360')
    # CN360: ORDO Error (need check from ordo team)
    @pytest.allure.story('prepare purchase')
    def test_prepare_purchase_should_succeed_when_premium_product_have_variable_price(
            self,
            config
    ):
        trilogy_cost = round(config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.AMOUNT / 168.2, 2)

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.CODE],
            config.environment['us_wgid'],
            config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.COUNTRY,
            config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        url = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(url).get()
        product_response.assert_is_success()

        assert_that(product_response.content, has_key('product_id'))
        product_id = product_response.content['product_id']

        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.COUNTRY,
            config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.LANGUAGE,
            config.environment['us_wgid'],
            config.environment['us_wgid'],
            [PurchaseProductItem(product_id, config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.AMOUNT)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(
                config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.CURRENCY_CODE,
                '{0:.2f}'.format(trilogy_cost)
            ),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            storefront=config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.STOREFRONT
        )
        prepare_response.assert_is_success()

    @pytest.mark.skip_for_regions('cn360')
    # Delete when ordo get valid cpid for cn360
    @pytest.allure.story('purchase product with money v2')
    def test_purchase_product_with_rm_v2_should_succeed_when_premium_product_have_variable_price(self, config):
        trilogy_cost = round(config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.AMOUNT / 168.2, 2)

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.CODE],
            config.environment['us_wgid'],
            config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.COUNTRY,
            config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        assert_that(product_response.content, has_key('product_id'))
        product_id = product_response.content['product_id']

        cost = product_response.content['price']['real_price']
        assert_that(cost, not_none())
        config.log.info('cost: {0}'.format(cost['code']))
        config.log.info('amount: {0}'.format(cost['amount']))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.COUNTRY,
            config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.LANGUAGE,
            config.environment['us_wgid'],
            'blocker_test@qa.wargaming.net',
            config.environment['us_wgid'],
            [PurchaseProductItem(product_id, config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(
                config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.CURRENCY_CODE,
                '{0:.2f}'.format(trilogy_cost)
            ),
            payer_current_ip='127.0.0.1',
            storefront=config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.STOREFRONT,
            client_payment_method_id=config.environment['client_payment_id']
        )
        purchase_response.assert_is_success()

        assert_that(purchase_response.content['body'], has_key('required_action'))
        assert_that(purchase_response.content['body']['required_action'], has_key('action_code'))

        url = purchase_response.content['body']['required_action']['action_data']['payment_url']
        config.log.info('commerce url: {0}'.format(url))
        money_request = RequestBuilder(url).get(verify=False)
        money_request.assert_is_success()
        assert_that(money_request.is_html)

    @pytest.allure.story('fetch product list')
    def test_fetch_product_list_should_fail_when_override_set_vis_purch_to_false_on_variable_price_premium_product(
            self,
            config
    ):
        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.STOREFRONT,
            config.environment['us_wgid'],
            config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.COUNTRY,
            config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri_list = fetch_response.content['body']['uriList']

        product = next(
            (
                product for product in PurchaseUtil.get_product_infos(uri_list)
                if product['product_code'] == config.data.PREMIUM_BLOCKER_VARIABLE_PRICE.CODE
            ),
            None
        )
        assert_that(product, none())

    @pytest.mark.skip("PM not production ready")
    @pytest.allure.story('fetch product price v2')
    def test_fetch_product_price_should_succeed_and_return_all_available_payment_methods(self, config):

        fetch_response = config.freya.server_gateway.fetch_product_price_v2(
            config.data.PREMIUM_BLOCKER_PAYMENT_METHODS.CODE,
            config.data.PREMIUM_BLOCKER_PAYMENT_METHODS.COUNTRY,
            quantity=1,
            wgid=config.environment['us_wgid'],
            response_fields={'client_payment_methods': True}
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body'], has_key('client_payment_methods'))
        assert_that(fetch_response.content['body']['client_payment_methods'], is_not(empty()))
