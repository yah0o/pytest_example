from integration.main.request import RequestBuilder, Response
from integration.main.helpers import PurchaseUtil


class Psa(object):
    """
    Psa Service
    """

    def __init__(self, url):
        """
        Initialized with PSA base url from the environment YAML file
        :param url: Base url for PSA
        :type url: str
        """
        self.__url = url

    @property
    def service(self):
        return PsaService(self.__url)

    def request(self, path):
        """
        :param path: Path of the http request
        :type path: str
        :return: Request formatted as http
        :rtype: RequestBuilder
        """
        url = 'http://{0}{1}'.format(self.__url, path)
        return RequestBuilder(url, session=None)


class PsaService(Psa):

    def __init__(self, base_url):
        """
        Initialized with PSA base url passed in from PSA
        :param base_url: Base URL
        :type base_url: str
        """
        Psa.__init__(self, base_url)

    def bind(
            self,
            wgid,
            payment_method,
            payment_method_nonce):
        """
        Bind paypal payment method to account
        :param wgid: WGID of account for binding
        :type wgid: int
        :param payment_method: Payment method
        :type payment_method: PurchaseUtil
        :param payment_method_nonce: Payment method nonce
        :type payment_method_nonce: PurchaseUtil
        :return: braintree_paypal response to bind account
        :rtype: Response
        """

        port = 50030

        return self.request(
            ':{}/shop/bind/'.format(port)
        ).headers({
        }).data({
            'spa_id': wgid,
            'payment_method': payment_method,
            'payment_method_nonce': payment_method_nonce
        }).post()

    def bind_init(
            self,
            wgid,
            payment_method,
            username):
        """
        Bind qiwi payment method to account
        :param wgid: WGID of account to initialize binding
        :type wgid: int
        :param payment_method: Payment method
        :type payment_method: PurchaseUtil
        :param username: Username of account
        :type username: str
        :return: iqp_qiwi bind initialize request
        :rtype: Response
        """

        port = 50030
        if payment_method is 'credit_card_adyen':
            port = 50036

        return self.request(
            ':{}/shop/bind/init/'.format(port)
        ).headers({
        }).data({
            'spa_id': wgid,
            'payment_method': payment_method,
            'username': username
        }).post()

    def bind_confirm(
            self,
            wgid,
            payment_method,
            otp):
        """
        Confirm payment method binding to account
        :param wgid: WGID of account to confirm binding
        :type wgid: int
        :param payment_method: Payment method
        :type payment_method: PurchaseUtil
        :param otp: OTP password
        :type otp: str
        :return: iqp_qiwi bind confirm response
        :rtype: Response
        """

        return self.request(
            ':50030/shop/bind/confirm/'
        ).headers({
        }).data({
            'spa_id': wgid,
            'payment_method': payment_method,
            'otp': otp
        }).post()
