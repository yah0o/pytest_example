import os
import re
import sys

from environment import Environment
from integration.main.services import ConsulManager, ServerAdmin


class Version(object):
    __CACHED_CURRENT_VERSION = None
    __CONSUL_CACHE = None
    __ENV_NAME_CACHE = None

    @staticmethod
    def __get_current_version():

        is_running_xdist = len(sys.argv) == 1  # x-dist will have only one sys.arg
        if is_running_xdist:
            assert 'FREYA_VERSION' in os.environ, 'FREYA_VERSION must be set in environment variables to use xdist'
            return os.environ['FREYA_VERSION']

        if Version.__CONSUL_CACHE is None or Version.__ENV_NAME_CACHE is None:
            # this is used in annotations which run when the python is loaded up/"compiled"
            # so we have to load this up in a separate way than use the pytest definitions

            # this is called outside of the pytest initialization flow so we have to directly get the --environment
            # from the command line interface

            # redefining environment because we cannot get this from pytest because this will run completely separate
            # from the main pytest flow

            environment_argument = next((arg for arg in sys.argv if arg.startswith('--env')), None)
            assert environment_argument is not None
            env_file = environment_argument.split('=')[1]

            environment = Environment(env_file, None)
            Version.__ENV_NAME_CACHE = environment.environment_name
            Version.__CONSUL_CACHE = environment.consul

        if Version.__CACHED_CURRENT_VERSION is None:

            environment_argument = next((arg for arg in sys.argv if arg.startswith('--env')), None)
            assert environment_argument is not None
            env_file = environment_argument.split('=')[1]

            environment = Environment(env_file, None)

            admin_url = environment['url']['base']
            if environment['region'] == 'wgie' \
                    or environment['region'] == 'asia' \
                    or environment['region'] == 'eu' \
                    or environment['region'] == 'na' \
                    or environment['region'] == 'ru':
                consul = ConsulManager(Version.__CONSUL_CACHE, Version.__ENV_NAME_CACHE)

                color_argument = next((arg for arg in sys.argv if arg.startswith('--env_color')), None)
                color = color_argument.split('=')[1] if color_argument is not None else 'blue'

                admin_url = consul.get_server_admin_url(color)

            server_admin = ServerAdmin(admin_url)

            build_info_response = server_admin.get_build_info()
            build_info_response.assert_is_success()

            version = build_info_response.content['Implementation-Version']
            Version.__CACHED_CURRENT_VERSION = version.split('-')[0]

        return Version.__CACHED_CURRENT_VERSION

    @staticmethod
    def __version_compare(version1, version2):

        return cmp(Version.normalize(version1), Version.normalize(version2))

    @staticmethod
    def normalize(ver):

        return [int(x) for x in re.sub(r'[a-zA-z_-]+$', '', ver).split(".")]

    @staticmethod
    def is_before(feature_version):

        current_version = Version.__get_current_version()
        env_name = Version.__ENV_NAME_CACHE

        return {
            'condition': Version.__version_compare(feature_version, current_version) > 0,
            'reason': 'This is not ready until version {}. Current version on {} is {}'.format(feature_version,
                                                                                               env_name,
                                                                                               current_version)
        }

    @staticmethod
    def is_after(feature_version):

        current_version = Version.__get_current_version()
        env_name = Version.__ENV_NAME_CACHE

        return {
            'condition': Version.__version_compare(feature_version, current_version) <= 0,
            'reason': 'This test is no longer available on {}. Current version on {} is {}'.format(feature_version,
                                                                                                   env_name,
                                                                                                   current_version)
        }
