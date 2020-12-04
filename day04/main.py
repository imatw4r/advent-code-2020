import os
from operator import add
from functools import reduce

from reader import PassportFileReader
from validators import is_valid_by_basic_rules, is_valid_by_enhanced_rules


BASE_DIR = os.path.dirname(__file__)
FILE_PATH = os.path.join(BASE_DIR, "data.in")


def count_valid_passwords(is_valid, reader):
    return reduce(add, map(is_valid, reader))


with open(FILE_PATH, "r") as fp:
    reader = PassportFileReader(fp)
    count = count_valid_passwords(is_valid_by_basic_rules, reader)
    print(f"Part 1 count: {count}")

with open(FILE_PATH, "r") as fp:
    reader = PassportFileReader(fp)
    count = count_valid_passwords(is_valid_by_enhanced_rules, reader)
    print(f"Part 2 count: {count}")
