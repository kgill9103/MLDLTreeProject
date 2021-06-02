import numpy as np

class GraphConnectionError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

def get_center_node(nodes):
    ls = []
    for n in nodes:
        ls.append(np.array(n))
    arr = np.array(ls)
    arr = np.mean(arr, axis=0, dtype=int)
    return tuple(arr)

def tuple_distance(a, b):
    arr_a = np.array(a)
    arr_b = np.array(b)
    return np.linalg.norm(arr_a-arr_b)

def get_distance(g, node, key='d'):
    min = np.inf
    nodes = g.nodes
    for n in g.neighbors(node):
        v = nodes[n][key]
        if v > 0:
            v += tuple_distance(node, n)
            if v < min:
                min = v
    return min