from pyrsistent import pmap
from utils.utils import Point4D

import pudb  # noqa


def is_active(elem):
    return elem == "#"


def is_inactive(elem):
    return elem == "."


with open("input.txt") as f:
    lines = map(lambda line: line.strip(), f.readlines())


def initialize(rows):
    d = dict()
    for i, row in enumerate(rows):
        for j, c in enumerate(row):
            p = Point4D(i, j, 0, 0)
            d[p] = True if is_active(c) else False
    return pmap(d)


def expand(field):
    d = field
    for location in field.keys():
        for neighbor in location.neighbors():
            d = d.set(neighbor, field.get(neighbor, False))
    assert sum(d.values()) == sum(field.values())
    return d


def update(field):

    # If a cube is active and exactly 2 or 3 of its neighbors are also active,
    # the cube remains active. Otherwise, the cube becomes inactive.
    # If a cube is inactive but exactly 3 of its neighbors are active,
    # the cube becomes active. Otherwise, the cube remains inactive.

    d = field
    for location, elem in field.items():
        active_neighbors = sum(
            [field.get(neighbor, False) for neighbor in location.neighbors()]
        )
        if elem:
            if not (active_neighbors == 2 or active_neighbors == 3):
                # become inactive
                d = d.set(location, False)
        else:
            if active_neighbors == 3:
                # become active
                d = d.set(location, True)
    return d


d = initialize(lines)
print(min(d.keys()), max(d.keys()))
print(sum(d.values()))

for i in range(4):
    d = expand(d)
    d = update(d)
    print(i, sum(d.values()))
