import random
import string


class Parameters(object):
    class RandomInt(object):

        def __init__(self, minimum, maximum):
            self.min = minimum
            self.max = maximum

    class RandomStr(object):

        def __init__(self, length, character_set=None):
            self.character_set = character_set if character_set is not None else string.ascii_uppercase + string.ascii_lowercase + string.digits
            self.length = length

    @staticmethod
    def evaluate(parameter):

        if parameter.__class__ == Parameters.RandomInt:
            return random.randint(parameter.min, parameter.max)
        if parameter.__class__ == Parameters.RandomStr:
            return ''.join(random.choice(parameter.character_set) for _ in range(parameter.length))
        return parameter
