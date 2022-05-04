import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities, PurchaseUtil
from integration.main.request import RequestConstants, ResponseMessage


@pytest.allure.feature('server')
@pytest.allure.story('get account commerce info')
class TestGetAccountCommerceInfo(object):

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

        config.store.profile_id = account_created.content['id']

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

    @pytest.allure.severity(severity_level.BLOCKER)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_get_account_commerce_info_v2_should_succeed_when_account_payment_type_is_not_bound(self, config,
                                                                                                content_type):
        commerce_response = config.freya.server_gateway.get_account_commerce_info_v2(
            config.store.profile_id,
            'US',
            content_type=content_type)
        commerce_response.assert_is_success()

        assert_that(commerce_response.content['body'], has_key('payment_methods'))
        payment_methods = commerce_response.content['body']['payment_methods']

        assert_that(payment_methods, greater_than(0))

    @pytest.mark.skip_for_regions('trie', 'wgt1')
    @pytest.allure.severity(severity_level.BLOCKER)
    @pytest.mark.notprodsafe
    @pytest.mark.notpreprodsafe
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_get_account_commerce_info_v2_should_succeed_when_account_payment_type_is_bound(self, config,
                                                                                            bind_account, content_type):
        commerce_response = config.freya.server_gateway.get_account_commerce_info_v2(
            config.store.profile_id,
            'US',
            content_type=content_type)
        commerce_response.assert_is_success()

        assert_that(commerce_response.content['body'],
                    has_key('payment_methods'))

        payment_methods = commerce_response.content['body']['payment_methods']

        paypal_bindings = next(payment_method for payment_method in payment_methods
                               if payment_method['name'] == PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL)
        assert_that(paypal_bindings, has_key('bindings'))

        assert_that(paypal_bindings['bindings'][0], has_length(3))

    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_profile_id', [-1, 0, 0.50, None, ''])
    def test_get_account_commerce_info_v2_should_fail_when_profile_id_is_invalid(self, config, invalid_profile_id):
        commerce_response = config.freya.server_gateway.get_account_commerce_info_v2(invalid_profile_id)
        commerce_response.expect_failure(result_code='ERROR')

    @pytest.allure.severity(severity_level.MINOR)
    def test_get_account_commerce_info_v2_should_fail_when_profile_id_is_a_string(self, config):
        commerce_response = config.freya.server_gateway.get_account_commerce_info_v2('bad_profile')
        commerce_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                         result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)
