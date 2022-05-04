import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities, RequestBuilder


@pytest.allure.feature('functional')
@pytest.allure.story('discounted rounding price')
class TestPromotionLATAMRounding(object):

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
        config.store.account_wgid = account_created.content['id']

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(config.store.account_wgid)
        delete_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_argentina_round_down_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.ARGENTINA.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.ARGENTINA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.ARGENTINA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_bolivia_round_down_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.BOLIVIA.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.BOLIVIA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.BOLIVIA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_chile_round_down_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.CHILE.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.CHILE.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.CHILE.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_colombia_round_down_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COLOMBIA.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COLOMBIA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.COLOMBIA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_costa_rica_round_down_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COSTA_RICA.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COSTA_RICA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.COSTA_RICA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_mexico_round_down_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.MEXICO.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.MEXICO.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.MEXICO.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_nicaragua_round_down_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.NICARAGUA.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.NICARAGUA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.NICARAGUA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_uruguay_round_down_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.URUGUAY.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.URUGUAY.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.URUGUAY.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_argentina_round_up_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.ARGENTINA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(
            prod_response.content['product_code'],
            equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT)
        )

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.ARGENTINA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.ARGENTINA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_bolivia_round_up_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.BOLIVIA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.BOLIVIA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.BOLIVIA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_chile_round_up_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.CHILE.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.CHILE.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.CHILE.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_colombia_round_up_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COLOMBIA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COLOMBIA_COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COLOMBIA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COLOMBIA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COLOMBIA_COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_costa_rica_round_up_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COSTA_RICA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COSTA_RICA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COSTA_RICA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_mexico_round_up_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.MEXICO.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.MEXICO.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.MEXICO.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_nicaragua_round_up_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.NICARAGUA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.NICARAGUA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.NICARAGUA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_uruguay_round_up_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.URUGUAY.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.URUGUAY.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.URUGUAY.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_argentina_round_up_price_has_abs_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.ARGENTINA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.ARGENTINA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.ARGENTINA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_bolivia_round_up_price_has_abs_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT],
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.BOLIVIA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE,
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_STORE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], has_length(1))
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.BOLIVIA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.BOLIVIA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_argentina_round_down_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE,
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.ARGENTINA.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.ARGENTINA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.ARGENTINA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_bolivia_round_down_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE,
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.BOLIVIA.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.BOLIVIA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.BOLIVIA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_chile_round_down_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE,
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.CHILE.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.CHILE.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.CHILE.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_colombia_round_down_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE,
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COLOMBIA.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COLOMBIA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.COLOMBIA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_costa_rica_round_down_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE,
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COSTA_RICA.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COSTA_RICA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.COSTA_RICA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_mexico_round_down_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE,
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.MEXICO.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.MEXICO.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.MEXICO.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_nicaragua_round_down_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE,
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.NICARAGUA.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.NICARAGUA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.NICARAGUA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_uruguay_round_down_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE,
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.URUGUAY.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.URUGUAY.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.URUGUAY.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_argentina_round_up_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE,
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.ARGENTINA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.ARGENTINA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.ARGENTINA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_bolivia_round_up_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE,
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.BOLIVIA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.BOLIVIA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.BOLIVIA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_chile_round_up_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE,
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.CHILE.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.CHILE.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.CHILE.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_colombia_round_up_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE,
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COLOMBIA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COLOMBIA_COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COLOMBIA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COLOMBIA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COLOMBIA_COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_costa_rica_round_up_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE,
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COSTA_RICA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COSTA_RICA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COSTA_RICA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_mexico_round_up_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE,
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.MEXICO.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.MEXICO.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.MEXICO.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_nicaragua_round_up_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE,
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.NICARAGUA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.NICARAGUA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.NICARAGUA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_uruguay_round_up_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE,
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.URUGUAY.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.URUGUAY.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.URUGUAY.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_argentina_round_up_price_has_abs_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_STORE,
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.ARGENTINA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.ARGENTINA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.ARGENTINA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_bolivia_round_up_price_has_abs_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_STORE,
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.BOLIVIA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.BOLIVIA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.BOLIVIA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_chile_round_up_price_has_abs_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_STORE,
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.CHILE.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.CHILE.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.CHILE.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_colombia_round_up_price_has_abs_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_STORE,
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COLOMBIA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COLOMBIA_COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COLOMBIA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COLOMBIA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COLOMBIA_COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_costa_rica_round_up_price_has_abs_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_STORE,
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COSTA_RICA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COSTA_RICA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COSTA_RICA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_mexico_round_up_price_has_abs_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_STORE,
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.MEXICO.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.MEXICO.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.MEXICO.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_uruguay_round_up_price_has_abs_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_STORE,
            config.store.account_wgid,
            config.data.TEST_LATAM_ROUND_UP_PROMO.URUGUAY.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri = fetch_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content['product_code'],
                    equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT))

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.URUGUAY.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.URUGUAY.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_argentina_round_down_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.ARGENTINA.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.AMOUNT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        cost = fetch_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.ARGENTINA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.ARGENTINA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_bolivia_round_down_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.BOLIVIA.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.AMOUNT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        cost = fetch_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.BOLIVIA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.BOLIVIA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_chile_round_down_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.CHILE.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.AMOUNT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        cost = fetch_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.CHILE.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.CHILE.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_colombia_round_down_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COLOMBIA.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.AMOUNT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        cost = fetch_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COLOMBIA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.COLOMBIA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_costa_rica_round_down_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COSTA_RICA.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.AMOUNT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        cost = fetch_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COSTA_RICA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.COSTA_RICA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_mexico_round_down_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.MEXICO.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.AMOUNT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        cost = fetch_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.MEXICO.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.MEXICO.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_nicaragua_round_down_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.NICARAGUA.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.AMOUNT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        cost = fetch_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.NICARAGUA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.NICARAGUA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_uruguay_round_down_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.URUGUAY.COUNTRY,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.AMOUNT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        cost = fetch_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_DOWN_PROMO.URUGUAY.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.URUGUAY.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_DOWN_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_argentina_round_up_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.ARGENTINA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        cost = fetch_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.ARGENTINA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.ARGENTINA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_bolivia_round_up_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.BOLIVIA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        cost = fetch_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.BOLIVIA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.BOLIVIA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_chile_round_up_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.CHILE.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        cost = fetch_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.CHILE.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.CHILE.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_colombia_round_up_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COLOMBIA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        cost = fetch_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COLOMBIA_COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COLOMBIA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COLOMBIA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COLOMBIA_COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_costa_rica_round_up_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COSTA_RICA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        cost = fetch_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COSTA_RICA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COSTA_RICA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_mexico_round_up_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.MEXICO.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        cost = fetch_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.MEXICO.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.MEXICO.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_nicaragua_round_up_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.NICARAGUA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        cost = fetch_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.NICARAGUA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.NICARAGUA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_uruguay_round_up_price_has_pct_pro_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.URUGUAY.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_STORE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        cost = fetch_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.PCT_PRO_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.URUGUAY.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.URUGUAY.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_argentina_round_up_price_has_abs_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.ARGENTINA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_STORE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        cost = fetch_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.ARGENTINA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.ARGENTINA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_bolivia_round_up_price_has_abs_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.BOLIVIA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_STORE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        cost = fetch_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.BOLIVIA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.BOLIVIA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_chile_round_up_price_has_abs_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.CHILE.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_STORE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        cost = fetch_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.CHILE.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.CHILE.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_colombia_round_up_price_has_abs_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COLOMBIA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_STORE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        cost = fetch_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COLOMBIA_COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COLOMBIA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COLOMBIA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COLOMBIA_COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_costa_rica_round_up_price_has_abs_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COSTA_RICA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_STORE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        cost = fetch_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COSTA_RICA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COSTA_RICA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_mexico_round_up_price_has_abs_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.MEXICO.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_STORE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        cost = fetch_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.MEXICO.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.MEXICO.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_nicaragua_round_up_price_has_abs_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.NICARAGUA.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_STORE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        cost = fetch_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.NICARAGUA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.NICARAGUA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_uruguay_round_up_price_has_abs_disc(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT
        ))

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.URUGUAY.COUNTRY,
            config.data.TEST_LATAM_ROUND_UP_PROMO.AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_STORE
        )
        fetch_response.assert_is_success()

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        cost = fetch_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATAM_ROUND_UP_PROMO.ABS_DISC_PRODUCT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT,
            config.data.TEST_LATAM_ROUND_UP_PROMO.URUGUAY.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.URUGUAY.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(int(cost['amount']), equal_to(config.data.TEST_LATAM_ROUND_UP_PROMO.COST_AMOUNT))
