import os
from collections import defaultdict
import re


def to_passport(data: str) -> dict:
    return dict((element.split(":") for element in (" ").join(data).split(" ")))


def byr_validator(value):
    return value.isalnum() and 1920 <= int(value) <= 2002


def iyr_validator(value):
    return value.isalnum() and 2010 <= int(value) <= 2020


def eyr_validator(value):
    return value.isalnum() and 2020 <= int(value) <= 2030


def hgt_validator(value):
    ranges = {"cm": range(150, 194), "in": range(59, 77)}
    match = re.match(r"(^[0-9]+)(in|cm)$", value)
    if not match:
        return False
    value, unit = match.groups()
    return int(value) in ranges[unit]


def hcl_validator(value):
    return len(value) == 7 and re.match(r"^#[0-9a-f]{6}", value) is not None


def ecl_validator(value):
    return value in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}


def pid_validator(value):
    return len(value) == 9 and value.isalnum()


def cid_validator(value):
    return True


def is_valid(passport):
    required_fields = {
        "byr",
        "iyr",
        "eyr",
        "hgt",
        "hcl",
        "ecl",
        "pid",
    }
    return required_fields.issubset(set(passport.keys()))


def is_valid2(passport):
    validators = {
        "byr": byr_validator,
        "iyr": iyr_validator,
        "eyr": eyr_validator,
        "hgt": hgt_validator,
        "hcl": hcl_validator,
        "ecl": ecl_validator,
        "pid": pid_validator,
        "cid": cid_validator,
    }
    if not is_valid(passport):
        return False

    return all((validators[key](value) for key, value in passport.items()))


BASE_DIR = os.path.dirname(__file__)
FILE_PATH = os.path.join(BASE_DIR, "data.in")


with open(FILE_PATH, "r") as fp:
    data = defaultdict(list)
    i = 0
    for line in fp:
        if line != "\n":
            data[i].append(line)
        else:
            i += 1

    passports = list(map(to_passport, data.values()))
    print(sum(map(is_valid, passports)))
    print(sum(map(is_valid2, passports)))
