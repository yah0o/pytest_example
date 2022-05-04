import json

from integration.main.request import RequestBuilder, RequestConstants


class ConsulManager(object):

    def __init__(self, base_ip, env_name):
        self.__base_ip = base_ip
        self.__env_name = env_name

    def get_url(self, service_name, env_color):
        data_url = '{}/v1/health/service/{}'.format(self.__base_ip, service_name)

        response = RequestBuilder(data_url).headers({
            'Content-Type': 'application/json'
        }).params({
            'passing': 'true'
        }).get()
        response.assert_is_success()

        consul_data = response.content

        admin = next((node for node in consul_data
                      if node['Service']['Service'] == service_name and
                      self.__env_name in node['Service']['Tags'] and
                      env_color in node['Service']['Tags']), None)

        assert admin, 'Couldn\'t get info for {}-{} in consul data [{}/v1/health/service/{}] -> data: {}'.format(
            env_color,
            self.__env_name,
            self.__base_ip,
            service_name,
            json.dumps(consul_data, indent=4)
        )

        # us4 check is a hack because us4 connects to the node address instead of the service address
        address = admin['Service']['Address'] if 'us4' not in admin['Service']['ID'] else admin['Node']['Address']
        port = admin['Service']['Port']

        return 'http://{}:{}/'.format(address, port)

    def get_auth_admin_url(self, env_color):
        return self.get_url('gateway-auth-service-admin', env_color)

    def get_server_admin_url(self, env_color):
        return self.get_url('gateway-server-service-admin', env_color)

    def get_tools_admin_url(self, env_color):
        return self.get_url('tools-service-admin', env_color)

    def get_kv(self, key, token=RequestConstants.Parameters.OPTIONAL):
        """
        Get consul value for given key

        :param key: Key for which you want the value
        :type key: str
        :return: Value of the requested key
        :rtype: str
        """
        return RequestBuilder('{}/v1/kv/{}?raw'.format(self.__base_ip, key)).headers({
            'X-Consul-Token': token}).get()
