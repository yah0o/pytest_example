from integration.main.request import RequestBuilder


class Cats(object):
    """
    Cats Service
    """

    def __init__(self, url):
        """
        Initialized with Cats base url from the environment YAML file
        :param url: Base url for Cats
        :type url: str
        """
        self.__url = url

    @property
    def service(self):
        return CatsService(self.__url)

    def request(self, path):
        """
        :param path: Path of the http request
        :type path: str
        :return: Request formatted as http
        :rtype: RequestBuilder
        """
        url = 'http://{0}/{1}'.format(self.__url, path)
        return RequestBuilder(url, session=None)


class CatsService(Cats):

    def __init__(self, base_url):
        """
        Initialized with Cats base url passed in from Cats
        :param base_url: Base URL
        :type base_url: str
        """
        Cats.__init__(self, base_url)

    def active_catalogs(self, title_code):
        """
        Get active catalog
        :param title_code: title code
        :type title_code: str
        """
        url = 'api/v1/titles/{}/active_catalogs'.format(title_code)
        return self.request(url).get()

    def get_entity_title_by_type_and_code(self, title_code, entity_type, code):
        """
        Get entity  by title code and entity type and entity code
        :param title_code: title code
        :type title_code: str
        :param entity_type: type of entity (storefront, currency, etc.)
        :type entity_type: str
        :param code: entity code
        :type code: str
        """
        url = 'api/v1/titles/{title_code}/entities/{entity_type}/{code}'.format(title_code=title_code,
                                                                                entity_type=entity_type,
                                                                                code=code)
        return self.request(url).get()
