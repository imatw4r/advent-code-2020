import os
import re
from functools import reduce
from typing import Dict, List, Tuple


BASE_DIR = os.path.dirname(__file__)
NAME_PATTERN = re.compile(r"^(\w+ \w+)")
CONTENT_PATTERN = re.compile(r"(\d+) (\w+ \w+|no other bags.)")

BagName = str
RawBagOccurences = str
BagOccurences = int

BagContent = Dict[BagName, BagOccurences]
BagRules = Dict[BagName, BagContent]


def to_name(line: str) -> str:
    return re.match(NAME_PATTERN, line).group()


def to_content(line: str) -> BagContent:
    return dict(
        [
            (bag_name, int(occurences))
            for occurences, bag_name in re.findall(CONTENT_PATTERN, line)
        ]
    )


def build_bag_rules(data: List[str]) -> BagRules:
    """
    Input:
        [
            "light red bags contain 1 bright white bag, 2 muted yellow bags.",
            "dark orange bags contain 3 bright white bags, 4 muted yellow bags.",
            "bright white bags contain 1 shiny gold bag.",
            "muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.",
            "shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.",
            "dark olive bags contain 3 faded blue bags, 4 dotted black bags.",
            "vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.",
            "faded blue bags contain no other bags.",
            "dotted black bags contain no other bags.",
        ]


    Output:
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
    def _get_bags(bag_name: str) -> List[str]:
        matching_bags = [bag for bag, content in rules.items() if bag_name in content]
        for bag in matching_bags:
            yield from _get_bags(bag)
        yield matching_bags

    return len(reduce(set.union, map(set, _get_bags(bag_name))))


def count_bags_inside_bag(
    bag_name: str,
    rules: BagRules,
) -> int:
    def _count_bags(bag_name: str):
        bag_content = rules[bag_name].items()
        if not bag_content:
            return 1

        return sum((amount * _count_bags(bag) for bag, amount in bag_content)) + 1

    # We have to subtract one to not count the bag itself.
    return _count_bags(bag_name) - 1


with open(os.path.join(BASE_DIR, "data.in"), "r") as fp:
    data = list(map(str.strip, fp))
    rules = build_bag_rules(data)
    bag_name = "shiny gold"
    count_1 = count_bags_containing_bag(bag_name=bag_name, rules=rules)
    count_2 = count_bags_inside_bag(bag_name=bag_name, rules=rules)
    print(f"Number of bags that can contain {bag_name!r} bag:", count_1)
    print(f"Number of bags inside {bag_name!r} bag:", count_2)