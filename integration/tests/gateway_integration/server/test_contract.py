import pytest
from hamcrest import assert_that, has_item, equal_to, not_none


@pytest.allure.feature('server')
@pytest.allure.story('call contract')
def test_call_non_ggapi_contract(config):
    contract = 'commerce.fetch-product-list.v1'
    schema = {"title_code": config.environment['integration_title'],
              "country_code": "US",
              "storefront": "test_store",
              "language": "en"}
    response = config.freya.server_gateway.contract_call(schema=schema, contract_id=contract)
    response.assert_is_success()
    assert_that(response.content['payload']['items'], not_none())

@pytest.allure.feature('server')
@pytest.allure.story('call contract')
def test_call_ggapi_contract(config):
    contract = 'ggapi.get-registered-methods.v2'
    schema = {"title": config.environment['integration_title']}
    response = config.freya.server_gateway.contract_call(schema=schema, contract_id=contract)
    response.assert_is_success()
    assert_that(response.content['payload'], has_item('methods'))


@pytest.allure.feature('server')
@pytest.allure.story('call contract')
def test_call_contract_empty_schema(config):
    contract = 'ggapi.get-registered-methods.v2'
    schema = {}
    response = config.freya.server_gateway.contract_call(schema=schema, contract_id=contract)
    response.expect_failure()
    assert_that(response.content['error']['code'], equal_to('common.v1.validation-error'))

@pytest.allure.feature('server')
@pytest.allure.story('call contract')
def test_call_contract_invalid_api_key(config):
    contract = 'ggapi.get-registered-methods.v2'
    schema = {"title": config.environment['integration_title']}
    response = config.freya.server_gateway.contract_call(schema=schema, contract_id=contract, freya_api_key='invalid')
    response.expect_failure(result_code='ERROR', result_message='Unknown server API key')

@pytest.allure.feature('server')
@pytest.allure.story('call contract')
def test_call_not_exist_contract(config):
    contract = 'system.v1.roll-call1'
    schema = {"reason": "abc"}
    response = config.freya.server_gateway.contract_call(schema=schema, contract_id=contract)
    response.expect_failure()
    assert_that(response.content['error']['code'], equal_to('common.v1.client-error'))
    assert_that(response.content['error']['context']['reason'], equal_to('contract not found'))