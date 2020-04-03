import random

from .werder import get_werder_werds


def werder_name():
    return '{}-{}'.format(get_werder_werds(1)[0], int(random.uniform(0, 999)))
