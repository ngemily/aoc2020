from collections import defaultdict
from pyrsistent import pvector

with open("input.txt") as f:
    lines = f.readlines()

NOP = "nop"
JMP = "jmp"
ACC = "acc"


def process_instruction(instructions, ptr, acc):
    """Process instruction at ptr

    return new value of ptr, acc
    """
    ins, arg = instructions[ptr].split()
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
            return None
        seen[ptr] = True
        if ptr >= len(instructions):
            return acc
        ptr, acc = process_instruction(instructions, ptr, acc)


instructions = pvector(map(lambda s: s.strip(), lines))
for i, instruction in enumerate(instructions):
    if NOP in instruction:
        result = run_instructions(instructions.set(i, instruction.replace(NOP, JMP)))
        if result:
            print(result)
            break
    elif JMP in instruction:
        result = run_instructions(instructions.set(i, instruction.replace(JMP, NOP)))
        if result:
            print(result)
            break
