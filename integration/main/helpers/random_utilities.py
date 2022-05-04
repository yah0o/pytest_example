import random
import string


class RandomUtilities(object):

    @staticmethod
    def create_unique_id():
        # a random id that provides an (25 + 10)^12 entropy
        return ''.join(random.sample(string.lowercase + string.digits, 12))

    @staticmethod
    def create_unique_pin():
        # a random 4 characters pin
        return ''.join(random.sample(string.lowercase, 4))
