import uuid

import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities, PurchaseUtil
from integration.main.helpers.utils import tid, cid
from integration.main.request import RequestConstants, RequestBuilder
from integration.main.request.constants import ResponseMessage
from integration.main.services import CurrencyItem, PurchaseProductItem, GoogleAnalyticsItem


# Preparation to test:
# Make sure that products payment_method_settings in np.integration.catalog.json are actual.
# To check ppm usage, call commerce.get-partner-payment-methods.v1 contract to see all ppm and actualize catalog.


@pytest.mark.notprodsafe
class TestPurchaseProductWithMoneyv2(object):

    @pytest.fixture(autouse=True)
    def setup(self, config):
        ###
        # Test setup

        # account with unknown country
        config.store.account = AccountUtilities.create_account(attrs='user_stated_country=ZZ')
        account_created = config.spa.http.create_account(config.store.account.__dict__)
        account_created.assert_is_success()
        update_account = config.spa.http.update(account_created.content['id'],
                                                game=config.environment['test_title_pgn'])
        update_account.assert_is_success()
        config.store.wgid = account_created.content['id']
        config.store.profile_id = account_created.content['id']

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(config.store.wgid)
        delete_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product with money pm product')
    @pytest.allure.severity(severity_level.NORMAL)
    def test_purchase_product_with_money_stest_purchase_product_with_money_should_succeed_non_restricted_countrieshould_succeed_non_restricted_countries(self, config):
        #  PRODO-613
        # Should pass when country is not restricted (e.g. RU is allowed in product)
        config.log.info('product code: {0}'.format(config.data.TEST_PM_RESTRICTED.PRODUCT))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PM_RESTRICTED.PRODUCT],
            config.store.wgid,
            config.data.TEST_PM_RESTRICTED.COUNTRY,
            config.data.TEST_PM_RESTRICTED.LANGUAGE,
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        product_id = product_response.content["product_id"]
        assert_that(product_id, not_none())
        config.log.info('product id: {0}'.format(product_id))

        cost = product_response.content['price']['real_price']
        assert_that(cost, not_none())
        config.log.info('cost: {0}'.format(cost['code']))
        config.log.info('amount: {0}'.format(cost['amount']))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_PM_RESTRICTED.COUNTRY,
            config.data.TEST_PM_RESTRICTED.LANGUAGE,
            config.store.wgid,
            config.store.account.email,
            config.store.wgid,
            [PurchaseProductItem(product_id, 1, [])],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            receiver_country='US',
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_PM_RESTRICTED.STOREFRONT,
            client_payment_method_id=product_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

        assert_that(purchase_response.content['body'], has_key('required_action'))
        assert_that(purchase_response.content['body']['required_action'], has_key('action_code'))

        url = purchase_response.content['body']['required_action']['action_data']['payment_url']
        config.log.info('commerce url: {0}'.format(url))
        money_request = RequestBuilder(url).get(verify=False)
        money_request.assert_is_success()
        assert_that(money_request.is_html)

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product with money without ppm')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_purchase_product_with_money_product_without_pm(self, config, content_type):
        config.log.info('product code: {0}'.format(config.data.TEST_MONEY.PRODUCT_CODE))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_MONEY.PRODUCT_CODE],
            config.store.wgid,
            config.data.TEST_MONEY.COUNTRY,
            config.data.TEST_MONEY.LANGUAGE,
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        product_id = product_response.content["product_id"]
        assert_that(product_id, not_none())
        config.log.info('product id: {0}'.format(product_id))

        cost = product_response.content['price']['real_price']
        assert_that(cost, not_none())
        config.log.info('cost: {0}'.format(cost['code']))
        config.log.info('amount: {0}'.format(cost['amount']))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_MONEY.COUNTRY,
            config.data.TEST_MONEY.LANGUAGE,
            config.store.wgid,
            config.store.account.email,
            config.store.wgid,
            [PurchaseProductItem(product_id, 1, [])],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            content_type=content_type,
            storefront=config.data.TEST_MONEY.STOREFRONT,
            client_payment_method_id=123
        )
        purchase_response.expect_failure()

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product with money no pm product')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_purchase_product_with_money_no_pm(self, config, content_type):
        config.log.info('product code: {0}'.format(config.data.TEST_PM.PRODUCT))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PM.PRODUCT],
            config.store.wgid,
            config.data.TEST_PM.COUNTRY,
            config.data.TEST_PM.LANGUAGE,
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        product_id = product_response.content["product_id"]
        assert_that(product_id, not_none())
        config.log.info('product id: {0}'.format(product_id))

        cost = product_response.content['price']['real_price']
        assert_that(cost, not_none())
        config.log.info('cost: {0}'.format(cost['code']))
        config.log.info('amount: {0}'.format(cost['amount']))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_PM.COUNTRY,
            config.data.TEST_PM.LANGUAGE,
            config.store.wgid,
            config.store.account.email,
            config.store.wgid,
            [PurchaseProductItem(product_id, 1, [])],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            content_type=content_type,
            storefront=config.data.TEST_PM.STOREFRONT,
            client_payment_method_id=123
        )
        purchase_response.expect_failure()

    @pytest.mark.skip_for_regions('wgt1')
    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product with money with payment method settings empty')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_purchase_product_with_money_empty_pm(self, config, content_type):
        config.log.info('product code: {0}'.format(config.data.TEST_PM.PRODUCT_WITHOUT_SETTINGS))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PM.PRODUCT_WITHOUT_SETTINGS],
            config.store.wgid,
            config.data.TEST_PM.COUNTRY,
            config.data.TEST_PM.LANGUAGE,
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        product_id = product_response.content["product_id"]
        assert_that(product_id, not_none())
        config.log.info('product id: {0}'.format(product_id))

        cost = product_response.content['price']['real_price']
        assert_that(cost, not_none())
        config.log.info('cost: {0}'.format(cost['code']))
        config.log.info('amount: {0}'.format(cost['amount']))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_PM.COUNTRY,
            config.data.TEST_PM.LANGUAGE,
            config.store.wgid,
            config.store.account.email,
            config.store.wgid,
            [PurchaseProductItem(product_id, 1, [])],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            content_type=content_type,
            storefront=config.data.TEST_PM.STOREFRONT,
            client_payment_method_id=RequestConstants.PaymentGroupID.DEFAULT
        )
        purchase_response.expect_failure(result_code=ResponseMessage.PARTNER_PAYMENT_METHODS_NOT_FOUND)

    @pytest.mark.skip_for_regions('wgt1')
    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product with money with payment method settings empty')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_purchase_product_with_money_korean(self, config, content_type):
        #config.log.info('product code: {0}'.format(config.data.TEST_PM.PRODUCT_WITHOUT_SETTINGS))
        config.log.info('product code: {0}'.format(config.data.TEST_PM.PRODUCT))
        config.spa.http.update_account(wgid=config.store.wgid, update_name='/personal/country/legal/',
                                       update_value='kr')

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PM.PRODUCT],
            config.store.wgid,
            config.data.TEST_PM.COUNTRY,
            config.data.TEST_PM.LANGUAGE,
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        product_id = product_response.content["product_id"]
        assert_that(product_id, not_none())
        config.log.info('product id: {0}'.format(product_id))

        cost = product_response.content['price']['real_price']
        assert_that(cost, not_none())
        config.log.info('cost: {0}'.format(cost['code']))
        config.log.info('amount: {0}'.format(cost['amount']))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_PM.COUNTRY,
            config.data.TEST_PM.LANGUAGE,
            config.store.wgid,
            config.store.account.email,
            config.store.wgid,
            [PurchaseProductItem(product_id, 1, [])],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            content_type=content_type,
            storefront=config.data.TEST_PM.STOREFRONT,
            client_payment_method_id=product_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

        assert_that(purchase_response.content['body'], has_key('required_action'))
        assert_that(purchase_response.content['body']['required_action'], has_key('action_code'))

        url = purchase_response.content['body']['required_action']['action_data']['payment_url']
        config.log.info('commerce url: {0}'.format(url))
        money_request = RequestBuilder(url).get(verify=False)
        money_request.assert_is_success()
        assert_that(money_request.is_html)

    @pytest.mark.skip_for_regions('wgt1')
    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product with money pm product')
    @pytest.allure.severity(severity_level.NORMAL)
    def test_purchase_product_with_money_pm_and_ga_params(self, config):
        # FREYA-454
        config.log.info('product code: {0}'.format(config.data.TEST_PM.PRODUCT))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PM.PRODUCT],
            config.store.wgid,
            config.data.TEST_PM.COUNTRY,
            config.data.TEST_PM.LANGUAGE,
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        product_id = product_response.content["product_id"]
        assert_that(product_id, not_none())
        config.log.info('product id: {0}'.format(product_id))

        cost = product_response.content['price']['real_price']
        assert_that(cost, not_none())
        config.log.info('cost: {0}'.format(cost['code']))
        config.log.info('amount: {0}'.format(cost['amount']))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_PM.COUNTRY,
            config.data.TEST_PM.LANGUAGE,
            config.store.wgid,
            config.store.account.email,
            config.store.wgid,
            [PurchaseProductItem(product_id, 1, [])],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_PM.STOREFRONT,
            client_payment_method_id=product_response.content['client_payment_methods'][0],
            meta=(GoogleAnalyticsItem(tid(), cid())).as_json
        )
        purchase_response.assert_is_success()

    @pytest.mark.skip(reason='FREYA-895')
    @pytest.allure.feature('server')
    @pytest.allure.story('purchase gift product with money pm product')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_purchase_gift_product_with_money_pm(self, config, content_type):
        config.log.info('product code: {0}'.format(config.data.TEST_PRODUCT_RM_GIFT.PRODUCT))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT_RM_GIFT.PRODUCT],
            config.store.wgid,
            config.data.TEST_PRODUCT_RM_GIFT.COUNTRY,
            config.data.TEST_PRODUCT_RM_GIFT.LANGUAGE,
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        product_id = product_response.content["product_id"]
        assert_that(product_id, not_none())
        config.log.info('product id: {0}'.format(product_id))

        cost = product_response.content['price']['real_price']
        assert_that(cost, not_none())
        config.log.info('cost: {0}'.format(cost['code']))
        config.log.info('amount: {0}'.format(cost['amount']))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            tx_id=str(uuid.uuid4()),
            country=config.data.TEST_PRODUCT_RM_GIFT.COUNTRY,
            language=config.data.TEST_PRODUCT_RM_GIFT.LANGUAGE,
            payer_wgid=config.store.wgid,
            payer_email=config.store.account.email,
            receiver_wgid=config.store.wgid,
            products=[PurchaseProductItem(product_id, 1, [])],
            payment_type=PurchaseUtil.PaymentType.PSA,
            expected_price=CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            content_type=content_type,
            storefront=config.data.TEST_PRODUCT_RM_GIFT.STOREFRONT,
            client_payment_method_id=product_response.content['client_payment_methods'][0],
            gift={"enabled": True, "message": "gift message"}
        )
        purchase_response.assert_is_success()

        assert_that(purchase_response.content['body'], has_key('required_action'))
        assert_that(purchase_response.content['body']['required_action'], has_key('action_code'))

        url = purchase_response.content['body']['required_action']['action_data']['payment_url']
        config.log.info('commerce url: {0}'.format(url))
        money_request = RequestBuilder(url).get(verify=False)
        money_request.assert_is_success()
        assert_that(money_request.is_html)

    @pytest.mark.skip_for_regions('trie')
    @pytest.allure.feature('server')
    @pytest.allure.story('purchase gift product with money pm product')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_purchase_non_giftable_product_with_money(self, config, content_type):
        config.log.info('product code: {0}'.format(config.data.TEST_PRODUCT_NOT_GIFTABLE.PRODUCT))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT_NOT_GIFTABLE.PRODUCT],
            config.store.wgid,
            config.data.TEST_PRODUCT_NOT_GIFTABLE.COUNTRY,
            config.data.TEST_PRODUCT_NOT_GIFTABLE.LANGUAGE,
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        product_id = product_response.content["product_id"]
        assert_that(product_id, not_none())
        config.log.info('product id: {0}'.format(product_id))

        cost = product_response.content['price']['real_price']
        assert_that(cost, not_none())
        config.log.info('cost: {0}'.format(cost['code']))
        config.log.info('amount: {0}'.format(cost['amount']))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            tx_id=str(uuid.uuid4()),
            country=config.data.TEST_PRODUCT_NOT_GIFTABLE.COUNTRY,
            language=config.data.TEST_PRODUCT_NOT_GIFTABLE.LANGUAGE,
            payer_wgid=config.store.wgid,
            payer_email=config.store.account.email,
            receiver_wgid=config.store.wgid,
            products=[PurchaseProductItem(product_id, 1, [])],
            payment_type=PurchaseUtil.PaymentType.PSA,
            expected_price=CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            content_type=content_type,
            storefront=config.data.TEST_PRODUCT_NOT_GIFTABLE.STOREFRONT,
            client_payment_method_id=product_response.content['client_payment_methods'][0],
            gift={"enabled": True, "message": "gift message"}
        )
        purchase_response.expect_failure(result_code=ResponseMessage.PRODUCT_NOT_GIFTABLE)

    @pytest.mark.skip_for_regions('trie')
    @pytest.allure.feature('server')
    @pytest.allure.story('purchase gift product with money pm product')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('client_payment_method_id, error_message', [
        (None, 'CLIENT_PAYMENT_METHOD_NOT_FOUND'),
        pytest.param(-1, 'CLIENT_PAYMENT_METHOD_NOT_FOUND', marks=pytest.mark.xfail(reason="FREYA-895")),
        ('', 'CLIENT_PAYMENT_METHOD_NOT_FOUND')
    ])
    def test_purchase_gift_product_with_money_should_fail_invalid_client_pm(self, config, client_payment_method_id,
                                                                            error_message):
        config.log.info('product code: {0}'.format(config.data.TEST_PM.PRODUCT))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT_RM_GIFT.PRODUCT],
            config.store.wgid,
            config.data.TEST_PRODUCT_RM_GIFT.COUNTRY,
            config.data.TEST_PRODUCT_RM_GIFT.LANGUAGE,
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        product_id = product_response.content["product_id"]
        assert_that(product_id, not_none())
        config.log.info('product id: {0}'.format(product_id))

        cost = product_response.content['price']['real_price']
        assert_that(cost, not_none())
        config.log.info('cost: {0}'.format(cost['code']))
        config.log.info('amount: {0}'.format(cost['amount']))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            tx_id=str(uuid.uuid4()),
            country=config.data.TEST_PRODUCT_RM_GIFT.COUNTRY,
            language=config.data.TEST_PRODUCT_RM_GIFT.LANGUAGE,
            payer_wgid=config.store.wgid,
            payer_email=config.store.account.email,
            receiver_wgid=config.store.wgid,
            products=[PurchaseProductItem(product_id, 1, [])],
            payment_type=PurchaseUtil.PaymentType.PSA,
            expected_price=CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_PRODUCT_RM_GIFT.STOREFRONT,
            client_payment_method_id=client_payment_method_id,
            gift={"enabled": True, "message": "gift message"}
        )
        purchase_response.expect_failure()
        assert_that(purchase_response.content['body']['result_code'], equal_to(error_message))

    @pytest.mark.skip_for_regions('trie', 'wgt1')
    @pytest.allure.feature('server')
    @pytest.allure.story('purchase gift product with money pm product')
    @pytest.allure.severity(severity_level.MINOR)
    def test_purchase_gift_product_with_money_pm_gift_false(self, config):
        config.log.info('product code: {0}'.format(config.data.TEST_PRODUCT_RM_GIFT.PRODUCT))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT_RM_GIFT.PRODUCT],
            config.store.wgid,
            config.data.TEST_PRODUCT_RM_GIFT.COUNTRY,
            config.data.TEST_PRODUCT_RM_GIFT.LANGUAGE,
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        product_id = product_response.content["product_id"]
        assert_that(product_id, not_none())
        config.log.info('product id: {0}'.format(product_id))

        cost = product_response.content['price']['real_price']
        assert_that(cost, not_none())
        config.log.info('cost: {0}'.format(cost['code']))
        config.log.info('amount: {0}'.format(cost['amount']))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            tx_id=str(uuid.uuid4()),
            country=config.data.TEST_PRODUCT_RM_GIFT.COUNTRY,
            language=config.data.TEST_PRODUCT_RM_GIFT.LANGUAGE,
            payer_wgid=config.store.wgid,
            payer_email=config.store.account.email,
            receiver_wgid=config.store.wgid,
            products=[PurchaseProductItem(product_id, 1, [])],
            payment_type=PurchaseUtil.PaymentType.PSA,
            expected_price=CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_PRODUCT_RM_GIFT.STOREFRONT,
            client_payment_method_id=product_response.content['client_payment_methods'][0],
            gift={"enabled": False, "message": "gift message"}
        )
        purchase_response.assert_is_success()

        assert_that(purchase_response.content['body'], has_key('required_action'))
        assert_that(purchase_response.content['body']['required_action'], has_key('action_code'))

        url = purchase_response.content['body']['required_action']['action_data']['payment_url']
        config.log.info('commerce url: {0}'.format(url))
        money_request = RequestBuilder(url).get(verify=False)
        money_request.assert_is_success()
        assert_that(money_request.is_html)

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase gift product with money pm product')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('gift', [-1, 0, .50, '', False, 'str', []])
    def test_purchase_gift_product_with_money_pm_should_fail_with_incorrect_gift(self, config, gift):
        config.log.info('product code: {0}'.format(config.data.TEST_PRODUCT_RM_GIFT.PRODUCT))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT_RM_GIFT.PRODUCT],
            config.store.wgid,
            config.data.TEST_PRODUCT_RM_GIFT.COUNTRY,
            config.data.TEST_PRODUCT_RM_GIFT.LANGUAGE,
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        product_id = product_response.content["product_id"]
        assert_that(product_id, not_none())
        config.log.info('product id: {0}'.format(product_id))

        cost = product_response.content['price']['real_price']
        assert_that(cost, not_none())
        config.log.info('cost: {0}'.format(cost['code']))
        config.log.info('amount: {0}'.format(cost['amount']))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            tx_id=str(uuid.uuid4()),
            country=config.data.TEST_PRODUCT_RM_GIFT.COUNTRY,
            language=config.data.TEST_PRODUCT_RM_GIFT.LANGUAGE,
            payer_wgid=config.store.wgid,
            payer_email=config.store.account.email,
            receiver_wgid=config.store.wgid,
            products=[PurchaseProductItem(product_id, 1, [])],
            payment_type=PurchaseUtil.PaymentType.PSA,
            expected_price=CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_PRODUCT_RM_GIFT.STOREFRONT,
            client_payment_method_id=product_response.content['client_payment_methods'][0],
            gift=gift
        )
        purchase_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                         result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase gift product with money pm product')
    @pytest.allure.severity(severity_level.MINOR)
    def test_purchase_gift_product_with_money_pm_should_fail_with_no_gift_enable(self, config):
        config.log.info('product code: {0}'.format(config.data.TEST_PRODUCT_RM_GIFT.PRODUCT))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT_RM_GIFT.PRODUCT],
            config.store.wgid,
            config.data.TEST_PRODUCT_RM_GIFT.COUNTRY,
            config.data.TEST_PRODUCT_RM_GIFT.LANGUAGE,
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        product_id = product_response.content["product_id"]
        assert_that(product_id, not_none())
        config.log.info('product id: {0}'.format(product_id))

        cost = product_response.content['price']['real_price']
        assert_that(cost, not_none())
        config.log.info('cost: {0}'.format(cost['code']))
        config.log.info('amount: {0}'.format(cost['amount']))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            tx_id=str(uuid.uuid4()),
            country=config.data.TEST_PRODUCT_RM_GIFT.COUNTRY,
            language=config.data.TEST_PRODUCT_RM_GIFT.LANGUAGE,
            payer_wgid=config.store.wgid,
            payer_email=config.store.account.email,
            receiver_wgid=config.store.wgid,
            products=[PurchaseProductItem(product_id, 1, [])],
            payment_type=PurchaseUtil.PaymentType.PSA,
            expected_price=CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_PRODUCT_RM_GIFT.STOREFRONT,
            client_payment_method_id=product_response.content['client_payment_methods'][0],
            gift={"message": "gift message"}
        )
        purchase_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR)

    @pytest.mark.skip_for_regions('wgt1')
    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product with money pm product')
    @pytest.allure.severity(severity_level.NORMAL)
    def test_purchase_product_with_money_pm_gg_receiver_country(self, config):
        # FREYA-675

        config.log.info('product code: {0}'.format(config.data.TEST_PM.PRODUCT))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PM.PRODUCT],
            config.store.wgid,
            config.data.TEST_PM.COUNTRY,
            config.data.TEST_PM.LANGUAGE,
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        product_id = product_response.content["product_id"]
        assert_that(product_id, not_none())
        config.log.info('product id: {0}'.format(product_id))

        cost = product_response.content['price']['real_price']
        assert_that(cost, not_none())
        config.log.info('cost: {0}'.format(cost['code']))
        config.log.info('amount: {0}'.format(cost['amount']))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            'GG',
            config.data.TEST_PM.LANGUAGE,
            config.store.wgid,
            config.store.account.email,
            config.store.wgid,
            [PurchaseProductItem(product_id, 1, [])],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem('EUR', '18.00'),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_PM.STOREFRONT,
            client_payment_method_id=product_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

        assert_that(purchase_response.content['body'], has_key('required_action'))
        assert_that(purchase_response.content['body']['required_action'], has_key('action_code'))

        url = purchase_response.content['body']['required_action']['action_data']['payment_url']
        config.log.info('commerce url: {0}'.format(url))
        money_request = RequestBuilder(url).get(verify=False)
        money_request.assert_is_success()
        assert_that(money_request.is_html)

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product with money pm product')
    @pytest.allure.severity(severity_level.NORMAL)
    def test_purchase_product_with_money_pm_country_mismatch(self, config):
        config.log.info('product code: {0}'.format(config.data.TEST_PM.PRODUCT))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PM.PRODUCT],
            config.store.wgid,
            config.data.TEST_PM.COUNTRY,
            config.data.TEST_PM.LANGUAGE,
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        product_id = product_response.content["product_id"]
        assert_that(product_id, not_none())
        config.log.info('product id: {0}'.format(product_id))

        cost = product_response.content['price']['real_price']
        assert_that(cost, not_none())
        config.log.info('cost: {0}'.format(cost['code']))
        config.log.info('amount: {0}'.format(cost['amount']))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            'GG',
            config.data.TEST_PM.LANGUAGE,
            config.store.wgid,
            config.store.account.email,
            config.store.wgid,
            [PurchaseProductItem(product_id, 1, [])],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_PM.STOREFRONT,
            client_payment_method_id=product_response.content['client_payment_methods'][0]
        )
        purchase_response.expect_failure(result_code=ResponseMessage.COUNTRY_EXPECTED_MISMATCH)

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product with money pm product')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('receiver_country', ['UNDEFINED', 'ZZ'])
    def test_purchase_product_with_money_pm_undefined_country(self, config, receiver_country):
        #  PRODO-613
        # Should fail when country is undefined (e.g. 'UNDEFINED', 'ZZ' is undefined)
        config.log.info('product code: {0}'.format(config.data.TEST_PM.PRODUCT))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PM.PRODUCT],
            config.store.wgid,
            config.data.TEST_PM.COUNTRY,
            config.data.TEST_PM.LANGUAGE,
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        product_id = product_response.content["product_id"]
        assert_that(product_id, not_none())
        config.log.info('product id: {0}'.format(product_id))

        cost = product_response.content['price']['real_price']
        assert_that(cost, not_none())
        config.log.info('cost: {0}'.format(cost['code']))
        config.log.info('amount: {0}'.format(cost['amount']))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            receiver_country,
            config.data.TEST_PM.LANGUAGE,
            config.store.wgid,
            config.store.account.email,
            config.store.wgid,
            [PurchaseProductItem(product_id, 1, [])],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_PM.STOREFRONT,
            client_payment_method_id=product_response.content['client_payment_methods'][0]
        )
        purchase_response.expect_failure(result_code=ResponseMessage.COUNTRY_NOT_DEFINED)

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product with money pm product')
    @pytest.allure.severity(severity_level.NORMAL)
    def test_purchase_product_with_money_should_fail_restricted_countries(self, config):
        #  PRODO-613
        # Should fail when country is restricted (e.g. BY is restricted in product)
        config.log.info('product code: {0}'.format(config.data.TEST_PM_RESTRICTED.PRODUCT))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PM_RESTRICTED.PRODUCT],
            config.store.wgid,
            config.data.TEST_PM_RESTRICTED.COUNTRY,
            config.data.TEST_PM_RESTRICTED.LANGUAGE,
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        product_id = product_response.content["product_id"]
        assert_that(product_id, not_none())
        config.log.info('product id: {0}'.format(product_id))

        cost = product_response.content['price']['real_price']
        assert_that(cost, not_none())
        config.log.info('cost: {0}'.format(cost['code']))
        config.log.info('amount: {0}'.format(cost['amount']))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            'BY',
            config.data.TEST_PM_RESTRICTED.LANGUAGE,
            config.store.wgid,
            config.store.account.email,
            config.store.wgid,
            [PurchaseProductItem(product_id, 1, [])],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            receiver_country=config.data.TEST_PM_RESTRICTED.RESTRICTED_COUNTRY,
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_PM_RESTRICTED.STOREFRONT,
            client_payment_method_id=RequestConstants.PaymentGroupID.DEFAULT
        )
        purchase_response.expect_failure(result_code=ResponseMessage.PRODUCT_NOT_ALLOWED)

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase gift product with money pm product')
    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('payer_country', ['US', 'BY'])
    def test_purchase_gift_product_with_money_pm_restricted_countries_and_payer_restriction(self, config,
                                                                                            payer_country):
        #  PRODO-613
        # Should fail when payer country is restricted (e.g. BY is restricted in product)
        # Should success if not PRODO-1174
        config.log.info('product code: {0}'.format(config.data.TEST_PM_RESTRICTED.PRODUCT))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PM_RESTRICTED.PRODUCT],
            config.store.wgid,
            'US',
            config.data.TEST_PM_RESTRICTED.LANGUAGE,
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        product_id = product_response.content["product_id"]
        assert_that(product_id, not_none())
        config.log.info('product id: {0}'.format(product_id))

        cost = product_response.content['price']['real_price']
        assert_that(cost, not_none())
        config.log.info('cost: {0}'.format(cost['code']))
        config.log.info('amount: {0}'.format(cost['amount']))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            tx_id=str(uuid.uuid4()),
            country=payer_country,
            language=config.data.TEST_PM_RESTRICTED.LANGUAGE,
            payer_wgid=config.store.wgid,
            payer_email=config.store.account.email,
            receiver_wgid=config.store.wgid,
            products=[PurchaseProductItem(product_id, 1, [])],
            payment_type=PurchaseUtil.PaymentType.PSA,
            expected_price=CurrencyItem(cost['code'], cost['amount']),
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_PM_RESTRICTED.STOREFRONT,
            receiver_country=config.data.TEST_PM_RESTRICTED.RESTRICTED_COUNTRY,
            client_payment_method_id=RequestConstants.PaymentGroupID.DEFAULT,
            gift={"enabled": True, "message": "gift message"}
        )
        if payer_country != 'BY':
            purchase_response.assert_is_success()
        else:
            purchase_response.expect_failure(result_code=ResponseMessage.PRODUCT_NOT_ALLOWED)

    @pytest.mark.skip_for_regions('wgt1')
    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product with money pm product')
    @pytest.allure.severity(severity_level.NORMAL)
    def test_purchase_product_with_money_should_succeed_non_restricted_countries(self, config):
        #  PRODO-613
        # Should pass when country is not restricted (e.g. RU is allowed in product)
        config.log.info('product code: {0}'.format(config.data.TEST_PM_RESTRICTED.PRODUCT))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PM_RESTRICTED.PRODUCT],
            config.store.wgid,
            config.data.TEST_PM_RESTRICTED.COUNTRY,
            config.data.TEST_PM_RESTRICTED.LANGUAGE,
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        product_id = product_response.content["product_id"]
        assert_that(product_id, not_none())
        config.log.info('product id: {0}'.format(product_id))

        cost = product_response.content['price']['real_price']
        assert_that(cost, not_none())
        config.log.info('cost: {0}'.format(cost['code']))
        config.log.info('amount: {0}'.format(cost['amount']))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_PM_RESTRICTED.COUNTRY,
            config.data.TEST_PM_RESTRICTED.LANGUAGE,
            config.store.wgid,
            config.store.account.email,
            config.store.wgid,
            [PurchaseProductItem(product_id, 1, [])],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(cost['code'], cost['amount']),
            receiver_country='US',
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_PM_RESTRICTED.STOREFRONT,
            client_payment_method_id=product_response.content['client_payment_methods'][0]
        )
        purchase_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('purchase product with money pm product')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_code_type, result_code', [('', ResponseMessage.VALIDATION_ERROR),
                                                                (None, ResponseMessage.VALIDATION_ERROR),
                                                                (True, ResponseMessage.COUNTRY_EXPECTED_MISMATCH),
                                                                (-1, ResponseMessage.COUNTRY_EXPECTED_MISMATCH)])
    def test_purchase_product_with_money_should_fail_when_expected_currency_code_is_invalid(self, config,
                                                                                            invalid_code_type,
                                                                                            result_code):
        config.log.info('product code: {0}'.format(config.data.TEST_PM_RESTRICTED.PRODUCT))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PM_RESTRICTED.PRODUCT],
            config.store.wgid,
            config.data.TEST_PM_RESTRICTED.COUNTRY,
            config.data.TEST_PM_RESTRICTED.LANGUAGE,
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        product_id = product_response.content["product_id"]
        assert_that(product_id, not_none())
        config.log.info('product id: {0}'.format(product_id))

        cost = product_response.content['price']['real_price']
        assert_that(cost, not_none())
        config.log.info('cost: {0}'.format(cost['code']))
        config.log.info('amount: {0}'.format(cost['amount']))

        purchase_response = config.freya.server_gateway.purchase_product_with_money_v2(
            str(uuid.uuid4()),
            config.data.TEST_PM_RESTRICTED.COUNTRY,
            config.data.TEST_PM_RESTRICTED.LANGUAGE,
            config.store.wgid,
            config.store.account.email,
            config.store.wgid,
            [PurchaseProductItem(product_id, 1, [])],
            PurchaseUtil.PaymentType.PSA,
            CurrencyItem(invalid_code_type, cost['amount']),
            receiver_country='US',
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_PM_RESTRICTED.STOREFRONT,
            client_payment_method_id=product_response.content['client_payment_methods'][0]
        )
        purchase_response.expect_failure(result_code=result_code)
