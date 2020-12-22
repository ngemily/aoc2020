from copy import copy
from itertools import product, combinations
from utils.utils import chunker
from collections import defaultdict
from toolz.curried import pipe, reduce, valfilter
from operator import mul

import re


class Tile:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return str(self.data)

    def bottom_edge(self):
        yield self.data[-1]

    def edges(self):
        yield self.data[0]
        yield "".join([r[0] for r in self.data])
        yield "".join([r[-1] for r in self.data])
        yield self.data[-1]
        yield "".join(reversed(self.data[0]))
        yield "".join(reversed(self.data[-1]))
        yield "".join(reversed([r[0] for r in self.data]))
        yield "".join(reversed([r[-1] for r in self.data]))


with open("input.txt") as f:
    lines = map(lambda line: line.strip(), f.readlines())


def parse_tiles(lines):
    tiles = dict()
    for chunk in chunker(lines):
        tile_id = chunk.pop(0)
        tile_id = int(re.match("Tile (\d+):", tile_id).groups()[0])  # noqa
        tiles[tile_id] = Tile(copy(chunk))
    return tiles


def tiles_match(t1, t2):
    """
    Checks if there exists any orientation of tile t1 and tile 2 such that
    they share a matching edge.
    """
    for e1, e2 in product(t1.edges(), t2.edges()):
        if e1 == e2:
            return True
    return False


tiles = parse_tiles(lines)
matches = defaultdict(bool)
for tid1, tid2 in combinations(tiles.keys(), 2):
    if tiles_match(tiles[tid1], tiles[tid2]):
        matches[tid1] += 1
        matches[tid2] += 1


corner_ids = pipe(matches, valfilter(lambda x: x == 2), dict.keys)
assert len(corner_ids) == 4
print(reduce(mul, corner_ids))
