import pytest
from allure import severity_level
from hamcrest import *
from integration.main.helpers import AccountUtilities, PurchaseUtil
from integration.main.request import RequestBuilder

"""
    See https://confluence.wargaming.net/pages/viewpage.action?pageId=512172851 for rules on how discounts are
    supposed to be applied

"""


@pytest.allure.feature('functional')
@pytest.allure.story('promotions')
class TestPromotions(object):

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
        delete_response = config.spa.http.delete_account(config.store.wgid)
        delete_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_promotions_should_apply_promotion_overrides_when_storefront_is_not_specified(self, config):
        """
        Use case: an active promotion has an empty storefront_refs: [], and references a product + override;
        Because it does not reference a specific storefront, its product+override will apply to all requests,
            so the overridden product will be shown to the user even when an empty storefront is requested.
        """
        config.log.info('fetching promotion without storefront product')
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PROMOTION_WITHOUT_STOREFRONTS.PRODUCT],
            config.store.wgid,
            config.data.TEST_PROMOTION_WITHOUT_STOREFRONTS.COUNTRY,
            config.data.TEST_PROMOTION_WITHOUT_STOREFRONTS.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('ensure request only returned one product')
        assert_that(fetch_response.content['body'], has_key('uriList'))
        uri_list = fetch_response.content['body']['uriList']
        assert_that(uri_list), has_length(1)

        config.log.info('getting promotion product info')
        product_response = RequestBuilder(uri_list[0]).get()
        product_response.assert_is_success()
        product_info = product_response.content

        config.log.info('checking promotion product returns expected fields/entitlement')
        assert_that(product_info['product_code'], config.data.TEST_PROMOTION_WITHOUT_STOREFRONTS.PRODUCT)
        assert_that(product_info['friendly_name'],
                    equal_to(config.data.TEST_PROMOTION_WITHOUT_STOREFRONTS.EXPECTED_FRIENDLY_NAME))
        assert_that(product_info['applied_promotions'], is_(empty()))

        metadata = product_info['metadata']
        assert_that(metadata[config.data.TEST_PROMOTION_WITHOUT_STOREFRONTS.METADATA_NAMESPACE],
                    has_key(config.data.TEST_PROMOTION_WITHOUT_STOREFRONTS.ORIGINAL_METADATA_KEY))
