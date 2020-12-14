from collections import defaultdict, namedtuple

import re
import pudb  # noqa

Mask = namedtuple("Mask", ["and_mask", "or_mask"])

with open("input.txt") as f:
    lines = map(lambda line: line.strip(), f.readlines())


def process_mask_instruction(instruction):
    # | mask for 1s (replace non-one with 0)
    # & mask for 0s (replace non-zero with 1)
    _, mask = instruction.split(" = ")
    or_mask = int("0b" + mask.replace("X", "0"), 2)
    and_mask = int("0b" + mask.replace("X", "1"), 2)
    return Mask(and_mask, or_mask)


def process_memory_instruction(memory, instruction, mask):
    address, value = instruction.split(" = ")
    address = re.match("mem\[(\d+)\]", address).groups()[0]  # noqa
    memory[int(address)] = int(value) & mask.and_mask | mask.or_mask
    return memory


def process_instruction(memory, instruction, mask):
    if "mask" in instruction:
        mask = process_mask_instruction(instruction)
    elif "mem" in instruction:
        memory = process_memory_instruction(memory, instruction, mask)
    else:
        raise ValueError
    return memory, mask


memory = defaultdict(int)
mask = Mask(0, 0)
for instruction in lines:
    memory, mask = process_instruction(memory, instruction, mask)

print(sum(memory.values()))
