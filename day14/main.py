import os
from typing import List, Iterable, Tuple
import re

BASE_DIR = os.path.dirname(__file__)

FileLine = str
InputData = List[FileLine]

# BitMask is different than MemoryMask
# as it may contain '0', '1', and 'X' while
# MemoryMask only contains '0' and '1'
BitMask = str
MemoryMask = str

MemoryAddress = int
Value = int

MASK_RE = re.compile(r"^mask = (.+)")
MEMORY_RE = re.compile(r"mem\[(\d+)\] = (\d+)")


def apply_mask_to_value(mask: BitMask, value: int) -> int:
    val_in_bin = f"{bin(value)[2:]:0>36}"
    return int(
        "".join((vb if mv == "X" else mv for vb, mv in zip(val_in_bin, mask))), 2
    )


def apply_mask_to_memory_mask(mask: BitMask, memory_mask: MemoryMask) -> BitMask:
    return "".join(
        (
            mv if mv == "X" else str(int(mv) or int(memv))
            for mv, memv in zip(mask, memory_mask)
        )
    )


def groupby_mask(data: InputData) -> Iterable[Tuple[BitMask, MemoryAddress, Value]]:
    groups = []
    for line in data:
        if line.startswith("mask"):
            groups.append([re.match(MASK_RE, line).group(1)])
        else:
            groups[-1].append(re.match(MEMORY_RE, line).groups())

    for group in groups:
        mask, *addresses = group
        for address, value in addresses:
            yield mask, int(address), int(value)


def generate_memory_addresses(
    memory_mask: MemoryMask, prefix: str = ""
) -> Iterable[MemoryAddress]:
    for idx, char in enumerate(memory_mask):
        if char == "X":
            yield from generate_memory_addresses(
                "0" + memory_mask[idx + 1 :], prefix + memory_mask[:idx]
            )
            yield from generate_memory_addresses(
                "1" + memory_mask[idx + 1 :], prefix + memory_mask[:idx]
            )
        if "X" not in prefix + memory_mask:
            yield int(prefix + memory_mask, 2)


def use_decoder_v1(data: InputData) -> int:
    memory = {}
    for mask, address, value in groupby_mask(data):
        memory[address] = apply_mask_to_value(mask, value)
    return sum(memory.values())


def use_decoder_v2(data: InputData) -> int:
    memory = {}
    for mask, address, value in groupby_mask(data):
        binary_address = f"{bin(address)[2:]:0>36}"
        memory_mask = apply_mask_to_memory_mask(mask, binary_address)
        for new_addres in generate_memory_addresses(memory_mask):
            memory[new_addres] = value
    return sum(memory.values())


with open(os.path.join(BASE_DIR, "data.in"), "r") as fp:
    data = list(map(str.strip, fp))
    v1_decoded_sum = use_decoder_v1(data)
    v2_decoded_sum = use_decoder_v2(data)
    print("Task 1 answer:", v1_decoded_sum)
    print("Task 2 answer:", v2_decoded_sum)
