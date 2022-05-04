from gateway import Gateway
from integration.main.request import RequestConstants, Response
from requests import Session


class TitleRegService(Gateway):
    """
    Title Registry
    """

    def __init__(self, base_url, session):
        """
        Initializes Gateway with base url and session object
        :param base_url: Gateway base url from environment file
        :type base_url: str
        :param session: Session object which manages and persists settings across requests (cookies, auth, proxies)
        :type session: Session
        """

        Gateway.__init__(self, base_url, session)

    def get_titles(
            self,
            include=RequestConstants.Parameters.OPTIONAL
    ):
        """
        Retrieves a list of all registered titles
        :param include: String query parameters to include in the list of titles being retrieved
        :type include: str
        :return: Response to get titles request
        :rtype: Response
        """

        return self.request(
            'titleconfig/titles'
        ).json({
            'include': include
        }).get()

    def get_components(self):
        """
        Retrieves a list of components
        :return: Response to get components request
        :rtype: Response
        """

        return self.request('titleconfig/titles/components').get()

    def get_currencies(self):
        """
        Retrieves a list of all virtual and real currencies per title
        :return: Response to get currencies request
        :rtype: Response
        """

        return self.request('titleconfig/titles/currencies').get()

    def get_currencies_virtual(self):
        """
        Retrieves a list of all virtual currencies per title
        :return: Response to get currencies virtual request
        :rtype: Response
        """

        return self.request('titleconfig/titles/currencies/map').get()

    def get_currencies_real(self):
        """
        Retrieves a list of all real currencies per title
        :return: Response to get currencies real request
        :rtype: Response
        """

        return self.request('titleconfig/titles/currencies/real').get()

    def get_entitlements(self):
        """
        Retrieves a list of all entitlements per title
        :return: Response to get entitlements request
        :rtype: Response
        """

        return self.request('titleconfig/titles/entitlements').get()

    def get_entitlements_map(self):
        """
        Retrieves a map of all entitlements per title
        :return: Response to get entitlements request
        :rtype: Response
        """

        return self.request('titleconfig/titles/entitlements/map').get()

    def get_namespaces(self):
        """
        Retrieves a list of namespaces per title
        :return: Response to get namespaces request
        :rtype: Response
        """

        return self.request('titleconfig/titles/namespaces').get()

    def ping(self):
        """
        Request a ping method
        :return: Response with 'pong'
        :rtype: Response
        """

        return self.request('ping').get()
