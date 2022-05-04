from integration.main.request import RequestBuilder, Response
from requests import Session


class Gateway(object):

    def __init__(self, base_url, session):
        """

        :param base_url: Base url passed in from environment file
        :type base_url: str
        :param session: Provides cookie persistence, connection-pooling, and configuration.
        :type session: Session
        """

        self.__base_url = base_url
        self.__session = session

    @property
    def session(self):
        """
        Session object which manages and persists settings across requests (cookies, auth, proxies)
        :return: Session object from configuration
        :rtype: Session
        """

        return self.__session

    @property
    def url(self):
        """
        :return: Base url from the environment YAML
        :rtype: str
        """

        return self.__base_url

    def ping(self):
        """
        :return: The ping response from Gateway
        :rtype: Response
        """

        return self.request('ping').get()

    def request(self, path):
        """
        Forms the request by joining the base URL and path and sends them through to RequestBuilder
        :param path: Specific http path of gateway request
        :type path: str
        :return: Formatted request
        :rtype: RequestBuilder
        """

        url = '{0}{1}'.format(self.__base_url, path)
        return RequestBuilder(url, session=self.__session)
