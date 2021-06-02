import math
import networkx as nx
from itertools import permutations
from utils import *
from tqdm.auto import tqdm
import numpy as np

class BuildObjGraph:

    def __init__(self, x, y, z, faces, n_size=50):
        unit = self._unit(x, y, z, n_size)
        self.obj_list, self.idx_to_obj = self._vertext2voxel(x, y, z, unit)
        self.edges = self._edges(faces)
        self.graph = self._graph(self.obj_list)
        self.g = self._graph(self.obj_list)
        self.root = self._root(self.obj_list)
        self.y_len = self._y_len(y, unit)

        self._check_graph_connectivity()

        self.distance_map = self._distance_map()

    def _unit(self, x, y, z, n_size):
        units = [max(x) - min(x), max(y) - min(y), max(z) - min(z)]
        unit = n_size / max(units)
        return unit

    def _edges(self, faces):
        edges = []
        for face in faces:
            e1 = (self.idx_to_obj[face[0]], self.idx_to_obj[face[1]])
            e2 = (self.idx_to_obj[face[1]], self.idx_to_obj[face[2]])
            e3 = (self.idx_to_obj[face[2]], self.idx_to_obj[face[0]])
            edges.extend([e1, e2, e3])

        edges = set(edges)
        return edges

    def _vertext2voxel(self, x, y, z, unit):

        x_min, y_min, z_min = math.floor(min(x)*unit), math.floor(min(y)*unit), math.floor(min(z)*unit)

        obj_list = []
        idx_to_obj = dict()

        for idx, (i,j,k) in enumerate(zip(x, y, z)):
            a, b, c = round(i*unit) - x_min, round(j*unit) - y_min, round(k*unit) - z_min
            obj_list.append((a,b,c))
            idx_to_obj[idx] = (a,b,c)

        return obj_list, idx_to_obj

    def _graph(self, obj_list):
        g = nx.Graph()

        for node in obj_list:
            g.add_node(node)
        
        nodes = set(g.nodes)
        
        for edge in tqdm(self.edges):
            n1, n2 = edge
            if n1 in nodes and n2 in nodes:
                g.add_edge(n1, n2)

        return g
    
    def _root(self, obj_list):
        root_idx = np.argmin(obj_list, axis=0)[1]
        root = obj_list[root_idx]
        return root

    def _distance_map(self):
        for n in self.g.nodes:
            self.g.nodes[n]['d'] = 0
        self.g.nodes[self.root]['d'] = 1

        distance_map = dict()
        distance_map[self.root] = 0
        for node in list(nx.bfs_tree(self.g, self.root))[1:]:
            d = get_distance(self.g, node)
            self.g.nodes[node]['d'] = d
            distance_map[node] = d - 1
        return distance_map

    def _y_len(self, y, unit):
        y_min = math.floor(min(y)*unit)
        y_len = math.ceil(max(y)*unit) - y_min
        return y_len

    def _check_graph_connectivity(self):
        if not len(list(nx.bfs_tree(self.g, self.root))) == len(list(self.g.nodes)):
            raise GraphConnectionError("Graph is not connected, Please resize n_size")