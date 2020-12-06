import os
from itertools import takewhile, dropwhile
from functools import reduce
from typing import List

BASE_DIR = os.path.dirname(__file__)


# Each set represents Passenger answers
# Example:
#   "ayz" -> {"a", "y", "z"}
#   "dzy" -> {"d", "z", "y"}
PassengerAnswers = set

# Each Group is a list of Passenger answers
# Example:
#   ayz
#   dzy
#
#   => [{"a", "y", "z"}, {"d", "z", "y"}]
PassengerGroup = List[PassengerAnswers]


def to_groups(acc: List[PassengerGroup], val: str) -> List[PassengerGroup]:
    if val == "":
        acc.append([])
    else:
        acc[-1].append(set(val))
    return acc


with open(os.path.join(BASE_DIR, "data.in"), "r") as fp:
    data = list(map(str.strip, fp))
    groups: List[PassengerGroup] = reduce(to_groups, data, [[]])
    count_1 = sum(map(len, (reduce(set.union, group) for group in groups)))
    count_2 = sum(map(len, (reduce(set.intersection, group) for group in groups)))
    print("Part 1 answer:", count_1)
    print("Part 2 answer:", count_2)
