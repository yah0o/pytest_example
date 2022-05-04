import os.path

from integration.main.model import Yaml
from integration.schemas.schemas import Schemas


class Environment(object):

    def __init__(self, environment_file, color):
        """
        Initializes environment object from an environment file
        :param environment_file: Name of the environment file to load
        :type environment_file: file
        :param color: Environment color, using blue/green format
        :type color: object
        """

        self.__contents = Yaml.load(environment_file)
        Schemas.validate(self.__contents.as_json(), Schemas.TEST_ENVIRONMENT)

        script_dir = os.path.dirname(environment_file)
        full_title_path = os.path.join(script_dir, self.__contents['title'])
        self.__data = Yaml.load(full_title_path)
        self.__color = color

    def __getitem__(self, item):
        """
        :param item: str 
        :return: 
        """

        return self.__contents[item]

    @property
    def color(self):

        return self.__color

    @property
    def contents(self):
        """
        :return: dict
        """

        return self.__contents

    def has(self, item):
        """
        :param item: str 
        :return: bool 
        """

        return self.__contents.has(item)

    @property
    def data(self):
        """
        :return: :py:class: `model.Object` 
        """

        return self.__data

    @property
    def title(self):
        """
        :return: str
        """
        try:
            title = self.data.TEST_TITLE.CODE
        except AttributeError:
            title = self.data.TEST_TITLE

        return title

    @property
    def db_host(self):
        """
        :return:
        """

        return self['db']['host'] if self.has('db') else None

    @property
    def db_port(self):
        """
        :return:
        """

        return self['db']['port'] if self.has('db') else None

    @property
    def db_user(self):
        """
        :return:
        """

        return self['db']['user'] if self.has('db') else None

    @property
    def db_password(self):
        """
        :return:
        """

        return self['db']['password'] if self.has('db') else None

    @property
    def environment_name(self):
        """
        :return:
        """

        return self['environment'] if self.has('environment') else None

    @property
    def consul(self):
        """
        :return:
        """

        return self['consul'] if self.has('consul') else None

    @property
    def use_consul_urls(self):
        """
        Returns true If use_consul_urls is not defined in environment config.
        :return:
        """

        return self['use_consul_urls'] if self.has('use_consul_urls') else True

    @property
    def s3_region(self):
        """
        :return:
        """

        if self.has('s3') and self['s3'].has('region'):
            return self['s3']['region']

        return None

    @property
    def s3_url(self):
        """
        :return:
        """

        if self.has('s3') and self['s3'].has('url'):
            return self['s3']['url']

        return None

    @property
    def s3_access_key(self):
        """
        :return:
        """

        if self.has('s3') and self['s3'].has('access_key'):
            return self['s3']['access_key']

        return None

    @property
    def s3_secret_key(self):
        """
        :return:
        """

        if self.has('s3') and self['s3'].has('secret_key'):
            return self['s3']['secret_key']

        return None
