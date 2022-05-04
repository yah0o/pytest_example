import uuid

import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities, PurchaseUtil
from integration.main.request import RequestBuilder, RequestConstants
from integration.main.request.constants import ResponseMessage
from integration.main.services import CurrencyItem, PurchaseProductItem


@pytest.mark.skip_for_regions('trie', 'wgt1')
@pytest.mark.notprodsafe
@pytest.mark.notpreprodsafe
@pytest.allure.feature('server')
@pytest.allure.story('commit purchase')
class TestCommitPurchase(object):

    @pytest.fixture(autouse=True)
    def setup(self, config):
        ###
        # Test setup
        account = AccountUtilities.create_account()
        account_created = config.spa.http.create_account(account.__dict__)
        account_created.assert_is_success()
        update_account = config.spa.http.update(account_created.content['id'],
                                                game=config.environment['test_title_pgn'])
        update_account.assert_is_success()

        config.store.wgid = account_created.content['id']


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
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        product_id = product_response.content["product_id"]
        assert_that(product_id, not_none())

        cost = product_response.content['price']['real_price']
        assert_that(cost, not_none())
        prepare_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_MONEY.COUNTRY,
            config.data.TEST_MONEY.LANGUAGE,
            config.store.wgid,
            config.store.wgid,
            [PurchaseProductItem(product_id, 1)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(cost['code'], cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            config.data.TEST_MONEY.STOREFRONT,
            RequestConstants.Parameters.OPTIONAL,
            RequestConstants.Parameters.OPTIONAL
        )
        prepare_response.assert_is_success()

        config.store.order_id = prepare_response.content['body']['order_id']
        config.store.action_data = prepare_response.content['body']['required_action']['action_data']

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(config.store.wgid)
        delete_response.assert_is_success()

    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_commit_purchase_should_succeed_when_completing_purchase(self, config, content_type):
        tx_id = str(uuid.uuid4())

        commit_response = config.freya.server_gateway.commit_purchase(
            tx_id,
            config.store.order_id,
            config.store.wgid,
            config.store.action_data['payment_data']['amount'],
            config.store.action_data['payment_data']['currency_code'],
            config.store.action_data['payment_data']['payment_method'],
            '123456',
            config.store.action_data['2fa']['type'],
            payer_current_ip='127.0.0.1',
            content_type=content_type
        )
        commit_response.assert_is_success()
        assert_that(commit_response.content['body']['transaction_id'], equal_to(tx_id))
        assert_that(commit_response.content['body']['order_id'], equal_to(config.store.order_id))

    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_transaction_id', [
        '00000000-0000-0000-0000-00000000000000',
        '00000000-0000-0000-0000-0000000000',
        '00000000-0000-XXXX-0000-000000000000',
        'bad_transaction_id',
        0,
        -1
    ])
    def test_commit_purchase_should_fail_when_transaction_id_is_invalid(self, config, invalid_transaction_id):
        commit_response = config.freya.server_gateway.commit_purchase(
            invalid_transaction_id,
            config.store.order_id,
            config.store.wgid,
            config.store.action_data['payment_data']['amount'],
            config.store.action_data['payment_data']['currency_code'],
            config.store.action_data['payment_data']['payment_method'],
            '123456',
            config.store.action_data['2fa']['type']
        )
        commit_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                       result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.severity(severity_level.MINOR)
    def test_commit_purchase_should_fail_when_transaction_id_is_all_zero(self, config):
        commit_response = config.freya.server_gateway.commit_purchase(
            '00000000-0000-0000-0000-000000000000',
            config.store.order_id,
            config.store.wgid,
            config.store.action_data['payment_data']['amount'],
            config.store.action_data['payment_data']['currency_code'],
            config.store.action_data['payment_data']['payment_method'],
            '123456',
            config.store.action_data['2fa']['type']
        )
        commit_response.expect_failure(result_code=ResponseMessage.ORDER_PROCESSING_ERROR)

    @pytest.allure.severity(severity_level.MINOR)
    def test_commit_purchase_should_fail_when_transaction_id_is_none(self, config):
        commit_response = config.freya.server_gateway.commit_purchase(
            None,
            config.store.order_id,
            config.store.wgid,
            config.store.action_data['payment_data']['amount'],
            config.store.action_data['payment_data']['currency_code'],
            config.store.action_data['payment_data']['payment_method'],
            '123456',
            config.store.action_data['2fa']['type']
        )
        commit_response.expect_failure(result_code=ResponseMessage.MISSING_PARAMETER)

    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_order_id', [
        '00000000-0000-0000-0000-00000000000000',
        '00000000-0000-0000-0000-0000000000',
        '00000000-0000-XXXX-0000-000000000000',
        'bad_order_id',
        0,
        -1
    ])
    def test_commit_purchase_should_fail_when_order_id_is_invalid(self, config, invalid_order_id):
        commit_response = config.freya.server_gateway.commit_purchase(
            str(uuid.uuid4()),
            invalid_order_id,
            config.store.wgid,
            config.store.action_data['payment_data']['amount'],
            config.store.action_data['payment_data']['currency_code'],
            config.store.action_data['payment_data']['payment_method'],
            '123456',
            config.store.action_data['2fa']['type']
        )
        commit_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                       result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.severity(severity_level.MINOR)
    def test_commit_purchase_should_fail_when_order_id_is_all_zero(self, config):
        commit_response = config.freya.server_gateway.commit_purchase(
            str(uuid.uuid4()),
            '00000000-0000-0000-0000-000000000000',
            config.store.wgid,
            config.store.action_data['payment_data']['amount'],
            config.store.action_data['payment_data']['currency_code'],
            config.store.action_data['payment_data']['payment_method'],
            '123456',
            config.store.action_data['2fa']['type']
        )
        commit_response.expect_failure(result_code=ResponseMessage.ORDER_DOESNOT_EXIST)

    @pytest.allure.severity(severity_level.MINOR)
    def test_commit_purchase_should_fail_when_order_id_is_none(self, config):
        commit_response = config.freya.server_gateway.commit_purchase(
            str(uuid.uuid4()),
            None,
            config.store.wgid,
            config.store.action_data['payment_data']['amount'],
            config.store.action_data['payment_data']['currency_code'],
            config.store.action_data['payment_data']['payment_method'],
            '123456',
            config.store.action_data['2fa']['type']
        )
        commit_response.expect_failure(result_code=ResponseMessage.MISSING_PARAMETER)

    @pytest.allure.severity(severity_level.MINOR)
    def test_commit_purchase_should_fail_when_wgid_is_unbound(self, config):
        commit_response = config.freya.server_gateway.commit_purchase(
            str(uuid.uuid4()),
            config.store.order_id,
            1,
            config.store.action_data['payment_data']['amount'],
            config.store.action_data['payment_data']['currency_code'],
            config.store.action_data['payment_data']['payment_method'],
            '123456',
            config.store.action_data['2fa']['type']
        )
        commit_response.expect_failure(result_code=ResponseMessage.USER_BIND_DOESNOT_EXIST)

    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_wgid', ['', None])
    def test_commit_purchase_should_fail_when_wgid_is_invalid(self, config, invalid_wgid):
        # CommitPurchase failed for wgid: 0 - expected
        commit_response = config.freya.server_gateway.commit_purchase(
            str(uuid.uuid4()),
            config.store.order_id,
            invalid_wgid,
            config.store.action_data['payment_data']['amount'],
            config.store.action_data['payment_data']['currency_code'],
            config.store.action_data['payment_data']['payment_method'],
            '123456',
            config.store.action_data['2fa']['type']
        )
        commit_response.expect_failure(result_code=ResponseMessage.ERROR)

    @pytest.allure.severity(severity_level.MINOR)
    def test_commit_purchase_should_fail_when_wgid_is_string(self, config):
        commit_response = config.freya.server_gateway.commit_purchase(
            str(uuid.uuid4()),
            config.store.order_id,
            'bad_wgid',
            config.store.action_data['payment_data']['amount'],
            config.store.action_data['payment_data']['currency_code'],
            config.store.action_data['payment_data']['payment_method'],
            '123456',
            config.store.action_data['2fa']['type']
        )
        commit_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                       result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.severity(severity_level.MINOR)
    def test_commit_purchase_should_fail_when_amount_is_float(self, config):
        commit_response = config.freya.server_gateway.commit_purchase(
            str(uuid.uuid4()),
            config.store.order_id,
            config.store.wgid,
            .50,
            config.store.action_data['payment_data']['currency_code'],
            config.store.action_data['payment_data']['payment_method'],
            '123456',
            config.store.action_data['2fa']['type']
        )
        commit_response.expect_failure(result_code=ResponseMessage.ORDER_PROCESSING_ERROR)

    @pytest.allure.severity(severity_level.MINOR)
    def test_commit_purchase_should_fail_when_amount_is_none(self, config):
        commit_response = config.freya.server_gateway.commit_purchase(
            str(uuid.uuid4()),
            config.store.order_id,
            config.store.wgid,
            None,
            config.store.action_data['payment_data']['currency_code'],
            config.store.action_data['payment_data']['payment_method'],
            '123456',
            config.store.action_data['2fa']['type']
        )
        commit_response.expect_failure(result_code=ResponseMessage.MISSING_PARAMETER)

    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('bad_amount', [-1, 0, '', 'bad_amount'])
    def test_commit_purchase_should_fail_when_amount_is_invalid(self, config, bad_amount):
        commit_response = config.freya.server_gateway.commit_purchase(
            str(uuid.uuid4()),
            config.store.order_id,
            config.store.wgid,
            bad_amount,
            config.store.action_data['payment_data']['currency_code'],
            config.store.action_data['payment_data']['payment_method'],
            '123456',
            config.store.action_data['2fa']['type']
        )
        commit_response.expect_failure(result_code=ResponseMessage.INVALID_PARAMETER_FORMAT)

    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_payment_code', [
        -1,
        0,
        .50,
        'invalid_payment_code',
        '3kIWAOOG8xWF28oJakAWblSflHoQ5EZpRA6f3oNXHFaueV8McSskVVbUe2zzhRIGI7Qx0vsEVnWPqmIbfgTnbncM7XqIduVU9OC1'
    ])
    def test_commit_purchase_should_fail_when_payment_code_is_invalid(self, config, invalid_payment_code):
        commit_response = config.freya.server_gateway.commit_purchase(
            str(uuid.uuid4()),
            config.store.order_id,
            config.store.wgid,
            config.store.action_data['payment_data']['amount'],
            invalid_payment_code,
            config.store.action_data['payment_data']['payment_method'],
            '123456',
            config.store.action_data['2fa']['type']
        )
        commit_response.expect_failure(result_code=ResponseMessage.ORDER_PROCESSING_ERROR)

    @pytest.allure.severity(severity_level.MINOR)
    def test_commit_purchase_should_fail_when_payment_code_is_none(self, config):
        commit_response = config.freya.server_gateway.commit_purchase(
            str(uuid.uuid4()),
            config.store.order_id,
            config.store.wgid,
            config.store.action_data['payment_data']['amount'],
            None,
            config.store.action_data['payment_data']['payment_method'],
            '123456',
            config.store.action_data['2fa']['type']
        )
        commit_response.expect_failure(result_code=ResponseMessage.MISSING_PARAMETER)

    @pytest.allure.severity(severity_level.MINOR)
    def test_commit_purchase_should_fail_when_payment_code_is_empty(self, config):
        commit_response = config.freya.server_gateway.commit_purchase(
            str(uuid.uuid4()),
            config.store.order_id,
            config.store.wgid,
            config.store.action_data['payment_data']['amount'],
            '',
            config.store.action_data['payment_data']['payment_method'],
            '123456',
            config.store.action_data['2fa']['type']
        )
        commit_response.expect_failure(result_code=ResponseMessage.ORDER_PROCESSING_ERROR)

    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_payment_method', [
        -1,
        0,
        .50,
        'invalid_payment_method',
        '3kIWAOOG8xWF28oJakAWblSflHoQ5EZpRA6f3oNXHFaueV8McSskVVbUe2zzhRIGI7Qx0vsEVnWPqmIbfgTnbncM7XqIduVU9OC1',
        ''
    ])
    def test_commit_purchase_should_fail_when_payment_method_is_invalid(self, config, invalid_payment_method):
        commit_response = config.freya.server_gateway.commit_purchase(
            str(uuid.uuid4()),
            config.store.order_id,
            config.store.wgid,
            config.store.action_data['payment_data']['amount'],
            config.store.action_data['payment_data']['currency_code'],
            invalid_payment_method,
            '123456',
            config.store.action_data['2fa']['type']
        )
        commit_response.expect_failure(result_code=ResponseMessage.PAYMENT_METHOD_DOESNOT_EXIST)

    @pytest.allure.severity(severity_level.MINOR)
    def test_commit_purchase_should_fail_when_payment_method_is_none(self, config):
        commit_response = config.freya.server_gateway.commit_purchase(
            str(uuid.uuid4()),
            config.store.order_id,
            config.store.wgid,
            config.store.action_data['payment_data']['amount'],
            config.store.action_data['payment_data']['currency_code'],
            None,
            '123456',
            config.store.action_data['2fa']['type']
        )
        commit_response.expect_failure(result_code=ResponseMessage.MISSING_PARAMETER)

    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_otp_code', [
        -1,
        0,
        .50,
        None,
        '',
        'invalid_otp_code',
        '3kIWAOOG8xWF28oJakAWblSflHoQ5EZpRA6f3oNXHFaueV8McSskVVbUe2zzhRIGI7Qx0vsEVnWPqmIbfgTnbncM7XqIduVU9OC1'
    ])
    def test_commit_purchase_should_fail_when_otp_code_is_invalid(self, config, invalid_otp_code):
        commit_response = config.freya.server_gateway.commit_purchase(
            str(uuid.uuid4()),
            config.store.order_id,
            config.store.wgid,
            config.store.action_data['payment_data']['amount'],
            config.store.action_data['payment_data']['currency_code'],
            config.store.action_data['payment_data']['payment_method'],
            invalid_otp_code,
            config.store.action_data['2fa']['type']
        )
        commit_response.assert_is_success()

    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_2fa_type', [
        -1,
        0,
        .50,
        'invalid_2fa_type',
        '3kIWAOOG8xWF28oJakAWblSflHoQ5EZpRA6f3oNXHFaueV8McSskVVbUe2zzhRIGI7Qx0vsEVnWPqmIbfgTnbncM7XqIduVU9OC1',
        ''
    ])
    def test_commit_purchase_should_fail_when_2fa_type_is_invalid(self, config, invalid_2fa_type):
        commit_response = config.freya.server_gateway.commit_purchase(
            str(uuid.uuid4()),
            config.store.order_id,
            config.store.wgid,
            config.store.action_data['payment_data']['amount'],
            config.store.action_data['payment_data']['currency_code'],
            config.store.action_data['payment_data']['payment_method'],
            '123456',
            invalid_2fa_type
        )
        commit_response.expect_failure(result_code=ResponseMessage.INVALID_PARAMETER_FORMAT)

    @pytest.allure.severity(severity_level.MINOR)
    def test_commit_purchase_fail_when_2fa_type_is_none(self, config):
        commit_response = config.freya.server_gateway.commit_purchase(
            str(uuid.uuid4()),
            config.store.order_id,
            config.store.wgid,
            config.store.action_data['payment_data']['amount'],
            config.store.action_data['payment_data']['currency_code'],
            config.store.action_data['payment_data']['payment_method'],
            '123456',
            None
        )
        commit_response.expect_failure(result_code=ResponseMessage.MISSING_PARAMETER)

    @pytest.allure.severity(severity_level.NORMAL)
    def test_commit_purchase_should_succeed_with_3ds_param(self, config):
        tx_id = str(uuid.uuid4())

        commit_response = config.freya.server_gateway.commit_purchase(
            tx_id,
            config.store.order_id,
            config.store.wgid,
            config.store.action_data['payment_data']['amount'],
            config.store.action_data['payment_data']['currency_code'],
            config.store.action_data['payment_data']['payment_method'],
            '123456',
            config.store.action_data['2fa']['type'],
            payer_current_ip='127.0.0.1',
            set3ds_data={
                "browser_info": {
                    "accept_header": "application/json, text/javascript, */*; q=0.01",
                    "color_depth": 24,
                    "java_enabled": False,
                    "screen_height": 992,
                    "screen_width": 1768,
                    "time_zone_offset": -120,
                    "user_agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 "
                                  "(KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
                    "language": "ru-RU"
                }
            }
        )
        commit_response.assert_is_success()
        assert_that(commit_response.content['body']['transaction_id'], equal_to(tx_id))
        assert_that(commit_response.content['body']['order_id'], equal_to(config.store.order_id))

    @pytest.allure.severity(severity_level.MINOR)
    def test_commit_purchase_should_fail_with_3ds_param_and_empty_browser_info(self, config):
        tx_id = str(uuid.uuid4())

        commit_response = config.freya.server_gateway.commit_purchase(
            tx_id,
            config.store.order_id,
            config.store.wgid,
            config.store.action_data['payment_data']['amount'],
            config.store.action_data['payment_data']['currency_code'],
            config.store.action_data['payment_data']['payment_method'],
            '123456',
            config.store.action_data['2fa']['type'],
            payer_current_ip='127.0.0.1',
            set3ds_data={}
        )
        commit_response.expect_failure(result_code=ResponseMessage.ERROR)

    @pytest.allure.severity(severity_level.NORMAL)
    def test_commit_purchase_should_succeed_with_3ds_param_and_3ds_payment_url(self, config):
        tx_id = str(uuid.uuid4())

        commit_response = config.freya.server_gateway.commit_purchase(
            tx_id,
            config.store.order_id,
            config.store.wgid,
            config.store.action_data['payment_data']['amount'],
            config.store.action_data['payment_data']['currency_code'],
            config.store.action_data['payment_data']['payment_method'],
            '123456',
            config.store.action_data['2fa']['type'],
            payer_current_ip='127.0.0.1',
            set3ds_url='http://premiumshop/payment/3ds2?query_params',
            set3ds_data={
                "browser_info": {
                    "accept_header": "application/json, text/javascript, */*; q=0.01",
                    "color_depth": 24,
                    "java_enabled": False,
                    "screen_height": 992,
                    "screen_width": 1768,
                    "time_zone_offset": -120,
                    "user_agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 "
                                  "(KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
                    "language": "ru-RU"
                }
            }
        )
        commit_response.assert_is_success()
        assert_that(commit_response.content['body']['transaction_id'], equal_to(tx_id))
        assert_that(commit_response.content['body']['order_id'], equal_to(config.store.order_id))

    @pytest.allure.severity(severity_level.NORMAL)
    @pytest.mark.parametrize('invalid_3ds_url', [
        -1,
        1,
        .50,
        '',
        {}
    ])
    def test_commit_purchase_should_fail_with_3ds_payment_url_incorrect_type(self, config, invalid_3ds_url):
        tx_id = str(uuid.uuid4())

        commit_response = config.freya.server_gateway.commit_purchase(
            tx_id,
            config.store.order_id,
            config.store.wgid,
            config.store.action_data['payment_data']['amount'],
            config.store.action_data['payment_data']['currency_code'],
            config.store.action_data['payment_data']['payment_method'],
            '123456',
            config.store.action_data['2fa']['type'],
            payer_current_ip='127.0.0.1',
            set3ds_url=invalid_3ds_url,
            set3ds_data={
                "browser_info": {
                    "accept_header": "application/json, text/javascript, */*; q=0.01",
                    "color_depth": 24,
                    "java_enabled": False,
                    "screen_height": 992,
                    "screen_width": 1768,
                    "time_zone_offset": -120,
                    "user_agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 "
                                  "(KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
                    "language": "ru-RU"
                }
            }
        )
        commit_response.assert_is_success()
