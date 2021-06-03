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

def get_thickness(nodes, obj_to_real_pts):
    arr = []
    for node in nodes:
        arr.extend(obj_to_real_pts[node])
    arr = np.array(arr)
    min_values = np.min(arr, axis=0)
    max_values = np.max(arr, axis=0)
    x_thickness = max_values[0] - min_values[0] + 1
    y_thickness = max_values[2] - min_values[2] + 1
    thickness = (x_thickness * y_thickness) / 4
    return thickness

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

def convert_attributes_format(attribute_dict, attribute_name):
    changed_format = []
    for node in attribute_dict:
        t = (node, {attribute_name:attribute_dict[node]})
        changed_format.append(t)
    return changed_format