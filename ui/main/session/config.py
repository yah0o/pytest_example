import StringIO

import requests

from environment import Environment
from integration.main.services import Freya
from ui.main.logger import log
from ui.main.patterns import Singleton
from ui.main.session import AdminAccount


class Store(object):
    """
    """

    def __str__(self):
        """
        String out put of the current values in the store object
        :return: stringified data
        :rtype: str
        """

        output = StringIO.StringIO()
        for k, v in self.__dict__.iteritems():
            output.write('config.store - {}: str({})\n'.format(k, str(v)))
        return output.getvalue()


class ConfigAdapter(object):
    # needs to be a singleton because persistent test session data is stored here
    __metaclass__ = Singleton

    __slots__ = ['reset_store', 'store', 'admin', 'freya', 'data', 'environment', 'log', 'session']

    def __init__(self, environment_file, username, password, pin, secret_key, env_color=None):
        self.admin = AdminAccount(username, password, pin, secret_key)
        self.log = log
        self.session = requests.Session()
        self.environment = Environment(environment_file, env_color if env_color is not None else 'blue')
        self.data = self.environment.data
        self.store = Store()

        self.freya = Freya(
            self.environment['services_url']['base'],
            str(self.environment['api_key']),
            session=self.session,
            service_domains=self.environment['services_url']['services'].as_json() if self.environment[
                'services_url'].has('services') else {}
        )

    def reset_store(self):
        """
        Resets the store object saved in config
        """
        self.store = Store()
