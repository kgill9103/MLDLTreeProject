import matplotlib.pyplot as plt
import networkx as nx
import json
import ast
import numpy as np
import argparse, sys

def main(argv):

    parser=argparse.ArgumentParser()

    parser.add_argument('--only_node', help='Draw only node. Write T or F')

    args=parser.parse_args()

    result = nx.Graph()

    with open('result3d.txt', 'r') as f:
        nodes = f.readline()
        nodes = ast.literal_eval(nodes)
        result.add_nodes_from(nodes)

        edges = f.readline()
        edges = ast.literal_eval(edges)
        result.add_edges_from(edges)

    fig = plt.figure()
    ax = plt.axes(projection='3d')

    ax.scatter(*zip(*list(result.nodes)), s=1)

    only_node = 'F'
    if args.only_node is not None:
        only_node = args.only_node.upper()
    if only_node == 'F':
        for edge in result.edges:
            ax.plot(*zip(*edge), 'ro-')

    plt.show()

if __name__ == "__main__":
    main(sys.argv)