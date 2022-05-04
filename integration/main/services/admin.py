from gateway import Gateway
from integration.main.request import RequestConstants, Response


class Admin(object):

    def __init__(self, server_admin_url, auth_admin_url, tools_admin_url):
        """
        Initialized Admin object with server, auth and tools admin urls
        :param server_admin_url: Server admin url from CONSUL
        :type server_admin_url: str
        :param auth_admin_url: Auth admin url from CONSUL
        :type auth_admin_url: str
        :param tools_admin_url: Tools admin url from CONSUL
        :type tools_admin_url: str
        """
        self.__server_admin_url = server_admin_url
        self.__auth_admin_url = auth_admin_url
        self.__tools_admin_url = tools_admin_url

    @property
    def server(self):
        """
        Retrieves Server Admin object
        :return: Server Admin object
        :rtype: ServerAdmin
        """

        return ServerAdmin(self.__server_admin_url)

    @property
    def auth(self):
        """
        Retrieves Auth Admin object
        :return: Auth Admin object
        :rtype: AuthAdmin
        """

        raise AuthAdmin(self.__auth_admin_url)

    @property
    def tools(self):
        """
        Retrieves Tools Admin object
        :return:  Tools Admin object
        :rtype: ToolsAdmin
        """

        raise ToolsAdmin(self.__tools_admin_url)


class AdminGateway(Gateway):

    def __init__(self, base_url):
        """
        Initialized Admin Gateway with base url
        :param base_url: Base admin url from CONSUL
        :type base_url: str
        """

        Gateway.__init__(self, base_url, None)

    def get_server_time(self):
        """
        Retrieves time from admin server
        :return: Response to get server time request
        :rtype: Response
        """
        return self.request('admin/time').get()

    def get_catalog(self, title_code):
        """
        Retrieves catalog with specified title code
        :param title_code: Title code to retrieve catalog from
        :type title_code: str
        :return: Response to get catalog request
        :rtype: Response
        """

        return self.request('admin/catalog/{}'.format(title_code)).get()

    def service_configuration(self):
        """
        Retrieves service configurations
        :return: Response to get service configurations
        :rtype: Response
        """

        return self.request('admin/config').get()

    def service_names(self):
        """
        Retrieves a list of services in local service discovery
        :return: Response to get service names
        :rtype: Response
        """

        return self.request('admin/serviceNames').get()

    def service_discovery_info(self, service_name):
        """
        Retrieves service discovery information about specified service
        :param service_name: Service name to retrieve
        :type service_name: str
        :return: Response to get service discovery info
        :rtype: Response
        """

        return self.request('admin/services/{}'.format(service_name)).get()

    def reset_title_service_data_cache(self):
        """
        Resets and will reload the title data
        :return: Response to reset title service data cache
        :rtype: Response
        """

        return self.request('admin/resetTitleServiceDataCache').get()

    def title_all(self):
        """
        Retrieves title information in local service
        :return: Response to get title all
        :rtype: Response
        """

        return self.request('admin/title/all').get()

    def verify_emitter(self, service_chain):
        """
        Verify emitter values
        :param service_chain: List of service chains to verify
        :type service_chain: list
        :return: Response to verify emitter
        :rtype: Response
        """

        return self.request('admin/verifyEmitter').json({
            service_chain
        }).post()

    def get_build_info(self):
        """
        Retrieves build info
        :return: Response to get build info
        :rtype: Response
        """

        return self.request('buildinfo').get()

    def get_emitter(self, service_name):
        """
        Retrieves emitter for specified service
        :param service_name: Service name to retrieve emitter values
        :type service_name: str
        :return: Response to get emitter
        :rtype: Response
        """

        return self.request('admin/verifyEmitter/{}'.format(service_name)).get(RequestConstants.ContentTypes.JSON)


class AuthAdmin(AdminGateway):

    def __init__(self, base_url):
        """
        Initializes Auth Admin object
        :param base_url: Base admin url from CONSUL
        :type base_url: str
        """

        AdminGateway.__init__(self, base_url)

    def delete_session_token(self, namespace, profile_id):
        """
        Invalidate a session token from profile id
        :param namespace: Namespace of where session token is stored
        :type namespace: str
        :param profile_id: Profile id
        :type profile_id: int
        :return: Response to delete session token request
        :rtype: Response
        """

        return self.request('admin/session/{}/{}'.format(namespace, profile_id)).delete()


class ServerAdmin(AdminGateway):

    def __init__(self, base_url):
        """
        Initializes Server Admin object
        :param base_url: Base admin url from CONSUL
        :type base_url: str
        """

        AdminGateway.__init__(self, base_url)

    def http_client_test(self):
        """
        HTTP Client test
        :return: Response to HTTP client test
        :rtype: Response
        """
        return self.request('admin/http-client-test').get()


class ToolsAdmin(AdminGateway):

    def __init__(self, base_url):
        """
        Initializes Tools Admin object
        :param base_url: Base admin url from CONSUL
        :type base_url: str
        """

        AdminGateway.__init__(self, base_url)

    def title_info_by_version_id(self, version_uuid):
        """
        Retrieves title info by version id
        :param version_uuid: Version id in UUID
        :type version_uuid: str
        :return: Response to get title information by version id request
        :rtype: Response
        """

        return self.request('admin/title/versionId/{}'.format(version_uuid)).get()

    def title_info_by_server_api_key(self, server_api_key):
        """
        Retrieves title info by server api key
        :param server_api_key: Server API key
        :type server_api_key: str
        :return: Response to get title information by server API key
        :rtype: Response
        """

        return self.request('admin/title/serverApiKey/{}'.format(server_api_key)).get()

    def title_info_by_client_api_key(self, client_api_key):
        """
        Retrieves title info by client api key
        :param client_api_key: Client API key
        :type client_api_key: str
        :return: Response to get title information by client API key
        :rtype: Response
        """

        return self.request('admin/title/clientApiKey/{}'.format(client_api_key)).get()

    def title_info_by_entity_code(self, entity_code):
        """
        Retrieves title info by entity_code
        :param entity_code: Entity code specified for retrieval
        :type entity_code: str
        :return: Response to get title information by entity code
        :rtype: Response
        """

        return self.request('admin/catalog/entityCode/{}'.format(entity_code)).get()
