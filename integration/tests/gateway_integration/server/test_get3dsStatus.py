import pytest
import uuid
from allure import severity_level
from integration.main.request.constants import ResponseMessage


class TestServerGet3dsStatus(object):

    # e2e will be added by PSA team

    @pytest.allure.feature('server')
    @pytest.allure.story('get3dsStatus')
    @pytest.allure.severity(severity_level.MINOR)
    @pytest.mark.parametrize('fingerprint_sent, challenge_sent', [
                             (True, True),
                             (False, False),
                             (True, False),
                             (False, True)
                         ])
    def test_get_3ds_status_full_should_fail_with_not_exist_order(self, config, fingerprint_sent, challenge_sent):
        tx_id = str(uuid.uuid4())
        order_id = str(uuid.uuid4())
        get3ds_status_response = config.freya.server_gateway.get_3ds_status(transaction_id=tx_id,
                                                                            order_id=order_id,
                                                                            fingerprint_sent=fingerprint_sent,
                                                                            challenge_sent=challenge_sent
                                                                            )
        get3ds_status_response.expect_failure(result_code=ResponseMessage.ORDER_DOESNOT_EXIST)
