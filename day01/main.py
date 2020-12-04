import os

BASE_DIR = os.path.dirname(__file__)


def calculate(data):
    for i in range(0, len(data)):
        for j in range(i, len(data)):
            v1, v2 = data[i], data[j]
            if v1 + v2 == 2020:
                return v1 * v2


def calculate2(data):
    for i in range(0, len(data)):
        for j in range(i, len(data)):
            for k in range(j, len(data)):
                v1, v2, v3 = data[i], data[j], data[k]
                if v1 + v2 + v3 == 2020:
                    return v1 * v2 * v3


with open(os.path.join(BASE_DIR, "data.in"), "r") as fp:
    data = list(map(int, fp.readlines()))
    print("Part 1 count:", calculate(data))
    print("Part 2 count:", calculate2(data))
