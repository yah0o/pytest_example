import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities, PurchaseUtil
from integration.main.request import RequestBuilder
from integration.main.services import ConsulManager


class TestCompensation(object):

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

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(config.store.profile_id)
        delete_response.assert_is_success()

    @pytest.allure.feature('functional')
    @pytest.allure.story('compensation')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_compensation_field_is_within_a_product(self, config):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT_CONTAINS_COMPENSATION_WITHIN_PRODUCT.CODE],
            config.store.profile_id,
            config.data.TEST_PRODUCT_CONTAINS_COMPENSATION_WITHIN_PRODUCT.COUNTRY,
            config.data.TEST_PRODUCT_CONTAINS_COMPENSATION_WITHIN_PRODUCT.LANGUAGE
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        assert_that(product_response.content, has_key('entitlements'))
        entitlement = product_response.content['entitlements'][0]

        assert_that(entitlement, has_key('compensation'))
        compensation = entitlement['compensation']

        assert_that(compensation, has_key('code'))
        assert_that(
            compensation['code'],
            equal_to(config.data.TEST_PRODUCT_CONTAINS_COMPENSATION_WITHIN_PRODUCT.ENTITLEMENTS.COMPENSATION.CODE)
        )
        assert_that(compensation, has_key('amount'))
        assert_that(
            compensation['amount'],
            equal_to(config.data.TEST_PRODUCT_CONTAINS_COMPENSATION_WITHIN_PRODUCT.ENTITLEMENTS.COMPENSATION.AMOUNT)
        )

    @pytest.allure.feature('functional')
    @pytest.allure.story('compensation')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_compensation_field_is_within_an_entitlement(self, config):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PRODUCT_CONTAINS_COMPENSATION_WITHIN_ENTITLEMENT.CODE],
            config.store.profile_id,
            config.data.TEST_PRODUCT_CONTAINS_COMPENSATION_WITHIN_ENTITLEMENT.COUNTRY,
            config.data.TEST_PRODUCT_CONTAINS_COMPENSATION_WITHIN_ENTITLEMENT.LANGUAGE
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        assert_that(product_response.content, has_key('entitlements'))
        entitlement = product_response.content['entitlements'][0]

        assert_that(entitlement, has_key('compensation'))
        compensation = entitlement['compensation']

        assert_that(compensation, has_key('code'))
        assert_that(
            compensation['code'],
            equal_to(config.data.TEST_PRODUCT_CONTAINS_COMPENSATION_WITHIN_ENTITLEMENT.ENTITLEMENTS.COMPENSATION.CODE)
        )
        assert_that(compensation, has_key('amount'))
        assert_that(
            compensation['amount'],
            equal_to(config.data.TEST_PRODUCT_CONTAINS_COMPENSATION_WITHIN_ENTITLEMENT.ENTITLEMENTS.COMPENSATION.AMOUNT)
        )

    @pytest.allure.feature('functional')
    @pytest.allure.story('compensation')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_prod_with_compensation_have_pct_pro_disc_on_vc(self, config):
        fetch_product_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_VC_PCT_PRO_DISC_COMP.CODE],
            config.store.profile_id,
            config.data.TEST_VC_PCT_PRO_DISC_COMP.COUNTRY,
            config.data.TEST_VC_PCT_PRO_DISC_COMP.LANGUAGE,
            config.data.TEST_VC_PCT_PRO_DISC_COMP.STOREFRONT
        )
        fetch_product_response.assert_is_success()
        assert_that(fetch_product_response.content['body']['uriList'], has_length(1))
        url = fetch_product_response.content['body']['uriList'][0]

        product_response = RequestBuilder(url).get()
        product_response.assert_is_success()

        assert_that(product_response.content, has_key('entitlements'))
        assert_that(product_response.content['entitlements'], has_length(1))
        entitlement = product_response.content['entitlements'][0]

        assert_that(entitlement, has_key('code'))
        assert_that(entitlement['code'], equal_to(config.data.TEST_VC_PCT_PRO_DISC_COMP.ENTITLEMENT_CODE))

        assert_that(entitlement, has_key('compensation'))
        compensation = entitlement['compensation']

        assert_that(compensation, has_key('code'))
        assert_that(compensation['code'], equal_to(config.data.TEST_VC_PCT_PRO_DISC_COMP.COMPENSATION.CODE))
        assert_that(compensation, has_key('amount'))
        assert_that(compensation['amount'], equal_to(config.data.TEST_VC_PCT_PRO_DISC_COMP.COMPENSATION.AMOUNT))

    @pytest.allure.feature('functional')
    @pytest.allure.story('compensation')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_prod_with_compensation_have_fixed_disc_on_vc(self, config):

        fetch_product_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_VC_FIXED_DISC_COMP.CODE],
            config.store.profile_id,
            config.data.TEST_VC_FIXED_DISC_COMP.COUNTRY,
            config.data.TEST_VC_FIXED_DISC_COMP.LANGUAGE,
            config.data.TEST_VC_FIXED_DISC_COMP.STOREFRONT
        )
        fetch_product_response.assert_is_success()
        assert_that(fetch_product_response.content['body']['uriList'], has_length(1))
        url = fetch_product_response.content['body']['uriList'][0]

        product_response = RequestBuilder(url).get()
        product_response.assert_is_success()

        assert_that(product_response.content, has_key('entitlements'))
        assert_that(product_response.content['entitlements'], has_length(1))
        entitlement = product_response.content['entitlements'][0]

        assert_that(entitlement, has_key('code'))
        assert_that(entitlement['code'], equal_to(config.data.TEST_VC_FIXED_DISC_COMP.ENTITLEMENT_CODE))

        assert_that(entitlement, has_key('compensation'))
        compensation = entitlement['compensation']

        assert_that(compensation['code'], equal_to(config.data.TEST_VC_FIXED_DISC_COMP.COMPENSATION.CODE))
        assert_that(compensation['amount'], equal_to(config.data.TEST_VC_FIXED_DISC_COMP.COMPENSATION.AMOUNT))

    @pytest.allure.feature('functional')
    @pytest.allure.story('compensation')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_prod_with_compensation_have_abs_disc_on_vc(self, config):

        fetch_product_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_VC_ABS_DISC_COMP.CODE],
            config.store.profile_id,
            config.data.TEST_VC_ABS_DISC_COMP.COUNTRY,
            config.data.TEST_VC_ABS_DISC_COMP.LANGUAGE,
            config.data.TEST_VC_ABS_DISC_COMP.STOREFRONT
        )
        fetch_product_response.assert_is_success()
        assert_that(fetch_product_response.content['body']['uriList'], has_length(1))
        url = fetch_product_response.content['body']['uriList'][0]

        product_response = RequestBuilder(url).get()
        product_response.assert_is_success()

        assert_that(product_response.content, has_key('entitlements'))
        assert_that(product_response.content['entitlements'], has_length(1))
        entitlement = product_response.content['entitlements'][0]

        assert_that(entitlement, has_key('code'))
        assert_that(entitlement['code'], equal_to(config.data.TEST_VC_ABS_DISC_COMP.ENTITLEMENT_CODE))

        assert_that(entitlement, has_key('compensation'))
        compensation = entitlement['compensation']

        assert_that(compensation['code'], equal_to(config.data.TEST_VC_ABS_DISC_COMP.COMPENSATION.CODE))
        assert_that(compensation['amount'], equal_to(config.data.TEST_VC_ABS_DISC_COMP.COMPENSATION.AMOUNT))

    @pytest.allure.feature('functional')
    @pytest.allure.story('compensation')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_prod_with_compensation_have_pct_pro_disc_on_vc(self, config):

        fetch_product_list_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_VC_PCT_PRO_DISC_COMP.STOREFRONT,
            config.store.profile_id,
            config.data.TEST_VC_PCT_PRO_DISC_COMP.COUNTRY,
            config.data.TEST_VC_PCT_PRO_DISC_COMP.LANGUAGE
        )
        fetch_product_list_response.assert_is_success()

        assert_that(fetch_product_list_response.content['body'], has_key('uriList'))
        assert_that(fetch_product_list_response.content['body']['uriList'], not_none())
        uri_list = fetch_product_list_response.content['body']['uriList']

        prod = next(
            (
                prod_content for prod_content in PurchaseUtil.get_product_infos(uri_list)
                if prod_content['product_code'] == config.data.TEST_VC_PCT_PRO_DISC_COMP.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('entitlements'))
        assert_that(prod['entitlements'], has_length(1))
        entitlement = prod['entitlements'][0]

        assert_that(entitlement, has_key('code'))
        assert_that(entitlement['code'], equal_to(config.data.TEST_VC_PCT_PRO_DISC_COMP.ENTITLEMENT_CODE))

        assert_that(entitlement, has_key('compensation'))
        compensation = entitlement['compensation']

        assert_that(compensation, has_key('code'))
        assert_that(compensation['code'], equal_to(config.data.TEST_VC_PCT_PRO_DISC_COMP.COMPENSATION.CODE))
        assert_that(compensation, has_key('amount'))
        assert_that(compensation['amount'], equal_to(config.data.TEST_VC_PCT_PRO_DISC_COMP.COMPENSATION.AMOUNT))

    @pytest.allure.feature('functional')
    @pytest.allure.story('compensation')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_prod_with_compensation_have_fixed_disc_on_vc(self, config):

        fetch_product_list_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_VC_FIXED_DISC_COMP.STOREFRONT,
            config.store.profile_id,
            config.data.TEST_VC_FIXED_DISC_COMP.COUNTRY,
            config.data.TEST_VC_FIXED_DISC_COMP.LANGUAGE
        )
        fetch_product_list_response.assert_is_success()

        assert_that(fetch_product_list_response.content['body'], has_key('uriList'))
        assert_that(fetch_product_list_response.content['body']['uriList'], not_none())
        uri_list = fetch_product_list_response.content['body']['uriList']

        prod = next(
            (
                prod_content for prod_content in PurchaseUtil.get_product_infos(uri_list)
                if prod_content['product_code'] == config.data.TEST_VC_FIXED_DISC_COMP.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('entitlements'))
        assert_that(prod['entitlements'], has_length(1))
        entitlement = prod['entitlements'][0]

        assert_that(entitlement, has_key('code'))
        assert_that(entitlement['code'], equal_to(config.data.TEST_VC_FIXED_DISC_COMP.ENTITLEMENT_CODE))

        assert_that(entitlement, has_key('compensation'))
        compensation = entitlement['compensation']

        assert_that(compensation, has_key('code'))
        assert_that(compensation['code'], equal_to(config.data.TEST_VC_FIXED_DISC_COMP.COMPENSATION.CODE))
        assert_that(compensation, has_key('amount'))
        assert_that(compensation['amount'], equal_to(config.data.TEST_VC_FIXED_DISC_COMP.COMPENSATION.AMOUNT))

    @pytest.allure.feature('functional')
    @pytest.allure.story('compensation')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_prod_with_compensation_have_abs_disc_on_vc(self, config):

        fetch_product_list_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_VC_ABS_DISC_COMP.STOREFRONT,
            config.store.profile_id,
            config.data.TEST_VC_ABS_DISC_COMP.COUNTRY,
            config.data.TEST_VC_ABS_DISC_COMP.LANGUAGE
        )
        fetch_product_list_response.assert_is_success()

        assert_that(fetch_product_list_response.content['body'], has_key('uriList'))
        assert_that(fetch_product_list_response.content['body']['uriList'], not_none())
        uri_list = fetch_product_list_response.content['body']['uriList']

        prod = next(
            (
                prod_content for prod_content in PurchaseUtil.get_product_infos(uri_list)
                if prod_content['product_code'] == config.data.TEST_VC_ABS_DISC_COMP.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('entitlements'))
        assert_that(prod['entitlements'], has_length(1))
        entitlement = prod['entitlements'][0]

        assert_that(entitlement, has_key('code'))
        assert_that(entitlement['code'], equal_to(config.data.TEST_VC_ABS_DISC_COMP.ENTITLEMENT_CODE))

        assert_that(entitlement, has_key('compensation'))
        compensation = entitlement['compensation']

        assert_that(compensation, has_key('code'))
        assert_that(compensation['code'], equal_to(config.data.TEST_VC_ABS_DISC_COMP.COMPENSATION.CODE))
        assert_that(compensation, has_key('amount'))
        assert_that(compensation['amount'], equal_to(config.data.TEST_VC_ABS_DISC_COMP.COMPENSATION.AMOUNT))

    @pytest.allure.feature('functional')
    @pytest.allure.story('compensation')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_prod_with_compensation_have_pct_pro_disc_on_rm(self, config):

        fetch_product_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_RM_PCT_PRO_DISC_COMP.CODE],
            config.store.profile_id,
            config.data.TEST_RM_PCT_PRO_DISC_COMP.COUNTRY,
            config.data.TEST_RM_PCT_PRO_DISC_COMP.LANGUAGE,
            config.data.TEST_RM_PCT_PRO_DISC_COMP.STOREFRONT
        )
        fetch_product_response.assert_is_success()
        assert_that(fetch_product_response.content['body']['uriList'], has_length(1))
        url = fetch_product_response.content['body']['uriList'][0]

        product_response = RequestBuilder(url).get()
        product_response.assert_is_success()

        assert_that(product_response.content, has_key('entitlements'))
        assert_that(product_response.content['entitlements'], has_length(1))
        entitlement = product_response.content['entitlements'][0]

        assert_that(entitlement, has_key('code'))
        assert_that(entitlement['code'], equal_to(config.data.TEST_RM_PCT_PRO_DISC_COMP.ENTITLEMENT_CODE))

        assert_that(entitlement, has_key('compensation'))
        compensation = entitlement['compensation']

        assert_that(compensation, has_key('code'))
        assert_that(compensation['code'], equal_to(config.data.TEST_RM_PCT_PRO_DISC_COMP.COMPENSATION.CODE))

        assert_that(compensation, has_key('amount'))
        assert_that(compensation['amount'], equal_to(config.data.TEST_RM_PCT_PRO_DISC_COMP.COMPENSATION.AMOUNT))

    @pytest.allure.feature('functional')
    @pytest.allure.story('compensation')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_prod_with_compensation_have_fixed_disc_on_rm(self, config):

        fetch_product_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_RM_FIXED_DISC_COMP.CODE],
            config.store.profile_id,
            config.data.TEST_RM_FIXED_DISC_COMP.COUNTRY,
            config.data.TEST_RM_FIXED_DISC_COMP.LANGUAGE,
            config.data.TEST_RM_FIXED_DISC_COMP.STOREFRONT
        )
        fetch_product_response.assert_is_success()
        assert_that(fetch_product_response.content['body']['uriList'], has_length(1))
        url = fetch_product_response.content['body']['uriList'][0]

        product_response = RequestBuilder(url).get()
        product_response.assert_is_success()

        assert_that(product_response.content, has_key('entitlements'))
        assert_that(product_response.content['entitlements'], has_length(1))
        entitlement = product_response.content['entitlements'][0]

        assert_that(entitlement, has_key('code'))
        assert_that(entitlement['code'], equal_to(config.data.TEST_RM_FIXED_DISC_COMP.ENTITLEMENT_CODE))

        assert_that(entitlement, has_key('compensation'))
        compensation = entitlement['compensation']

        assert_that(compensation, has_key('code'))
        assert_that(compensation['code'], equal_to(config.data.TEST_RM_FIXED_DISC_COMP.COMPENSATION.CODE))

        assert_that(compensation, has_key('amount'))
        assert_that(compensation['amount'], equal_to(config.data.TEST_RM_FIXED_DISC_COMP.COMPENSATION.AMOUNT))

    @pytest.allure.feature('functional')
    @pytest.allure.story('compensation')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_prod_with_compensation_have_abs_disc_on_rm(self, config):

        fetch_product_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_RM_ABS_DISC_COMP.CODE],
            config.store.profile_id,
            config.data.TEST_RM_ABS_DISC_COMP.COUNTRY,
            config.data.TEST_RM_ABS_DISC_COMP.LANGUAGE,
            config.data.TEST_RM_ABS_DISC_COMP.STOREFRONT
        )
        fetch_product_response.assert_is_success()
        assert_that(fetch_product_response.content['body']['uriList'], has_length(1))
        url = fetch_product_response.content['body']['uriList'][0]

        product_response = RequestBuilder(url).get()
        product_response.assert_is_success()

        assert_that(product_response.content, has_key('entitlements'))
        assert_that(product_response.content['entitlements'], has_length(1))
        entitlement = product_response.content['entitlements'][0]

        assert_that(entitlement, has_key('code'))
        assert_that(entitlement['code'], equal_to(config.data.TEST_RM_ABS_DISC_COMP.ENTITLEMENT_CODE))

        assert_that(entitlement, has_key('compensation'))
        compensation = entitlement['compensation']

        assert_that(compensation, has_key('code'))
        assert_that(compensation['code'], equal_to(config.data.TEST_RM_ABS_DISC_COMP.COMPENSATION.CODE))

        assert_that(compensation, has_key('amount'))
        assert_that(compensation['amount'], equal_to(config.data.TEST_RM_ABS_DISC_COMP.COMPENSATION.AMOUNT))

    @pytest.allure.feature('functional')
    @pytest.allure.story('compensation')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_prod_with_compensation_have_pct_pro_disc_on_rm(self, config):

        fetch_product_list_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_RM_PCT_PRO_DISC_COMP.STOREFRONT,
            config.store.profile_id,
            config.data.TEST_RM_PCT_PRO_DISC_COMP.COUNTRY,
            config.data.TEST_RM_PCT_PRO_DISC_COMP.LANGUAGE
        )
        fetch_product_list_response.assert_is_success()

        assert_that(fetch_product_list_response.content['body'], has_key('uriList'))
        assert_that(fetch_product_list_response.content['body']['uriList'], not_none())
        uri_list = fetch_product_list_response.content['body']['uriList']

        prod = next(
            (
                prod_content for prod_content in PurchaseUtil.get_product_infos(uri_list)
                if prod_content['product_code'] == config.data.TEST_RM_PCT_PRO_DISC_COMP.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('entitlements'))
        assert_that(prod['entitlements'], has_length(1))
        entitlement = prod['entitlements'][0]

        assert_that(entitlement, has_key('code'))
        assert_that(entitlement['code'], equal_to(config.data.TEST_RM_PCT_PRO_DISC_COMP.ENTITLEMENT_CODE))

        assert_that(entitlement, has_key('compensation'))
        compensation = entitlement['compensation']

        assert_that(compensation, has_key('code'))
        assert_that(compensation['code'], equal_to(config.data.TEST_RM_PCT_PRO_DISC_COMP.COMPENSATION.CODE))
        assert_that(compensation, has_key('amount'))
        assert_that(compensation['amount'], equal_to(config.data.TEST_RM_PCT_PRO_DISC_COMP.COMPENSATION.AMOUNT))

    @pytest.allure.feature('functional')
    @pytest.allure.story('compensation')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_prod_with_compensation_have_fixed_disc_on_rm(self, config):

        fetch_product_list_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_RM_FIXED_DISC_COMP.STOREFRONT,
            config.store.profile_id,
            config.data.TEST_RM_FIXED_DISC_COMP.COUNTRY,
            config.data.TEST_RM_FIXED_DISC_COMP.LANGUAGE
        )
        fetch_product_list_response.assert_is_success()

        assert_that(fetch_product_list_response.content['body'], has_key('uriList'))
        assert_that(fetch_product_list_response.content['body']['uriList'], not_none())
        uri_list = fetch_product_list_response.content['body']['uriList']

        prod = next(
            (
                prod_content for prod_content in PurchaseUtil.get_product_infos(uri_list)
                if prod_content['product_code'] == config.data.TEST_RM_FIXED_DISC_COMP.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('entitlements'))
        assert_that(prod['entitlements'], has_length(1))
        entitlement = prod['entitlements'][0]

        assert_that(entitlement, has_key('code'))
        assert_that(entitlement['code'], equal_to(config.data.TEST_RM_FIXED_DISC_COMP.ENTITLEMENT_CODE))

        assert_that(entitlement, has_key('compensation'))
        compensation = entitlement['compensation']

        assert_that(compensation, has_key('code'))
        assert_that(compensation['code'], equal_to(config.data.TEST_RM_FIXED_DISC_COMP.COMPENSATION.CODE))
        assert_that(compensation, has_key('amount'))
        assert_that(compensation['amount'], equal_to(config.data.TEST_RM_FIXED_DISC_COMP.COMPENSATION.AMOUNT))

    @pytest.allure.feature('functional')
    @pytest.allure.story('compensation')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_prod_with_compensation_have_abs_disc_on_rm(self, config):

        fetch_product_list_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_RM_ABS_DISC_COMP.STOREFRONT,
            config.store.profile_id,
            config.data.TEST_RM_ABS_DISC_COMP.COUNTRY,
            config.data.TEST_RM_ABS_DISC_COMP.LANGUAGE
        )
        fetch_product_list_response.assert_is_success()

        assert_that(fetch_product_list_response.content['body'], has_key('uriList'))
        assert_that(fetch_product_list_response.content['body']['uriList'], not_none())
        uri_list = fetch_product_list_response.content['body']['uriList']

        prod = next(
            (
                prod_content for prod_content in PurchaseUtil.get_product_infos(uri_list)
                if prod_content['product_code'] == config.data.TEST_RM_ABS_DISC_COMP.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('entitlements'))
        assert_that(prod['entitlements'], has_length(1))
        entitlement = prod['entitlements'][0]

        assert_that(entitlement, has_key('code'))
        assert_that(entitlement['code'], equal_to(config.data.TEST_RM_ABS_DISC_COMP.ENTITLEMENT_CODE))

        assert_that(entitlement, has_key('compensation'))
        compensation = entitlement['compensation']

        assert_that(compensation, has_key('code'))
        assert_that(compensation['code'], equal_to(config.data.TEST_RM_ABS_DISC_COMP.COMPENSATION.CODE))
        assert_that(compensation, has_key('amount'))
        assert_that(compensation['amount'], equal_to(config.data.TEST_RM_ABS_DISC_COMP.COMPENSATION.AMOUNT))

    @pytest.allure.feature('functional')
    @pytest.allure.story('compensation')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_prod_with_compensation_have_fixed_disc_on_rm_and_vc(self, config):

        fetch_product_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_RM_AND_VC_FIXED_DISC_COMP.CODE],
            config.store.profile_id,
            config.data.TEST_RM_AND_VC_FIXED_DISC_COMP.COUNTRY,
            config.data.TEST_RM_AND_VC_FIXED_DISC_COMP.LANGUAGE,
            config.data.TEST_RM_AND_VC_FIXED_DISC_COMP.STOREFRONT
        )
        fetch_product_response.assert_is_success()

        assert_that(fetch_product_response.content['body']['uriList'], has_length(1))
        url = fetch_product_response.content['body']['uriList'][0]

        product_response = RequestBuilder(url).get()
        product_response.assert_is_success()

        assert_that(product_response.content, has_key('entitlements'))
        assert_that(product_response.content['entitlements'], has_length(1))
        entitlement = product_response.content['entitlements'][0]

        assert_that(entitlement, has_key('code'))
        assert_that(entitlement['code'], equal_to(config.data.TEST_RM_AND_VC_FIXED_DISC_COMP.ENTITLEMENT_CODE))

        assert_that(entitlement, has_key('compensation'))
        compensation = entitlement['compensation']

        assert_that(compensation, has_key('code'))
        assert_that(compensation['code'], equal_to(config.data.TEST_RM_AND_VC_FIXED_DISC_COMP.COMPENSATION.CODE))
        assert_that(compensation, has_key('amount'))
        assert_that(compensation['amount'], equal_to(config.data.TEST_RM_AND_VC_FIXED_DISC_COMP.COMPENSATION.AMOUNT))

    @pytest.allure.feature('functional')
    @pytest.allure.story('compensation')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_prod_with_compensation_have_abs_disc_on_rm_and_vc(self, config):

        fetch_product_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_RM_AND_VC_ABS_DISC_COMP.CODE],
            config.store.profile_id,
            config.data.TEST_RM_AND_VC_ABS_DISC_COMP.COUNTRY,
            config.data.TEST_RM_AND_VC_ABS_DISC_COMP.LANGUAGE,
            config.data.TEST_RM_AND_VC_ABS_DISC_COMP.STOREFRONT
        )
        fetch_product_response.assert_is_success()

        assert_that(fetch_product_response.content['body']['uriList'], has_length(1))
        url = fetch_product_response.content['body']['uriList'][0]

        product_response = RequestBuilder(url).get()
        product_response.assert_is_success()

        assert_that(product_response.content, has_key('entitlements'))
        assert_that(product_response.content['entitlements'], has_length(1))
        entitlement = product_response.content['entitlements'][0]

        assert_that(entitlement, has_key('code'))
        assert_that(entitlement['code'], equal_to(config.data.TEST_RM_AND_VC_ABS_DISC_COMP.ENTITLEMENT_CODE))

        assert_that(entitlement, has_key('compensation'))
        compensation = entitlement['compensation']

        assert_that(compensation, has_key('code'))
        assert_that(compensation['code'], equal_to(config.data.TEST_RM_AND_VC_ABS_DISC_COMP.COMPENSATION.CODE))
        assert_that(compensation, has_key('amount'))
        assert_that(compensation['amount'], equal_to(config.data.TEST_RM_AND_VC_ABS_DISC_COMP.COMPENSATION.AMOUNT))

    @pytest.allure.feature('functional')
    @pytest.allure.story('compensation')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_prod_with_compensation_have_fixed_disc_on_rm_and_vc(self, config):

        fetch_product_list_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_RM_AND_VC_FIXED_DISC_COMP.STOREFRONT,
            config.store.profile_id,
            config.data.TEST_RM_AND_VC_FIXED_DISC_COMP.COUNTRY,
            config.data.TEST_RM_AND_VC_FIXED_DISC_COMP.LANGUAGE
        )
        fetch_product_list_response.assert_is_success()

        assert_that(fetch_product_list_response.content['body'], has_key('uriList'))
        assert_that(fetch_product_list_response.content['body']['uriList'], not_none())
        uri_list = fetch_product_list_response.content['body']['uriList']

        prod = next(
            (
                prod_content for prod_content in PurchaseUtil.get_product_infos(uri_list)
                if prod_content['product_code'] == config.data.TEST_RM_AND_VC_FIXED_DISC_COMP.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('entitlements'))
        assert_that(prod['entitlements'], has_length(1))
        entitlement = prod['entitlements'][0]

        assert_that(entitlement, has_key('code'))
        assert_that(entitlement['code'], equal_to(config.data.TEST_RM_AND_VC_FIXED_DISC_COMP.ENTITLEMENT_CODE))

        assert_that(entitlement, has_key('compensation'))
        compensation = entitlement['compensation']

        assert_that(compensation, has_key('code'))
        assert_that(compensation['code'], equal_to(config.data.TEST_RM_AND_VC_FIXED_DISC_COMP.COMPENSATION.CODE))
        assert_that(compensation, has_key('amount'))
        assert_that(compensation['amount'], equal_to(config.data.TEST_RM_AND_VC_FIXED_DISC_COMP.COMPENSATION.AMOUNT))

    @pytest.allure.feature('functional')
    @pytest.allure.story('compensation')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_prod_with_compensation_have_abs_disc_on_rm_and_vc(self, config):

        fetch_product_list_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_RM_AND_VC_ABS_DISC_COMP.STOREFRONT,
            config.store.profile_id,
            config.data.TEST_RM_AND_VC_ABS_DISC_COMP.COUNTRY,
            config.data.TEST_RM_AND_VC_ABS_DISC_COMP.LANGUAGE
        )
        fetch_product_list_response.assert_is_success()

        assert_that(fetch_product_list_response.content['body'], has_key('uriList'))
        assert_that(fetch_product_list_response.content['body']['uriList'], not_none())
        uri_list = fetch_product_list_response.content['body']['uriList']

        prod = next(
            (
                prod_content for prod_content in PurchaseUtil.get_product_infos(uri_list)
                if prod_content['product_code'] == config.data.TEST_RM_AND_VC_ABS_DISC_COMP.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('entitlements'))
        assert_that(prod['entitlements'], has_length(1))
        entitlement = prod['entitlements'][0]

        assert_that(entitlement, has_key('code'))
        assert_that(entitlement['code'], equal_to(config.data.TEST_RM_AND_VC_ABS_DISC_COMP.ENTITLEMENT_CODE))

        assert_that(entitlement, has_key('compensation'))
        compensation = entitlement['compensation']

        assert_that(compensation, has_key('code'))
        assert_that(compensation['code'], equal_to(config.data.TEST_RM_AND_VC_ABS_DISC_COMP.COMPENSATION.CODE))
        assert_that(compensation, has_key('amount'))
        assert_that(compensation['amount'], equal_to(config.data.TEST_RM_AND_VC_ABS_DISC_COMP.COMPENSATION.AMOUNT))

    @pytest.allure.feature('functional')
    @pytest.allure.story('compensation')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_currency_exchange_product_with_pct_pro_disc(self, config):

        fetch_prod_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_RM_PCT_PRO_DISC_COMP.CODE],
            config.store.profile_id,
            config.data.TEST_RM_PCT_PRO_DISC_COMP.CURRENCY_EXCHANGE_COUNTRY,
            config.data.TEST_RM_PCT_PRO_DISC_COMP.LANGUAGE,
            config.data.TEST_RM_PCT_PRO_DISC_COMP.STOREFRONT
        )
        fetch_prod_response.assert_is_success()

        assert_that(fetch_prod_response.content['body'], has_key('uriList'))
        assert_that(fetch_prod_response.content['body']['uriList'], has_length(1))
        uri = fetch_prod_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('entitlements'))
        assert_that(prod_response.content['entitlements'], has_length(1))
        entitlement = prod_response.content['entitlements'][0]

        assert_that(entitlement, has_key('code'))
        assert_that(entitlement['code'], equal_to(config.data.TEST_RM_PCT_PRO_DISC_COMP.ENTITLEMENT_CODE))

        assert_that(entitlement, has_key('compensation'))
        compensation = entitlement['compensation']

        assert_that(compensation, has_key('code'))
        assert_that(compensation['code'], equal_to(config.data.TEST_RM_PCT_PRO_DISC_COMP.COMPENSATION.CODE))

        assert_that(compensation, has_key('amount'))
        assert_that(compensation['amount'], equal_to(config.data.TEST_RM_PCT_PRO_DISC_COMP.COMPENSATION.AMOUNT))

    @pytest.allure.feature('functional')
    @pytest.allure.story('compensation')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_currency_exchange_product_with_abs_disc(self, config):

        config.log.info('Fetching {}'.format(config.data.TEST_RM_ABS_DISC_COMP.CODE))

        fetch_prod_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_RM_ABS_DISC_COMP.CODE],
            config.store.profile_id,
            config.data.TEST_RM_ABS_DISC_COMP.CURRENCY_EXCHANGE.COUNTRY,
            config.data.TEST_RM_ABS_DISC_COMP.LANGUAGE,
            config.data.TEST_RM_ABS_DISC_COMP.STOREFRONT
        )
        fetch_prod_response.assert_is_success()

        assert_that(fetch_prod_response.content['body'], has_key('uriList'))
        assert_that(fetch_prod_response.content['body']['uriList'], has_length(1))
        uri = fetch_prod_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        config.log.info('Getting the discounted price of {}'.format(config.data.TEST_RM_ABS_DISC_COMP.CODE))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        discounted_cost = prod_response.content['price']['real_price']

        config.log.info('Getting the original cost of {}'.format(config.data.TEST_RM_ABS_DISC_COMP.CODE))

        assert_that(prod_response.content, has_key('original_price'))
        assert_that(prod_response.content['original_price'], has_key('real_price'))
        original_cost = prod_response.content['original_price']['real_price']

        assert_that(discounted_cost, has_key('code'))
        assert_that(original_cost, has_key('code'))
        assert_that(discounted_cost['code'], equal_to(original_cost['code']))

        config.log.info('Checking if discounted price ({}) is not equal to the original price ({})'.format(
            discounted_cost['amount'],
            original_cost['amount']
        ))

        assert_that(discounted_cost, has_key('amount'))
        assert_that(original_cost, has_key('amount'))

        config.log.info('Manually calculating the CES price of the original US price')

        ces_response = config.freya.product_service.get_ces_data()
        ces_response.assert_is_success()

        ces_data = ces_response.content[config.data.TEST_RM_ABS_DISC_COMP.RM_USD.CODE]
        assert_that(ces_data, has_key('quotes'))
        assert_that(ces_data['quotes'], has_key(config.data.TEST_RM_ABS_DISC_COMP.CURRENCY_EXCHANGE.CURRENCY_CODE))
        eur_ces = ces_data['quotes'][config.data.TEST_RM_ABS_DISC_COMP.CURRENCY_EXCHANGE.CURRENCY_CODE]

        assert_that(eur_ces, has_key('value'))
        ces_value = float(eur_ces['value'])

        euro = round(ces_value * config.data.TEST_RM_ABS_DISC_COMP.RM_USD.AMOUNT, 2)

        config.log.info('Calculating the difference between the manually calculated original cost and current cost')

        manual_cost_diff = euro - float(discounted_cost['amount'])

        config.log.info('Checking if discounted price ({}) is not original price ({})'.format(
            discounted_cost['amount'],
            original_cost['amount']
        ))

        config.log.info('Calculating difference of the cost')

        cost_diff = float(original_cost['amount']) - float(discounted_cost['amount'])

        config.log.info('Calculating the difference of the manual cost diff and the fetch diff')

        manual_fetch_cost_diff = abs(manual_cost_diff - cost_diff)

        config.log.info('The manual cost diff ({}) and the fetch cost diff ({}) should be similar'.format(
            manual_cost_diff,
            cost_diff
        ))

        assert_that(manual_fetch_cost_diff, equal_to(0.00))

        config.log.info('Calculating the percent discount of the cost')

        cost_disc = cost_diff / float(original_cost['amount'])

        config.log.info('Checking that entitlement is {}'.format(config.data.TEST_RM_ABS_DISC_COMP.ENTITLEMENT_CODE))

        assert_that(prod_response.content, has_key('entitlements'))
        assert_that(prod_response.content['entitlements'], has_length(1))
        entitlement = prod_response.content['entitlements'][0]

        assert_that(entitlement, has_key('code'))
        assert_that(entitlement['code'], equal_to(config.data.TEST_RM_ABS_DISC_COMP.ENTITLEMENT_CODE))

        assert_that(entitlement, has_key('compensation'))
        discounted_comp = entitlement['compensation']

        assert_that(discounted_comp, has_key('code'))
        assert_that(discounted_comp['code'], equal_to(config.data.TEST_RM_ABS_DISC_COMP.COMPENSATION.CODE))

        assert_that(discounted_comp, has_key('amount'))

        config.log.info(
            'Checking that compensation ({}) is not equal to the original compensation ({})'.format(
                discounted_comp['amount'],
                config.data.TEST_RM_ABS_DISC_COMP.ORIGINAL_COMPENSATION.AMOUNT
            ))

        assert_that(discounted_comp['amount'], is_not(config.data.TEST_RM_ABS_DISC_COMP.ORIGINAL_COMPENSATION.AMOUNT))

        config.log.info('Calculating the percent discount of the compensation')

        compensation_disc = 1.0 - (float(discounted_comp['amount']) / float(
            config.data.TEST_RM_ABS_DISC_COMP.ORIGINAL_COMPENSATION.AMOUNT))

        config.log.info('Calculating the difference between the percent cost disc and percent compensation disc')

        disc_comp_cost_difference = abs(round(compensation_disc - cost_disc, 2))

        config.log.info(
            'Checking if percentage price discount ({}) is about the same as the percentage compensation discount ({})'.format(
                cost_disc,
                compensation_disc
            ))

        assert_that(disc_comp_cost_difference, equal_to(0.00))

    @pytest.allure.feature('functional')
    @pytest.allure.story('compensation')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_currency_exchange_product_with_pct_pro_disc(self, config):

        fetch_product_list_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_RM_PCT_PRO_DISC_COMP.STOREFRONT,
            config.store.profile_id,
            config.data.TEST_RM_PCT_PRO_DISC_COMP.CURRENCY_EXCHANGE_COUNTRY,
            config.data.TEST_RM_PCT_PRO_DISC_COMP.LANGUAGE
        )
        fetch_product_list_response.assert_is_success()

        assert_that(fetch_product_list_response.content['body'], has_key('uriList'))
        assert_that(fetch_product_list_response.content['body']['uriList'], not_none())

        uri = fetch_product_list_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('entitlements'))
        assert_that(prod_response.content['entitlements'], has_length(1))
        entitlement = prod_response.content['entitlements'][0]

        assert_that(entitlement, has_key('code'))
        assert_that(entitlement['code'], equal_to(config.data.TEST_RM_PCT_PRO_DISC_COMP.ENTITLEMENT_CODE))

        assert_that(entitlement, has_key('compensation'))
        compensation = entitlement['compensation']

        assert_that(compensation, has_key('code'))
        assert_that(compensation['code'], equal_to(config.data.TEST_RM_PCT_PRO_DISC_COMP.COMPENSATION.CODE))

        assert_that(compensation, has_key('amount'))
        assert_that(compensation['amount'], equal_to(config.data.TEST_RM_PCT_PRO_DISC_COMP.COMPENSATION.AMOUNT))

    @pytest.allure.feature('functional')
    @pytest.allure.story('compensation')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_currency_exchange_product_with_abs_disc(self, config):

        config.log.info('Fetching {} products'.format(config.data.TEST_RM_ABS_DISC_COMP.STOREFRONT))

        fetch_product_list_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_RM_ABS_DISC_COMP.STOREFRONT,
            config.store.profile_id,
            config.data.TEST_RM_ABS_DISC_COMP.CURRENCY_EXCHANGE.COUNTRY,
            config.data.TEST_RM_ABS_DISC_COMP.LANGUAGE
        )
        fetch_product_list_response.assert_is_success()

        assert_that(fetch_product_list_response.content['body'], has_key('uriList'))
        assert_that(fetch_product_list_response.content['body']['uriList'], not_none())

        uri = fetch_product_list_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        config.log.info('Getting the discounted price')

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        discounted_cost = prod_response.content['price']['real_price']

        config.log.info('Getting the original price')

        assert_that(prod_response.content, has_key('original_price'))
        assert_that(prod_response.content['original_price'], has_key('real_price'))
        original_cost = prod_response.content['original_price']['real_price']

        assert_that(discounted_cost, has_key('code'))
        assert_that(original_cost, has_key('code'))
        assert_that(discounted_cost['code'], equal_to(original_cost['code']))

        assert_that(discounted_cost, has_key('amount'))
        assert_that(original_cost, has_key('amount'))

        config.log.info('Manually calculating the CES price of the original US price')

        ces_response = config.freya.product_service.get_ces_data()
        ces_response.assert_is_success()

        ces_data = ces_response.content[config.data.TEST_RM_ABS_DISC_COMP.RM_USD.CODE]
        assert_that(ces_data, has_key('quotes'))
        assert_that(ces_data['quotes'], has_key(config.data.TEST_RM_ABS_DISC_COMP.CURRENCY_EXCHANGE.CURRENCY_CODE))
        eur_ces = ces_data['quotes'][config.data.TEST_RM_ABS_DISC_COMP.CURRENCY_EXCHANGE.CURRENCY_CODE]

        assert_that(eur_ces, has_key('value'))
        ces_value = float(eur_ces['value'])

        euro = round(ces_value * config.data.TEST_RM_ABS_DISC_COMP.RM_USD.AMOUNT, 2)

        config.log.info('Calculating the difference between the manually calculated original cost and current cost')

        manual_cost_diff = euro - float(discounted_cost['amount'])

        config.log.info('Checking if discounted price ({}) is not original price ({})'.format(
            discounted_cost['amount'],
            original_cost['amount']
        ))

        config.log.info('Calculating difference of the cost')

        cost_diff = float(original_cost['amount']) - float(discounted_cost['amount'])

        config.log.info('Calculating the difference of the manual cost diff and the fetch diff')

        manual_fetch_cost_diff = abs(manual_cost_diff - cost_diff)

        config.log.info('The manual cost diff ({}) and the fetch cost diff ({}) should be similar'.format(
            manual_cost_diff,
            cost_diff
        ))

        assert_that(manual_fetch_cost_diff, equal_to(0.00))

        config.log.info('Calculating the percent discount of the cost')

        cost_discount = cost_diff / float(original_cost['amount'])

        config.log.info('Getting the entitlement {}'.format(config.data.TEST_RM_ABS_DISC_COMP.ENTITLEMENT_CODE))

        assert_that(prod_response.content, has_key('entitlements'))
        assert_that(prod_response.content['entitlements'], has_length(1))
        entitlement = prod_response.content['entitlements'][0]

        assert_that(entitlement, has_key('code'))
        assert_that(entitlement['code'], equal_to(config.data.TEST_RM_ABS_DISC_COMP.ENTITLEMENT_CODE))

        assert_that(entitlement, has_key('compensation'))
        compensation = entitlement['compensation']

        assert_that(compensation, has_key('code'))
        assert_that(compensation['code'], equal_to(config.data.TEST_RM_ABS_DISC_COMP.COMPENSATION.CODE))

        assert_that(compensation, has_key('amount'))

        config.log.info(
            'Checking if compensation amount ({}) is not original compensation amount ({})'.format(
                compensation['amount'],
                config.data.TEST_RM_ABS_DISC_COMP.ORIGINAL_COMPENSATION.AMOUNT
            ))

        assert_that(compensation['amount'], is_not(config.data.TEST_RM_ABS_DISC_COMP.ORIGINAL_COMPENSATION.AMOUNT))

        config.log.info('Calculating the percent discount of the compensation')

        comp_discount = 1.0 - (float(compensation['amount']) / float(
            config.data.TEST_RM_ABS_DISC_COMP.ORIGINAL_COMPENSATION.AMOUNT))

        config.log.info('Calculating the difference between the percent cost disc and percent compensation disc')

        disc_comp_cost_diff = round(cost_discount - comp_discount, 2)

        assert_that(disc_comp_cost_diff, equal_to(0.00))

    @pytest.allure.feature('functional')
    @pytest.allure.story('compensation')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_coefficients_is_enabled_with_pct_pro_disc(self, config):

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_RM_PCT_PRO_DISC_COMP.CODE],
            config.store.profile_id,
            config.data.TEST_RM_PCT_PRO_DISC_COMP.COEFFICIENT_COUNTRY,
            config.data.TEST_RM_PCT_PRO_DISC_COMP.LANGUAGE,
            config.data.TEST_RM_PCT_PRO_DISC_COMP.STOREFRONT
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        config.log.info('Getting the entitlement {}'.format(
            config.data.TEST_RM_PCT_PRO_DISC_COMP.ENTITLEMENT_CODE
        ))

        assert_that(prod_response.content, has_key('entitlements'))
        assert_that(prod_response.content['entitlements'], has_length(1))
        entitlement = prod_response.content['entitlements'][0]

        assert_that(entitlement, has_key('code'))
        assert_that(entitlement['code'], equal_to(config.data.TEST_RM_PCT_PRO_DISC_COMP.ENTITLEMENT_CODE))

        config.log.info('Getting the compensation of {}'.format(
            config.data.TEST_RM_PCT_PRO_DISC_COMP.ENTITLEMENT_CODE
        ))

        assert_that(entitlement, has_key('compensation'))
        comp = entitlement['compensation']

        config.log.info('Compensation should be {} {}'.format(
            config.data.TEST_RM_PCT_PRO_DISC_COMP.COMPENSATION.AMOUNT,
            config.data.TEST_RM_PCT_PRO_DISC_COMP.COMPENSATION.CODE
        ))

        assert_that(comp, has_key('code'))
        assert_that(comp['code'], equal_to(config.data.TEST_RM_PCT_PRO_DISC_COMP.COMPENSATION.CODE))

        assert_that(comp, has_key('amount'))
        assert_that(comp['amount'], equal_to(config.data.TEST_RM_PCT_PRO_DISC_COMP.COMPENSATION.AMOUNT))

    @pytest.mark.skip_for_regions('trie')
    @pytest.allure.feature('functional')
    @pytest.allure.story('compensation')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_coefficients_is_enabled_with_abs_disc(self, config):

        config.log.info('Get the coefficient')

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
            pytest.skip('Coefficient is not enabled')

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

        config.log.info('Get the CES for US to AR')

        ces_response = config.freya.product_service.get_ces_data()
        ces_response.assert_is_success()

        ces_data = ces_response.content[config.data.TEST_RM_ABS_DISC_COMP.RM_USD.CODE]
        assert_that(ces_data, has_key('quotes'))
        assert_that(ces_data['quotes'], has_key(config.data.TEST_RM_ABS_DISC_COMP.COEFFICIENT.CURRENCY_CODE))

        ar_ces = ces_data['quotes'][config.data.TEST_RM_ABS_DISC_COMP.COEFFICIENT.CURRENCY_CODE]
        assert_that(ar_ces, has_key('value'))
        ces = float(ar_ces['value'])

        config.log.info('CES for ARS to USD on {} is {}'.format(
            config.environment.environment_name,
            ces
        ))

        config.log.info('Calculate the cost of the ')

        manual_calculated_ars = int(round(config.data.TEST_RM_ABS_DISC_COMP.RM_USD.AMOUNT * coefficient * ces, 0))

        config.log.info('Fetch {}'.format(
            config.data.TEST_RM_ABS_DISC_COMP.CODE
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_RM_ABS_DISC_COMP.CODE],
            config.store.profile_id,
            config.data.TEST_RM_ABS_DISC_COMP.COEFFICIENT.COUNTRY,
            config.data.TEST_RM_ABS_DISC_COMP.LANGUAGE,
            config.data.TEST_RM_ABS_DISC_COMP.STOREFRONT
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        config.log.info('Get the discounted price')

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        disc_cost = prod_response.content['price']['real_price']

        assert_that(disc_cost, has_key('code'))
        assert_that(disc_cost['code'], equal_to(config.data.TEST_RM_ABS_DISC_COMP.COEFFICIENT.CURRENCY_CODE))
        assert_that(disc_cost, has_key('amount'))

        config.log.info('Get the original price')

        assert_that(prod_response.content, has_key('original_price'))
        assert_that(prod_response.content['original_price'], has_key('real_price'))
        original_cost = prod_response.content['original_price']['real_price']

        assert_that(original_cost, has_key('code'))
        assert_that(original_cost['code'], equal_to(config.data.TEST_RM_ABS_DISC_COMP.COEFFICIENT.CURRENCY_CODE))
        assert_that(original_cost, has_key('amount'))

        config.log.info('Calculate the difference between the manually converted cost and the discount cost')

        manual_cost_diff = manual_calculated_ars - int(disc_cost['amount'])

        config.log.info('Calcualte the difference between the fetched original cost and the discount cost')

        disc_cost_diff = int(original_cost['amount']) - int(disc_cost['amount'])

        config.log.info('Manually calculated cost discount {} should the same as the fetched cost discount {}'.format(
            manual_cost_diff,
            disc_cost_diff
        ))

        assert_that(manual_cost_diff, equal_to(disc_cost_diff))

        config.log.info('Calculate the percent discount of the cost')

        disc_cost_percent = round(disc_cost_diff / float(original_cost['amount']), 2)

        config.log.info('Get the entitlement {}'.format(
            config.data.TEST_RM_ABS_DISC_COMP.ENTITLEMENT_CODE
        ))

        assert_that(prod_response.content, has_key('entitlements'))
        assert_that(prod_response.content['entitlements'], has_length(1))
        entitlement = prod_response.content['entitlements'][0]

        config.log.info('Get the compensation')

        assert_that(entitlement, has_key('compensation'))
        disc_comp = entitlement['compensation']

        assert_that(disc_comp, has_key('code'))
        assert_that(disc_comp['code'], equal_to(config.data.TEST_RM_ABS_DISC_COMP.ORIGINAL_COMPENSATION.CODE))

        config.log.info('Calculate the percent discount of the compensation')

        disc_comp_percent = round(
            1 - (float(disc_comp['amount']) / config.data.TEST_RM_ABS_DISC_COMP.ORIGINAL_COMPENSATION.AMOUNT), 2)

        assert_that(disc_comp_percent, equal_to(disc_cost_percent))

    @pytest.allure.feature('functional')
    @pytest.allure.story('compensation')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_coefficients_is_enabled_with_pct_pro_disc(self, config):

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_RM_PCT_PRO_DISC_COMP.STOREFRONT,
            config.store.profile_id,
            config.data.TEST_RM_PCT_PRO_DISC_COMP.COEFFICIENT_COUNTRY,
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
            )
        )

        config.log.info('Getting the entitlement {}'.format(
            config.data.TEST_RM_PCT_PRO_DISC_COMP.ENTITLEMENT_CODE
        ))

        assert_that(prod, has_key('entitlements'))
        assert_that(prod['entitlements'], has_length(1))
        entitlement = prod['entitlements'][0]

        assert_that(entitlement, has_key('code'))
        assert_that(entitlement['code'], equal_to(config.data.TEST_RM_PCT_PRO_DISC_COMP.ENTITLEMENT_CODE))

        config.log.info('Getting the compensation of {}'.format(
            config.data.TEST_RM_PCT_PRO_DISC_COMP.ENTITLEMENT_CODE
        ))

        assert_that(entitlement, has_key('compensation'))
        comp = entitlement['compensation']

        config.log.info('Compensation should be {} {}'.format(
            config.data.TEST_RM_PCT_PRO_DISC_COMP.COMPENSATION.AMOUNT,
            config.data.TEST_RM_PCT_PRO_DISC_COMP.COMPENSATION.CODE
        ))

        assert_that(comp, has_key('code'))
        assert_that(comp['code'], equal_to(config.data.TEST_RM_PCT_PRO_DISC_COMP.COMPENSATION.CODE))

        assert_that(comp, has_key('amount'))
        assert_that(comp['amount'], equal_to(config.data.TEST_RM_PCT_PRO_DISC_COMP.COMPENSATION.AMOUNT))

    @pytest.mark.skip_for_regions('trie')
    @pytest.allure.feature('functional')
    @pytest.allure.story('compensation')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_coefficients_is_enabled_with_abs_disc(self, config):

        config.log.info('Get the coefficient')

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
            pytest.skip('Coefficient is not enabled')

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

        config.log.info('Get the CES for US to AR')

        ces_response = config.freya.product_service.get_ces_data()
        ces_response.assert_is_success()

        ces_data = ces_response.content[config.data.TEST_RM_ABS_DISC_COMP.RM_USD.CODE]
        assert_that(ces_data, has_key('quotes'))
        assert_that(ces_data['quotes'], has_key(config.data.TEST_RM_ABS_DISC_COMP.COEFFICIENT.CURRENCY_CODE))

        ar_ces = ces_data['quotes'][config.data.TEST_RM_ABS_DISC_COMP.COEFFICIENT.CURRENCY_CODE]
        assert_that(ar_ces, has_key('value'))
        ces = float(ar_ces['value'])

        config.log.info('CES for ARS to USD on {} is {}'.format(
            config.environment.environment_name,
            ces
        ))

        config.log.info('Calculate the cost of the ')

        manual_calculated_ars = int(round(config.data.TEST_RM_ABS_DISC_COMP.RM_USD.AMOUNT * coefficient * ces, 0))

        config.log.info('Fetch {}'.format(
            config.data.TEST_RM_ABS_DISC_COMP.CODE
        ))

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_RM_ABS_DISC_COMP.STOREFRONT,
            config.store.profile_id,
            config.data.TEST_RM_ABS_DISC_COMP.COEFFICIENT.COUNTRY,
            config.data.TEST_RM_ABS_DISC_COMP.LANGUAGE,

        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri_list = fetch_response.content['body']['uriList']

        prod = next(
            (
                prod for prod in PurchaseUtil.get_product_infos(uri_list)
                if prod['product_code'] == config.data.TEST_RM_ABS_DISC_COMP.CODE
            )
        )

        config.log.info('Get the discounted price')

        assert_that(prod, has_key('price'))
        assert_that(prod['price'], has_key('real_price'))
        disc_cost = prod['price']['real_price']

        assert_that(disc_cost, has_key('code'))
        assert_that(disc_cost['code'], equal_to(config.data.TEST_RM_ABS_DISC_COMP.COEFFICIENT.CURRENCY_CODE))
        assert_that(disc_cost, has_key('amount'))

        config.log.info('Get the original price')

        assert_that(prod, has_key('original_price'))
        assert_that(prod['original_price'], has_key('real_price'))
        original_cost = prod['original_price']['real_price']

        assert_that(original_cost, has_key('code'))
        assert_that(original_cost['code'], equal_to(config.data.TEST_RM_ABS_DISC_COMP.COEFFICIENT.CURRENCY_CODE))
        assert_that(original_cost, has_key('amount'))

        config.log.info('Calculate the difference between the manually converted cost and the discount cost')

        manual_cost_diff = manual_calculated_ars - int(disc_cost['amount'])

        config.log.info('Calcualte the difference between the fetched original cost and the discount cost')

        disc_cost_diff = int(original_cost['amount']) - int(disc_cost['amount'])

        config.log.info('Manually calculated cost discount {} should the same as the fetched cost discount {}'.format(
            manual_cost_diff,
            disc_cost_diff
        ))

        assert_that(manual_cost_diff, equal_to(disc_cost_diff))

        config.log.info('Calculate the percent discount of the cost')

        disc_cost_percent = round(disc_cost_diff / float(original_cost['amount']), 2)

        config.log.info('Get the entitlement {}'.format(
            config.data.TEST_RM_ABS_DISC_COMP.ENTITLEMENT_CODE
        ))

        assert_that(prod, has_key('entitlements'))
        assert_that(prod['entitlements'], has_length(1))
        entitlement = prod['entitlements'][0]

        config.log.info('Get the compensation')

        assert_that(entitlement, has_key('compensation'))
        disc_comp = entitlement['compensation']

        assert_that(disc_comp, has_key('code'))
        assert_that(disc_comp['code'], equal_to(config.data.TEST_RM_ABS_DISC_COMP.ORIGINAL_COMPENSATION.CODE))

        config.log.info('Calculate the percent discount of the compensation')

        disc_comp_percent = round(
            1 - (float(disc_comp['amount']) / config.data.TEST_RM_ABS_DISC_COMP.ORIGINAL_COMPENSATION.AMOUNT), 2)

        assert_that(disc_comp_percent, equal_to(disc_cost_percent))
