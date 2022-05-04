import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities, RequestBuilder, PurchaseUtil


@pytest.allure.feature('functional')
@pytest.allure.story('discount priority')
@pytest.allure.severity(severity_level.CRITICAL)
class TestDiscountPriority(object):

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

        config.store.wgid = account_created.content['id']

        ###
        # Runs test
        yield

        ###
        # Test cleanup

        delete_response = config.spa.http.delete_account(config.store.wgid)
        delete_response.assert_is_success()

    def test_fetch_products_should_succeed_when_promo_have_pct_pro_blank_and_pct_pro_vc_curr_disc(self, config):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_VC_CURRENCY_PROMO.CODE],
            config.store.wgid,
            config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_VC_CURRENCY_PROMO.COUNTRY,
            config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_VC_CURRENCY_PROMO.LANGUAGE,
            storefront=config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_VC_CURRENCY_PROMO.STOREFRONT
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('virtual_price'))
        assert_that(prod_response.content['price']['virtual_price'], has_length(1))

        cost = prod_response.content['price']['virtual_price'][0]

        assert_that(cost, has_key('code'))
        assert_that(
            cost['code'],
            equal_to(config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_VC_CURRENCY_PROMO.VIRTUAL_CURRENCY.CODE)
        )

        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to(str(config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_VC_CURRENCY_PROMO.VIRTUAL_CURRENCY.AMOUNT))
        )

    def test_fetch_product_list_should_succeed_when_promo_have_pct_pro_blank_and_pct_pro_vc_curr_disc(self, config):
        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_VC_CURRENCY_PROMO.STOREFRONT,
            config.store.wgid,
            config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_VC_CURRENCY_PROMO.COUNTRY,
            config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_VC_CURRENCY_PROMO.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri_list = fetch_response.content['body']['uriList']

        prod = next(
            (
                prod for prod in PurchaseUtil.get_product_infos(uri_list)
                if prod['product_code'] == config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_VC_CURRENCY_PROMO.CODE
            )
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('price'))
        assert_that(prod['price'], has_key('virtual_price'))
        assert_that(prod['price']['virtual_price'], has_length(1))

        cost = prod['price']['virtual_price'][0]

        assert_that(cost, has_key('code'))
        assert_that(
            cost['code'],
            equal_to(config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_VC_CURRENCY_PROMO.VIRTUAL_CURRENCY.CODE)
        )

        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to(str(config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_VC_CURRENCY_PROMO.VIRTUAL_CURRENCY.AMOUNT))
        )

    def test_fetch_products_should_succeed_when_promo_have_pct_pro_blank_and_pct_pro_zone_disc(self, config):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_ZONE_PROMO.CODE],
            config.store.wgid,
            config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_ZONE_PROMO.US.COUNTRY,
            config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_ZONE_PROMO.LANGUAGE,
            storefront=config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_ZONE_PROMO.STOREFRONT
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
        assert_that(
            cost['code'],
            equal_to(config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_ZONE_PROMO.US.REAL_MONEY.CODE)
        )
        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to('{0:.2f}'.format(config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_ZONE_PROMO.US.REAL_MONEY.AMOUNT))
        )

    def test_fetch_products_should_succeed_when_promo_have_pct_pro_blank_and_fixed_zone_disc(self, config):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PCT_PRO_BLANK_AND_FIXED_ZONE_PROMO.CODE],
            config.store.wgid,
            config.data.TEST_PCT_PRO_BLANK_AND_FIXED_ZONE_PROMO.US.COUNTRY,
            config.data.TEST_PCT_PRO_BLANK_AND_FIXED_ZONE_PROMO.LANGUAGE,
            storefront=config.data.TEST_PCT_PRO_BLANK_AND_FIXED_ZONE_PROMO.STOREFRONT
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
        assert_that(
            cost['code'],
            equal_to(config.data.TEST_PCT_PRO_BLANK_AND_FIXED_ZONE_PROMO.US.REAL_MONEY.CODE)
        )
        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to('{0:.2f}'.format(config.data.TEST_PCT_PRO_BLANK_AND_FIXED_ZONE_PROMO.US.REAL_MONEY.AMOUNT))
        )

    def test_fetch_product_list_should_succeed_when_promo_have_pct_pro_blank_and_fixed_zone_disc(self, config):
        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_PCT_PRO_BLANK_AND_FIXED_ZONE_PROMO.STOREFRONT,
            config.store.wgid,
            config.data.TEST_PCT_PRO_BLANK_AND_FIXED_ZONE_PROMO.US.COUNTRY,
            config.data.TEST_PCT_PRO_BLANK_AND_FIXED_ZONE_PROMO.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri_list = fetch_response.content['body']['uriList']

        prod = next(
            (
                prod for prod in PurchaseUtil.get_product_infos(uri_list)
                if prod['product_code'] == config.data.TEST_PCT_PRO_BLANK_AND_FIXED_ZONE_PROMO.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('price'))
        assert_that(prod['price'], has_key('real_price'))

        cost = prod['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(
            cost['code'],
            equal_to(config.data.TEST_PCT_PRO_BLANK_AND_FIXED_ZONE_PROMO.US.REAL_MONEY.CODE)
        )
        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to('{0:.2f}'.format(config.data.TEST_PCT_PRO_BLANK_AND_FIXED_ZONE_PROMO.US.REAL_MONEY.AMOUNT))
        )

    def test_fetch_products_should_succeed_when_promo_have_pct_pro_blank_and_abs_zone_disc(self, config):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_PROMO.CODE],
            config.store.wgid,
            config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_PROMO.US.COUNTRY,
            config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_PROMO.LANGUAGE,
            storefront=config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_PROMO.STOREFRONT
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
        assert_that(
            cost['code'],
            equal_to(config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_PROMO.US.REAL_MONEY.CODE)
        )
        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to('{0:.2f}'.format(config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_PROMO.US.REAL_MONEY.AMOUNT))
        )

    def test_fetch_product_list_should_succeed_when_promo_have_pct_pro_blank_and_abs_zone_disc(self, config):
        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_PROMO.STOREFRONT,
            config.store.wgid,
            config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_PROMO.US.COUNTRY,
            config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_PROMO.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri_list = fetch_response.content['body']['uriList']

        prod = next(
            (
                prod for prod in PurchaseUtil.get_product_infos(uri_list)
                if prod['product_code'] == config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_PROMO.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('price'))
        assert_that(prod['price'], has_key('real_price'))

        cost = prod['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(
            cost['code'],
            equal_to(config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_PROMO.US.REAL_MONEY.CODE)
        )
        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to('{0:.2f}'.format(config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_PROMO.US.REAL_MONEY.AMOUNT))
        )

    def test_fetch_products_should_succeed_when_promo_have_pct_pro_blank_and_abs_country_disc(self, config):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PCT_PRO_BLANK_AND_ABS_COUNTRY_PROMO.CODE],
            config.store.wgid,
            config.data.TEST_PCT_PRO_BLANK_AND_ABS_COUNTRY_PROMO.US.COUNTRY,
            config.data.TEST_PCT_PRO_BLANK_AND_ABS_COUNTRY_PROMO.LANGUAGE,
            storefront=config.data.TEST_PCT_PRO_BLANK_AND_ABS_COUNTRY_PROMO.STOREFRONT
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
        assert_that(
            cost['code'],
            equal_to(config.data.TEST_PCT_PRO_BLANK_AND_ABS_COUNTRY_PROMO.US.REAL_MONEY.CODE)
        )
        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to('{0:.2f}'.format(config.data.TEST_PCT_PRO_BLANK_AND_ABS_COUNTRY_PROMO.US.REAL_MONEY.AMOUNT))
        )

    def test_fetch_product_list_should_succeed_when_promo_have_pct_pro_blank_and_abs_country_disc(self, config):
        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_PCT_PRO_BLANK_AND_ABS_COUNTRY_PROMO.STOREFRONT,
            config.store.wgid,
            config.data.TEST_PCT_PRO_BLANK_AND_ABS_COUNTRY_PROMO.US.COUNTRY,
            config.data.TEST_PCT_PRO_BLANK_AND_ABS_COUNTRY_PROMO.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri_list = fetch_response.content['body']['uriList']

        prod = next(
            (
                prod for prod in PurchaseUtil.get_product_infos(uri_list)
                if prod['product_code'] == config.data.TEST_PCT_PRO_BLANK_AND_ABS_COUNTRY_PROMO.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('price'))
        assert_that(prod['price'], has_key('real_price'))

        cost = prod['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(
            cost['code'],
            equal_to(config.data.TEST_PCT_PRO_BLANK_AND_ABS_COUNTRY_PROMO.US.REAL_MONEY.CODE)
        )
        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to('{0:.2f}'.format(config.data.TEST_PCT_PRO_BLANK_AND_ABS_COUNTRY_PROMO.US.REAL_MONEY.AMOUNT))
        )

    def test_fetch_products_should_succeed_when_promo_have_pct_pro_zone_and_abs_country_disc(self, config):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PCT_PRO_ZONE_AND_ABS_COUNTRY_PROMO.CODE],
            config.store.wgid,
            config.data.TEST_PCT_PRO_ZONE_AND_ABS_COUNTRY_PROMO.US.COUNTRY,
            config.data.TEST_PCT_PRO_ZONE_AND_ABS_COUNTRY_PROMO.LANGUAGE,
            storefront=config.data.TEST_PCT_PRO_ZONE_AND_ABS_COUNTRY_PROMO.STOREFRONT
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
        assert_that(
            cost['code'],
            equal_to(config.data.TEST_PCT_PRO_ZONE_AND_ABS_COUNTRY_PROMO.US.REAL_MONEY.CODE)
        )
        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to('{0:.2f}'.format(config.data.TEST_PCT_PRO_ZONE_AND_ABS_COUNTRY_PROMO.US.REAL_MONEY.AMOUNT))
        )

    def test_fetch_product_list_should_succeed_when_promo_have_pct_pro_zone_and_abs_country_disc(self, config):
        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_PCT_PRO_ZONE_AND_ABS_COUNTRY_PROMO.STOREFRONT,
            config.store.wgid,
            config.data.TEST_PCT_PRO_ZONE_AND_ABS_COUNTRY_PROMO.US.COUNTRY,
            config.data.TEST_PCT_PRO_ZONE_AND_ABS_COUNTRY_PROMO.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri_list = fetch_response.content['body']['uriList']

        prod = next(
            (
                prod for prod in PurchaseUtil.get_product_infos(uri_list)
                if prod['product_code'] == config.data.TEST_PCT_PRO_ZONE_AND_ABS_COUNTRY_PROMO.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('price'))
        assert_that(prod['price'], has_key('real_price'))

        cost = prod['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(
            cost['code'],
            equal_to(config.data.TEST_PCT_PRO_ZONE_AND_ABS_COUNTRY_PROMO.US.REAL_MONEY.CODE)
        )
        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to('{0:.2f}'.format(config.data.TEST_PCT_PRO_ZONE_AND_ABS_COUNTRY_PROMO.US.REAL_MONEY.AMOUNT))
        )

    def test_fetch_products_should_succeed_when_promo_have_fixed_zone_and_abs_country_disc(self, config):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_FIXED_ZONE_AND_ABS_COUNTRY_PROMO.CODE],
            config.store.wgid,
            config.data.TEST_FIXED_ZONE_AND_ABS_COUNTRY_PROMO.US.COUNTRY,
            config.data.TEST_FIXED_ZONE_AND_ABS_COUNTRY_PROMO.LANGUAGE,
            storefront=config.data.TEST_FIXED_ZONE_AND_ABS_COUNTRY_PROMO.STOREFRONT
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
        assert_that(
            cost['code'],
            equal_to(config.data.TEST_FIXED_ZONE_AND_ABS_COUNTRY_PROMO.US.REAL_MONEY.CODE)
        )
        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to('{0:.2f}'.format(config.data.TEST_FIXED_ZONE_AND_ABS_COUNTRY_PROMO.US.REAL_MONEY.AMOUNT))
        )

    def test_fetch_product_list_should_succeed_when_promo_have_fixed_zone_and_abs_country_disc(self, config):
        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_FIXED_ZONE_AND_ABS_COUNTRY_PROMO.STOREFRONT,
            config.store.wgid,
            config.data.TEST_FIXED_ZONE_AND_ABS_COUNTRY_PROMO.US.COUNTRY,
            config.data.TEST_FIXED_ZONE_AND_ABS_COUNTRY_PROMO.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri_list = fetch_response.content['body']['uriList']

        prod = next(
            (
                prod for prod in PurchaseUtil.get_product_infos(uri_list)
                if prod['product_code'] == config.data.TEST_FIXED_ZONE_AND_ABS_COUNTRY_PROMO.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('price'))
        assert_that(prod['price'], has_key('real_price'))

        cost = prod['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(
            cost['code'],
            equal_to(config.data.TEST_FIXED_ZONE_AND_ABS_COUNTRY_PROMO.US.REAL_MONEY.CODE)
        )
        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to('{0:.2f}'.format(config.data.TEST_FIXED_ZONE_AND_ABS_COUNTRY_PROMO.US.REAL_MONEY.AMOUNT))
        )

    def test_fetch_products_should_succeed_when_promo_have_abs_zone_and_abs_country_disc(self, config):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_ABS_ZONE_AND_ABS_COUNTRY_PROMO.CODE],
            config.store.wgid,
            config.data.TEST_ABS_ZONE_AND_ABS_COUNTRY_PROMO.US.COUNTRY,
            config.data.TEST_ABS_ZONE_AND_ABS_COUNTRY_PROMO.LANGUAGE,
            storefront=config.data.TEST_ABS_ZONE_AND_ABS_COUNTRY_PROMO.STOREFRONT
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
        assert_that(
            cost['code'],
            equal_to(config.data.TEST_ABS_ZONE_AND_ABS_COUNTRY_PROMO.US.REAL_MONEY.CODE)
        )
        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to('{0:.2f}'.format(config.data.TEST_ABS_ZONE_AND_ABS_COUNTRY_PROMO.US.REAL_MONEY.AMOUNT))
        )

    def test_fetch_product_list_should_succeed_when_promo_have_abs_zone_and_abs_country_disc(self, config):
        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_ABS_ZONE_AND_ABS_COUNTRY_PROMO.STOREFRONT,
            config.store.wgid,
            config.data.TEST_ABS_ZONE_AND_ABS_COUNTRY_PROMO.US.COUNTRY,
            config.data.TEST_ABS_ZONE_AND_ABS_COUNTRY_PROMO.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri_list = fetch_response.content['body']['uriList']

        prod = next(
            (
                prod for prod in PurchaseUtil.get_product_infos(uri_list)
                if prod['product_code'] == config.data.TEST_ABS_ZONE_AND_ABS_COUNTRY_PROMO.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('price'))
        assert_that(prod['price'], has_key('real_price'))

        cost = prod['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(
            cost['code'],
            equal_to(config.data.TEST_ABS_ZONE_AND_ABS_COUNTRY_PROMO.US.REAL_MONEY.CODE)
        )
        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to('{0:.2f}'.format(config.data.TEST_ABS_ZONE_AND_ABS_COUNTRY_PROMO.US.REAL_MONEY.AMOUNT))
        )

    def test_fetch_products_should_succeed_when_promo_have_pct_pro_blank_and_abs_zone_and_country_disc(self, config):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_COUNTRY_PROMO.CODE],
            config.store.wgid,
            config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_COUNTRY_PROMO.US.COUNTRY,
            config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_COUNTRY_PROMO.LANGUAGE,
            storefront=config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_COUNTRY_PROMO.STOREFRONT
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
        assert_that(
            cost['code'],
            equal_to(config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_COUNTRY_PROMO.US.REAL_MONEY.CODE)
        )
        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to('{0:.2f}'.format(config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_COUNTRY_PROMO.US.REAL_MONEY.AMOUNT))
        )

    def test_fetch_product_list_should_succeed_when_promo_have_pct_pro_blank_and_abs_zone_and_country_disc(self,
                                                                                                           config):
        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_COUNTRY_PROMO.STOREFRONT,
            config.store.wgid,
            config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_COUNTRY_PROMO.US.COUNTRY,
            config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_COUNTRY_PROMO.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri_list = fetch_response.content['body']['uriList']

        prod = next(
            (
                prod for prod in PurchaseUtil.get_product_infos(uri_list)
                if prod['product_code'] == config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_COUNTRY_PROMO.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('price'))
        assert_that(prod['price'], has_key('real_price'))

        cost = prod['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(
            cost['code'],
            equal_to(config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_COUNTRY_PROMO.US.REAL_MONEY.CODE)
        )
        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to('{0:.2f}'.format(config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_COUNTRY_PROMO.US.REAL_MONEY.AMOUNT))
        )
