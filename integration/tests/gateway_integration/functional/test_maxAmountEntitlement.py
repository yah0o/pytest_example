import uuid

import pytest
from allure import severity_level
from hamcrest import *
from integration.main.helpers import AccountUtilities, InventoryUtilities, ReturnValue, WaitOn
from integration.main.helpers.utils import random_transaction_id
from integration.main.request import ResponseMessage
from integration.main.services import CurrencyItem, LegacyProductItem


@pytest.allure.feature('functional')
@pytest.allure.story('max amount entitlement')
class TestMaxAmountEntitlement(object):

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

        grant_response = config.freya.server_gateway.grant_entitlement(
            config.store.profile_id,
            config.data.TEST_ENTITLEMENT_MAX_OF_1.CODE,
            config.data.TEST_ENTITLEMENT_MAX_OF_1.AMOUNT,
            tx_id=random_transaction_id()
        )
        grant_response.assert_is_success()

        assert_that(grant_response.content['body'], has_key('entitlement'))
        assert_that(grant_response.content['body']['entitlement']['amount'],
                    equal_to(config.data.TEST_ENTITLEMENT_MAX_OF_1.AMOUNT))

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(config.store.profile_id)
        delete_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_grant_entitlement_will_succeed_when_entitlement_has_no_max_limit(self, config):
        config.log.info('first time granting {} amount of {}'.format(
            config.data.TEST_PRODUCT_ENTITLEMENT.ENTITLEMENTS.AMOUNT,
            config.data.TEST_PRODUCT_ENTITLEMENT.ENTITLEMENTS.CODE
        ))
        grant_response = config.freya.server_gateway.grant_entitlement(
            config.store.profile_id,
            config.data.TEST_PRODUCT_ENTITLEMENT.ENTITLEMENTS.CODE,
            config.data.TEST_PRODUCT_ENTITLEMENT.ENTITLEMENTS.AMOUNT,
            tx_id=random_transaction_id()
        )
        grant_response.assert_is_success()

        config.log.info('second time granting {} amount of {}'.format(
            config.data.TEST_PRODUCT_ENTITLEMENT.ENTITLEMENTS.AMOUNT,
            config.data.TEST_PRODUCT_ENTITLEMENT.ENTITLEMENTS.CODE
        ))
        grant_response = config.freya.server_gateway.grant_entitlement(
            config.store.profile_id,
            config.data.TEST_PRODUCT_ENTITLEMENT.ENTITLEMENTS.CODE,
            config.data.TEST_PRODUCT_ENTITLEMENT.ENTITLEMENTS.AMOUNT,
            tx_id=random_transaction_id()
        )
        grant_response.assert_is_success()

        inventory_waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={},
            to_check_entitlements={config.data.TEST_PRODUCT_ENTITLEMENT.ENTITLEMENTS.CODE: 2}
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)

        inventory_waiter.wait('Did not get {} {}.'.format(
            config.data.TEST_PRODUCT_ENTITLEMENT.ENTITLEMENTS.CODE,
            2
        ))

    @pytest.mark.skip_for_regions('trie')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_grant_product_will_succeed_when_entitlement_has_no_max_limit(self, config):
        config.log.info("First time granting {} amount of {}".format(
            config.data.TEST_PRODUCT_ENTITLEMENT.AMOUNT,
            config.data.TEST_PRODUCT_ENTITLEMENT.CODE
        ))
        grant_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT.COUNTRY,
            config.data.TEST_PRODUCT.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT_ENTITLEMENT.CODE, config.data.TEST_PRODUCT_ENTITLEMENT.AMOUNT)]
        )
        grant_response.assert_is_success()

        config.log.info("Second time granting {} amount of {}".format(
            config.data.TEST_PRODUCT_ENTITLEMENT.AMOUNT,
            config.data.TEST_PRODUCT_ENTITLEMENT.CODE
        ))
        grant_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT.COUNTRY,
            config.data.TEST_PRODUCT.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT_ENTITLEMENT.CODE, config.data.TEST_PRODUCT_ENTITLEMENT.AMOUNT)]
        )
        grant_response.assert_is_success()

        inventory_waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={},
            to_check_entitlements={config.data.TEST_PRODUCT_ENTITLEMENT.ENTITLEMENTS.CODE: 2}
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)

        inventory_waiter.wait('Did not get {} {}.'.format(
            config.data.TEST_PRODUCT_ENTITLEMENT.ENTITLEMENTS.CODE,
            2
        ))

    @pytest.mark.skip_for_regions('trie')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_will_succeed_when_entitlement_has_no_max_amount_limit(self, config):
        config.log.info('Granting {} amount of {}'.format(
            config.data.TEST_PRODUCT_ENTITLEMENT.COST.AMOUNT * 2,
            config.data.TEST_PRODUCT_ENTITLEMENT.COST.CURRENCY_CODE
        ))
        grant_response = config.freya.server_gateway.grant_currency(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.data.TEST_PRODUCT_ENTITLEMENT.COST.CURRENCY_CODE,
            config.data.TEST_PRODUCT_ENTITLEMENT.COST.AMOUNT * 2
        )
        grant_response.assert_is_success()

        config.log.info('First time purchasing {} amount of {}'.format(
            config.data.TEST_PRODUCT_ENTITLEMENT.COST.AMOUNT,
            config.data.TEST_PRODUCT_ENTITLEMENT.COST.CURRENCY_CODE
        ))
        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PRODUCT_ENTITLEMENT.CODE,
            config.data.TEST_PRODUCT_ENTITLEMENT.AMOUNT,
            [CurrencyItem(
                config.data.TEST_PRODUCT_ENTITLEMENT.COST.CURRENCY_CODE,
                str(config.data.TEST_PRODUCT_ENTITLEMENT.COST.AMOUNT)
            )],
            storefront=config.data.TEST_PRODUCT_ENTITLEMENT.STOREFRONT
        )
        purchase_response.assert_is_success()

        config.log.info('Second time purchasing {} amount of {}'.format(
            config.data.TEST_PRODUCT_ENTITLEMENT.COST.AMOUNT,
            config.data.TEST_PRODUCT_ENTITLEMENT.COST.CURRENCY_CODE
        ))
        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PRODUCT_ENTITLEMENT.CODE,
            config.data.TEST_PRODUCT_ENTITLEMENT.AMOUNT,
            [CurrencyItem(
                config.data.TEST_PRODUCT_ENTITLEMENT.COST.CURRENCY_CODE,
                str(config.data.TEST_PRODUCT_ENTITLEMENT.COST.AMOUNT)
            )],
            storefront=config.data.TEST_PRODUCT_ENTITLEMENT.STOREFRONT
        )
        purchase_response.assert_is_success()

        inventory_waiter = WaitOn(lambda: InventoryUtilities.inventory_has(
            config.freya.server_gateway,
            config.log,
            config.store.profile_id,
            to_check_currencies={},
            to_check_entitlements={config.data.TEST_PRODUCT_ENTITLEMENT.ENTITLEMENTS.CODE: 2}
        )).until(ReturnValue.EQUAL_TO(True), timeout=30)

        inventory_waiter.wait('Did not get {} {}.'.format(
            config.data.TEST_PRODUCT_ENTITLEMENT.ENTITLEMENTS.CODE,
            2
        ))

    @pytest.mark.skip_for_regions('trie')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_grant_entitlement_should_fail_when_profile_has_max_amount_of_entitlement(self, config):
        grant_response = config.freya.server_gateway.grant_entitlement(
            config.store.profile_id,
            config.data.TEST_ENTITLEMENT_MAX_OF_1.CODE,
            config.data.TEST_ENTITLEMENT_MAX_OF_1.AMOUNT,
            tx_id=random_transaction_id()
        )
        grant_response.expect_failure(result_code=ResponseMessage.ENTITLEMENT_ILLEGAL_STATE_ERROR)

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_grant_product_should_fail_when_profile_has_max_amount_of_entitlement(self, config):
        grant_response = config.freya.server_gateway.grant_product(
            str(uuid.uuid4()),
            config.data.TEST_PRODUCT.COUNTRY,
            config.data.TEST_PRODUCT.LANGUAGE,
            config.store.profile_id,
            [LegacyProductItem(config.data.TEST_PRODUCT_MAX_OF_1.CODE, config.data.TEST_PRODUCT_MAX_OF_1.AMOUNT)]
        )
        grant_response.expect_failure()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_purchase_product_should_fail_when_profile_has_max_amount_of_entitlement(self, config):
        purchase_response = config.freya.server_gateway.purchase_product(
            str(uuid.uuid4()),
            config.store.profile_id,
            config.store.profile_id,
            config.data.TEST_PRODUCT_MAX_OF_1.CODE,
            config.data.TEST_PRODUCT_MAX_OF_1.AMOUNT,
            [],
            storefront=config.data.TEST_PRODUCT_ENTITLEMENT.STOREFRONT
        )
        purchase_response.expect_failure()
