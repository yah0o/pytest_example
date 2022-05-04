import pytest
from allure import severity_level
from hamcrest import *
from integration.main.helpers import AccountUtilities, PurchaseUtil, RequestBuilder
from integration.main.services import ConsulManager, RequestConstants


@pytest.mark.skip_for_regions('trie')
@pytest.allure.feature('functional')
@pytest.allure.story('coefficients')
class TestCoefficients(object):

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

        config.log.info('Make sure that coefficient is enabled')

        if config.environment.has('consul_token'):
            token = config.environment['consul_token']
        else:
            token = RequestConstants.Parameters.OPTIONAL

        consul = ConsulManager(config.environment.consul, config.environment.environment_name)
        enabled_response = consul.get_kv(
            '{}/product-price-coefficients/coefficients.enabled'.format(config.environment.environment_name),
            token=token
        )
        enabled = enabled_response.content

        if type(enabled) is not str or not enabled:
            config.log.info('Enabled on {} is {}'.format(
                config.environment.environment_name,
                enabled
            ))
            pytest.skip('Coefficient is not enabled')

        config.log.info('Get the Coefficient for AR')

        coefficient_response = consul.get_kv(
            '{}/product-price-coefficients/AR'.format(config.environment.environment_name),
            token=token
        )
        coefficient_response.assert_is_success()
        coefficient = coefficient_response.content

        config.log.info('Coefficient on {} for AR is {}'.format(
            config.environment.environment_name,
            coefficient
        ))

        config.log.info('Get the CES for US to AR')

        ces_response = config.freya.product_service.get_ces_data()
        ces_response.assert_is_success()

        ces_data = ces_response.content[config.data.TEST_COEFFICIENTS.REAL_MONEY.CODE]
        assert_that(ces_data, has_key('quotes'))
        assert_that(ces_data['quotes'], has_key(config.data.TEST_COEFFICIENTS.RM_AR_CURRENCY_CODE))

        ar_ces = ces_data['quotes'][config.data.TEST_COEFFICIENTS.RM_AR_CURRENCY_CODE]
        assert_that(ar_ces, has_key('value'))
        ces = float(ar_ces['value'])

        config.log.info('CES for ARS to USD on {} is {}'.format(
            config.environment.environment_name,
            ces
        ))

        config.log.info('Convert to AR cost including coefficients')

        config.store.calculated_cost = int(
            round(config.data.TEST_COEFFICIENTS.REAL_MONEY.AMOUNT * coefficient * ces, 0))

        ###
        # Runs test
        yield

        ###
        # Test cleanup goes here
        delete_response = config.spa.http.delete_account(config.store.wgid)
        delete_response.assert_is_success()

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_products_should_succeed_when_coefficient_is_enabled(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_COEFFICIENTS.CODE
        ))

        fetch_response = config.freya.server_gateway.fetch_products(
            [config.data.TEST_COEFFICIENTS.CODE],
            config.store.wgid,
            config.data.TEST_COEFFICIENTS.COUNTRY,
            config.data.TEST_COEFFICIENTS.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_COEFFICIENTS.CODE
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri = fetch_response.content['body']['uriList'][0]

        prod = RequestBuilder(uri).get()
        prod.assert_is_success()

        assert_that(prod.content, has_key('product_code'))
        assert_that(prod.content['product_code'], equal_to(config.data.TEST_COEFFICIENTS.CODE))

        assert_that(prod.content, has_key('price'))
        assert_that(prod.content['price'], has_key('real_price'))
        cost = prod.content['price']['real_price']

        config.log.info('{} price should be {} {}'.format(
            config.data.TEST_COEFFICIENTS.CODE,
            config.store.calculated_cost,
            config.data.TEST_COEFFICIENTS.RM_AR_CURRENCY_CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_COEFFICIENTS.RM_AR_CURRENCY_CODE))

        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to(str(config.store.calculated_cost))
        )

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_list_should_succeed_when_coefficient_is_enabled(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_COEFFICIENTS.CODE
        ))

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_COEFFICIENTS.STOREFRONT,
            config.store.wgid,
            config.data.TEST_COEFFICIENTS.COUNTRY,
            config.data.TEST_COEFFICIENTS.LANGUAGE
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_COEFFICIENTS.CODE
        ))

        assert_that(fetch_response.content['body'], has_key('uriList'))
        assert_that(fetch_response.content['body']['uriList'], not_none())
        uri_list = fetch_response.content['body']['uriList']

        prod = next(
            (
                prod for prod in PurchaseUtil.get_product_infos(uri_list) if
                prod['product_code'] == config.data.TEST_COEFFICIENTS.CODE
            ),
            None
        )
        assert_that(prod, not_none())

        assert_that(prod, has_key('product_code'))
        assert_that(prod['product_code'], equal_to(config.data.TEST_COEFFICIENTS.CODE))

        assert_that(prod, has_key('price'))
        assert_that(prod['price'], has_key('real_price'))
        cost = prod['price']['real_price']

        config.log.info('{} price should be {} {}'.format(
            config.data.TEST_COEFFICIENTS.CODE,
            config.store.calculated_cost,
            config.data.TEST_COEFFICIENTS.RM_AR_CURRENCY_CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_COEFFICIENTS.RM_AR_CURRENCY_CODE))

        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to(str(config.store.calculated_cost))
        )

    @pytest.allure.severity(severity_level.CRITICAL)
    def test_fetch_product_price_should_succeed_when_coefficient_is_enabled(self, config):
        config.log.info('Fetching {}'.format(
            config.data.TEST_COEFFICIENTS.CODE
        ))

        fetch_response = config.freya.server_gateway.fetch_product_price(
            config.data.TEST_COEFFICIENTS.CODE,
            config.data.TEST_COEFFICIENTS.COUNTRY,
            config.data.TEST_COEFFICIENTS.AMOUNT
        )
        fetch_response.assert_is_success()

        config.log.info('Getting {} info'.format(
            config.data.TEST_COEFFICIENTS.CODE
        ))

        assert_that(fetch_response.content['body'], has_key('price'))
        assert_that(fetch_response.content['body']['price'], has_key('real_price'))
        cost = fetch_response.content['body']['price']['real_price']

        config.log.info('{} price should be {} {}'.format(
            config.data.TEST_COEFFICIENTS.CODE,
            config.store.calculated_cost,
            config.data.TEST_COEFFICIENTS.RM_AR_CURRENCY_CODE
        ))

        assert_that(cost, has_key('code'))
        assert_that(cost['code'], equal_to(config.data.TEST_COEFFICIENTS.RM_AR_CURRENCY_CODE))

        assert_that(cost, has_key('amount'))
        assert_that(
            cost['amount'],
            equal_to(str(config.store.calculated_cost))
        )
