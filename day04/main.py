import os
from operator import add
from functools import reduce

from reader import PassportFileReader
from validators import DefaultPassportValidator, EnhancedPassportValidator


BASE_DIR = os.path.dirname(__file__)
FILE_PATH = os.path.join(BASE_DIR, "data.in")


def count_valid_passwords(validator_cls, reader):
    return reduce(add, map(validator_cls.is_valid, reader))


with open(FILE_PATH, "r") as fp:
    reader = PassportFileReader(fp)
    count = count_valid_passwords(DefaultPassportValidator(), reader)
    print(f"Part 1 count: {count}")

with open(FILE_PATH, "r") as fp:
    reader = PassportFileReader(fp)
    count = count_valid_passwords(EnhancedPassportValidator(), reader)
    print(f"Part 2 count: {count}")
