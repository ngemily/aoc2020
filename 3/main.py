from collections import namedtuple
from itertools import cycle
from functools import reduce
from more_itertools import consume

import pudb  # noqa

with open("input.txt") as f:
    lines = f.readlines()


Slope = namedtuple("Slope", ["across", "down"])


SLOPES = [
    Slope(1, 1),
    Slope(3, 1),
    Slope(5, 1),
    Slope(7, 1),
    Slope(1, 2),
]


def print_tree_field(tree_field):
    for row in tree_field:
        consume(row, 3)
        for i in range(30):
            print(next(row), end="")
        print()


def get_tree_field():
    rows = map(lambda line: line.strip(), lines)
    tree_field = map(lambda row: cycle(row), rows)
    return tree_field


def is_tree(s):
    return s == "#"


def walk(tree_field, slope=Slope(1, 1)):
    i = 0
    next(tree_field)
    while True:
        try:
            consume(tree_field, slope.down - 1)
            row = next(tree_field)
            consume(row, slope.across * (i + 1))
            i += 1
            yield next(row)
        except StopIteration:
            break


def check_slope(slope):
    tree_field = get_tree_field()
    num_trees = reduce(lambda acc, s: acc + is_tree(s), walk(tree_field, slope), 0)
    print(num_trees)
    return num_trees


product = reduce(lambda acc, slope: acc * check_slope(slope), SLOPES, 1)
print(product)
