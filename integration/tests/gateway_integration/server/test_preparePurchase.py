import uuid

import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities, PurchaseUtil
from integration.main.helpers.utils import tid, cid
from integration.main.request import RequestBuilder, RequestConstants
from integration.main.request.constants import ResponseMessage
from integration.main.services import CurrencyItem, PurchaseProductItem, GoogleAnalyticsItem


@pytest.mark.skip_for_regions('trie', 'wgt1')
@pytest.mark.notprodsafe
@pytest.allure.feature('server')
@pytest.allure.story('prepare purchase')
class TestPreparePurchase(object):

    @pytest.fixture
    def account_setup(self, config):
        ###
        # Test setup
        config.store.account = AccountUtilities.create_account(attrs='user_stated_country=ZZ')
        account_created = config.spa.http.create_account(config.store.account.__dict__)
        account_created.assert_is_success()
        update_account = config.spa.http.update(account_created.content['id'],
                                                game=config.environment['test_title_pgn'])
        update_account.assert_is_success()
        config.store.wgid = account_created.content['id']
        config.store.profile_id = account_created.content['id']

        bind_response = config.psa.service.bind(
            config.store.wgid,
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            PurchaseUtil.PaymentNone.PAYPAL_NONCE
        )
        bind_response.assert_is_success()

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(config.store.wgid)
        delete_response.assert_is_success()

    @pytest.fixture
    def currency_product_setup(self, config, account_setup):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_MONEY.PRODUCT_CODE],
            config.store.profile_id,
            config.data.TEST_MONEY.COUNTRY,
            config.data.TEST_MONEY.LANGUAGE
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        config.store.product_id = product_response.content["product_id"]
        assert_that(config.store.product_id, not_none())

        config.store.cost = product_response.content['price']['real_price']
        assert_that(config.store.cost, not_none())

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here

    @pytest.fixture
    def currency_product_restricted_setup(self, config, account_setup):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PM_RESTRICTED.PRODUCT],
            config.store.profile_id,
            config.data.TEST_PM_RESTRICTED.COUNTRY,
            config.data.TEST_PM_RESTRICTED.LANGUAGE
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        config.store.product_id = product_response.content["product_id"]
        assert_that(config.store.product_id, not_none())

        config.store.cost = product_response.content['price']['real_price']
        assert_that(config.store.cost, not_none())

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here

    @pytest.fixture
    def entitlement_product_setup(self, config, account_setup):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT_REAL_PRICE.CODE],
            config.store.profile_id,
            config.data.TEST_PRODUCT_REAL_PRICE.COUNTRY,
            config.data.TEST_PRODUCT_REAL_PRICE.LANGUAGE
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        config.store.product_id = product_response.content["product_id"]
        assert_that(config.store.product_id, not_none())

        config.store.cost = product_response.content['price']['real_price']
        assert_that(config.store.cost, not_none())

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here

    @pytest.fixture
    def full_product_setup(self, config, account_setup):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT_FULL_REAL_PRICE.CODE],
            config.store.profile_id,
            config.data.TEST_PRODUCT_FULL_REAL_PRICE.COUNTRY,
            config.data.TEST_PRODUCT_FULL_REAL_PRICE.LANGUAGE
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        config.store.product_id = product_response.content["product_id"]
        assert_that(config.store.product_id, not_none())

        config.store.cost = product_response.content['price']['real_price']
        assert_that(config.store.cost, not_none())

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here

    @pytest.fixture
    def variable_product_setup(self, config, account_setup):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE],
            config.store.profile_id,
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        config.store.product_id = product_response.content["product_id"]
        assert_that(config.store.product_id, not_none())

        config.store.cost = product_response.content['price']['real_price']
        assert_that(config.store.cost, not_none())

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here

    @pytest.fixture
    def fetch_product_list_setup(self, config, account_setup):
        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_STORE_FULL.STOREFRONT,
            config.store.wgid,
            config.data.TEST_STORE_FULL.COUNTRY,
            config.data.TEST_STORE_FULL.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        product_uriList = fetch_response.content['body']['uriList']
        product_info = next((product for product in PurchaseUtil.get_product_infos(product_uriList)
                             if product['product_code'] == config.data.TEST_PRODUCT_FULL_REAL_PRICE.CODE), None)

        config.store.product_id = product_info["product_id"]
        assert_that(config.store.product_id, not_none())

        config.store.cost = product_info['price']['real_price']
        assert_that(config.store.cost, not_none())

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here

    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_prepare_purchase_should_succeed_when_preparing_product_with_test_currency_for_purchase(self, config,
                                                                                                    currency_product_setup,
                                                                                                    content_type):
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_MONEY.COUNTRY,
            config.data.TEST_MONEY.LANGUAGE,
            config.store.wgid,
            config.store.wgid,
            [PurchaseProductItem(config.store.product_id, 1)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(config.store.cost['code'], config.store.cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            payer_current_ip='127.0.0.1',
            content_type=content_type,
            storefront=config.data.TEST_MONEY.STOREFRONT
        )
        prepare_response.assert_is_success()
        assert_that(prepare_response.content['body'], has_key('required_action'))
        assert_that(prepare_response.content['body']['required_action'], has_key('action_code'))
        assert_that(prepare_response.content['body']['required_action'], has_key('action_data'))
        assert_that(prepare_response.content['body']['required_action']['action_data']['payment_data'],
                    has_key('currency_code'))
        assert_that(prepare_response.content['body']['required_action']['action_data']['payment_data'],
                    has_key('amount'))

    @pytest.allure.severity(severity_level.NORMAL)
    def test_prepare_purchase_should_fail_restricted_country(self, config,
                                                             currency_product_restricted_setup
                                                             ):
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_PM_RESTRICTED.RESTRICTED_COUNTRY,
            config.data.TEST_PM_RESTRICTED.LANGUAGE,
            config.store.wgid,
            config.store.wgid,
            [PurchaseProductItem(config.store.product_id, 1)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(config.store.cost['code'], config.store.cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_PM_RESTRICTED.STOREFRONT
        )
        prepare_response.expect_failure(result_code=ResponseMessage.PRODUCT_NOT_ALLOWED)

    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_prepare_purchase_should_succeed_when_preparing_product_with_entitlement_for_purchase(self, config,
                                                                                                  entitlement_product_setup,
                                                                                                  content_type):
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_REAL_PRICE.COUNTRY,
            config.data.TEST_PRODUCT_REAL_PRICE.LANGUAGE,
            config.store.profile_id,
            config.store.profile_id,
            [PurchaseProductItem(config.store.product_id, 1)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(config.store.cost['code'], config.store.cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            content_type=content_type,
            storefront=config.data.TEST_PRODUCT_REAL_PRICE.STOREFRONT
        )
        prepare_response.assert_is_success()
        assert_that(prepare_response.content['body'], has_key('required_action'))
        assert_that(prepare_response.content['body']['required_action'], has_key('action_code'))
        assert_that(prepare_response.content['body']['required_action'], has_key('action_data'))
        assert_that(prepare_response.content['body']['required_action']['action_data']['payment_data'],
                    has_key('currency_code'))
        assert_that(prepare_response.content['body']['required_action']['action_data']['payment_data'],
                    has_key('amount'))

    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_prepare_purchase_should_succeed_when_preparing_product_with_test_currency_and_entitlement_for_purchase(
            self, config, full_product_setup, content_type):
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_FULL_REAL_PRICE.COUNTRY,
            config.data.TEST_PRODUCT_FULL_REAL_PRICE.LANGUAGE,
            config.store.profile_id,
            config.store.profile_id,
            [PurchaseProductItem(config.store.product_id, 1)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(config.store.cost['code'], config.store.cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            content_type=content_type,
            storefront=config.data.TEST_PRODUCT_FULL_REAL_PRICE.STOREFRONT
        )
        prepare_response.assert_is_success()
        assert_that(prepare_response.content['body'], has_key('required_action'))
        assert_that(prepare_response.content['body']['required_action'], has_key('action_code'))
        assert_that(prepare_response.content['body']['required_action'], has_key('action_data'))
        assert_that(prepare_response.content['body']['required_action']['action_data']['payment_data'],
                    has_key('currency_code'))
        assert_that(prepare_response.content['body']['required_action']['action_data']['payment_data'],
                    has_key('amount'))

    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    @pytest.mark.parametrize('quantity', [1, 10000])
    def test_prepare_purchase_should_succeed_when_preparing_variable_priced_product_with_test_currency_for_purchase(
            self, config, variable_product_setup, content_type, quantity):
        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            quantity
        )
        fetch_response.assert_is_success()
        fetch_cost = fetch_response.content['body']['price']['real_price']['amount']

        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            config.store.profile_id,
            [PurchaseProductItem(config.store.product_id, quantity)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(config.store.cost['code'], fetch_cost),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            content_type=content_type,
            storefront=config.data.TEST_PRODUCT_VARIABLE.STOREFRONT
        )
        prepare_response.assert_is_success()
        assert_that(prepare_response.content['body'], has_key('required_action'))
        assert_that(prepare_response.content['body']['required_action'], has_key('action_code'))
        assert_that(prepare_response.content['body']['required_action'], has_key('action_data'))
        assert_that(prepare_response.content['body']['required_action']['action_data']['payment_data'],
                    has_key('currency_code'))
        assert_that(prepare_response.content['body']['required_action']['action_data']['payment_data'],
                    has_key('amount'))

    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_prepare_purchase_should_succeed_when_preparing_product_with_info_from_fetch_product_list(self, config,
                                                                                                      fetch_product_list_setup,
                                                                                                      content_type):
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_FULL_REAL_PRICE.COUNTRY,
            config.data.TEST_PRODUCT_FULL_REAL_PRICE.LANGUAGE,
            config.store.profile_id,
            config.store.profile_id,
            [PurchaseProductItem(config.store.product_id, 1)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(config.store.cost['code'], config.store.cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            content_type=content_type,
            storefront=config.data.TEST_PRODUCT_FULL_REAL_PRICE.STOREFRONT
        )
        prepare_response.assert_is_success()
        assert_that(prepare_response.content['body'], has_key('required_action'))
        assert_that(prepare_response.content['body']['required_action'], has_key('action_code'))
        assert_that(prepare_response.content['body']['required_action'], has_key('action_data'))
        assert_that(prepare_response.content['body']['required_action']['action_data']['payment_data'],
                    has_key('currency_code'))
        assert_that(prepare_response.content['body']['required_action']['action_data']['payment_data'],
                    has_key('amount'))

    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_transaction_id', [
        '00000000-0000-0000-0000-00000000000000',
        '00000000-0000-0000-0000-0000000000',
        '00000000-0000-XXXX-0000-000000000000',
        'bad_transaction_id',
        0,
        -1
    ])
    def test_prepare_purchase_should_fail_when_transaction_id_is_invalid(self, config, currency_product_setup,
                                                                         invalid_transaction_id):
        prepare_response = config.freya.server_gateway.prepare_purchase(
            invalid_transaction_id,
            config.data.TEST_MONEY.COUNTRY,
            config.data.TEST_MONEY.LANGUAGE,
            config.store.profile_id,
            config.store.profile_id,
            [PurchaseProductItem(config.store.product_id, 1)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(config.store.cost['code'], config.store.cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            storefront=config.data.TEST_MONEY.STOREFRONT
        )
        prepare_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                        result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_country', [
        '',
        'invalid_country',
        'G1sMaHUbGxePOvjUm7Qo5YsBuBgkEYJ2l21u3qIg1gIj8u2ITd9mnbrVMMOLVGPtVEZaDdgTEheXg3vKnwz7Y4fe24f41StTGD5J',
        -1
    ])
    def test_prepare_purchase_should_fail_when_country_is_invalid(self, config, currency_product_setup,
                                                                  invalid_country):
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            invalid_country,
            config.data.TEST_MONEY.LANGUAGE,
            config.store.profile_id,
            config.store.profile_id,
            [PurchaseProductItem(config.store.product_id, 1)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(config.store.cost['code'], config.store.cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            storefront=config.data.TEST_MONEY.STOREFRONT
        )
        prepare_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                        result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.severity(severity_level.MINOR)
    def test_prepare_purchase_should_fail_when_country_is_none(self, config, currency_product_setup):
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            None,
            config.data.TEST_MONEY.LANGUAGE,
            config.store.profile_id,
            config.store.profile_id,
            [PurchaseProductItem(config.store.product_id, 1)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(config.store.cost['code'], config.store.cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            storefront=config.data.TEST_MONEY.STOREFRONT
        )
        prepare_response.expect_failure(result_code=ResponseMessage.COUNTRY_NOT_DEFINED)

    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('bad_language', [
        'not_defined',
        'G1sMaHUbGxePOvjUm7Qo5YsBuBgkEYJ2l21u3qIg1gIj8u2ITd9mnbrVMMOLVGPtVEZaDdgTEheXg3vKnwz7Y4fe24f41StTGD5J'
    ])
    def test_prepare_purchase_should_fail_when_language_is_string(self, config, currency_product_setup, bad_language):
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_MONEY.COUNTRY,
            bad_language,
            config.store.profile_id,
            config.store.profile_id,
            [PurchaseProductItem(config.store.product_id, 1)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(config.store.cost['code'], config.store.cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            storefront=config.data.TEST_MONEY.STOREFRONT
        )
        prepare_response.expect_failure(result_code=ResponseMessage.ORDER_PROCESSING_ERROR)

    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_language', ['', None])
    def test_prepare_purchase_should_fail_when_language_is_empty_string_or_none(self, config, currency_product_setup,
                                                                                invalid_language):
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_MONEY.COUNTRY,
            invalid_language,
            config.store.profile_id,
            config.store.profile_id,
            [PurchaseProductItem(config.store.product_id, 1)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(config.store.cost['code'], config.store.cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            storefront=config.data.TEST_MONEY.STOREFRONT
        )
        prepare_response.expect_failure(result_code=ResponseMessage.LANGUAGE_NOT_DEFINED)

    @pytest.allure.severity(severity_level.MINOR)
    def test_prepare_purchase_should_fail_when_language_is_invalid_type(self, config, currency_product_setup):
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_MONEY.COUNTRY,
            -1,
            config.store.profile_id,
            config.store.profile_id,
            [PurchaseProductItem(config.store.product_id, 1)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(config.store.cost['code'], config.store.cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            storefront=config.data.TEST_MONEY.STOREFRONT
        )
        prepare_response.assert_is_success()

    @pytest.allure.severity(severity_level.MINOR)
    def test_prepare_purchase_should_fail_when_payer_wgid_is_wrong_type(self, config, currency_product_setup):
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_MONEY.COUNTRY,
            config.data.TEST_MONEY.LANGUAGE,
            'invalid_wgid',
            config.store.profile_id,
            [PurchaseProductItem(config.store.product_id, 1)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(config.store.cost['code'], config.store.cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            storefront=config.data.TEST_MONEY.STOREFRONT
        )
        prepare_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                        result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('bad_wgid, result_code', [(-1, ResponseMessage.INVALID_PROFILE_ID),
                                                       (0, ResponseMessage.INVALID_PROFILE_ID),
                                                       (.50, ResponseMessage.INVALID_PROFILE_ID),
                                                       ('', ResponseMessage.INVALID_PROFILE_ID),
                                                       (None, ResponseMessage.INVALID_PROFILE_ID)])
    def test_prepare_purchase_should_fail_when_payer_wgid_is_invalid(self, config, currency_product_setup,
                                                                     bad_wgid, result_code):
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_MONEY.COUNTRY,
            config.data.TEST_MONEY.LANGUAGE,
            bad_wgid,
            config.store.profile_id,
            [PurchaseProductItem(config.store.product_id, 1)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(config.store.cost['code'], config.store.cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            storefront=config.data.TEST_MONEY.STOREFRONT
        )
        prepare_response.expect_failure(result_code=result_code)

    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_wgid, result_code', [(-1, ResponseMessage.INVALID_PROFILE_ID),
                                                           (0, ResponseMessage.INVALID_PROFILE_ID),
                                                           (.50, ResponseMessage.INVALID_PROFILE_ID),
                                                           ('', ResponseMessage.INVALID_PROFILE_ID),
                                                           (None, ResponseMessage.INVALID_PROFILE_ID)])
    def test_prepare_purchase_should_fail_when_receiver_wgid_is_invalid(self, config, currency_product_setup,
                                                                        invalid_wgid, result_code):
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_MONEY.COUNTRY,
            config.data.TEST_MONEY.LANGUAGE,
            config.store.profile_id,
            invalid_wgid,
            [PurchaseProductItem(config.store.product_id, 1)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(config.store.cost['code'], config.store.cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            storefront=config.data.TEST_MONEY.STOREFRONT
        )
        prepare_response.expect_failure(result_code=result_code)

    @pytest.allure.severity(severity_level.MINOR)
    def test_prepare_purchase_should_fail_when_receiver_wgid_is_wrong_type(self, config, currency_product_setup):
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_MONEY.COUNTRY,
            config.data.TEST_MONEY.LANGUAGE,
            config.store.profile_id,
            'bad_wgid',
            [PurchaseProductItem(config.store.product_id, 1)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(config.store.cost['code'], config.store.cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            storefront=config.data.TEST_MONEY.STOREFRONT
        )
        prepare_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                        result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.xfail(reason='PLAT-6256', raises=AssertionError)
    @pytest.mark.parametrize('invalid_email', [
        -1,
        10000,
        0.05,
        '',
        'plainaddress',
        '#@%^%#$@#$@#.com',
        '@wargaming.net',
        'email.wargaming.net',
        'email@wargaming@wargaming.net',
        'email@wargaming..net',
        True
    ])
    def test_prepare_purchase_should_fail_when_email_is_invalid(self, config, currency_product_setup, invalid_email):
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_MONEY.COUNTRY,
            config.data.TEST_MONEY.LANGUAGE,
            config.store.profile_id,
            config.store.profile_id,
            [PurchaseProductItem(config.store.product_id, 1)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(config.store.cost['code'], config.store.cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            payer_email=invalid_email,
            storefront=config.data.TEST_MONEY.STOREFRONT
        )
        prepare_response.expect_failure(result_code=ResponseMessage.ORDER_PROCESSING_ERROR)

    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_amount', [
        -1,
        0,
        '',
        None
    ])
    def test_prepare_purchase_should_fail_when_product_amount_is_invalid(self, config, currency_product_setup,
                                                                         invalid_amount):
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_MONEY.COUNTRY,
            config.data.TEST_MONEY.LANGUAGE,
            config.store.profile_id,
            config.store.profile_id,
            [PurchaseProductItem(config.store.product_id, invalid_amount)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(config.store.cost['code'], config.store.cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            storefront=config.data.TEST_MONEY.STOREFRONT
        )
        prepare_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR)

    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('float_amount, result_code', [
        (.50, ResponseMessage.VALIDATION_ERROR)
    ])
    def test_prepare_purchase_should_fail_when_amount_is_under_1(self, config, currency_product_setup,
                                                                 float_amount, result_code):
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_MONEY.COUNTRY,
            config.data.TEST_MONEY.LANGUAGE,
            config.store.profile_id,
            config.store.profile_id,
            [PurchaseProductItem(config.store.product_id, float_amount)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(config.store.cost['code'], config.store.cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            storefront=config.data.TEST_MONEY.STOREFRONT
        )
        prepare_response.expect_failure(result_code=result_code)

    @pytest.allure.severity(severity_level.MINOR)
    def test_prepare_purchase_should_success_when_amount_is_float(self, config, currency_product_setup):
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_MONEY.COUNTRY,
            config.data.TEST_MONEY.LANGUAGE,
            config.store.profile_id,
            config.store.profile_id,
            [PurchaseProductItem(config.store.product_id, 1.3)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(config.store.cost['code'], config.store.cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            storefront=config.data.TEST_MONEY.STOREFRONT
        )
        prepare_response.assert_success()

    @pytest.mark.notprodsafe
    @pytest.mark.notpreprodsafe
    @pytest.allure.severity(severity_level.MINOR)
    def test_prepare_purchase_should_fail_when_amount_is_wrong_type(self, config, currency_product_setup):
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_MONEY.COUNTRY,
            config.data.TEST_MONEY.LANGUAGE,
            config.store.profile_id,
            config.store.profile_id,
            [PurchaseProductItem(config.store.product_id, 'bad_amount')],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(config.store.cost['code'], config.store.cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            storefront=config.data.TEST_MONEY.STOREFRONT
        )
        prepare_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                        result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_product_id', [
        -1,
        0,
        .50,
        'bad_product_id',
        '3kIWAOOG8xWF28oJakAWblSflHoQ5EZpRA6f3oNXHFaueV8McSskVVbUe2zzhRIGI7Qx0vsEVnWPqmIbfgTnbncM7XqIduVU9OC1'
    ])
    def test_prepare_purchase_should_fail_when_product_id_is_invalid(self, config, currency_product_setup,
                                                                     invalid_product_id):
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_MONEY.COUNTRY,
            config.data.TEST_MONEY.LANGUAGE,
            config.store.profile_id,
            config.store.profile_id,
            [PurchaseProductItem(invalid_product_id, 1)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(config.store.cost['code'], config.store.cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            storefront=config.data.TEST_MONEY.STOREFRONT
        )
        prepare_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                        result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('bad_product_id', [None, ''])
    def test_prepare_purchase_should_fail_when_product_id_is_empty_string_or_none(self, config,
                                                                                  currency_product_setup,
                                                                                  bad_product_id):
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_MONEY.COUNTRY,
            config.data.TEST_MONEY.LANGUAGE,
            config.store.profile_id,
            config.store.profile_id,
            [PurchaseProductItem(bad_product_id, 1)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(config.store.cost['code'], config.store.cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            storefront=config.data.TEST_MONEY.STOREFRONT
        )
        prepare_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR)

    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_amount, result_code', [(-1, ResponseMessage.VALIDATION_ERROR),
                                                             (0, ResponseMessage.EXPECTED_PRICE_MISMATCH),
                                                             (.50, ResponseMessage.EXPECTED_PRICE_MISMATCH),
                                                             (1.3, ResponseMessage.EXPECTED_PRICE_MISMATCH)])
    def test_prepare_purchase_should_fail_when_expected_price_amount_is_invalid(self, config, currency_product_setup,
                                                                                invalid_amount, result_code):
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_MONEY.COUNTRY,
            config.data.TEST_MONEY.LANGUAGE,
            config.store.profile_id,
            config.store.profile_id,
            [PurchaseProductItem(config.store.product_id, 1)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(config.store.cost['code'], invalid_amount),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            storefront=config.data.TEST_MONEY.STOREFRONT
        )
        prepare_response.expect_failure(result_code=result_code)

    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('bad_amount, result_code', [('', ResponseMessage.VALIDATION_ERROR),
                                                         (None, ResponseMessage.VALIDATION_ERROR),
                                                         ('bad_amount', ResponseMessage.VALIDATION_ERROR)])
    def test_prepare_purchase_should_fail_when_expected_price_amount_is_wrong_type(self, config, currency_product_setup,
                                                                                   bad_amount, result_code):
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_MONEY.COUNTRY,
            config.data.TEST_MONEY.LANGUAGE,
            config.store.profile_id,
            config.store.profile_id,
            [PurchaseProductItem(config.store.product_id, 1)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(config.store.cost['code'], bad_amount),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            storefront=config.data.TEST_MONEY.STOREFRONT
        )
        prepare_response.expect_failure(result_code=result_code)

    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_product_code, result_code', [
        (-1, ResponseMessage.COUNTRY_EXPECTED_MISMATCH),
        (0, ResponseMessage.COUNTRY_EXPECTED_MISMATCH),
        (.50, ResponseMessage.COUNTRY_EXPECTED_MISMATCH),
        ('bad_product_code', ResponseMessage.COUNTRY_EXPECTED_MISMATCH),
        ('3kIWAOOG8xWF28oJakAWblSflHoQ5EZpRA6f3oNXHFaueV8McSskVVbUe2zzhRIGI7Qx0vsEVnWPqmIbfgTnbncM7XqIduVU9OC1',
         ResponseMessage.COUNTRY_EXPECTED_MISMATCH),
        (None, ResponseMessage.VALIDATION_ERROR),
        ('', ResponseMessage.VALIDATION_ERROR)
    ])
    def test_prepare_purchase_should_fail_when_expected_price_product_code_is_invalid(self, config,
                                                                                      currency_product_setup,
                                                                                      invalid_product_code,
                                                                                      result_code):
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_MONEY.COUNTRY,
            config.data.TEST_MONEY.LANGUAGE,
            config.store.profile_id,
            config.store.profile_id,
            [PurchaseProductItem(config.store.product_id, 1)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(invalid_product_code, config.store.cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            storefront=config.data.TEST_MONEY.STOREFRONT
        )
        prepare_response.expect_failure(result_code=result_code)

    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_payment_type', [
        '',
        'invalid_payment_type',
        'G1sMaHUbGxePOvjUm7Qo5YsBuBgkEYJ2l21u3qIg1gIj8u2ITd9mnbrVMMOLVGPtVEZaDdgTEheXg3vKnwz7Y4fe24f41StTGD5J',
        -1
    ])
    def test_prepare_purchase_should_fail_when_payment_type_is_invalid(self, config, currency_product_setup,
                                                                       invalid_payment_type):
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_MONEY.COUNTRY,
            config.data.TEST_MONEY.LANGUAGE,
            config.store.profile_id,
            config.store.profile_id,
            [PurchaseProductItem(config.store.product_id, 1)],
            invalid_payment_type,
            CurrencyItem(config.store.cost['code'], config.store.cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            storefront=config.data.TEST_MONEY.STOREFRONT
        )
        prepare_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                        result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.mark.skip(reason='FREYA-850')
    @pytest.allure.severity(severity_level.MINOR)
    def test_prepare_purchase_should_fail_when_payment_type_is_none(self, config, currency_product_setup):
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_MONEY.COUNTRY,
            config.data.TEST_MONEY.LANGUAGE,
            config.store.profile_id,
            config.store.profile_id,
            [PurchaseProductItem(config.store.product_id, 1)],
            None,
            CurrencyItem(config.store.cost['code'], config.store.cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            storefront=config.data.TEST_MONEY.STOREFRONT
        )
        prepare_response.expect_failure(result_code=ResponseMessage.PAYMENT_TYPE_EXPECTED_MISMATCH,
                                        result_message=ResponseMessage.NO_PAYMENT_TYPE)

    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_payment_group', [0, 1, 5, None])
    def test_prepare_purchase_should_succeed_when_payment_group_id_is_invalid(self, config, currency_product_setup,
                                                                              invalid_payment_group):
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_MONEY.COUNTRY,
            config.data.TEST_MONEY.LANGUAGE,
            config.store.wgid,
            config.store.wgid,
            [PurchaseProductItem(config.store.product_id, 1)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(config.store.cost['code'], config.store.cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            payment_group_id=invalid_payment_group,
            storefront=config.data.TEST_MONEY.STOREFRONT
        )
        prepare_response.assert_success()

    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_payment_method, result_code', [
        ('', ResponseMessage.ORDER_PROCESSING_ERROR),
        ('invalid_payment_method', ResponseMessage.ORDER_PROCESSING_ERROR),
        (None, ResponseMessage.COMMON_EXCEPTION),
        ('G1sMaHUbGxePOvjUm7Qo5YsBuBgkEYJ2l21u3qIg1gIj8u2ITd9mnbrVMMOLVGPtVEZaDdgTEheXg3vKnwz7Y4fe24f41StTGD5J',
         ResponseMessage.ORDER_PROCESSING_ERROR),
        (-1, ResponseMessage.ORDER_PROCESSING_ERROR)
    ])
    def test_prepare_purchase_should_fail_when_payment_method_is_invalid(self, config, currency_product_setup,
                                                                         invalid_payment_method, result_code):
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_MONEY.COUNTRY,
            config.data.TEST_MONEY.LANGUAGE,
            config.store.profile_id,
            config.store.profile_id,
            [PurchaseProductItem(config.store.product_id, 1)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(config.store.cost['code'], config.store.cost['amount']),
            invalid_payment_method,
            storefront=config.data.TEST_MONEY.STOREFRONT
        )
        prepare_response.expect_failure(result_code=result_code)

    @pytest.allure.severity(severity_level.MINOR)
    def test_prepare_purchase_should_fail_when_payment_method_is_none(self, config, currency_product_setup):
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_MONEY.COUNTRY,
            config.data.TEST_MONEY.LANGUAGE,
            config.store.profile_id,
            config.store.profile_id,
            [PurchaseProductItem(config.store.product_id, 1)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(config.store.cost['code'], config.store.cost['amount']),
            None,
            storefront=config.data.TEST_MONEY.STOREFRONT
        )
        prepare_response.expect_failure()

    @pytest.allure.severity(severity_level.NORMAL)
    def test_prepare_purchase_should_fail_with_no_storefront_param_in_req(self, config, currency_product_setup):
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_MONEY.COUNTRY,
            config.data.TEST_MONEY.LANGUAGE,
            config.store.wgid,
            config.store.wgid,
            [PurchaseProductItem(config.store.product_id, 1)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(config.store.cost['code'], config.store.cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            payer_current_ip='127.0.0.1',
            storefront=None
        )
        prepare_response.expect_failure(code=200, result_code=ResponseMessage.STOREFRONT_NOT_DEFINED)

    @pytest.allure.severity(severity_level.NORMAL)
    def test_prepare_purchase_should_succeed_with_ga_params(
            self, config, full_product_setup):
        # FREYA-454
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_MONEY.COUNTRY,
            config.data.TEST_MONEY.LANGUAGE,
            config.store.wgid,
            config.store.wgid,
            [PurchaseProductItem(config.store.product_id, 1)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(config.store.cost['code'], config.store.cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_MONEY.STOREFRONT,
            meta=GoogleAnalyticsItem(tid(), cid()).as_json
        )
        prepare_response.assert_is_success()

    @pytest.allure.severity(severity_level.MINOR)
    def test_prepare_purchase_should_fail_with_no_txid(
            self, config, full_product_setup):
        # FREYA-608
        prepare_response = config.freya.server_gateway.prepare_purchase(
            '',
            config.data.TEST_MONEY.COUNTRY,
            config.data.TEST_MONEY.LANGUAGE,
            config.store.wgid,
            config.store.wgid,
            [PurchaseProductItem(config.store.product_id, 1)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(config.store.cost['code'], config.store.cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            payer_current_ip='127.0.0.1',
            storefront=config.data.TEST_MONEY.STOREFRONT
        )
        prepare_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR)
