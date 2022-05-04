import random, string


class RandomUtilities(object):

    @staticmethod
    def create_unique_id_lowercase():
        # a random id that provides an (25 + 10)^10 entropy
        return ''.join(random.sample(string.ascii_lowercase + string.digits, 10))

    @staticmethod
    def create_unique_pin():
        # a random 4 characters pin
        return ''.join(random.sample(string.ascii_letters, 4))
