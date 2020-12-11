from collections import defaultdict
from pyrsistent import pvector

with open("input.txt") as f:
    lines = f.readlines()


def process_instruction(instructions, ptr, acc):
    """Process instruction at ptr

    return new value of ptr, acc
    """
    ins, arg = instructions[ptr].split()
    arg = int(arg)

    func_map = {
        "nop": lambda ptr, acc, x: (ptr + 1, acc),
        "acc": lambda ptr, acc, x: (ptr + 1, acc + x),
        "jmp": lambda ptr, acc, x: (ptr + x, acc),
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
            print(acc)
            return None
        seen[ptr] = True
        if ptr >= len(instructions):
            return acc
        ptr, acc = process_instruction(instructions, ptr, acc)


instructions = pvector(map(lambda s: s.strip(), lines))
print(run_instructions(instructions))
