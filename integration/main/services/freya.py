import requests

from admin import Admin
from auth import AuthGateway
from consul import ConsulManager
from inventory import InventoryService
from product import ProductService
from server import ServerGateway
from titleconfig import TitleConfigService
from titleregistry import TitleRegService
from tools import ToolsGateway


class Freya(object):
    class Endpoints(object):
        AUTH = 'auth'
        SERVER = 'server'
        TOOLS = 'tools'

        # Service endpoints
        INVENTORY = 'inventory'
        TITLECONFIG = 'titleconfig'
        TITLEREGISTRY = 'titleconfig'
        PRODUCT = 'product'

        # All
        ALL = [AUTH, SERVER, TOOLS, INVENTORY, TITLECONFIG, TITLEREGISTRY, PRODUCT]

    def __init__(self, url, api_key, session=None, service_domains=None):
        """
        Initializes Freya object with base url, API key, session and service_domains from environment YAML file
        :param url: Base URL from environment file
        :type url: str
        :param api_key: API key from environment file
        :type api_key: str
        :param session: Session object which manages and persists settings across requests (cookies, auth, proxies)
        :type session: Session
        :param service_domains: Service domains from environment file(Inventory, Tools, Product, TitleConfig) as json
        :type service_domains: str
        """

        self.__service_domains = {} if service_domains is None else service_domains
        self.__url = url
        self.__api_key = api_key

        # creates a new session if one has not been provided
        self.__session = requests.Session() if session is None else session

    @property
    def tools_gateway(self):
        """
        Retrieves ToolsGateway object
        :return: ToolsGateway object
        :rtype: ToolsGateway
        """

        return ToolsGateway(self.__get_endpoint(Freya.Endpoints.TOOLS), self.__session)

    @property
    def title_config(self):
        """
        Retrieves TitleConfigService object
        :return: TitleConfigService object
        :rtype: TitleConfigService
        """

        return TitleConfigService(self.__get_endpoint(Freya.Endpoints.TITLECONFIG), self.__session)

    @property
    def title_registry(self):
        """
        Retrieves TitleRegService object
        :return: TitleRegService object
        :rtype: TitleRegService
        """

        return TitleRegService(self.__get_endpoint(Freya.Endpoints.TITLEREGISTRY), self.__session)

    @property
    def server_gateway(self):
        """
        Retrieves ServerGateway object
        :return: ServerGateway object
        :rtype: ServerGateway
        """
        return ServerGateway(self.__get_endpoint(Freya.Endpoints.SERVER), self.__api_key, self.__session)

    @property
    def auth_gateway(self):
        """
        Retrieves AuthGateway object
        :return: AuthGateway object
        :rtype: AuthGateway
        """

        return AuthGateway(self.__get_endpoint(Freya.Endpoints.AUTH), self.__api_key, self.__session)

    @property
    def inventory_service(self):
        """
        Retrieves InventoryService object
        :return: InventoryService object
        :rtype: InventoryService
        """

        return InventoryService(self.__get_endpoint(Freya.Endpoints.INVENTORY), self.__session)

    @property
    def product_service(self):
        """
        Retrieves ProductService object
        :return: ProductService object
        :rtype: ProductService
        """

        return ProductService(self.__get_endpoint(Freya.Endpoints.PRODUCT), self.__session)

    def admin(self, consul_base_url, environment_name, color):
        """
        Admin portal providing URLs to server, tools or auth
        :param consul_base_url: Consul URL from environment YAML file
        :type consul_base_url: str
        :param environment_name: Environment name
        :type environment_name: str
        :param color: Environment color default to blue unless specified differently from environment YAML file
        :type color: str
        :return: Admin object
        :rtype: Admin
        """
        consul_manager = ConsulManager(consul_base_url, environment_name)

        server_admin_url = consul_manager.get_server_admin_url(color)
        auth_admin_url = consul_manager.get_auth_admin_url(color)
        tools_admin_url = consul_manager.get_tools_admin_url(color)

        return Admin(server_admin_url, auth_admin_url, tools_admin_url)

    def __get_endpoint(self, item):
        """
        Gets the endpoint for auth/server/tools in the case where the env file specifies one is not under the main
        domain such as in the case of local testing where one of the services might be on localhost
        :param item: Name of service
        :type item: str
        :return: Domain of service
        :rtype: str
        """

        assert item in Freya.Endpoints.ALL, 'Invalid Freya endpoint. {0} not in {1}'.format(item, Freya.Endpoints.ALL)

        if item in self.__service_domains:
            return self.__service_domains[item]
        return self.__url
