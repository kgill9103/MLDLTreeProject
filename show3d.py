import matplotlib.pyplot as plt
import networkx as nx
import json
import ast

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

for edge in result.edges:
    ax.plot(*zip(*edge), 'ro-')

plt.show()