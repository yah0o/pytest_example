import StringIO
import requests

from admin import AdminAccount
from environment import Environment
from integration.main.helpers import log
from integration.main.patterns import Singleton
from integration.main.services import Freya, Psa, Spa, Wgw
from integration.main.services.banw import Banw
from integration.main.services.cats import Cats


class Store(object):
    """
    Storage of instance test references
    """

    def __str__(self):
        """
        For debugging purposes
        :return: Value associated with stored key
        :rtype: str
        """

        output = StringIO.StringIO()
        for k, v in self.__dict__.iteritems():
            output.write('config.store - {}: str({})\n'.format(k, str(v)))
        return output.getvalue()

    def __contains__(self, key):
        return self.__dict__.__contains__(key)


class ConfigAdapter(object):
    # needs to be a singleton because persistent test session data is stored here
    __metaclass__ = Singleton

    __slots__ = ['reset_store', 'store', 'admin', 'freya', 'psa', 'spa', 'wgw', 'data', 'environment', 'log', 'session',
                 'region', 'cats', 'banw']

    def __init__(self, environment_file, username, password, pin, secret_key, name, env_color=None):
        self.admin = AdminAccount(username, password, pin, secret_key, name)
        self.log = log
        self.session = requests.Session()
        self.environment = Environment(environment_file, env_color if env_color is not None else 'blue')
        self.data = self.environment.data
        self.store = Store()

        self.freya = Freya(
            self.environment['url']['base'],
            str(self.environment['api']['key']),
            session=self.session,
            service_domains=self.environment['url']['services'].as_json() if self.environment['url'].has(
                'services') else {}
        )

        self.region = self.environment['region']

        self.psa = Psa(
            self.environment['psa']['http']['host']
        )

        self.cats = Cats(
            self.environment['cats']['http']['host']
        )

        self.spa = Spa(
            self.environment['spa']['http']['host']
        )

        self.banw = Banw(
            self.environment['banw']['http']['host']
        )

        if self.environment['wgw'] is not None:
            # wgw is not on all environment, initialize Wgw object if environment has wgw
            self.wgw = Wgw(
                self.environment['wgw']['http']['host']
            )

    def reset_store(self):
        self.store = Store()
