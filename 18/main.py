from operator import add, mul
from collections import deque

import pudb  # noqa

with open("input.txt") as f:
    lines = map(lambda line: line.strip(), f.readlines())


def compute(expr):
    c = deque()
    value = 0
    op = add

    for token in expr.replace(" ", ""):
        if token == "+":
            op = add
        elif token == "*":
            op = mul
        elif token == "(":
            c.append((value, op))
            value = 0
            op = add
        elif token == ")":
            popped_value, popped_op = c.pop()
            value = popped_op(popped_value, value)
        else:
            value = op(value, int(token))
    return value


print(sum(map(lambda line: compute(line), lines)))
