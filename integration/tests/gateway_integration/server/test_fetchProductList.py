import pytest
from allure import severity_level
from hamcrest import *
from requests import get, codes

from integration.main.helpers import AccountUtilities
from integration.main.helpers.matchers import not_empty
from integration.main.request import RequestBuilder, RequestConstants, ResponseMessage


class TestFetchProductList(object):

    @pytest.fixture(autouse=True)
    def setup(self, config):

        ###
        # Test setup

        account = AccountUtilities.create_account()
        account_created = config.spa.http.create_account(account.__dict__)
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

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product list')
    @pytest.allure.severity(severity_level.CRITICAL)
    @pytest.mark.parametrize('content_type', [
        RequestConstants.ContentTypes.JSON,
        RequestConstants.ContentTypes.MSG_PACK
    ])
    def test_fetch_product_list_should_succeed_when_fetching_storefront(self, config, content_type):

        expected_products = config.data.TEST_STORE.PRODUCTS

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_STORE.STOREFRONT,
            config.store.profile_id,
            config.data.TEST_STORE.COUNTRY,
            config.data.TEST_STORE.LANGUAGE,
            content_type=content_type
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body'], has_key('uriList'))

        assert_that(fetch_response.content['body']['uriList'], not_empty(),
                    'fetch_product_list_response key uriList is empty')

        for uri in fetch_response.content['body']['uriList']:
            product_response = get(uri, verify=False)
            assert_that(product_response.status_code, equal_to(codes.ok),
                        'product_response status code is not ok')

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product list')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_profile_id', [0, None, '', .50])
    def test_fetch_product_list_with_invalid_profile(self, config, invalid_profile_id):

        # Unknown WGID error is an old behavior. Now it pass to PRODO like 0 WGID - correct by arch.

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_STORE.STOREFRONT,
            invalid_profile_id,
            config.data.TEST_STORE.COUNTRY,
            config.data.TEST_STORE.LANGUAGE
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body'], has_key('uriList'))

        for uri in fetch_response.content['body']['uriList']:
            product_response = RequestBuilder(uri).get()
            product_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product list')
    @pytest.allure.severity(severity_level.MINOR)
    def test_fetch_product_list_should_fail_when_profile_is_invalid(self, config):

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_STORE.STOREFRONT,
            -1,
            config.data.TEST_STORE.COUNTRY,
            config.data.TEST_STORE.LANGUAGE
        )
        fetch_response.expect_failure(result_code=ResponseMessage.INVALID_WGID)

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product list')
    @pytest.allure.severity(severity_level.MINOR)
    def test_fetch_product_list_should_fail_when_profile_is_string(self, config):

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_STORE.STOREFRONT,
            'bad_profile_id',
            config.data.TEST_STORE.COUNTRY,
            config.data.TEST_STORE.LANGUAGE
        )
        fetch_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                      result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product list')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_store', [
        None,
        ''
    ])
    def test_fetch_product_list_should_fail_when_store_is_invalid(self, config, invalid_store):

        fetch_response = config.freya.server_gateway.fetch_product_list(
            invalid_store,
            config.store.profile_id,
            config.data.TEST_STORE.COUNTRY,
            config.data.TEST_STORE.LANGUAGE
        )
        fetch_response.expect_failure(result_code=ResponseMessage.NO_PRODUCTS)

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product list')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('nonexistent_store', [
        0,
        'invalid_store',
        'Yl5noNof1c8bczPTnaDdsaqZDh4OMFLFgWTSViPypUM1YXjdxtmHvjCFOMmR0PhbBw8cnxCcNYBPD9uAD4owJHNI6SgnsSoEtDAm'
    ])
    def test_fetch_product_list_should_fail_when_store_does_not_exist(self, config, nonexistent_store):

        fetch_response = config.freya.server_gateway.fetch_product_list(
            nonexistent_store,
            config.store.profile_id,
            config.data.TEST_STORE.COUNTRY,
            config.data.TEST_STORE.LANGUAGE
        )
        fetch_response.expect_failure(result_code=ResponseMessage.STOREFRONT_NOT_FOUND)

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product list')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_country', [0, '', 'invalid_country'])
    def test_fetch_product_list_should_fail_when_country_is_invalid(self, config, invalid_country):

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_STORE.STOREFRONT,
            config.store.profile_id,
            invalid_country,
            config.data.TEST_STORE.LANGUAGE
        )
        fetch_response.expect_failure(result_code=ResponseMessage.VALIDATION_ERROR,
                                      result_message=ResponseMessage.UNABLE_TO_PROCESS_JSON)

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product list')
    @pytest.allure.severity(severity_level.MINOR)
    def test_fetch_product_list_should_succeed_when_country_is_none(self, config):

        # default country for environment applied using currency_data.yaml

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_STORE.STOREFRONT,
            config.store.profile_id,
            None,
            config.data.TEST_STORE.LANGUAGE
        )
        fetch_response.assert_is_success()
        assert_that(fetch_response.content['body'], has_key('uriList'))

        for uri in fetch_response.content['body']['uriList']:
            product_response = RequestBuilder(uri).get()
            product_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product list')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('invalid_language', [0, '', 'invalid_language'])
    def test_fetch_product_list_should_succeed_when_language_is_invalid(self, config, invalid_language):

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_STORE.STOREFRONT,
            config.store.profile_id,
            config.data.TEST_STORE.COUNTRY,
            invalid_language
        )
        fetch_response.assert_is_success()

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product list')
    @pytest.allure.severity(severity_level.MINOR)
    def test_fetch_product_list_should_fail_when_language_is_none(self, config):

        fetch_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_STORE.STOREFRONT,
            config.store.profile_id,
            config.data.TEST_STORE.COUNTRY,
            None
        )
        fetch_response.expect_failure(result_code=ResponseMessage.LANGUAGE_NOT_DEFINED)

    @pytest.allure.feature('server')
    @pytest.allure.story('fetch product list')
    @pytest.allure.severity(severity_level.MINOR)
    def test_fetch_product_list_should_succeed_when_product_have_min_of_two(self, config):

        fetch_prod_list_response = config.freya.server_gateway.fetch_product_list(
            config.data.TEST_MIN_OF_2.STOREFRONT,
            config.store.profile_id,
            config.data.TEST_MIN_OF_2.COUNTRY,
            config.data.TEST_MIN_OF_2.LANGUAGE
        )
        fetch_prod_list_response.assert_is_success()

        assert_that(fetch_prod_list_response.content['body'], has_key('uriList'))
        assert_that(fetch_prod_list_response.content['body']['uriList'], has_length(1))
        uri = fetch_prod_list_response.content['body']['uriList'][0]

        prod_response = RequestBuilder(uri).get()
        prod_response.assert_is_success()

        assert_that(prod_response.content, has_key('price'))
        assert_that(prod_response.content['price'], has_key('real_price'))
        price = prod_response.content['price']['real_price']

        assert_that(price, has_key('code'))
        assert_that(price['code'], equal_to(config.data.TEST_MIN_OF_2.COST.CODE))
        assert_that(price, has_key('amount'))
        assert_that(float(price['amount']), equal_to(config.data.TEST_MIN_OF_2.COST.AMOUNT))
