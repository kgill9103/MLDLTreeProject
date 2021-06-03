import numpy as np
from sklearn.decomposition import PCA

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
    xz = arr[:, [0, 2]]
    arr = pca(xz)

    min_values = np.min(arr, axis=0)
    max_values = np.max(arr, axis=0)
    x_thickness = max_values[0] - min_values[0]
    y_thickness = max_values[1] - min_values[1]
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

def pca(X):
    # Normalizing X
    norm_X = X-X.mean(axis=0)
    norm_X = norm_X/X.std(axis=0)

    # Covariance Matrix
    cov_norm_X = np.cov(norm_X.T)

    # Correlation Matrix
    corr_norm_X = np.corrcoef(norm_X.T)

    # Eigendecomposition
    eigen_val, eigen_vec = np.linalg.eig(cov_norm_X)

    z1 = eigen_vec[:,0][0] * norm_X[:,0] + eigen_vec[:,0][1] * norm_X[:,1]
    z2 = eigen_vec[:,1][0] * norm_X[:,0] + eigen_vec[:,1][1] * norm_X[:,1]
    pca_res = np.vstack([z1,z2]).T

    return pca_res[:,:2]