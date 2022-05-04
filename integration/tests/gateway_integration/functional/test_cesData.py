import uuid

import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities, InventoryUtilities, PurchaseUtil, RequestBuilder, ReturnValue, \
    WaitOn
from integration.main.services import ConsulManager, CurrencyItem, PurchaseProductItem


@pytest.allure.feature('functional')
@pytest.allure.story('CES data')
class TestCESData(object):

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

        config.log.info('Get CES data for US to EUR currency')

        ces_response = config.freya.product_service.get_ces_data()
        ces_response.assert_is_success()

        ces_data = ces_response.content[config.data.TEST_CES_DATA.US_CURRENCY_CODE]
        assert_that(ces_data, has_key('quotes'))
        assert_that(ces_data['quotes'], has_key(config.data.TEST_CES_DATA.EUR_CURRENCY_CODE))

        eur_ces = ces_data['quotes'][config.data.TEST_CES_DATA.EUR_CURRENCY_CODE]
        assert_that(eur_ces, has_key('value'))
        config.store.eur_ces = float(eur_ces['value'])

        config.log.info('CES for EU is {}'.format(config.store.eur_ces))

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(config.store.profile_id)
        delete_response.assert_is_success()

    @pytest.fixture
    def bind_account(self, config):
        bind_response = config.psa.service.bind(
            config.store.profile_id,
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            PurchaseUtil.PaymentNone.PAYPAL_NONCE
        )
        bind_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_currency_exchange_occurs(self, config):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT_REAL_PRICE.CODE],
            config.store.profile_id,
            config.data.TEST_CES_DATA.COUNTRY,
            config.data.TEST_PRODUCT_REAL_PRICE.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_CES_DATA.EUR_CURRENCY_CODE))

        config.log.info('Calculate manually the cost of the product in Euros')

        calculated_cost = config.data.TEST_PRODUCT_REAL_PRICE.REAL_MONEY_AMOUNT * config.store.eur_ces

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to('{0:.2f}'.format(calculated_cost)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_currency_exchange_occurs(self, config):
        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_PRODUCT_REAL_PRICE.STOREFRONT,
            config.store.profile_id,
            config.data.TEST_CES_DATA.COUNTRY,
            config.data.TEST_PRODUCT_REAL_PRICE.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri_list = fetch_response.content['body']['uriList']

        prod = next((
            prod for prod in PurchaseUtil.get_product_infos(uri_list)
            if prod['product_code'] == config.data.TEST_PRODUCT_REAL_PRICE.CODE
        ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('price'))
        assert_that(prod['price'], has_key('real_price'))
        cost = prod['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_CES_DATA.EUR_CURRENCY_CODE))

        config.log.info('Calculating manually the cost of the product in Euros')

        calculated_cost = config.data.TEST_PRODUCT_REAL_PRICE.REAL_MONEY_AMOUNT * config.store.eur_ces

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to('{0:.2f}'.format(calculated_cost)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_currency_exchange_have_pct_pro_discount(self, config):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_RM_PCT_PRO_DISC_COMP.CODE],
            config.store.profile_id,
            config.data.TEST_CES_DATA.COUNTRY,
            config.data.TEST_RM_PCT_PRO_DISC_COMP.LANGUAGE,
            storefront=config.data.TEST_RM_PCT_PRO_DISC_COMP.STOREFRONT
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('Calculate the cost in Euros')
        converted_cost = round(config.data.TEST_RM_PCT_PRO_DISC_COMP.REAL_MONEY_AMOUNT * config.store.eur_ces, 2)

        config.log.info('Calculate the final cost in Euros with discount is taken off')
        final_cost = converted_cost * (1.0 - config.data.TEST_RM_PCT_PRO_DISC_COMP.DISCOUNT)

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_CES_DATA.EUR_CURRENCY_CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to('{0:.2f}'.format(final_cost)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_currency_exchange_have_pct_pro_discount(self, config):
        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_RM_PCT_PRO_DISC_COMP.STOREFRONT,
            config.store.profile_id,
            config.data.TEST_CES_DATA.COUNTRY,
            config.data.TEST_RM_PCT_PRO_DISC_COMP.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri_list = fetch_response.content['body']['uriList']

        prod = next(
            (
                prod for prod in PurchaseUtil.get_product_infos(uri_list)
                if prod['product_code'] == config.data.TEST_RM_PCT_PRO_DISC_COMP.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('price'))
        assert_that(prod['price'], has_key('real_price'))
        cost = prod['price']['real_price']

        config.log.info('Calculate the cost in Euros')
        converted_cost = round(config.data.TEST_RM_PCT_PRO_DISC_COMP.REAL_MONEY_AMOUNT * config.store.eur_ces, 2)

        config.log.info('Calculate the final cost in Euros with discount is taken off')
        final_cost = converted_cost * (1.0 - config.data.TEST_RM_PCT_PRO_DISC_COMP.DISCOUNT)

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_CES_DATA.EUR_CURRENCY_CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to('{0:.2f}'.format(final_cost)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_currency_exchange_have_abs_discount(self, config):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_RM_ABS_DISC_COMP.CODE],
            config.store.profile_id,
            config.data.TEST_CES_DATA.COUNTRY,
            config.data.TEST_RM_ABS_DISC_COMP.LANGUAGE,
            storefront=config.data.TEST_RM_ABS_DISC_COMP.STOREFRONT
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_CES_DATA.EUR_CURRENCY_CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to('{0:.2f}'.format(config.data.TEST_RM_ABS_DISC_COMP.DISCOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_currency_exchange_have_abs_discount(self, config):
        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_RM_ABS_DISC_COMP.STOREFRONT,
            config.store.profile_id,
            config.data.TEST_CES_DATA.COUNTRY,
            config.data.TEST_RM_ABS_DISC_COMP.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri_list = fetch_response.content['body']['uriList']

        prod = next(
            (
                prod for prod in PurchaseUtil.get_product_infos(uri_list)
                if prod['product_code'] == config.data.TEST_RM_ABS_DISC_COMP.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('price'))
        assert_that(prod['price'], has_key('real_price'))
        cost = prod['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_CES_DATA.EUR_CURRENCY_CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to('{0:.2f}'.format(config.data.TEST_RM_ABS_DISC_COMP.DISCOUNT)))

    @pytest.mark.skip_for_regions('trie')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_currency_exchange_and_coefficients_occur(self, config):
        config.log.info('Check if coefficient is enabled on {}'.format(
            config.environment.environment_name
        ))

        consul = ConsulManager(config.environment.consul, config.environment.environment_name)
        enabled_response = consul.get_kv('{}/product-price-coefficients/coefficients.enabled'.format(
            config.environment.environment_name
        ))
        enabled = enabled_response.content

        if type(enabled) is not bool or not enabled:
            config.log.info('Enabled on {} is {}'.format(
                config.environment.environment_name,
                enabled
            ))
            pytest.skip('Coefficients is not enabled')

        config.log.info('Get the Coefficient for AR')

        coefficient_response = consul.get_kv('{}/product-price-coefficients/AR'.format(
            config.environment.environment_name
        ))
        coefficient_response.assert_is_success()
        coefficient = coefficient_response.content

        config.log.info('Coefficient on {} for AR is {}'.format(
            config.environment.environment_name,
            coefficient
        ))

        config.log.info('Get CES data for USD to ARS currency')

        ces_response = config.freya.product_service.get_ces_data()
        ces_response.assert_is_success()

        ces_data = ces_response.content[config.data.TEST_COEFFICIENTS.REAL_MONEY.CODE]
        assert_that(ces_data, has_key('quotes'))
        assert_that(ces_data['quotes'], has_key(config.data.TEST_COEFFICIENTS.RM_AR_CURRENCY_CODE))

        ar_ces = ces_data['quotes'][config.data.TEST_COEFFICIENTS.RM_AR_CURRENCY_CODE]
        assert_that(ar_ces, has_key('value'))

        ces = float(ar_ces['value'])

        config.log.info('CES value is {}'.format(
            ces
        ))

        config.log.info('Calculate the cost in ARS')
        calculated_cost = int(round(config.data.TEST_COEFFICIENTS.REAL_MONEY.AMOUNT * ces * coefficient, 0))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_COEFFICIENTS.CODE],
            config.store.profile_id,
            config.data.TEST_COEFFICIENTS.COUNTRY,
            config.data.TEST_COEFFICIENTS.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_COEFFICIENTS.RM_AR_CURRENCY_CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(calculated_cost)))

    @pytest.mark.skip_for_regions('trie')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_currency_exchange_and_coefficients_occur(self, config):
        config.log.info('Check if coefficient is enabled on {}'.format(
            config.environment.environment_name
        ))

        consul = ConsulManager(config.environment.consul, config.environment.environment_name)
        enabled_response = consul.get_kv('{}/product-price-coefficients/coefficients.enabled'.format(
            config.environment.environment_name
        ))
        enabled = enabled_response.content

        if type(enabled) is not str or not enabled:
            config.log.info('Enabled on {} is {}'.format(
                config.environment.environment_name,
                enabled
            ))
            pytest.skip('Coefficients is not enabled')

        config.log.info('Get the Coefficient for AR')

        coefficient_response = consul.get_kv('{}/product-price-coefficients/AR'.format(
            config.environment.environment_name
        ))
        coefficient_response.assert_is_success()
        coefficient = coefficient_response.content

        config.log.info('Coefficient on {} for AR is {}'.format(
            config.environment.environment_name,
            coefficient
        ))

        config.log.info('Get CES data for USD to ARS currency')

        ces_response = config.freya.product_service.get_ces_data()
        ces_response.assert_is_success()

        ces_data = ces_response.content[config.data.TEST_COEFFICIENTS.REAL_MONEY.CODE]
        assert_that(ces_data, has_key('quotes'))
        assert_that(ces_data['quotes'], has_key(config.data.TEST_COEFFICIENTS.RM_AR_CURRENCY_CODE))

        ar_ces = ces_data['quotes'][config.data.TEST_COEFFICIENTS.RM_AR_CURRENCY_CODE]
        assert_that(ar_ces, has_key('value'))

        ces = float(ar_ces['value'])

        config.log.info('CES value is {}'.format(
            ces
        ))

        config.log.info('Calculate the cost in ARS')
        calculated_cost = int(round(config.data.TEST_COEFFICIENTS.REAL_MONEY.AMOUNT * ces * coefficient, 0))

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_COEFFICIENTS.STOREFRONT,
            config.store.profile_id,
            config.data.TEST_COEFFICIENTS.COUNTRY,
            config.data.TEST_COEFFICIENTS.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri_list = fetch_response.content['body']['uriList']

        prod = next(
            (
                prod for prod in PurchaseUtil.get_product_infos(uri_list)
                if prod['product_code'] == config.data.TEST_COEFFICIENTS.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('price'))
        assert_that(prod['price'], has_key('real_price'))
        cost = prod['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_COEFFICIENTS.RM_AR_CURRENCY_CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(calculated_cost)))
