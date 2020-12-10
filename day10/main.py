from collections import defaultdict
import os


BASE_DIR = os.path.dirname(__file__)

memory = {}


def build_chain(source_joltage, adapters):
    adapters_used = defaultdict(int)
    for adapter_joltage in adapters:
        power = adapter_joltage - source_joltage
        assert power <= 3, "Can't amplify source joltage by more than 3!"
        source_joltage += power
        adapters_used[power] += 1
    # We have to add one extra adapter as in description:
    #       In addition, your device has a built-in joltage adapter
    #       rated for 3 jolts higher than the highest-rated adapter
    #       in your bag.

    adapters_used[3] += 1
    return source_joltage, adapters_used


def distinct_arrangement_count(source_joltage, adapters, destination_joltage):
    if source_joltage in memory:
        return memory[source_joltage]

    if source_joltage == destination_joltage:
        return 1

    if not adapters:
        return 0

    sum_ = 0
    for idx, adapter_joltage in enumerate(adapters):
        joltage_diff = adapter_joltage - source_joltage
        if joltage_diff > 3:
            break
        sum_ += distinct_arrangement_count(
            adapter_joltage, adapters[idx + 1 :], destination_joltage
        )
    memory[source_joltage] = sum_
    return sum_


with open(os.path.join(BASE_DIR, "data.in"), "r") as fp:
    data = sorted(map(int, map(str.strip, fp)))
    source_joltage = 0
    new_joltage, adapters_used = build_chain(source_joltage, adapters=data)
    count_1 = adapters_used[1] * adapters_used[3]
    count_2 = distinct_arrangement_count(
        source_joltage=0, adapters=data, destination_joltage=new_joltage
    )
    print("Task 1 answer:", count_1)
    print("Task 2 answer:", count_2)


"""
Adapters: 1, 4, 5, 6, 7, 10, 11

0, 1, 4, 5, 6, 7, 10, 11
0, 1, 4, 6, 7, 10, 11,
0, 1, 4, 7, 10, 11 

(0) [1],                  # 0
  (1), [4],               # 0, 1
    (4), [5, 6, 7],       # 0, 1, 4
      (5) [6, 7],         # 0, 1, 4, 5
        (6) [7]           # 0, 1, 4, 5, 6
          (7) [10]        # 0, 1, 4, 5, 6, 7
            (10) [11]     # 0, 1, 4, 5, 6, 7, 10
              (11) 0      # 0, 1, 4, 5, 6, 7, 10, 11
        (7) [10]          # 0, 1, 4, 5, 7
          (10) [11]       # 0, 1, 4, 5, 7, 10
            (11) 0        # 0, 1, 4, 5, 7, 10, 11
      (6) [7]             # 0, 1, 4, 6
        (7) [10]          # 0, 1, 4, 6, 7
          (10) [11]       # 0, 1, 4, 6, 7, 10
            (11) 0        # 0, 1, 4, 6, 7, 10, 11
      (7) [10]            # 0, 1, 4, 7
          (10) [11]       # 0, 1, 4, 7, 10
            (11) 0        # 0, 1, 4, 7, 10, 11


(0), 1, 4, 5, 6, 7, 10, 11, 12
(0), 1, 4, 5, 6, 7, 10, 12
(0), 1, 4, 5, 7, 10, 11, 12
(0), 1, 4, 5, 7, 10, 12,
(0), 1, 4, 6, 7, 10, 11, 12
(0), 1, 4, 6, 7, 10, 12, # 15, 16, 19, (22)
(0), 1, 4, 7, 10, 11, 12,# 15, 16, 19, (22)
(0), 1, 4, 7, 10, 12,#  15, 16, 19, (22)
"""
