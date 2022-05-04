import uuid

import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities, InventoryUtilities, ProductUtilities, PurchaseUtil, \
    RequestBuilder, ReturnValue, WaitOn
from integration.main.services import CurrencyItem, LegacyProductItem, PurchaseProductItem


@pytest.mark.skip_for_regions('trie')
# ORDO errors
@pytest.allure.feature('functional')
@pytest.allure.story('prerequisites')
class TestPrerequisites(object):

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

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(config.store.profile_id)
        delete_response.assert_is_success()

    @pytest.fixture
    def grant_prereq_a(self, config):
        config.log.info('granting profile {0} amount of {1} needed for prerequisite'.format(
            config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENT.AMOUNT,
            config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENT.ENTITLEMENT_A))

        grant_product_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_REQUIREMENT.COUNTRY,
            config.data.TEST_PRODUCT_REQUIREMENT.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENT.PRODUCT_A,
                config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENT.AMOUNT
            )]
        )
        grant_product_response.assert_is_success()

    @pytest.fixture
    def grant_prereq_a_excess(self, config):
        config.log.info('granting profile {0} amount of {1} needed for prerequisite'.format(
            config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENT.AMOUNT,
            config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENT.ENTITLEMENT_A))

        grant_product_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_REQUIREMENT.COUNTRY,
            config.data.TEST_PRODUCT_REQUIREMENT.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENT.PRODUCT_A,
                config.data.TEST_PRODUCT_REQUIREMENT.EXCEEDED_AMOUNT
            )]
        )
        grant_product_response.assert_is_success()

    @pytest.fixture
    def grant_prereq_b(self, config):
        config.log.info('granting profile {0} amount of {1} needed for prerequisite'.format(
            config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENT.AMOUNT,
            config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENT.ENTITLEMENT_B))

        grant_product_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_REQUIREMENT.COUNTRY,
            config.data.TEST_PRODUCT_REQUIREMENT.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENT.PRODUCT_B,
                config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENT.AMOUNT
            )]
        )
        grant_product_response.assert_is_success()

    @pytest.fixture
    def bind_account(self, config):
        config.log.info('Binding payment method to account')
        bind_response = config.psa.service.bind(
            config.store.wgid,
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            PurchaseUtil.PaymentNone.PAYPAL_NONCE
        )
        bind_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_profile_has_requirement_for_less_than_one_prereq_op(self, config):
        """
        Testing that less than one operator works as expected. The account will not have any entitlements.
        We should only get back product_with_less_than_prereq.
        """
        expected_products = config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENT_NOT_MET_PRODUCTS

        product_response = config.freya.server_gateway.fetch_products(
            list(expected_products),
            config.store.wgid,
            config.data.TEST_PRODUCT_REQUIREMENT.COUNTRY,
            config.data.TEST_PRODUCT_REQUIREMENT.LANGUAGE
        )
        product_response.assert_is_success()

        config.log.info('comparing product codes from uri list to expected')
        assert_that(product_response.content['body'], has_key('uriList'))
        uri_list_products = ProductUtilities.product_codes_from_uri_list(product_response.content['body']['uriList'])
        assert_that(sorted(expected_products), equal_to(sorted(uri_list_products)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_profile_has_requirement_for_equal_zero_prereq_op(self, config):
        """
        Testing that equal zero operator works as expected. The account will have 0 ENTITLEMENT_A.
        We should only get back product_with_equals_zero_prereq.
        """
        expected_products = config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENTS_EQUALS_ZERO_PRODUCT

        product_response = config.freya.server_gateway.fetch_products(
            list(expected_products),
            config.store.wgid,
            config.data.TEST_PRODUCT_REQUIREMENT.COUNTRY,
            config.data.TEST_PRODUCT_REQUIREMENT.LANGUAGE
        )
        product_response.assert_is_success()

        config.log.info('comparing product codes from uri list to expected')
        assert_that(product_response.content['body'], has_key('uriList'))
        uri_list_products = ProductUtilities.product_codes_from_uri_list(product_response.content['body']['uriList'])
        assert_that(sorted(expected_products), equal_to(sorted(uri_list_products)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_profile_has_requirement_for_less_than_one_prereq_op(self, config):
        """
        Testing that less than one operator works as expected. The account will not have any entitlements.
        Of the 3 products in the storefront, we should only get back
        product_with_less_than_prereq. The other 2 should not be present in the response.
        """
        expected_products = config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENT_NOT_MET_PRODUCTS

        product_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_PRODUCT_REQUIREMENT.STOREFRONT,
            config.store.wgid,
            config.data.TEST_PRODUCT_REQUIREMENT.COUNTRY,
            config.data.TEST_PRODUCT_REQUIREMENT.LANGUAGE
        )
        product_response.assert_is_success()

        config.log.info('comparing product codes from uri list to expected')
        assert_that(product_response.content['body'], has_key('uriList'))
        uri_list_products = ProductUtilities.product_codes_from_uri_list(product_response.content['body']['uriList'])
        assert_that(sorted(expected_products), equal_to(sorted(uri_list_products)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_profile_has_requirement_for_equal_one_prereq_op(
            self,
            config,
            grant_prereq_a
    ):
        """
        Testing that equal to one operator works as expected. The account is granted 1 ENTITLEMENT_A.
        Of the 2 products in the storefront, we should only get back
        product_with_equals_one_prereq. The other should not be present in the response.
        """
        expected_products = config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENTS_EQUALS_ONE_PRODUCT

        product_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_PRODUCT_REQUIREMENT.EQUALS_PREREG_STOREFRONT,
            config.store.wgid,
            config.data.TEST_PRODUCT_REQUIREMENT.COUNTRY,
            config.data.TEST_PRODUCT_REQUIREMENT.LANGUAGE
        )
        product_response.assert_is_success()

        config.log.info('comparing product codes from uri list to expected')
        assert_that(product_response.content['body'], has_key('uriList'))
        uri_list_products = ProductUtilities.product_codes_from_uri_list(product_response.content['body']['uriList'])
        assert_that(sorted(expected_products), equal_to(sorted(uri_list_products)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_profile_has_requirement_for_equal_zero_prereq_op(self, config):
        """
        Testing that equal to one operator works as expected. The account will have no entitlements.
        Of the 2 products in the storefront, we should only get back
        product_with_equals_zero_prereq. The other should not be present in the response.
        """
        expected_products = config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENTS_EQUALS_ZERO_PRODUCT

        product_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_PRODUCT_REQUIREMENT.EQUALS_PREREG_STOREFRONT,
            config.store.wgid,
            config.data.TEST_PRODUCT_REQUIREMENT.COUNTRY,
            config.data.TEST_PRODUCT_REQUIREMENT.LANGUAGE
        )
        product_response.assert_is_success()

        config.log.info('comparing product codes from uri list to expected')
        assert_that(product_response.content['body'], has_key('uriList'))
        uri_list_products = ProductUtilities.product_codes_from_uri_list(product_response.content['body']['uriList'])
        assert_that(sorted(expected_products), equal_to(sorted(uri_list_products)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_should_succeed_when_profile_has_requirement_for_less_than_one_prereq_op(
            self,
            config
    ):
        config.log.info('Granting {} test currency for purchasing {}'.format(
            config.data.TEST_PRODUCT_REQUIREMENT.VIRTUAL_CURRENCY.AMOUNT,
            config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENT_NOT_MET_PRODUCTS[0]
        ))

        grant_prod_with_test_currency_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                config.data.TEST_PRODUCT_REQUIREMENT.VIRTUAL_CURRENCY.AMOUNT
            )]
        )
        grant_prod_with_test_currency_response.assert_is_success()

        config.log.info('Fetching {}'.format(config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENT_NOT_MET_PRODUCTS[0]))

        fetch_product_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENT_NOT_MET_PRODUCTS[0]],
            config.store.profile_id,
            config.data.TEST_PRODUCT_REQUIREMENT.COUNTRY,
            config.data.TEST_PRODUCT_REQUIREMENT.LANGUAGE
        )
        fetch_product_response.assert_is_success()

        assert_that(fetch_product_response.content['body']['uriList'], has_length(1))
        uri = fetch_product_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('virtual_price'))
        assert_that(prod_response.content['price']['virtual_price'], has_length(1))
        cost = prod_response.content['price']['virtual_price'][0]

        assert_that(cost, has_key('code'))
        assert_that(cost, has_key('amount'))

        config.log.info('Purchasing {}'.format(config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENT_NOT_MET_PRODUCTS[0]))

        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENT_NOT_MET_PRODUCTS[0],
            config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENT.AMOUNT,
            [CurrencyItem(
                cost['code'],
                cost['amount']
            )],
            storefront=config.data.TEST_PRODUCT_REQUIREMENT.STOREFRONT
        )
        purchase_response.assert_is_success()

        config.log.info('Checking if inventory has {} {}'.format(
            config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENT.AMOUNT,
            config.data.TEST_PRODUCT_REQUIREMENT.ENTITLEMENT
        ))

        waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={},
            to_check_entitlements={
                config.data.TEST_PRODUCT_REQUIREMENT.ENTITLEMENT: config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENT.AMOUNT
            }
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)

        waiter.wait('Failed to purchase {} with {} {}\n{}'.format(
            config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENT_NOT_MET_PRODUCTS[0],
            config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENT.AMOUNT,
            config.data.TEST_PRODUCT_REQUIREMENT.ENTITLEMENT,
            config.freya.server_gateway.get_full_inventory(config.store.profile_id).details
        ))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_should_succeed_when_profile_has_requirement_for_equal_to_zero_prereq_op(self, config):
        config.log.info('Granting {} test currency for purchasing {}'.format(
            config.data.TEST_PRODUCT_REQUIREMENT.VIRTUAL_CURRENCY.AMOUNT,
            config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENTS_EQUALS_ZERO_PRODUCT[0]
        ))

        grant_prod_with_test_currency_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_VARIABLE.COUNTRY,
            config.data.TEST_PRODUCT_VARIABLE.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(
                config.data.TEST_PRODUCT_VARIABLE.PRODUCT_CODE,
                config.data.TEST_PRODUCT_REQUIREMENT.VIRTUAL_CURRENCY.AMOUNT
            )]
        )
        grant_prod_with_test_currency_response.assert_is_success()

        config.log.info('Fetching {}'.format(config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENTS_EQUALS_ZERO_PRODUCT[0]))

        fetch_product_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENTS_EQUALS_ZERO_PRODUCT[0]],
            config.store.profile_id,
            config.data.TEST_PRODUCT_REQUIREMENT.COUNTRY,
            config.data.TEST_PRODUCT_REQUIREMENT.LANGUAGE
        )
        fetch_product_response.assert_is_success()

        assert_that(fetch_product_response.content['body']['uriList'], has_length(1))
        uri = fetch_product_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('virtual_price'))
        assert_that(prod_response.content['price']['virtual_price'], has_length(1))
        cost = prod_response.content['price']['virtual_price'][0]

        assert_that(cost, has_key('code'))
        assert_that(cost, has_key('amount'))

        config.log.info(
            'Purchasing {}'.format(config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENTS_EQUALS_ZERO_PRODUCT[0]))

        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENTS_EQUALS_ZERO_PRODUCT[0],
            config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENT.AMOUNT,
            [CurrencyItem(
                cost['code'],
                cost['amount']
            )],
            storefront=config.data.TEST_PRODUCT_REQUIREMENT.EQUALS_PREREG_STOREFRONT
        )
        purchase_response.assert_is_success()

        config.log.info('Checking if inventory have {} {}'.format(
            config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENT.AMOUNT,
            config.data.TEST_PRODUCT_REQUIREMENT.ENTITLEMENT
        ))

        waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={},
            to_check_entitlements={
                config.data.TEST_PRODUCT_REQUIREMENT.ENTITLEMENT: config.data.TEST_PRODUCT_REQUIREMENT.REQUIREMENT.AMOUNT
            }
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)

    @pytest.mark.skip_for_regions('trie', 'wgt1')
    @pytest.mark.notprodsafe
    @pytest.mark.notpreprodsafe
    def test_prepare_and_commit_purchase_should_succeed_when_profile_has_requirement_for_less_than_one_prereq_op(
            self,
            config,
            bind_account
    ):
        config.log.info('Fetching {}'.format(config.data.TEST_PRODUCT_REQUIREMENT_RM.REQUIREMENT_NOT_MET_PRODUCT))

        fetch_product_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT_REQUIREMENT_RM.REQUIREMENT_NOT_MET_PRODUCT],
            config.store.profile_id,
            config.data.TEST_PRODUCT_REQUIREMENT_RM.COUNTRY,
            config.data.TEST_PRODUCT_REQUIREMENT_RM.LANGUAGE
        )
        fetch_product_response.assert_is_success()

        assert_that(fetch_product_response.content['body']['uriList'], has_length(1))
        uri = fetch_product_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(cost, has_key('amount'))

        config.log.info('Preparing to purchase {}'.format(
            config.data.TEST_PRODUCT_REQUIREMENT_RM.REQUIREMENT_NOT_MET_PRODUCT
        ))

        prepare_purchase_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_REQUIREMENT_RM.COUNTRY,
            config.data.TEST_PRODUCT_REQUIREMENT_RM.LANGUAGE,
            config.store.profile_id,
            config.store.profile_id,
            [PurchaseProductItem(product_id, config.data.TEST_PRODUCT_REQUIREMENT_RM.AMOUNT)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(cost['code'], cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            storefront=config.data.TEST_PRODUCT_REQUIREMENT_RM.STOREFRONT_RM_PREREQ
        )
        prepare_purchase_response.assert_is_success()

        order_id = prepare_purchase_response.content['body']['order_id']
        action_data = prepare_purchase_response.content['body']['required_action']['action_data']

        config.log.info('Committing purchase for {}'.format(
            config.data.TEST_PRODUCT_REQUIREMENT_RM.REQUIREMENT_NOT_MET_PRODUCT
        ))

        commit_product_response = config.freya.server_gateway.commit_purchase(
            str(uuid.uuid4()),
            order_id,
            config.store.wgid,
            action_data['payment_data']['amount'],
            action_data['payment_data']['currency_code'],
            action_data['payment_data']['payment_method'],
            '123456',
            action_data['2fa']['type']
        )
        commit_product_response.assert_is_success()

        config.log.info('Checking if inventory has {} {}'.format(
            config.data.TEST_PRODUCT_REQUIREMENT_RM.AMOUNT,
            config.data.TEST_PRODUCT_REQUIREMENT_RM.ENTITLEMENT
        ))

        waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.wgid,
            to_check_currencies={},
            to_check_entitlements={
                config.data.TEST_PRODUCT_REQUIREMENT_RM.ENTITLEMENT: config.data.TEST_PRODUCT_REQUIREMENT_RM.AMOUNT
            }
        )).until(ReturnValue.EQUAL_TO(True), 30)

    @pytest.mark.skip_for_regions('trie', 'wgt1')
    @pytest.mark.notprodsafe
    @pytest.mark.notpreprodsafe
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_prepare_and_commit_purchase_should_succeed_when_profile_has_requirement_for_equal_to_zero_prereq_op(
            self,
            config,
            bind_account
    ):
        config.log.info('Fetching {}'.format(config.data.TEST_PRODUCT_REQUIREMENT_RM.REQUIREMENTS_EQUAL_ZERO_PRODUCT))

        fetch_product_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT_REQUIREMENT_RM.REQUIREMENTS_EQUAL_ZERO_PRODUCT],
            config.store.profile_id,
            config.data.TEST_PRODUCT_REQUIREMENT_RM.COUNTRY,
            config.data.TEST_PRODUCT_REQUIREMENT_RM.LANGUAGE
        )
        fetch_product_response.assert_is_success()

        assert_that(fetch_product_response.content['body']['uriList'], has_length(1))
        uri = fetch_product_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('product_id'))
        product_id = prod_response.content['product_id']

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(cost, has_key('amount'))

        config.log.info('Preparing to purchase {}'.format(
            config.data.TEST_PRODUCT_REQUIREMENT_RM.REQUIREMENTS_EQUAL_ZERO_PRODUCT
        ))

        prepare_purchase_response = config.freya.server_gateway.prepare_purchase(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT_REQUIREMENT_RM.COUNTRY,
            config.data.TEST_PRODUCT_REQUIREMENT_RM.LANGUAGE,
            config.store.profile_id,
            config.store.profile_id,
            [PurchaseProductItem(product_id, config.data.TEST_PRODUCT_REQUIREMENT_RM.AMOUNT)],
            PurchaseUtil.PaymentType.IGP,
            CurrencyItem(cost['code'], cost['amount']),
            PurchaseUtil.PaymentCode.BRAINTREE_PAYPAL,
            storefront=config.data.TEST_PRODUCT_REQUIREMENT_RM.STOREFRONT_RM_PREREQ
        )
        prepare_purchase_response.assert_is_success()

        order_id = prepare_purchase_response.content['body']['order_id']
        action_data = prepare_purchase_response.content['body']['required_action']['action_data']

        config.log.info('Committing purchase for {}'.format(
            config.data.TEST_PRODUCT_REQUIREMENT_RM.REQUIREMENTS_EQUAL_ZERO_PRODUCT
        ))

        commit_product_response = config.freya.server_gateway.commit_purchase(
            str(uuid.uuid4()),
            order_id,
            config.store.wgid,
            action_data['payment_data']['amount'],
            action_data['payment_data']['currency_code'],
            action_data['payment_data']['payment_method'],
            '123456',
            action_data['2fa']['type']
        )
        commit_product_response.assert_is_success()

        config.log.info('Checking if inventory has {} {}'.format(
            config.data.TEST_PRODUCT_REQUIREMENT_RM.AMOUNT,
            config.data.TEST_PRODUCT_REQUIREMENT_RM.ENTITLEMENT
        ))

        waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.wgid,
            to_check_currencies={},
            to_check_entitlements={
                config.data.TEST_PRODUCT_REQUIREMENT_RM.ENTITLEMENT: config.data.TEST_PRODUCT_REQUIREMENT_RM.AMOUNT
            }
        )).until(ReturnValue.EQUAL_TO(True), 30)
