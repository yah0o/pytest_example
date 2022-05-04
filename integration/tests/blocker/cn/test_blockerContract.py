import pytest
from hamcrest import assert_that, has_item
from allure import severity_level


@pytest.allure.feature('Contract')
@pytest.allure.story('call contract')
@pytest.allure.severity(severity_level.BLOCKER)
class TestContract(object):

    def test_call_system_v1_roll_call_contract(self, config):
        contract = 'system.v1.roll-call'
        schema = {"reason": "abc"}
        response = config.freya.server_gateway.contract_call(schema=schema, contract_id=contract)
        response.assert_is_success()
        assert_that(response.content['payload']['serving_contracts'], has_item('system.v1.roll-call'))
