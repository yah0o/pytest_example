import uuid

from integration.main.request import RequestBuilder


class PurchaseUtil(object):
    class PaymentType(object):
        WGM = "WGM"
        PSA = "PSA"
        BONUS_CODE = "BONUS_CODE"
        IGP = "IGP"

    class PaymentCode(object):
        IGP_QIWI = 'igp_qiwi'
        BRAINTREE_PAYPAL = 'braintree_paypal'
        ALFABANK = 'igp_credit_card_ab'

    class PaymentNone(object):
        PAYPAL_NONCE = 'fake-paypal-future-nonce'

    class PurchaseStatus(object):
        SUCCESS = 'SUCCESS'
        COMMITTED = 'COMMITTED'
        FINISHED = 'FINISHED'
        PENDING = 'PENDING'

        SUCCESSFUL_STATUSES = ['SUCCESS', 'COMMITTED', 'FINISHED']

    @staticmethod
    def get_product_infos(uri_list):
        for uri in uri_list:
            uri_response = RequestBuilder(uri).get()
            uri_response.assert_is_success()
            yield uri_response.content

    @staticmethod
    def get_transaction_id(request):
        """
        gets the transaction id from a request that was used if there is one, else None

        :return: uuid 
        """

        if request.details['json']:
            body = request.details['json']
        elif request.details['data']:
            body = request.details['data']
        else:
            return None

        if 'body' in body:
            body = body['body']
            return uuid.UUID(body['transaction_id']) if 'transaction_id' in body else None

        return None
