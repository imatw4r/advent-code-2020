import os
from collections import namedtuple
import re
from functools import partial

BASE_DIR = os.path.dirname(__file__)

PasswordPolicy = namedtuple("PasswordPolicy", "left_value, right_value, char")
Password = namedtuple("Password", "value, policy")

RE_POLICY_PATTERN = r"([0-9]+)-([0-9]+) ([a-z]{1})"


def is_valid_by_default_policy(password: Password) -> bool:
    policy = password.policy
    return policy.left_value <= password.value.count(policy.char) <= policy.right_value


def is_valid_by_enhanced_policy(password: Password) -> bool:
    policy = password.policy
    pos_1 = slice(policy.left_value - 1, policy.left_value)
    pos_2 = slice(policy.right_value - 1, policy.right_value)
    value = password.value
    hits = sum((value[pos_1] == policy.char, value[pos_2] == policy.char))
    return hits == 1


def to_password(line: str) -> Password:
    policy, password = line.split(": ")
    min_, max_, char = re.match(RE_POLICY_PATTERN, policy).groups()
    return Password(password.strip(), PasswordPolicy(int(min_), int(max_), char))


with open(os.path.join(BASE_DIR, "data.in"), "r") as fp:
    data = list(map(to_password, fp.readlines()))
    print("Part 1 count:", sum(map(is_valid_by_default_policy, data)))
    print("Part 2 count:", sum(map(is_valid_by_enhanced_policy, data)))