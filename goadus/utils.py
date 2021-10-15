import random

from .werder import Werder


def werder_api_key():
    w = Werder()
    return "-".join([w.werd() for _ in range(4)])


def werder_name():
    w = Werder()
    return "{}-{}".format(w.werd(), int(random.uniform(0, 999)))
