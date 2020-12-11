from functools import reduce

import networkx as nx
import pudb  # noqa


TARGET = "shiny_gold"


with open("input.txt") as f:
    lines = f.readlines()


def parse_bag(bag):
    num, adj, color, _ = bag.split()
    content_color = "_".join([adj, color])
    return (content_color, int(num))


def parse_line(line):
    container, contents = line.split("contain")
    adj, color, _ = container.split()
    container_color = "_".join([adj, color])
    edges = [(container_color, *parse_bag(bag)) for bag in contents.split(",")]
    return edges


def construct_graph(lines):
    G = nx.DiGraph()
    for line in filter(lambda line: "no other" not in line, lines):
        G.add_weighted_edges_from(parse_line(line))
    return G


def get_node_weight(node):
    node_weight = 0
    for neighbor in nx.neighbors(G, node):
        count = G.get_edge_data(node, neighbor).get("weight")
        node_weight += count + count * get_node_weight(neighbor)
    return node_weight


G = construct_graph(lines)
print(len(nx.ancestors(G, TARGET)))
target_node = next(filter(lambda node: node == TARGET, G.nodes()))
print(get_node_weight(target_node))
