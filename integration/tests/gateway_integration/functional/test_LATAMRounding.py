import pytest
from allure import severity_level
from hamcrest import *

from integration.main.helpers import AccountUtilities, RequestBuilder, PurchaseUtil


@pytest.allure.feature('functional')
@pytest.allure.story('rounding price')
class TestLATAMRounding(object):

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
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(config.store.wgid)
        delete_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_rounding_down_argentina_cost(self, config):
        config.log.info('fetching {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE))

        fetch_products_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE],
            config.store.wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.ARGENTINA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.LANGUAGE
        )
        fetch_products_response.assert_is_success()

        assert_that(fetch_products_response.content['body'], has_key('uriList'))
        assert_that(fetch_products_response.content['body']['uriList'], has_length(1))
        uri = fetch_products_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.ARGENTINA.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.ARGENTINA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.ARGENTINA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.ARGENTINA.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_rounding_up_argentina_cost(self, config):
        config.log.info('fetching {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE))

        fetch_products_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE],
            config.store.wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.ARGENTINA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.LANGUAGE
        )
        fetch_products_response.assert_is_success()

        assert_that(fetch_products_response.content['body'], has_key('uriList'))
        assert_that(fetch_products_response.content['body']['uriList'], has_length(1))
        uri = fetch_products_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.ARGENTINA.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.ARGENTINA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_UP.ARGENTINA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_UP.ARGENTINA.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_rounding_down_bolivia_cost(self, config):
        config.log.info('fetching {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE))

        fetch_products_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE],
            config.store.wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.BOLIVIA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.LANGUAGE
        )
        fetch_products_response.assert_is_success()

        assert_that(fetch_products_response.content['body'], has_key('uriList'))
        assert_that(fetch_products_response.content['body']['uriList'], has_length(1))
        uri = fetch_products_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.BOLIVIA.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.BOLIVIA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.BOLIVIA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.BOLIVIA.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_rounding_up_bolivia_cost(self, config):
        config.log.info('fetching {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE))

        fetch_products_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE],
            config.store.wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.BOLIVIA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.LANGUAGE
        )
        fetch_products_response.assert_is_success()

        assert_that(fetch_products_response.content['body'], has_key('uriList'))
        assert_that(fetch_products_response.content['body']['uriList'], has_length(1))
        uri = fetch_products_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.BOLIVIA.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.BOLIVIA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_UP.BOLIVIA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_UP.BOLIVIA.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_rounding_down_chile_cost(self, config):
        config.log.info('fetching {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE))

        fetch_products_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE],
            config.store.wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CHILE.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.LANGUAGE
        )
        fetch_products_response.assert_is_success()

        assert_that(fetch_products_response.content['body'], has_key('uriList'))
        assert_that(fetch_products_response.content['body']['uriList'], has_length(1))
        uri = fetch_products_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CHILE.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CHILE.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CHILE.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CHILE.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_rounding_up_chile_cost(self, config):
        config.log.info('fetching {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE))

        fetch_products_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE],
            config.store.wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CHILE.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.LANGUAGE
        )
        fetch_products_response.assert_is_success()

        assert_that(fetch_products_response.content['body'], has_key('uriList'))
        assert_that(fetch_products_response.content['body']['uriList'], has_length(1))
        uri = fetch_products_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CHILE.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CHILE.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CHILE.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CHILE.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_rounding_down_colombia_cost(self, config):
        config.log.info('fetching {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE))

        fetch_products_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE],
            config.store.wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COLOMBIA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.LANGUAGE
        )
        fetch_products_response.assert_is_success()

        assert_that(fetch_products_response.content['body'], has_key('uriList'))
        assert_that(fetch_products_response.content['body']['uriList'], has_length(1))
        uri = fetch_products_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COLOMBIA.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COLOMBIA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COLOMBIA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COLOMBIA.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_rounding_up_colombia_cost(self, config):
        config.log.info('fetching {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE))

        fetch_products_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE],
            config.store.wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.COLOMBIA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.LANGUAGE
        )
        fetch_products_response.assert_is_success()

        assert_that(fetch_products_response.content['body'], has_key('uriList'))
        assert_that(fetch_products_response.content['body']['uriList'], has_length(1))
        uri = fetch_products_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.COLOMBIA.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.COLOMBIA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_UP.COLOMBIA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_UP.COLOMBIA.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_rounding_down_costa_rica_cost(self, config):
        config.log.info('fetching {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE))

        fetch_products_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE],
            config.store.wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COSTA_RICA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.LANGUAGE
        )
        fetch_products_response.assert_is_success()

        assert_that(fetch_products_response.content['body'], has_key('uriList'))
        assert_that(fetch_products_response.content['body']['uriList'], has_length(1))
        uri = fetch_products_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COSTA_RICA.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COSTA_RICA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COSTA_RICA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COSTA_RICA.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_rounding_up_costa_rica_cost(self, config):
        config.log.info('fetching {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE))

        fetch_products_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE],
            config.store.wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.COSTA_RICA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.LANGUAGE
        )
        fetch_products_response.assert_is_success()

        assert_that(fetch_products_response.content['body'], has_key('uriList'))
        assert_that(fetch_products_response.content['body']['uriList'], has_length(1))
        uri = fetch_products_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.COSTA_RICA.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.COSTA_RICA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_UP.COSTA_RICA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_UP.COSTA_RICA.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_rounding_down_mexico_cost(self, config):
        config.log.info('fetching {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE))

        fetch_products_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE],
            config.store.wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.MEXICO.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.LANGUAGE
        )
        fetch_products_response.assert_is_success()

        assert_that(fetch_products_response.content['body'], has_key('uriList'))
        assert_that(fetch_products_response.content['body']['uriList'], has_length(1))
        uri = fetch_products_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.MEXICO.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.MEXICO.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.MEXICO.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.MEXICO.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_rounding_up_mexico_cost(self, config):
        config.log.info('fetching {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE))

        fetch_products_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE],
            config.store.wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.MEXICO.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.LANGUAGE
        )
        fetch_products_response.assert_is_success()

        assert_that(fetch_products_response.content['body'], has_key('uriList'))
        assert_that(fetch_products_response.content['body']['uriList'], has_length(1))
        uri = fetch_products_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.MEXICO.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.MEXICO.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_UP.MEXICO.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_UP.MEXICO.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_rounding_down_nicaragua_cost(self, config):
        config.log.info('fetching {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE))

        fetch_products_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE],
            config.store.wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.NICARAGUA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.LANGUAGE
        )
        fetch_products_response.assert_is_success()

        assert_that(fetch_products_response.content['body'], has_key('uriList'))
        assert_that(fetch_products_response.content['body']['uriList'], has_length(1))
        uri = fetch_products_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.NICARAGUA.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.NICARAGUA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.NICARAGUA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.NICARAGUA.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_rounding_up_nicaragua_cost(self, config):
        config.log.info('fetching {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE))

        fetch_products_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE],
            config.store.wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.NICARAGUA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.LANGUAGE
        )
        fetch_products_response.assert_is_success()

        assert_that(fetch_products_response.content['body'], has_key('uriList'))
        assert_that(fetch_products_response.content['body']['uriList'], has_length(1))
        uri = fetch_products_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.NICARAGUA.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.NICARAGUA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_UP.NICARAGUA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_UP.NICARAGUA.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_rounding_down_uruguay_cost(self, config):
        config.log.info('fetching {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE))

        fetch_products_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE],
            config.store.wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.URUGUAY.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.LANGUAGE
        )
        fetch_products_response.assert_is_success()

        assert_that(fetch_products_response.content['body'], has_key('uriList'))
        assert_that(fetch_products_response.content['body']['uriList'], has_length(1))
        uri = fetch_products_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.URUGUAY.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.URUGUAY.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.URUGUAY.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.URUGUAY.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_rounding_up_uruguay_cost(self, config):
        config.log.info('fetching {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE))

        fetch_products_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE],
            config.store.wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.URUGUAY.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.LANGUAGE
        )
        fetch_products_response.assert_is_success()

        assert_that(fetch_products_response.content['body'], has_key('uriList'))
        assert_that(fetch_products_response.content['body']['uriList'], has_length(1))
        uri = fetch_products_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        cost = prod_response.content['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.URUGUAY.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.URUGUAY.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_UP.URUGUAY.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_UP.URUGUAY.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_rounding_down_argentina_cost(self, config):
        config.log.info('Fetching {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE))

        fetch_product_list_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.STOREFRONT,
            config.store.wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.ARGENTINA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.LANGUAGE
        )
        fetch_product_list_response.assert_is_success()

        assert_that(fetch_product_list_response.content['body'], has_key('uriList'))
        assert_that(fetch_product_list_response.content['body']['uriList'], not_none())
        uri_list = fetch_product_list_response.content['body']['uriList']

        prod = next((
                prod_content for prod_content in PurchaseUtil.get_product_infos(uri_list)
                if prod_content['product_code'] == config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('price'))
        assert_that(prod['price'], has_key('real_price'))
        cost = prod['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.ARGENTINA.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.ARGENTINA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.ARGENTINA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.ARGENTINA.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_rounding_up_argentina_cost(self, config):
        config.log.info('Fetching {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE))

        fetch_product_list_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.STOREFRONT,
            config.store.wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.ARGENTINA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.LANGUAGE
        )
        fetch_product_list_response.assert_is_success()

        assert_that(fetch_product_list_response.content['body'], has_key('uriList'))
        assert_that(fetch_product_list_response.content['body']['uriList'], not_none())
        uri_list = fetch_product_list_response.content['body']['uriList']

        prod = next((
                prod_content for prod_content in PurchaseUtil.get_product_infos(uri_list)
                if prod_content['product_code'] == config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('price'))
        assert_that(prod['price'], has_key('real_price'))
        cost = prod['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.ARGENTINA.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.ARGENTINA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_UP.ARGENTINA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_UP.ARGENTINA.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_rounding_down_bolivia_cost(self, config):
        config.log.info('Fetching {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE))

        fetch_product_list_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.STOREFRONT,
            config.store.wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.BOLIVIA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.LANGUAGE
        )
        fetch_product_list_response.assert_is_success()

        assert_that(fetch_product_list_response.content['body'], has_key('uriList'))
        assert_that(fetch_product_list_response.content['body']['uriList'], not_none())
        uri_list = fetch_product_list_response.content['body']['uriList']

        prod = next((
                prod_content for prod_content in PurchaseUtil.get_product_infos(uri_list)
                if prod_content['product_code'] == config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('price'))
        assert_that(prod['price'], has_key('real_price'))
        cost = prod['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.BOLIVIA.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.BOLIVIA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.BOLIVIA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.BOLIVIA.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_rounding_up_bolivia_cost(self, config):
        config.log.info('Fetching {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE))

        fetch_product_list_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.STOREFRONT,
            config.store.wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.BOLIVIA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.LANGUAGE
        )
        fetch_product_list_response.assert_is_success()

        assert_that(fetch_product_list_response.content['body'], has_key('uriList'))
        assert_that(fetch_product_list_response.content['body']['uriList'], not_none())
        uri_list = fetch_product_list_response.content['body']['uriList']

        prod = next((
                prod_content for prod_content in PurchaseUtil.get_product_infos(uri_list)
                if prod_content['product_code'] == config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('price'))
        assert_that(prod['price'], has_key('real_price'))
        cost = prod['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.BOLIVIA.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.BOLIVIA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_UP.BOLIVIA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_UP.BOLIVIA.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_rounding_down_chile_cost(self, config):
        config.log.info('Fetching {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE))

        fetch_product_list_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.STOREFRONT,
            config.store.wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CHILE.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.LANGUAGE
        )
        fetch_product_list_response.assert_is_success()

        assert_that(fetch_product_list_response.content['body'], has_key('uriList'))
        assert_that(fetch_product_list_response.content['body']['uriList'], not_none())
        uri_list = fetch_product_list_response.content['body']['uriList']

        prod = next((
                prod_content for prod_content in PurchaseUtil.get_product_infos(uri_list)
                if prod_content['product_code'] == config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('price'))
        assert_that(prod['price'], has_key('real_price'))
        cost = prod['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CHILE.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CHILE.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CHILE.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CHILE.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_rounding_up_chile_cost(self, config):
        config.log.info('Fetching {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE))

        fetch_product_list_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.STOREFRONT,
            config.store.wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CHILE.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.LANGUAGE
        )
        fetch_product_list_response.assert_is_success()

        assert_that(fetch_product_list_response.content['body'], has_key('uriList'))
        assert_that(fetch_product_list_response.content['body']['uriList'], not_none())
        uri_list = fetch_product_list_response.content['body']['uriList']

        prod = next((
                prod_content for prod_content in PurchaseUtil.get_product_infos(uri_list)
                if prod_content['product_code'] == config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('price'))
        assert_that(prod['price'], has_key('real_price'))
        cost = prod['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CHILE.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CHILE.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CHILE.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CHILE.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_rounding_down_colombia_cost(self, config):
        config.log.info('Fetching {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE))

        fetch_product_list_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.STOREFRONT,
            config.store.wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COLOMBIA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.LANGUAGE
        )
        fetch_product_list_response.assert_is_success()

        assert_that(fetch_product_list_response.content['body'], has_key('uriList'))
        assert_that(fetch_product_list_response.content['body']['uriList'], not_none())
        uri_list = fetch_product_list_response.content['body']['uriList']

        prod = next((
                prod_content for prod_content in PurchaseUtil.get_product_infos(uri_list)
                if prod_content['product_code'] == config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('price'))
        assert_that(prod['price'], has_key('real_price'))
        cost = prod['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COLOMBIA.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COLOMBIA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COLOMBIA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COLOMBIA.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_rounding_up_colombia_cost(self, config):
        config.log.info('Fetching {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE))

        fetch_product_list_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.STOREFRONT,
            config.store.wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.COLOMBIA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.LANGUAGE
        )
        fetch_product_list_response.assert_is_success()

        assert_that(fetch_product_list_response.content['body'], has_key('uriList'))
        assert_that(fetch_product_list_response.content['body']['uriList'], not_none())
        uri_list = fetch_product_list_response.content['body']['uriList']

        prod = next((
                prod_content for prod_content in PurchaseUtil.get_product_infos(uri_list)
                if prod_content['product_code'] == config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('price'))
        assert_that(prod['price'], has_key('real_price'))
        cost = prod['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.COLOMBIA.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.COLOMBIA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_UP.COLOMBIA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_UP.COLOMBIA.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_rounding_down_costa_rica_cost(self, config):
        config.log.info('Fetching {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE))

        fetch_product_list_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.STOREFRONT,
            config.store.wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COSTA_RICA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.LANGUAGE
        )
        fetch_product_list_response.assert_is_success()

        assert_that(fetch_product_list_response.content['body'], has_key('uriList'))
        assert_that(fetch_product_list_response.content['body']['uriList'], not_none())
        uri_list = fetch_product_list_response.content['body']['uriList']

        prod = next((
                prod_content for prod_content in PurchaseUtil.get_product_infos(uri_list)
                if prod_content['product_code'] == config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('price'))
        assert_that(prod['price'], has_key('real_price'))
        cost = prod['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COSTA_RICA.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COSTA_RICA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COSTA_RICA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COSTA_RICA.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_rounding_up_costa_rica_cost(self, config):
        config.log.info('Fetching {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE))

        fetch_product_list_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.STOREFRONT,
            config.store.wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.COSTA_RICA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.LANGUAGE
        )
        fetch_product_list_response.assert_is_success()

        assert_that(fetch_product_list_response.content['body'], has_key('uriList'))
        assert_that(fetch_product_list_response.content['body']['uriList'], not_none())
        uri_list = fetch_product_list_response.content['body']['uriList']

        prod = next((
                prod_content for prod_content in PurchaseUtil.get_product_infos(uri_list)
                if prod_content['product_code'] == config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('price'))
        assert_that(prod['price'], has_key('real_price'))
        cost = prod['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.COSTA_RICA.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.COSTA_RICA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_UP.COSTA_RICA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_UP.COSTA_RICA.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_rounding_down_mexico_cost(self, config):
        config.log.info('Fetching {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE))

        fetch_product_list_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.STOREFRONT,
            config.store.wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.MEXICO.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.LANGUAGE
        )
        fetch_product_list_response.assert_is_success()

        assert_that(fetch_product_list_response.content['body'], has_key('uriList'))
        assert_that(fetch_product_list_response.content['body']['uriList'], not_none())
        uri_list = fetch_product_list_response.content['body']['uriList']

        prod = next((
                prod_content for prod_content in PurchaseUtil.get_product_infos(uri_list)
                if prod_content['product_code'] == config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('price'))
        assert_that(prod['price'], has_key('real_price'))
        cost = prod['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.MEXICO.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.MEXICO.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.MEXICO.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.MEXICO.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_rounding_up_mexico_cost(self, config):
        config.log.info('Fetching {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE))

        fetch_product_list_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.STOREFRONT,
            config.store.wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.MEXICO.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.LANGUAGE
        )
        fetch_product_list_response.assert_is_success()

        assert_that(fetch_product_list_response.content['body'], has_key('uriList'))
        assert_that(fetch_product_list_response.content['body']['uriList'], not_none())
        uri_list = fetch_product_list_response.content['body']['uriList']

        prod = next((
                prod_content for prod_content in PurchaseUtil.get_product_infos(uri_list)
                if prod_content['product_code'] == config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('price'))
        assert_that(prod['price'], has_key('real_price'))
        cost = prod['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.MEXICO.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.MEXICO.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_UP.MEXICO.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_UP.MEXICO.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_rounding_down_nicaragua_cost(self, config):
        config.log.info('Fetching {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE))

        fetch_product_list_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.STOREFRONT,
            config.store.wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.NICARAGUA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.LANGUAGE
        )
        fetch_product_list_response.assert_is_success()

        assert_that(fetch_product_list_response.content['body'], has_key('uriList'))
        assert_that(fetch_product_list_response.content['body']['uriList'], not_none())
        uri_list = fetch_product_list_response.content['body']['uriList']

        prod = next((
                prod_content for prod_content in PurchaseUtil.get_product_infos(uri_list)
                if prod_content['product_code'] == config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('price'))
        assert_that(prod['price'], has_key('real_price'))
        cost = prod['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.NICARAGUA.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.NICARAGUA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.NICARAGUA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.NICARAGUA.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_rounding_up_nicaragua_cost(self, config):
        config.log.info('Fetching {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE))

        fetch_product_list_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.STOREFRONT,
            config.store.wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.NICARAGUA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.LANGUAGE
        )
        fetch_product_list_response.assert_is_success()

        assert_that(fetch_product_list_response.content['body'], has_key('uriList'))
        assert_that(fetch_product_list_response.content['body']['uriList'], not_none())
        uri_list = fetch_product_list_response.content['body']['uriList']

        prod = next((
                prod_content for prod_content in PurchaseUtil.get_product_infos(uri_list)
                if prod_content['product_code'] == config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('price'))
        assert_that(prod['price'], has_key('real_price'))
        cost = prod['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.NICARAGUA.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.NICARAGUA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_UP.NICARAGUA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_UP.NICARAGUA.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_rounding_down_uruguay_cost(self, config):
        config.log.info('Fetching {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE))

        fetch_product_list_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.STOREFRONT,
            config.store.wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.URUGUAY.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.LANGUAGE
        )
        fetch_product_list_response.assert_is_success()

        assert_that(fetch_product_list_response.content['body'], has_key('uriList'))
        assert_that(fetch_product_list_response.content['body']['uriList'], not_none())
        uri_list = fetch_product_list_response.content['body']['uriList']

        prod = next((
                prod_content for prod_content in PurchaseUtil.get_product_infos(uri_list)
                if prod_content['product_code'] == config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('price'))
        assert_that(prod['price'], has_key('real_price'))
        cost = prod['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.URUGUAY.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.URUGUAY.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.URUGUAY.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.URUGUAY.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_rounding_up_uruguay_cost(self, config):
        config.log.info('Fetching {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE))

        fetch_product_list_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.STOREFRONT,
            config.store.wgid,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.URUGUAY.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.LANGUAGE
        )
        fetch_product_list_response.assert_is_success()

        assert_that(fetch_product_list_response.content['body'], has_key('uriList'))
        assert_that(fetch_product_list_response.content['body']['uriList'], not_none())
        uri_list = fetch_product_list_response.content['body']['uriList']

        prod = next((
                prod_content for prod_content in PurchaseUtil.get_product_infos(uri_list)
                if prod_content['product_code'] == config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('price'))
        assert_that(prod['price'], has_key('real_price'))
        cost = prod['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.URUGUAY.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.URUGUAY.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_UP.URUGUAY.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_UP.URUGUAY.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_rounding_down_argentina_cost(self, config):
        config.log.info('Fetching price for {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE))

        fetch_product_price_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.ARGENTINA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.AMOUNT
        )
        fetch_product_price_response.assert_is_success()

        assert_that(fetch_product_price_response.content['body'], has_key('price'))
        assert_that(fetch_product_price_response.content['body']['price'], has_key('real_price'))
        cost = fetch_product_price_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.ARGENTINA.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.ARGENTINA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.ARGENTINA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.ARGENTINA.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_rounding_up_argentina_cost(self, config):
        config.log.info('Fetching price for {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE))

        fetch_product_price_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.ARGENTINA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.AMOUNT
        )
        fetch_product_price_response.assert_is_success()

        assert_that(fetch_product_price_response.content['body'], has_key('price'))
        assert_that(fetch_product_price_response.content['body']['price'], has_key('real_price'))
        cost = fetch_product_price_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.ARGENTINA.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.ARGENTINA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_UP.ARGENTINA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_UP.ARGENTINA.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_rounding_down_bolivia_cost(self, config):
        config.log.info('Fetching price for {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE))

        fetch_product_price_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.BOLIVIA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.AMOUNT
        )
        fetch_product_price_response.assert_is_success()

        assert_that(fetch_product_price_response.content['body'], has_key('price'))
        assert_that(fetch_product_price_response.content['body']['price'], has_key('real_price'))
        cost = fetch_product_price_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.BOLIVIA.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.BOLIVIA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.BOLIVIA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.BOLIVIA.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_rounding_up_bolivia_cost(self, config):
        config.log.info('Fetching price for {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE))

        fetch_product_price_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.BOLIVIA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.AMOUNT
        )
        fetch_product_price_response.assert_is_success()

        assert_that(fetch_product_price_response.content['body'], has_key('price'))
        assert_that(fetch_product_price_response.content['body']['price'], has_key('real_price'))
        cost = fetch_product_price_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.BOLIVIA.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.BOLIVIA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_UP.BOLIVIA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_UP.BOLIVIA.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_rounding_down_chile_cost(self, config):
        config.log.info('Fetching price for {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE))

        fetch_product_price_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CHILE.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.AMOUNT
        )
        fetch_product_price_response.assert_is_success()

        assert_that(fetch_product_price_response.content['body'], has_key('price'))
        assert_that(fetch_product_price_response.content['body']['price'], has_key('real_price'))
        cost = fetch_product_price_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CHILE.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CHILE.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CHILE.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CHILE.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_rounding_up_chile_cost(self, config):
        config.log.info('Fetching price for {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE))

        fetch_product_price_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CHILE.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.AMOUNT
        )
        fetch_product_price_response.assert_is_success()

        assert_that(fetch_product_price_response.content['body'], has_key('price'))
        assert_that(fetch_product_price_response.content['body']['price'], has_key('real_price'))
        cost = fetch_product_price_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CHILE.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CHILE.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CHILE.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CHILE.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_rounding_down_colombia_cost(self, config):
        config.log.info('Fetching price for {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE))

        fetch_product_price_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COLOMBIA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.AMOUNT
        )
        fetch_product_price_response.assert_is_success()

        assert_that(fetch_product_price_response.content['body'], has_key('price'))
        assert_that(fetch_product_price_response.content['body']['price'], has_key('real_price'))
        cost = fetch_product_price_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COLOMBIA.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COLOMBIA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COLOMBIA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COLOMBIA.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_rounding_up_colombia_cost(self, config):
        config.log.info('Fetching price for {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE))

        fetch_product_price_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.COLOMBIA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.AMOUNT
        )
        fetch_product_price_response.assert_is_success()

        assert_that(fetch_product_price_response.content['body'], has_key('price'))
        assert_that(fetch_product_price_response.content['body']['price'], has_key('real_price'))
        cost = fetch_product_price_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.COLOMBIA.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.COLOMBIA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_UP.COLOMBIA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_UP.COLOMBIA.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_rounding_down_costa_rica_cost(self, config):
        config.log.info('Fetching price for {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE))

        fetch_product_price_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COSTA_RICA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.AMOUNT
        )
        fetch_product_price_response.assert_is_success()

        assert_that(fetch_product_price_response.content['body'], has_key('price'))
        assert_that(fetch_product_price_response.content['body']['price'], has_key('real_price'))
        cost = fetch_product_price_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COSTA_RICA.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COSTA_RICA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COSTA_RICA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.COSTA_RICA.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_rounding_up_costa_rica_cost(self, config):
        config.log.info('Fetching price for {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE))

        fetch_product_price_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.COSTA_RICA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.AMOUNT
        )
        fetch_product_price_response.assert_is_success()

        assert_that(fetch_product_price_response.content['body'], has_key('price'))
        assert_that(fetch_product_price_response.content['body']['price'], has_key('real_price'))
        cost = fetch_product_price_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.COSTA_RICA.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.COSTA_RICA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_UP.COSTA_RICA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_UP.COSTA_RICA.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_rounding_down_mexico_cost(self, config):
        config.log.info('Fetching price for {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE))

        fetch_product_price_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.MEXICO.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.AMOUNT
        )
        fetch_product_price_response.assert_is_success()

        assert_that(fetch_product_price_response.content['body'], has_key('price'))
        assert_that(fetch_product_price_response.content['body']['price'], has_key('real_price'))
        cost = fetch_product_price_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.MEXICO.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.MEXICO.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.MEXICO.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.MEXICO.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_rounding_up_mexico_cost(self, config):
        config.log.info('Fetching price for {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE))

        fetch_product_price_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.MEXICO.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.AMOUNT
        )
        fetch_product_price_response.assert_is_success()

        assert_that(fetch_product_price_response.content['body'], has_key('price'))
        assert_that(fetch_product_price_response.content['body']['price'], has_key('real_price'))
        cost = fetch_product_price_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.MEXICO.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.MEXICO.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_UP.MEXICO.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_UP.MEXICO.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_rounding_down_nicaragua_cost(self, config):
        config.log.info('Fetching price for {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE))

        fetch_product_price_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.NICARAGUA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.AMOUNT
        )
        fetch_product_price_response.assert_is_success()

        assert_that(fetch_product_price_response.content['body'], has_key('price'))
        assert_that(fetch_product_price_response.content['body']['price'], has_key('real_price'))
        cost = fetch_product_price_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.NICARAGUA.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.NICARAGUA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.NICARAGUA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.NICARAGUA.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_rounding_up_nicaragua_cost(self, config):
        config.log.info('Fetching price for {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE))

        fetch_product_price_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.NICARAGUA.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.AMOUNT
        )
        fetch_product_price_response.assert_is_success()

        assert_that(fetch_product_price_response.content['body'], has_key('price'))
        assert_that(fetch_product_price_response.content['body']['price'], has_key('real_price'))
        cost = fetch_product_price_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.NICARAGUA.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.NICARAGUA.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_UP.NICARAGUA.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_UP.NICARAGUA.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_rounding_down_uruguay_cost(self, config):
        config.log.info('Fetching price for {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE))

        fetch_product_price_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.URUGUAY.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.AMOUNT
        )
        fetch_product_price_response.assert_is_success()

        assert_that(fetch_product_price_response.content['body'], has_key('price'))
        assert_that(fetch_product_price_response.content['body']['price'], has_key('real_price'))
        cost = fetch_product_price_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.URUGUAY.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.URUGUAY.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.URUGUAY.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_DOWN.URUGUAY.AMOUNT)))

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_rounding_up_uruguay_cost(self, config):
        config.log.info('Fetching price for {}'.format(config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE))

        fetch_product_price_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.URUGUAY.COUNTRY,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.AMOUNT
        )
        fetch_product_price_response.assert_is_success()

        assert_that(fetch_product_price_response.content['body'], has_key('price'))
        assert_that(fetch_product_price_response.content['body']['price'], has_key('real_price'))
        cost = fetch_product_price_response.content['body']['price']['real_price']

        config.log.info('{} should cost {} {}'.format(
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.CODE,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.URUGUAY.AMOUNT,
            config.data.TEST_LATIN_COUNTRY_ROUND_UP.URUGUAY.CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_LATIN_COUNTRY_ROUND_UP.URUGUAY.CODE))

        assert_that(cost, has_key('amount'))
        assert_that(cost['amount'], equal_to(str(config.data.TEST_LATIN_COUNTRY_ROUND_UP.URUGUAY.AMOUNT)))
