import re
from functools import partial


RE_HGT_PATTERN = r"(^[0-9]+)(in|cm)$"
RE_HCL_PATTERN = r"^#[0-9a-f]{6}$"


def hcl_is_valid(value: str) -> bool:
    return re.match(RE_HCL_PATTERN, value) is not None


def ecl_is_valid(value: str) -> bool:
    return value in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}


def pid_is_valid(value: str) -> bool:
    return len(value) == 9 and value.isalnum()


def cid_is_valid(value: str) -> bool:
    return True


def range_is_valid(value: str, min_value: int, max_value: int) -> bool:
    return min_value <= int(value) <= max_value


byr_is_valid = partial(range_is_valid, min_value=1920, max_value=2002)
iyr_is_valid = partial(range_is_valid, min_value=2010, max_value=2020)
eyr_is_valid = partial(range_is_valid, min_value=2020, max_value=2030)
hgt_cm_is_valid = partial(range_is_valid, min_value=150, max_value=193)
hgt_in_is_valid = partial(range_is_valid, min_value=59, max_value=76)


def hgt_is_valid(value: str) -> bool:
    ranges = {"cm": hgt_cm_is_valid, "in": hgt_in_is_valid}
    match = re.match(RE_HGT_PATTERN, value)
    if not match:
        return False
    value, unit = match.groups()
    return ranges[unit](value)


def is_valid_by_basic_rules(passport) -> bool:
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


def is_valid_by_enhanced_rules(passport) -> bool:
    validators = {
        "byr": byr_is_valid,
        "iyr": iyr_is_valid,
        "eyr": eyr_is_valid,
        "hgt": hgt_is_valid,
        "hcl": hcl_is_valid,
        "ecl": ecl_is_valid,
        "pid": pid_is_valid,
        "cid": cid_is_valid,
    }
    if not is_valid_by_basic_rules(passport):
        return False
    return all((validators[key](value) for key, value in passport.items()))
