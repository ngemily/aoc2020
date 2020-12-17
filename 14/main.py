from collections import defaultdict, namedtuple, deque
from copy import copy
from itertools import product, chain
from functools import lru_cache

import re
import pudb  # noqa

Mask = namedtuple("Mask", ["and_mask", "or_mask"])

with open("input.txt") as f:
    lines = map(lambda line: line.strip(), f.readlines())


def parse_mask_instruction(instruction):
    _, mask = instruction.split(" = ")
    return mask


def parse_memory_instruction(instruction):
    address, value = instruction.split(" = ")
    address = re.match("mem\[(\d+)\]", address).groups()[0]  # noqa
    return int(address), int(value)


def process_mask_instruction1(instruction):
    # | mask for 1s (replace non-one with 0)
    # & mask for 0s (replace non-zero with 1)
    mask = parse_mask_instruction(instruction)
    or_mask = int("0b" + mask.replace("X", "0"), 2)
    and_mask = int("0b" + mask.replace("X", "1"), 2)
    return Mask(and_mask, or_mask)


def process_memory_instruction1(memory, instruction, mask):
    address, value = parse_mask_instruction(instruction)
    memory[address] = value & mask.and_mask | mask.or_mask
    return memory


def process_mask_instruction(instruction):
    return parse_mask_instruction(instruction)


def generate_addresses(acc, address):
    c = address.popleft()
    if len(address) > 0:
        if c == "X":
            yield from generate_addresses(acc + "0", copy(address))
            yield from generate_addresses(acc + "1", copy(address))
        else:
            yield from generate_addresses(acc + c, address)
    else:
        if c == "X":
            yield acc + "0"
            yield acc + "1"
        else:
            yield acc + c


def apply_mask(address, mask):
    # address: 00101010  (decimal 42)
    # mask:    00X1001X
    # result:  00X1101X
    address = bin(address)[2:]
    address = "0" * (len(mask) - len(address)) + address

    def mask_char(a, m):
        return a if m == "0" else m

    masked_address = deque(map(lambda t: mask_char(*t), zip(address, mask)))
    return masked_address


def process_memory_instruction(memory, instruction, mask):
    address, value = parse_memory_instruction(instruction)
    masked_address = apply_mask(address, mask)
    for address in generate_addresses("0b", masked_address):
        address = int(address, 2)
        memory[address] = value
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

sum = sum(memory.values())
print(sum)
if sum == 4355897790573:
    print("pass!")
