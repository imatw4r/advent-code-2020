import os
from typing import List
from collections import namedtuple


BASE_DIR = os.path.dirname(__file__)

TREE_CHAR = "#"

Position = namedtuple("Position", "x, y")
MapPoint = namedtuple("MapPoint", "value, x, y")


class FoldedMap(object):
    def __init__(self, raw_map: List[str]):
        self.raw_map = raw_map
        self.height = len(raw_map)
        self.width = len(raw_map[0])

    def __getitem__(self, position: Position) -> MapPoint:
        value = self.raw_map[position.x % self.height][position.y % self.width]
        return MapPoint(value, position.x, position.y)


def make_stepper(x_delta, y_delta):
    def stepper(position: Position):
        return Position(position.x + x_delta, position.y + y_delta)

    return stepper


# X = down, Y = right

default_step = make_stepper(1, 3)
step_1_1 = make_stepper(1, 1)
step_1_5 = make_stepper(1, 5)
step_1_7 = make_stepper(1, 7)
step_2_1 = make_stepper(2, 1)


def get_visited_points(folded_map: FoldedMap, step_strategy=default_step):
    position = Position(0, 0)
    while position.x < folded_map.height:
        yield folded_map[position]
        position = step_strategy(position)


def count_trees(folded_map: FoldedMap, step_strategy=default_step):
    def is_tree(point: MapPoint):
        return point.value == TREE_CHAR

    visited_points = get_visited_points(folded_map, step_strategy)
    return len(list(filter(is_tree, visited_points)))


with open(os.path.join(BASE_DIR, "data.in"), "r") as fp:
    folded_map = FoldedMap(list(map(str.strip, fp.readlines())))
    print("Part 1 count:", count_trees(folded_map, step_strategy=default_step))

    mul = 1
    for step in [default_step, step_1_1, step_1_5, step_1_7, step_2_1]:
        mul *= count_trees(folded_map, step)
    print("Part 2 count:", mul)
