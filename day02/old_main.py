import os
from collections import namedtuple, Counter


BASE_DIR = os.path.dirname(__file__)

PasswordPolicy = namedtuple("PasswordPolicy", "min, max, letter")
Password = namedtuple("Password", "value, policy")


def to_password(line):
    range_, letter, password = line.split(" ")
    min_, max_ = range_.split("-")
    policy = PasswordPolicy(int(min_), int(max_), letter.strip(":"))
    password = Password(password.rstrip(), policy)
    return password


def is_valid(password: Password):
    """
    Validate policy according to 1st task
    """
    policy = password.policy
    count = Counter(password.value)

    return policy.min <= count.get(policy.letter, -1) <= policy.max


def is_valid2(password: Password):
    """
    Validate policy according to 2nd task
    """
    policy = password.policy
    value = password.value
    password_letters = [value[policy.min - 1], value[policy.max - 1]]
    return policy.letter in password_letters and len(set(password_letters)) == 2


with open(os.path.join(BASE_DIR, "data.in"), "r") as fp:
    data = list(map(to_password, fp.readlines()))
    print("Part 1 count:", sum(map(is_valid, data)))
    print("Part 2 count:", sum(map(is_valid2, data)))