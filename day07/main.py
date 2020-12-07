import os
import re
from functools import reduce, partial
from typing import Dict, List, Tuple


BASE_DIR = os.path.dirname(__file__)
name_pattern = re.compile(r"^(\w+ \w+)")
content_pattern = re.compile(r"(\d+) (\w+ \w+|no other bags.)")

BagName = str
RawBagOccurences = str
BagOccurences = int

BagContent = Dict[BagName, BagOccurences]
BagRules = Dict[BagName, BagContent]


def to_name(line: str) -> str:
    return re.match(name_pattern, line).group()


def to_content(line: str) -> BagContent:
    return dict(
        [
            (bag_name, int(occurences))
            for occurences, bag_name in re.findall(content_pattern, line)
        ]
    )


def build_bag_rules(data: List[str]) -> BagRules:
    """
    Example output:
        {
            "light red": {"bright white": 1, "muted yellow": 2},
            "dark orange": {"bright white": 3, "muted yellow": 4},
            "bright white": {"shiny gold": 1},
            "muted yellow": {"shiny gold": 2, "faded blue": 9},
            "shiny gold": {"dark olive": 1, "vibrant plum": 2},
            "dark olive": {"faded blue": 3, "dotted black": 4},
            "vibrant plum": {"faded blue": 5, "dotted black": 6},
            "faded blue": {},
            "dotted black": {},
        }
    """
    return dict(
        zip(
            map(to_name, data),
            map(to_content, data),
        ),
    )


def count_bags_containing_bag(bag_name: str, rules: BagRules) -> int:
    def _get_bags(bag_name: str, available_bags: set):
        bags = [bag for bag, content in rules.items() if bag_name in content]
        if not bags:
            return available_bags

        available_bags.update(bags)
        for bag in bags:
            available_bags.update(_get_bags(bag, available_bags))
        return available_bags

    return len(_get_bags(bag_name, set()))


def count_bags_inside_bag(
    bag_name: str,
    rules: BagRules,
) -> int:
    def _count_bags(bag_name: str):
        bag_content = rules[bag_name].items()
        if not bag_content:
            return 1

        return sum((amount * _count_bags(bag) for bag, amount in bag_content)) + 1

    return _count_bags(bag_name) - 1


with open(os.path.join(BASE_DIR, "data.in"), "r") as fp:
    data = list(map(str.strip, fp))
    rules = build_bag_rules(data)
    count_1 = count_bags_containing_bag(bag_name="shiny gold", rules=rules)
    count_2 = count_bags_inside_bag(bag_name="shiny gold", rules=rules)
    print("Part 1 answer:", count_1)
    print("Part 2 answer:", count_2)