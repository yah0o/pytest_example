import json

from model_object import Object


class Json(object):

    @staticmethod
    def load(path):
        with open(path, 'r') as content:
            return Object(json.load(content))

    @staticmethod
    def parse(content):
        return Object(json.loads(content if content is not None else '{}'))

    @staticmethod
    def save(path, js):
        with open(path, 'w') as content:
            json.dump(js, content, indent=2)
