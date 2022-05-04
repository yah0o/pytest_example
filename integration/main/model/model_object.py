import json


class Object(object):

    def __init__(self, attributes, path=None):
        self._attributes = attributes
        self._path = path

    def __repr__(self):
        return json.dumps(self._attributes, indent=2)

    def __iter__(self):
        for k, v in self._attributes.iteritems():
            yield k, v

    def __getattr__(self, name):
        if name not in self._attributes:
            raise RuntimeError('Invalid Property: {0}'.format(name))

        return self.__wrap(name)

    def __getitem__(self, item):

        if isinstance(item, list):
            surveyor = self
            for arg in item:

                if isinstance(surveyor, Object) and surveyor.has(arg):
                    surveyor = surveyor[arg]
                else:
                    return None

            return surveyor

        if item not in self._attributes:
            return None

        return self.__wrap(item)

    @property
    def path(self):
        return self._path

    @property
    def request(self):
        return Object(self._attributes['__request__'])

    def as_json(self):
        return self._attributes

    def has(self, key):
        return key in self._attributes

    def stringify(self):
        return json.dumps(self._attributes)

    def __wrap(self, name):
        attribute = self._attributes[name]
        if isinstance(attribute, dict):
            return Object(self._attributes[name])

        if isinstance(attribute, list):
            return Collection(self._attributes[name])

        return self._attributes[name]


class Collection(object):

    def __init__(self, attributes):
        self._attributes = attributes

    def __repr__(self):
        return json.dumps(self._attributes, indent=2)

    def __getitem__(self, index):
        if isinstance(self._attributes[index], dict):
            return Object(self._attributes[index])

        return self._attributes[index]

    def __len__(self):
        return len(self._attributes)

    def stringify(self):
        return json.dumps(self._attributes)
