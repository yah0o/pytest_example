import random
import time
from uuid import uuid4


def generate_unixtime_based_string(cut_symbols_from_beginning=8):
    return str(int(time.time() * 1000))[cut_symbols_from_beginning:]


def cid():
    """Google client id. Format: str (uuid)"""
    return str(uuid4())


def tid():
    """Google account identifier. Format: str (UA-XXXX-X)"""
    return 'UA-{}-{}'.format(random.randint(1000, 100000), random.randint(0, 10))


def generate_random_int32():
    return random.randint(0, 2147483647)


def random_transaction_id():
    return str(uuid4())
