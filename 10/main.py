from itertools import product
from more_itertools import windowed
from functools import lru_cache, reduce
from operator import add
from collections import deque

import networkx as nx
import pudb  # noqa

with open("input.txt") as f:
    lines = f.readlines()


def get_differences(elements):
    """Return the pairwise difference between elements as an iterator."""
    return map(lambda t: t[1] - t[0], windowed(elements, 2))


def create_graph(elements, threshold=1):
    """Create a graph connecting all elements in `elements` whose difference is
    less than `threshold`.  Edges are directed from smaller to larger element.

    `elements` must be sorted
    """
    G = nx.DiGraph()
    total_difference = 0
    leaves = deque()
    for element, difference in zip(elements, get_differences(elements)):
        # add edges
        leaf_nodes = [t[0] for t in leaves]
        G.add_edges_from(product(leaf_nodes, [element]))

        # update leaves
        leaves.append((element, difference))
        total_difference += difference
        while total_difference > threshold:
            _, difference = leaves.popleft()
            total_difference -= difference
    return G


@lru_cache
def total_unique_paths(G, source=0):
    neighbors = nx.neighbors(G, source)
    if len(list(neighbors)) == 0:
        return 1
    total_paths = 0
    for node in nx.neighbors(G, source):
        total_paths += total_unique_paths(G, node)
    return total_paths


# bag of adapters, each adapter may take input 1, 2, 3 jolts lower than rating
# device rated for 3 jolts higher than highest adapter
# outlet effective joltage 0

# outlet -> bag of adapters -> device
adapters = sorted(map(lambda line: int(line.strip()), lines))
adapters = [0] + adapters + [max(adapters) + 3]

differences = list(get_differences(adapters))
one_steps = differences.count(1)
three_steps = differences.count(3)
print(one_steps, three_steps, one_steps * three_steps)

adapter_graph = create_graph(adapters, threshold=3)
print(total_unique_paths(adapter_graph, source=0))
