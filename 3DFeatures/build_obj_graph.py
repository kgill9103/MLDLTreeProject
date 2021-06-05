import math
import networkx as nx
from itertools import permutations
from utils import *
from tqdm.auto import tqdm
import numpy as np
from sklearn.neighbors import KDTree, BallTree

class BuildObjGraph:

    def __init__(self, x, y, z, faces, pairs=None, n_size=50):
        unit = self._unit(x, y, z, n_size)
        self.obj_list, self.idx_to_obj, self.obj_to_real_pts = self._vertext2voxel(x, y, z, unit)
        self.edges = self._edges(faces) if pairs is None else self._edges_from_pair(pairs)
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
    
    def _edges_from_pair(self, pairs):
        edges = []
        for pair in pairs:
            edge = (self.idx_to_obj[pair[0]], self.idx_to_obj[pair[1]])
            edges.append(edge)
        edges = set(edges)
        return edges

    def _vertext2voxel(self, x, y, z, unit):

        x_min, y_min, z_min = math.floor(min(x)*unit), math.floor(min(y)*unit), math.floor(min(z)*unit)

        obj_list = []
        idx_to_obj = dict()
        obj_to_real_pts = dict()

        for idx, (i,j,k) in enumerate(zip(x, y, z)):
            a, b, c = round(i*unit) - x_min, round(j*unit) - y_min, round(k*unit) - z_min
            obj_list.append((a,b,c))
            idx_to_obj[idx] = (a,b,c)
            if (a,b,c) in obj_to_real_pts:
                obj_to_real_pts[(a,b,c)].append((i*unit,j*unit,k*unit))
            else:
                obj_to_real_pts[(a,b,c)] = [(i*unit,j*unit,k*unit)]

        return obj_list, idx_to_obj, obj_to_real_pts

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
            self._add_additional_edge()
            # raise GraphConnectionError("Graph is not connected, Please resize n_size")

    def _add_additional_edge(self):
        # g 를 구성하는 그룹
        components = list(nx.connected_components(self.g))

        # 노드를 좌표로 변환
        components_pts = []
        for component in components:
            cs = list(component)
            components_pts.append(cs)
        
        # 그룹 간의 거리 계산
        num_groups = len(components_pts)
        group_to_nearest_pt = dict()
        group_to_distance = []
        for i, g1 in enumerate(components_pts):
            kdt = KDTree(g1, leaf_size=2, metric='euclidean')
            for j, g2 in enumerate(components_pts):
                if i >= j:
                    continue
                distance, ind = kdt.query(g2, k=2)
                nearest_pt2 = np.argmin(distance[:,1]) # g2 에서의 pt
                nearest_pt1 = ind[nearest_pt2, 1]      # g1 에서의 pt
                nearest_distance = distance[nearest_pt2, 1]
                group_to_nearest_pt[(i,j)] = (g1[nearest_pt1], g2[nearest_pt2])
                group_to_distance.append(((i,j), nearest_distance))
        
        group_to_distance = sorted(group_to_distance, key=lambda x:x[1])

        # 그룹 연결 관계 확인용 그래프
        G = nx.Graph()

        for i in range(len(components_pts)):
            G.add_node(i)

        for pair, distance in group_to_distance:
            a, b = pair
            if nx.has_path(G, a, b):
                continue
            else:
                x, y = group_to_nearest_pt[(a, b)]
                self.g.add_edge(x, y)
                self.edges.add((x, y))
                G.add_edge(a, b)
            if nx.is_connected(G):
                break
        
        if not nx.is_connected(self.g):
            raise GraphConnectionError("Graph is not connected, Please resize n_size")