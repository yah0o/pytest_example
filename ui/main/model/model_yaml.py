import yaml

from ui.main.model import Object


class Yaml(Object):

    @staticmethod
    def load(path):
        with open(path, 'r') as content:
            return Object(yaml.load(content), path=path)

    @staticmethod
    def parse(content):
        return Object(yaml.load(content))
