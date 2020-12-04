import os
from collections import namedtuple

BASE_DIR = os.path.dirname(__file__)
TREE_CHAR = "#"

Position = namedtuple("Position", "x, y")


def make_stepper(x_delta, y_delta):
    def stepper(position: Position):
        return Position(position.x + x_delta, position.y + y_delta)

    return stepper


# X = down, Y = right
default_step = make_stepper(x_delta=1, y_delta=3)
step_1_1 = make_stepper(x_delta=1, y_delta=1)
step_1_5 = make_stepper(x_delta=1, y_delta=5)
step_1_7 = make_stepper(x_delta=1, y_delta=7)
step_2_1 = make_stepper(x_delta=2, y_delta=1)


def count_trees(data, step_strategy=default_step):
    position = Position(0, 0)
    width, height = len(data[0]), len(data)
    count = 0
    while position.x < height:
        if data[position.x % height][position.y % width] == TREE_CHAR:
            count += 1

        position = step_strategy(position)
    return count


with open(os.path.join(BASE_DIR, "data.in"), "r") as fp:
    data = list(map(str.strip, fp.readlines()))
    # Part 1
    print("Part 1 count:", count_trees(data, default_step))

    # Part 2
    m = 1
    for step in [default_step, step_1_1, step_1_5, step_1_7, step_2_1]:
        m *= count_trees(data, step)

    print("Part 2 count:", m)