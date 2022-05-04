import uuid

import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities, PurchaseUtil, RequestBuilder
from integration.main.services import CurrencyItem, PurchaseProductItem


@pytest.mark.skip_for_regions('trie', 'wgt1')
@pytest.mark.notprodsafe
@pytest.allure.feature('functional')
@pytest.allure.story('purchase latam rounding')
@pytest.mark.notprodsafe
class TestPurchaseLATAMRounding(object):

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

        config.store.account_wgid = account_created.content['id']
        config.store.wgid = account_created.content['id']

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(config.store.wgid)
        delete_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_argentina_price_round_down(self, config):
        config.log.info('fetching {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE],
            config.store.account_wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.ARGENTINA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('getting the product information')

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('purchasing {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.ARGENTINA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.STOREFRONT,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_bolivia_price_round_down(self, config):
        config.log.info('fetching {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE],
            config.store.account_wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.BOLIVIA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('getting the product information')

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('purchasing {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.BOLIVIA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.STOREFRONT,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_chile_price_round_down(self, config):
        config.log.info('fetching {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE],
            config.store.account_wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CHILE.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('getting the product information')

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('purchasing {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CHILE.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.STOREFRONT,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_colombia_price_round_down(self, config):
        config.log.info('fetching {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE],
            config.store.account_wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COLOMBIA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('getting the product information')

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('purchasing {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COLOMBIA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.STOREFRONT,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_costa_rica_price_round_down(self, config):
        config.log.info('fetching {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE],
            config.store.account_wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COSTA_RICA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('getting the product information')

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('purchasing {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COSTA_RICA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.STOREFRONT,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_mexico_price_round_down(self, config):
        config.log.info('fetching {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE],
            config.store.account_wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.MEXICO.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('getting the product information')

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('purchasing {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.MEXICO.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.STOREFRONT,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_nicaragua_price_round_down(self, config):
        config.log.info('fetching {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE],
            config.store.account_wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.NICARAGUA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('getting the product information')

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('purchasing {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.NICARAGUA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.STOREFRONT,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_uruguay_price_round_down(self, config):
        config.log.info('fetching {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE],
            config.store.account_wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.URUGUAY.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('getting the product information')

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('purchasing {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.URUGUAY.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.STOREFRONT,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_argentina_price_round_up(self, config):
        config.log.info('fetching {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE],
            config.store.account_wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.ARGENTINA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('getting the product information')

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('purchasing {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.ARGENTINA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATIN_COUNTRY_ROUND_UP.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATIN_COUNTRY_ROUND_UP.STOREFRONT,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_bolivia_price_round_up(self, config):
        config.log.info('fetching {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE],
            config.store.account_wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.BOLIVIA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('getting the product information')

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('purchasing {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.BOLIVIA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATIN_COUNTRY_ROUND_UP.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATIN_COUNTRY_ROUND_UP.STOREFRONT,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_chile_price_round_up(self, config):
        config.log.info('fetching {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE],
            config.store.account_wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CHILE.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('getting the product information')

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('purchasing {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CHILE.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATIN_COUNTRY_ROUND_UP.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATIN_COUNTRY_ROUND_UP.STOREFRONT,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_colombia_price_round_up(self, config):
        config.log.info('fetching {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE],
            config.store.account_wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.COLOMBIA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('getting the product information')

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('purchasing {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.COLOMBIA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATIN_COUNTRY_ROUND_UP.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATIN_COUNTRY_ROUND_UP.STOREFRONT,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_costa_rica_price_round_up(self, config):
        config.log.info('fetching {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE],
            config.store.account_wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.COSTA_RICA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('getting the product information')

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('purchasing {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.COSTA_RICA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATIN_COUNTRY_ROUND_UP.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATIN_COUNTRY_ROUND_UP.STOREFRONT,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_mexico_price_round_up(self, config):
        config.log.info('fetching {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE],
            config.store.account_wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.MEXICO.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('getting the product information')

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('purchasing {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.MEXICO.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATIN_COUNTRY_ROUND_UP.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATIN_COUNTRY_ROUND_UP.STOREFRONT,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_nicaragua_price_round_up(self, config):
        config.log.info('fetching {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE],
            config.store.account_wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.NICARAGUA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('getting the product information')

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('purchasing {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.NICARAGUA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATIN_COUNTRY_ROUND_UP.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATIN_COUNTRY_ROUND_UP.STOREFRONT,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_uruguay_price_round_up(self, config):
        config.log.info('fetching {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE],
            config.store.account_wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.URUGUAY.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('getting the product information')

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('purchasing {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.URUGUAY.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATIN_COUNTRY_ROUND_UP.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATIN_COUNTRY_ROUND_UP.STOREFRONT,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_argentia_price_round_down_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.ARGENTINA.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('Purchasing {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.ARGENTINA.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATAM_ROUND_DOWN_PROMO.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_bolivia_price_round_down_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.BOLIVIA.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('Purchasing {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.BOLIVIA.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATAM_ROUND_DOWN_PROMO.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_chile_price_round_down_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.CHILE.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('Purchasing {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.CHILE.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATAM_ROUND_DOWN_PROMO.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_colombia_price_round_down_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COLOMBIA.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('Purchasing {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COLOMBIA.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATAM_ROUND_DOWN_PROMO.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_costa_rica_price_round_down_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COSTA_RICA.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('Purchasing {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COSTA_RICA.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATAM_ROUND_DOWN_PROMO.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_mexico_price_round_down_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.MEXICO.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('Purchasing {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.MEXICO.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATAM_ROUND_DOWN_PROMO.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_nicaragua_price_round_down_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.NICARAGUA.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('Purchasing {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.NICARAGUA.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATAM_ROUND_DOWN_PROMO.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_uruguay_price_round_down_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.URUGUAY.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('Purchasing {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.URUGUAY.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATAM_ROUND_DOWN_PROMO.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_nicaragua_price_round_down_has_fixed_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.FIXED_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_DOWN_PROMO.FIXED_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.NICARAGUA.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.FIXED_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.FIXED_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.FIXED_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('Purchasing {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.FIXED_DISC_PRODUCT
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.NICARAGUA.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATAM_ROUND_DOWN_PROMO.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATAM_ROUND_DOWN_PROMO.FIXED_STORE,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_uruguay_price_round_down_has_fixed_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.FIXED_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_DOWN_PROMO.FIXED_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.URUGUAY.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.FIXED_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.FIXED_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.FIXED_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('Purchasing {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.FIXED_DISC_PRODUCT
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.URUGUAY.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATAM_ROUND_DOWN_PROMO.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATAM_ROUND_DOWN_PROMO.FIXED_STORE,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_argentia_price_round_up_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.ARGENTINA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('Purchasing {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATAM_ROUND_UP_PROMO.ARGENTINA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATAM_ROUND_UP_PROMO.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_bolivia_price_round_up_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.BOLIVIA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('Purchasing {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATAM_ROUND_UP_PROMO.BOLIVIA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATAM_ROUND_UP_PROMO.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_chile_price_round_up_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.CHILE.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('Purchasing {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATAM_ROUND_UP_PROMO.CHILE.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATAM_ROUND_UP_PROMO.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_colombia_price_round_up_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COLOMBIA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('Purchasing {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATAM_ROUND_UP_PROMO.COLOMBIA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATAM_ROUND_UP_PROMO.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_costa_rica_price_round_up_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COSTA_RICA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('Purchasing {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATAM_ROUND_UP_PROMO.COSTA_RICA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATAM_ROUND_UP_PROMO.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_mexico_price_round_up_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.MEXICO.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('Purchasing {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATAM_ROUND_UP_PROMO.MEXICO.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATAM_ROUND_UP_PROMO.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_nicaragua_price_round_up_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.NICARAGUA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('Purchasing {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATAM_ROUND_UP_PROMO.NICARAGUA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATAM_ROUND_UP_PROMO.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_uruguay_price_round_up_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.URUGUAY.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('Purchasing {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATAM_ROUND_UP_PROMO.URUGUAY.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATAM_ROUND_UP_PROMO.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_argentia_price_round_up_has_abs_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.ARGENTINA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('Purchasing {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATAM_ROUND_UP_PROMO.ARGENTINA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATAM_ROUND_UP_PROMO.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_STORE,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_bolivia_price_round_up_has_abs_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.BOLIVIA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('Purchasing {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATAM_ROUND_UP_PROMO.BOLIVIA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATAM_ROUND_UP_PROMO.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_STORE,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_chile_price_round_up_has_abs_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.CHILE.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('Purchasing {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATAM_ROUND_UP_PROMO.CHILE.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATAM_ROUND_UP_PROMO.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_STORE,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_colombia_price_round_up_has_abs_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COLOMBIA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('Purchasing {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATAM_ROUND_UP_PROMO.COLOMBIA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATAM_ROUND_UP_PROMO.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_STORE,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_costa_rica_price_round_up_has_abs_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COSTA_RICA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('Purchasing {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATAM_ROUND_UP_PROMO.COSTA_RICA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATAM_ROUND_UP_PROMO.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_STORE,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_with_money_should_succeed_when_mexico_price_round_up_has_abs_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.MEXICO.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        config.log.info('Purchasing {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_LATAM_ROUND_UP_PROMO.MEXICO.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.store.account_wgid,
            config.store.account.email,
            config.store.account_wgid,
            [PurchaseProductItem(product_id, config.data.TEST_LATAM_ROUND_UP_PROMO.AMOUNT)],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_STORE,
            client_payment_method_id=prod_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()
