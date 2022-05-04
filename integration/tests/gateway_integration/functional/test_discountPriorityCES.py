import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities, RequestBuilder, PurchaseUtil


@pytest.allure.feature('functional')
@pytest.allure.story('discount priority for CES conversion')
@pytest.allure.severity(severity_level.CRITICAL)
class TestDiscountPriorityCES(object):

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

        config.log.info('Get CES data for US to BO currency')

        ces_response = config.freya.product_service.get_ces_data()
        ces_response.assert_is_success()

        ces_data = ces_response.content[config.data.TEST_DISCOUNT_PRIORITY_CES.US_CURRENCY_CODE]
        assert_that(ces_data, has_key('quotes'))
        assert_that(ces_data['quotes'], has_key(config.data.TEST_DISCOUNT_PRIORITY_CES.BO_CURRENCY_CODE))

        bo_ces = ces_data['quotes'][config.data.TEST_DISCOUNT_PRIORITY_CES.BO_CURRENCY_CODE]
        assert_that(bo_ces, has_key('value'))
        bo_ces_value = float(bo_ces['value'])

        config.log.info('CES for BO is {}'.format(bo_ces_value))

        config.store.ces_cost = int(
            round(config.data.TEST_DISCOUNT_PRIORITY_CES.ORIGINAL_COST_AMOUNT * bo_ces_value, 0)
        )

        config.log.info('Calculated converted price is {} {}'.format(
            config.store.ces_cost,
            config.data.TEST_DISCOUNT_PRIORITY_CES.BO_CURRENCY_CODE
        ))

        ###
        # Run test
        yield

        ###
        # Test cleanup
        delete_response = config.spa.http.delete_account(config.store.wgid)
        delete_response.assert_is_success()

    def test_fetch_products_should_succeed_when_promo_have_pct_pro_blank_and_pct_pro_zone_disc_in_bo(self, config):
        config.log.info('Calculating discounted price for {}'.format(
            config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_ZONE_PROMO.CODE
        ))

        calculated_cost = int(round(
            config.store.ces_cost * (1 - config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_ZONE_PROMO.DISCOUNT),
            0
        ))

        config.log.info('Calculated cost is {} {}'.format(
            calculated_cost,
            config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_ZONE_PROMO.BO.REAL_MONEY_CODE
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_ZONE_PROMO.CODE],
            config.store.wgid,
            config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_ZONE_PROMO.BO.COUNTRY,
            config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_ZONE_PROMO.LANGUAGE,
            storefront=config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_ZONE_PROMO.STOREFRONT
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        url = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(url).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_ZONE_PROMO.BO.REAL_MONEY_CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(calculated_cost)))

    def test_fetch_product_list_should_succeed_when_promo_have_pct_pro_blank_and_pct_pro_zone_disc_in_bo(self, config):
        config.log.info('Calculating discounted price for {}'.format(
            config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_ZONE_PROMO.CODE
        ))

        calculated_cost = int(round(
            config.store.ces_cost * (1 - config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_ZONE_PROMO.DISCOUNT),
            0
        ))

        config.log.info('Calculated cost is {} {}'.format(
            calculated_cost,
            config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_ZONE_PROMO.BO.REAL_MONEY_CODE
        ))

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_ZONE_PROMO.STOREFRONT,
            config.store.wgid,
            config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_ZONE_PROMO.BO.COUNTRY,
            config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_ZONE_PROMO.LANGUAGE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri_list = fetch_response.content['body']['uriList']

        prod = next(
            (
                prod for prod in PurchaseUtil.get_product_infos(uri_list)
                if prod['product_code'] == config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_ZONE_PROMO.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('price'))
        assert_that(prod['price'], has_key('real_price'))
        cost = prod['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_PCT_PRO_BLANK_AND_PCT_PRO_ZONE_PROMO.BO.REAL_MONEY_CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(calculated_cost)))

    def test_fetch_products_should_succeed_when_promo_have_pct_pro_blank_and_fixed_zone_disc_in_bo(self, config):
        config.log.info('Calculating discounted price for {}'.format(
            config.data.TEST_PCT_PRO_BLANK_AND_FIXED_ZONE_PROMO.CODE
        ))

        calculated_cost = int(round(config.store.ces_cost * (
                config.data.TEST_PCT_PRO_BLANK_AND_FIXED_ZONE_PROMO.US.REAL_MONEY.AMOUNT / config.data.TEST_PCT_PRO_BLANK_AND_FIXED_ZONE_PROMO.ORIGINAL_BASE_PRICE),
                                    0))

        config.log.info('Calculated cost is {} {}'.format(
            calculated_cost,
            config.data.TEST_PCT_PRO_BLANK_AND_FIXED_ZONE_PROMO.BO.REAL_MONEY_CODE
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PCT_PRO_BLANK_AND_FIXED_ZONE_PROMO.CODE],
            config.store.wgid,
            config.data.TEST_PCT_PRO_BLANK_AND_FIXED_ZONE_PROMO.BO.COUNTRY,
            config.data.TEST_PCT_PRO_BLANK_AND_FIXED_ZONE_PROMO.LANGUAGE,
            storefront=config.data.TEST_PCT_PRO_BLANK_AND_FIXED_ZONE_PROMO.STOREFRONT
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        url = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(url).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_PCT_PRO_BLANK_AND_FIXED_ZONE_PROMO.BO.REAL_MONEY_CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(calculated_cost)))

    def test_fetch_product_list_should_succeed_when_promo_have_pct_pro_blank_and_fixed_zone_disc_in_bo(self, config):
        config.log.info('Calculating discounted price for {}'.format(
            config.data.TEST_PCT_PRO_BLANK_AND_FIXED_ZONE_PROMO.CODE
        ))

        calculated_cost = int(round(config.store.ces_cost * (
                config.data.TEST_PCT_PRO_BLANK_AND_FIXED_ZONE_PROMO.US.REAL_MONEY.AMOUNT / config.data.TEST_PCT_PRO_BLANK_AND_FIXED_ZONE_PROMO.ORIGINAL_BASE_PRICE),
                                    0))

        config.log.info('Calculated cost is {} {}'.format(
            calculated_cost,
            config.data.TEST_PCT_PRO_BLANK_AND_FIXED_ZONE_PROMO.BO.REAL_MONEY_CODE
        ))

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_PCT_PRO_BLANK_AND_FIXED_ZONE_PROMO.STOREFRONT,
            config.store.wgid,
            config.data.TEST_PCT_PRO_BLANK_AND_FIXED_ZONE_PROMO.BO.COUNTRY,
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
        assert_that(cost['code'], equal_to(config.data.TEST_PCT_PRO_BLANK_AND_FIXED_ZONE_PROMO.BO.REAL_MONEY_CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(calculated_cost)))

    def test_fetch_products_should_succeed_when_promo_have_pct_pro_blank_and_abs_zone_disc_in_bo(self, config):
        config.log.info('Calculating discounted price for {}'.format(
            config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_PROMO.CODE
        ))

        calculated_cost = int(round(config.store.ces_cost * (
                config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_PROMO.US.REAL_MONEY.AMOUNT / config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_PROMO.ORIGINAL_BASE_PRICE),
                                    0))

        config.log.info('Calculated cost is {} {}'.format(
            calculated_cost,
            config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_PROMO.BO.REAL_MONEY_CODE
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_PROMO.CODE],
            config.store.wgid,
            config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_PROMO.BO.COUNTRY,
            config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_PROMO.LANGUAGE,
            storefront=config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_PROMO.STOREFRONT
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        url = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(url).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_PROMO.BO.REAL_MONEY_CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(calculated_cost)))

    def test_fetch_product_list_should_succeed_when_promo_have_pct_pro_blank_and_abs_zone_disc_in_bo(self, config):
        config.log.info('Calculating discounted price for {}'.format(
            config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_PROMO.CODE
        ))

        calculated_cost = int(round(config.store.ces_cost * (
                config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_PROMO.US.REAL_MONEY.AMOUNT / config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_PROMO.ORIGINAL_BASE_PRICE),
                                    0))

        config.log.info('Calculated cost is {} {}'.format(
            calculated_cost,
            config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_PROMO.BO.REAL_MONEY_CODE
        ))

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_PROMO.STOREFRONT,
            config.store.wgid,
            config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_PROMO.BO.COUNTRY,
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
        assert_that(cost['code'], equal_to(config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_PROMO.BO.REAL_MONEY_CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(calculated_cost)))

    def test_fetch_products_should_succeed_when_promo_have_pct_pro_blank_and_abs_country_disc_in_bo(self, config):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PCT_PRO_BLANK_AND_ABS_COUNTRY_PROMO.CODE],
            config.store.wgid,
            config.data.TEST_PCT_PRO_BLANK_AND_ABS_COUNTRY_PROMO.BO.COUNTRY,
            config.data.TEST_PCT_PRO_BLANK_AND_ABS_COUNTRY_PROMO.LANGUAGE,
            storefront=config.data.TEST_PCT_PRO_BLANK_AND_ABS_COUNTRY_PROMO.STOREFRONT
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        url = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(url).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_PCT_PRO_BLANK_AND_ABS_COUNTRY_PROMO.BO.REAL_MONEY.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to(str(config.data.TEST_PCT_PRO_BLANK_AND_ABS_COUNTRY_PROMO.BO.REAL_MONEY.AMOUNT))
        )

    def test_fetch_product_list_should_succeed_when_promo_have_pct_pro_blank_and_abs_country_disc_in_bo(self, config):
        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_PCT_PRO_BLANK_AND_ABS_COUNTRY_PROMO.STOREFRONT,
            config.store.wgid,
            config.data.TEST_PCT_PRO_BLANK_AND_ABS_COUNTRY_PROMO.BO.COUNTRY,
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
        assert_that(cost['code'], equal_to(config.data.TEST_PCT_PRO_BLANK_AND_ABS_COUNTRY_PROMO.BO.REAL_MONEY.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to(str(config.data.TEST_PCT_PRO_BLANK_AND_ABS_COUNTRY_PROMO.BO.REAL_MONEY.AMOUNT))
        )

    def test_fetch_products_should_succeed_when_promo_have_pct_pro_zone_and_abs_country_disc_in_bo(self, config):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PCT_PRO_ZONE_AND_ABS_COUNTRY_PROMO.CODE],
            config.store.wgid,
            config.data.TEST_PCT_PRO_ZONE_AND_ABS_COUNTRY_PROMO.BO.COUNTRY,
            config.data.TEST_PCT_PRO_ZONE_AND_ABS_COUNTRY_PROMO.LANGUAGE,
            storefront=config.data.TEST_PCT_PRO_ZONE_AND_ABS_COUNTRY_PROMO.STOREFRONT
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        url = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(url).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_PCT_PRO_ZONE_AND_ABS_COUNTRY_PROMO.BO.REAL_MONEY.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to(str(config.data.TEST_PCT_PRO_ZONE_AND_ABS_COUNTRY_PROMO.BO.REAL_MONEY.AMOUNT))
        )

    def test_fetch_product_list_should_succeed_when_promo_have_pct_pro_zone_and_abs_country_disc_in_bo(self, config):
        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_PCT_PRO_ZONE_AND_ABS_COUNTRY_PROMO.STOREFRONT,
            config.store.wgid,
            config.data.TEST_PCT_PRO_ZONE_AND_ABS_COUNTRY_PROMO.BO.COUNTRY,
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
        assert_that(cost['code'], equal_to(config.data.TEST_PCT_PRO_ZONE_AND_ABS_COUNTRY_PROMO.BO.REAL_MONEY.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to(str(config.data.TEST_PCT_PRO_ZONE_AND_ABS_COUNTRY_PROMO.BO.REAL_MONEY.AMOUNT))
        )

    def test_fetch_products_should_succeed_when_promo_have_fixed_zone_and_abs_country_disc_in_bo(self, config):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_FIXED_ZONE_AND_ABS_COUNTRY_PROMO.CODE],
            config.store.wgid,
            config.data.TEST_FIXED_ZONE_AND_ABS_COUNTRY_PROMO.BO.COUNTRY,
            config.data.TEST_FIXED_ZONE_AND_ABS_COUNTRY_PROMO.LANGUAGE,
            storefront=config.data.TEST_FIXED_ZONE_AND_ABS_COUNTRY_PROMO.STOREFRONT
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        url = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(url).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_FIXED_ZONE_AND_ABS_COUNTRY_PROMO.BO.REAL_MONEY.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to(str(config.data.TEST_FIXED_ZONE_AND_ABS_COUNTRY_PROMO.BO.REAL_MONEY.AMOUNT))
        )

    def test_fetch_product_list_should_succeed_when_promo_have_fixed_zone_and_abs_country_disc_in_bo(self, config):
        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_FIXED_ZONE_AND_ABS_COUNTRY_PROMO.STOREFRONT,
            config.store.wgid,
            config.data.TEST_FIXED_ZONE_AND_ABS_COUNTRY_PROMO.BO.COUNTRY,
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
        assert_that(cost['code'], equal_to(config.data.TEST_FIXED_ZONE_AND_ABS_COUNTRY_PROMO.BO.REAL_MONEY.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to(str(config.data.TEST_FIXED_ZONE_AND_ABS_COUNTRY_PROMO.BO.REAL_MONEY.AMOUNT))
        )

    def test_fetch_products_should_succeed_when_promo_have_abs_zone_and_abs_country_disc_in_bo(self, config):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_ABS_ZONE_AND_ABS_COUNTRY_PROMO.CODE],
            config.store.wgid,
            config.data.TEST_ABS_ZONE_AND_ABS_COUNTRY_PROMO.BO.COUNTRY,
            config.data.TEST_ABS_ZONE_AND_ABS_COUNTRY_PROMO.LANGUAGE,
            storefront=config.data.TEST_ABS_ZONE_AND_ABS_COUNTRY_PROMO.STOREFRONT
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        url = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(url).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_ABS_ZONE_AND_ABS_COUNTRY_PROMO.BO.REAL_MONEY.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to(str(config.data.TEST_ABS_ZONE_AND_ABS_COUNTRY_PROMO.BO.REAL_MONEY.AMOUNT))
        )

    def test_fetch_product_list_should_succeed_when_promo_have_abs_zone_and_abs_country_disc_in_bo(self, config):
        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_ABS_ZONE_AND_ABS_COUNTRY_PROMO.STOREFRONT,
            config.store.wgid,
            config.data.TEST_ABS_ZONE_AND_ABS_COUNTRY_PROMO.BO.COUNTRY,
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
        assert_that(cost['code'], equal_to(config.data.TEST_ABS_ZONE_AND_ABS_COUNTRY_PROMO.BO.REAL_MONEY.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to(str(config.data.TEST_ABS_ZONE_AND_ABS_COUNTRY_PROMO.BO.REAL_MONEY.AMOUNT))
        )

    def test_fetch_products_should_succeed_when_promo_have_pct_pro_blank_and_abs_zone_and_country_disc_in_bo(self,
                                                                                                             config):
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_COUNTRY_PROMO.CODE],
            config.store.wgid,
            config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_COUNTRY_PROMO.BO.COUNTRY,
            config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_COUNTRY_PROMO.LANGUAGE,
            storefront=config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_COUNTRY_PROMO.STOREFRONT
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        url = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(url).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        assert_that(cost, has_key('code'))
        assert_that(
            cost['code'],
            equal_to(config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_COUNTRY_PROMO.BO.REAL_MONEY.CODE)
        )

        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to(str(config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_COUNTRY_PROMO.BO.REAL_MONEY.AMOUNT))
        )

    def test_fetch_product_list_should_succeed_when_promo_have_pct_pro_blank_and_abs_zone_and_country_disc_in_bo(self,
                                                                                                                 config):
        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_COUNTRY_PROMO.STOREFRONT,
            config.store.wgid,
            config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_COUNTRY_PROMO.BO.COUNTRY,
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
            equal_to(config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_COUNTRY_PROMO.BO.REAL_MONEY.CODE)
        )

        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to(str(config.data.TEST_PCT_PRO_BLANK_AND_ABS_ZONE_COUNTRY_PROMO.BO.REAL_MONEY.AMOUNT))
        )
