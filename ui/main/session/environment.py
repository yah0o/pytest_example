import os.path

from ui.main.model import Yaml


class Environment(object):

    def __init__(self, environment_file, color):
        """
        :param environment_file: environment file from which you want the data
        :type environment_file: str
        :param color: environment color
        :type color: str
        """

        self.__contents = Yaml.load(environment_file)

        script_dir = os.path.dirname(environment_file)
        full_title_path = os.path.join(script_dir, self.__contents['title'])
        self.__data = Yaml.load(full_title_path)
        self.__color = color

    def __getitem__(self, item):
        """
        :param item: item to retrieve
        :type item: str
        :return: item's value
        :rtype: str
        """

        return self.__contents[item]

    @property
    def color(self):
        """
        Color of the current environment
        :return: Environment color specified
        :rtype: str
        """
        return self.__color

    @property
    def contents(self):
        """
        Dictionary of the contents of the environment file
        :return: Dictionary of all key, value pairs in the environment file
        :rtype: dict
        """

        return self.__contents

    def has(self, item):
        """
        Check if the specified key is in the environment file
        :param item: Key to validate
        :type item: str
        :return: If the key is in the environment file
        :rtype: bool
        """

        return self.__contents.has(item)

    @property
    def data(self):
        """
        YAML data in the environment file
        :return: YAML formatted data
        :rtype: :py:class: `model.Object`
        """

        return self.__data

    @property
    def title(self):
        """
        Test title specified in the environment file
        :return: Name of the title used in the tests
        :rtype: str
        """

        return self.data.TEST_TITLE.CODE

    @property
    def environment_name(self):
        """
        Environment's name as specified in the environment file
        :return: Name of the environment
        :rtype: str
        """

        return self['environment'] if self.has('environment') else None
