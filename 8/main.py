from functools import lru_cache
from collections import defaultdict
from pyrsistent import pvector

with open("input.txt") as f:
    lines = f.readlines()

NOP = "nop"
JMP = "jmp"
ACC = "acc"


@lru_cache
def process_instruction(instruction, ptr, acc):
    """Process instruction at ptr

    return new value of ptr, acc
    """
    ins, arg = instruction.split()
    arg = int(arg)

    func_map = {
        NOP: lambda ptr, acc, x: (ptr + 1, acc),
        ACC: lambda ptr, acc, x: (ptr + 1, acc + x),
        JMP: lambda ptr, acc, x: (ptr + x, acc),
    }

    return func_map[ins](ptr, acc, arg)


def run_instructions(instructions):
    """Runs the program defined by instructions

    Return the final value of the accumulator if the program terminates.  If the
    program loops infinitely, return None.
    """
    acc = 0
    ptr = 0
    seen = defaultdict(bool)
    while True:
        if seen[ptr]:
            # program infinite loops
            return None
        seen[ptr] = True
        try:
            instruction = instructions[ptr]
        except IndexError:
            # program completed successfully
            return acc
        ptr, acc = process_instruction(instruction, ptr, acc)


def generate_flips(instructions):
    """Generate instructions with NOP or JMP flipped"""
    for i, instruction in enumerate(instructions):
        if NOP in instruction:
            yield instructions.set(i, instruction.replace(NOP, JMP))
        if JMP in instruction:
            yield instructions.set(i, instruction.replace(JMP, NOP))


instructions = pvector(map(lambda s: s.strip(), lines))
for flipped_instructions in generate_flips(instructions):
    result = run_instructions(flipped_instructions)
    if result:
        print(result)
        break
