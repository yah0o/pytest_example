import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities
from integration.main.request import RequestBuilder

"""

    See https://confluence.wargaming.net/pages/viewpage.action?pageId=512172851 for rules on how discounts are
    supposed to be applied

"""


@pytest.allure.feature('functional')
@pytest.allure.story('product override discount application')
class TestOverrideDiscountApplication(object):

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
    def test_virtual_currency_pct_pro_discount(self, config):
        """
        Calls /fetchProducts using a product and storefront;
        Associated promo has one PCT_PRO discount that applies to all VCs
        """
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_DISCOUNT_PCT_PRO_VC.PRODUCT],
            config.store.wgid,
            config.data.TEST_DISCOUNT_PCT_PRO_VC.COUNTRY,
            config.data.TEST_DISCOUNT_PCT_PRO_VC.LANGUAGE,
            config.data.TEST_DISCOUNT_PCT_PRO_VC.STOREFRONT
        )
        fetch_response.assert_is_success()

        product_urls = fetch_response.content['body']['uriList']
        assert_that(product_urls, has_length(1))
        uri = product_urls[0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        applied_promotions_list = product_response.content['applied_promotions']
        assert_that(applied_promotions_list, has_length(1))
        promo_summary = applied_promotions_list[0]
        assert_that(promo_summary['code'], equal_to(config.data.TEST_DISCOUNT_PCT_PRO_VC.PROMOTION))
        assert_that(promo_summary['discount_types'], has_length(2))
        assert_that(promo_summary['discount_types'].count('PCT_PRO'), equal_to(2))

        virtual_price_list = product_response.content['price']['virtual_price']

        assert_that(virtual_price_list, not_none())
        assert_that(len(virtual_price_list), 2)
        vc_dict = dict((currency['code'], currency) for currency in virtual_price_list)

        assert_that(vc_dict['test_currency'], not_none())
        assert_that(float(vc_dict['test_currency']['amount']),
                    equal_to(float(config.data.TEST_DISCOUNT_PCT_PRO_VC.EXPECTED_TEST_CURRENCY_AMOUNT)))

        assert_that(vc_dict['xp'], not_none())
        assert_that(float(vc_dict['xp']['amount']),
                    equal_to(float(config.data.TEST_DISCOUNT_PCT_PRO_VC.EXPECTED_XP_AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_real_price_abs_discount_using_country_price_overrides_with_discount(self, config):
        """
        Calls /fetchProducts using a product and storefront;
        Product has country-specific price real_money_overrides for RU and FR, among others
        Associated active promo has a ABS discount apply to RU only

        Requests are made using RU and FR, with base prices pulled from real_money_overrides;
            when RU is used, discount is applied;
            when FR is used, no discount is applied;
        """
        # request made using RU
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_DISCOUNT_ABS_REAL.PRODUCT],
            config.store.wgid,
            config.data.TEST_DISCOUNT_ABS_REAL.DISCOUNT_COUNTRY_1,
            config.data.TEST_DISCOUNT_ABS_REAL.LANGUAGE,
            config.data.TEST_DISCOUNT_ABS_REAL.STOREFRONT
        )
        fetch_response.assert_is_success()

        product_urls = fetch_response.content['body']['uriList']
        assert_that(product_urls, has_length(1))
        uri = product_urls[0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        applied_promotions_list = product_response.content['applied_promotions']
        assert_that(applied_promotions_list, has_length(1))
        promo_summary = applied_promotions_list[0]
        assert_that(promo_summary['discount_types'], has_length(1))
        assert_that(promo_summary['discount_types'].count('ABS'), equal_to(1))

        real_price = product_response.content['price']['real_price']
        assert_that(real_price['code'],
                    config.data.TEST_DISCOUNT_ABS_REAL.DISCOUNT_COUNTRY_CURRENCY_CODE_1)
        assert_that(float(real_price['amount']),
                    equal_to(float(config.data.TEST_DISCOUNT_ABS_REAL.DISCOUNT_COUNTRY_CURRENCY_AMOUNT_1)))

        # request made using FR
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_DISCOUNT_ABS_REAL.PRODUCT],
            config.store.wgid,
            config.data.TEST_DISCOUNT_ABS_REAL.DISCOUNT_COUNTRY_2,
            config.data.TEST_DISCOUNT_ABS_REAL.LANGUAGE,
            config.data.TEST_DISCOUNT_ABS_REAL.STOREFRONT
        )
        fetch_response.assert_is_success()

        product_urls = fetch_response.content['body']['uriList']
        assert_that(product_urls, has_length(1))
        uri = product_urls[0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        applied_promotions_list = product_response.content['applied_promotions']
        assert_that(applied_promotions_list, has_length(1))
        promo_summary = applied_promotions_list[0]
        assert_that(promo_summary['discount_types'], has_length(0))

        real_price = product_response.content['price']['real_price']
        assert_that(real_price['code'], config.data.TEST_DISCOUNT_ABS_REAL.DISCOUNT_COUNTRY_CURRENCY_CODE_2)
        assert_that(float(real_price['amount']),
                    equal_to(float(config.data.TEST_DISCOUNT_ABS_REAL.DISCOUNT_COUNTRY_CURRENCY_AMOUNT_2)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_real_price_abs_discount_using_country_price_override_without_discounts(self, config):
        """
        Calls /fetchProducts using a product and storefront;
        Product has certain country-specific prices in real_money_overrides, including for IN
        Associated active promo has a number of ABS discounts, none of which reference IN

        A request is made using IN, and the associated original price from real_money_overrides is displayed,
            with no discounts applied.
        """
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_DISCOUNT_ABS_REAL.PRODUCT],
            config.store.wgid,
            config.data.TEST_DISCOUNT_ABS_REAL.OVERRIDE_COUNTRY_WITHOUT_DISCOUNTS,
            config.data.TEST_DISCOUNT_ABS_REAL.LANGUAGE,
            config.data.TEST_DISCOUNT_ABS_REAL.STOREFRONT
        )
        fetch_response.assert_is_success()

        product_urls = fetch_response.content['body']['uriList']
        assert_that(product_urls, has_length(1))
        uri = product_urls[0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        applied_promotions_list = product_response.content['applied_promotions']
        assert_that(applied_promotions_list, has_length(1))
        promo_summary = applied_promotions_list[0]
        assert_that(promo_summary['code'], equal_to(config.data.TEST_DISCOUNT_ABS_REAL.PROMOTION))
        assert_that(promo_summary['discount_types'], has_length(0))

        real_price = product_response.content['price']['real_price']
        assert_that(real_price['code'],
                    config.data.TEST_DISCOUNT_ABS_REAL.OVERRIDE_COUNTRY_WITHOUT_DISCOUNTS_CURRENCY_CODE)
        assert_that(float(real_price['amount']),
                    equal_to(float(
                        config.data.TEST_DISCOUNT_ABS_REAL.OVERRIDE_COUNTRY_WITHOUT_DISCOUNTS_ORIGINAL_CURRENCY_AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_real_price_abs_discount_using_default_zone_price(self, config):
        """
        Calls /fetchProducts using a product and storefront;
        Product has certain country-specific prices in real_money_overrides;
        Product has a price associated with the "default" zone in base_real_money_prices;
        Associated active promo has a number of country-specific ABS discounts;

        Request is made using country NOT in real_money_overrides;
            the base price is pulled from "default" zone price;
            because the ABS discounts are country-specific, the "default" price is unchanged.
        """
        # request made using a generic country that no country-specific price overrides apply to
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_DISCOUNT_ABS_REAL.PRODUCT],
            config.store.wgid,
            config.data.TEST_DISCOUNT_ABS_REAL.UNREFERENCED_COUNTRY,
            config.data.TEST_DISCOUNT_ABS_REAL.LANGUAGE,
            config.data.TEST_DISCOUNT_ABS_REAL.STOREFRONT
        )
        fetch_response.assert_is_success()

        product_urls = fetch_response.content['body']['uriList']
        assert_that(product_urls, has_length(1))
        uri = product_urls[0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        applied_promotions_list = product_response.content['applied_promotions']
        assert_that(applied_promotions_list, has_length(1))
        promo_summary = applied_promotions_list[0]
        assert_that(promo_summary['code'], equal_to(config.data.TEST_DISCOUNT_ABS_REAL.PROMOTION))
        assert_that(promo_summary['discount_types'], has_length(0))

        real_price = product_response.content['price']['real_price']
        assert_that(real_price['code'],
                    config.data.TEST_DISCOUNT_ABS_REAL.DEFAULT_ZONE_CURRENCY_CODE)
        assert_that(float(real_price['amount']),
                    equal_to(float(config.data.TEST_DISCOUNT_ABS_REAL.DEFAULT_ZONE_ORIGINAL_CURRENCY_AMOUNT)))

    @pytest.mark.skip_for_regions('wgt1')
    @pytest.allure.severity(severity_level.CRITICAL)
    def test_vc_price_pct_pro_discount_with_rm_zone_does_not_affect_vc_price(self, config):
        """
        Calls /fetchProducts using a product and storefront;
        Product has a vc price;
        Associated active promo has one PCT_PRO discount that specifies a zone;

        Request is made using any country.
        Because the discount specifies an rm_zone, it will not be applied to shown vc price,
            and the discount will not be displayed in the discount_types list
        """
        # request made using a country that has a product-level price override:
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_DISCOUNT_PCT_PRO_WITH_ZONE_VC_UNCHANGED.PRODUCT],
            config.store.wgid,
            config.data.TEST_DISCOUNT_PCT_PRO_WITH_ZONE_VC_UNCHANGED.COUNTRY,  # does not matter
            config.data.TEST_DISCOUNT_PCT_PRO_WITH_ZONE_VC_UNCHANGED.LANGUAGE,
            config.data.TEST_DISCOUNT_PCT_PRO_WITH_ZONE_VC_UNCHANGED.STOREFRONT
        )
        fetch_response.assert_is_success()

        product_urls = fetch_response.content['body']['uriList']
        assert_that(product_urls, has_length(1))
        uri = product_urls[0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        applied_promotions_list = product_response.content['applied_promotions']
        assert_that(applied_promotions_list, has_length(1))
        promo_summary = applied_promotions_list[0]
        assert_that(promo_summary['code'], equal_to(config.data.TEST_DISCOUNT_PCT_PRO_WITH_ZONE_VC_UNCHANGED.PROMOTION))
        # assert_that(promo_summary['discount_types'], has_length(0))   # TODO: does this get displayed correctly?

        virtual_price_list = product_response.content['price']['virtual_price']

        assert_that(virtual_price_list, not_none())
        assert_that(len(virtual_price_list), 2)
        vc_dict = dict((currency['code'], currency) for currency in virtual_price_list)

        assert_that(vc_dict['test_currency'], not_none())
        assert_that(float(vc_dict['test_currency']['amount']),
                    equal_to(
                        float(config.data.TEST_DISCOUNT_PCT_PRO_WITH_ZONE_VC_UNCHANGED.EXPECTED_TEST_CURRENCY_AMOUNT)))

        assert_that(vc_dict['xp'], not_none())
        assert_that(float(vc_dict['xp']['amount']),
                    equal_to(float(config.data.TEST_DISCOUNT_PCT_PRO_WITH_ZONE_VC_UNCHANGED.EXPECTED_XP_AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_pct_pro_discount_with_rm_zone_should_be_applied_if_product_price_does_not_override_requested_country(
            self,
            config
    ):
        """
        Calls /fetchProducts using a product and storefront;
        Product has a vc price;
        Product has certain country-specific prices in real_money_overrides;
        Product has a price associated with the "default" zone in base_real_money_prices;
        Associated active promo has one PCT_PRO discount that specifies a zone;

        If request is made using any country NOT in real_money_overrides:
            the "default"-zone price will be displayed, with the discount applied,
            and discount WILL BE displayed in the discount_types list
        """
        # request made using a country that does not have a product-level price override:
        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_DISCOUNT_PCT_PRO_WITH_ZONE_UNREFERENCED_COUNTRY.PRODUCT],
            config.store.wgid,
            config.data.TEST_DISCOUNT_PCT_PRO_WITH_ZONE_UNREFERENCED_COUNTRY.COUNTRY_WITHOUT_PRICE_OVERRIDE,
            config.data.TEST_DISCOUNT_PCT_PRO_WITH_ZONE_UNREFERENCED_COUNTRY.LANGUAGE,
            config.data.TEST_DISCOUNT_PCT_PRO_WITH_ZONE_UNREFERENCED_COUNTRY.STOREFRONT
        )
        fetch_response.assert_is_success()

        product_urls = fetch_response.content['body']['uriList']
        assert_that(product_urls, has_length(1))
        uri = product_urls[0]

        product_response = RequestBuilder(uri).get()
        product_response.assert_is_success()

        applied_promotions_list = product_response.content['applied_promotions']
        assert_that(applied_promotions_list, has_length(1))
        promo_summary = applied_promotions_list[0]
        assert_that(promo_summary['code'],
                    equal_to(config.data.TEST_DISCOUNT_PCT_PRO_WITH_ZONE_UNREFERENCED_COUNTRY.PROMOTION))

        real_price = product_response.content['price']['real_price']
        assert_that(real_price['code'],
                    config.data.TEST_DISCOUNT_PCT_PRO_WITH_ZONE_UNREFERENCED_COUNTRY.DEFAULT_ZONE_CURRENCY_CODE)
        assert_that(float(real_price['amount']),
                    equal_to(float(
                        config.data.TEST_DISCOUNT_PCT_PRO_WITH_ZONE_UNREFERENCED_COUNTRY.EXPECTED_RM_CURRENCY_AMOUNT)))
