from integration.main.request import RequestBuilder, Response


class Wgw(object):
    """
    WGW Service
    """

    def __init__(self, url):
        """
        Initialized with WGW base url from the environment YAML file
        :param url: Base url for WGW
        :type url: str
        """
        self.__url = url

    @property
    def service(self):
        return WgwService(self.__url)

    def request(self, path):
        """
        :param path: Path of the http request
        :type path: str
        :return: Request formatted as http
        :rtype: RequestBuilder
        """
        url = 'http://{0}/{1}'.format(self.__url, path)
        return RequestBuilder(url, session=None)


class WgwService(Wgw):

    def __init__(self, base_url):
        """
        Initialized with WGW base url passed in from WGW
        :param base_url: Base URL
        :type base_url: str
        """
        Wgw.__init__(self, base_url)

    def premium_read(self, wgid):
        """
        Read from premium wallet
        :param wgid: WGID of account to read wallet from
        :type wgid: int
        :return: Response of the wallet read
        :rtype: Response
        """
        return self.request('v1/premium/read').json({
            'wgid': wgid
        }).post()
