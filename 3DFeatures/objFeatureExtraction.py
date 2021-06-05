import matplotlib.pyplot as plt
from time import time
from tqdm.auto import tqdm
import numpy as np
import plotly.graph_objects as go
import math
import networkx as nx
from utils import *
from itertools import product

class objFeatureDiGraph:

    def __init__(self, objGraph):
        distance_map, obj_list, y_len, edges, root = objGraph.distance_map, objGraph.obj_list, objGraph.y_len, objGraph.edges, objGraph.root
        obj_to_real_pts = objGraph.obj_to_real_pts
        self.result = nx.DiGraph()
        self.node_to_obj, self.result_root = self._add_node(obj_list, y_len, root, edges, obj_to_real_pts)
        self.node_distance_map = self._node_distance_map(distance_map)
        self._add_edge(edges)
        self._remove_unecessary_nodes()

        self._check_graph_connectivity()
        self._check_tree()

    def _add_node(self, obj_list, y_len, root, edges, obj_to_real_pts):
        node_to_obj = dict()
        empty_y = []
        for yv in tqdm(range(y_len)):
            ys = list(filter(lambda x:x[1] == yv, obj_list))
            if len(ys) < 1:
                empty_y.append(yv)
        #         print('empty : ', yv)
                continue
            tmp = nx.Graph()
            for n in ys:
                tmp.add_node(n)

            ys = set(ys)
            for edge in edges:
                n1, n2 = edge
                if n1 in ys and n2 in ys:
                    tmp.add_edge(n1, n2)
        #     print(yv, nx.number_connected_components(tmp), len(list(tmp.edges)))
            
            for components in list(nx.connected_components(tmp)):
                center_node = get_center_node(components)
                thickness = get_thickness(components, obj_to_real_pts)
                if root in components:
                    result_root = center_node
                if center_node in node_to_obj:
                    node_to_obj[center_node].update(components)
                    thickness = get_thickness(node_to_obj[center_node], obj_to_real_pts)
                    self.result.nodes[center_node]['thickness'] = thickness
                else:
                    self.result.add_node(center_node, thickness=thickness)
                    node_to_obj[center_node] = components
        return node_to_obj, result_root

    def _node_distance_map(self, distance_map):
        nodes = list(self.result.nodes)
        node_distance_map = dict()

        for node in nodes:
            objs = self.node_to_obj[node]
            distances = sorted(list(map(lambda x: distance_map[x], objs)))
            min_distance = min(distances)
            node_distance_map[node] = min_distance
        return node_distance_map

    def _add_edge(self, edges):
        nodes = list(self.result.nodes)
        # empty_y = set(empty_y)
        no_parent_nodes = []
        for node in tqdm(nodes):

            d = self.node_distance_map[node]
            pc = list(filter(lambda n: self.node_distance_map[n] < d, nodes))
            
            ps = []
            for p in pc:
                if self.is_node_connected(node, p, edges):
                    dd = d - self.node_distance_map[p]
                    ps.append((p, dd))
            if len(ps) < 1:
                no_parent_nodes.append(node)
            else:
                p = sorted(ps, key=lambda x: x[1])[0][0]
                self.result.add_edge(p, node)

    def _remove_unecessary_nodes(self):
        ### 필요없는 노드는 제거

        nodes = list(nx.bfs_tree(self.result, self.result_root))
        count = 0

        for node in nodes:
            pc = list(self.result.predecessors(node))
            sc = list(self.result.successors(node))
            if len(pc) == 1 and len(sc) == 1:
                count += 1
                self.result.remove_edge(pc[0], node)
                self.result.remove_edge(node, sc[0])
                self.result.add_edge(pc[0], sc[0])
                self.result.remove_node(node)

        print('delete {} nodes'.format(count))

    def _check_graph_connectivity(self):
        if not len(list(nx.bfs_tree(self.result, self.result_root))) == len(list(self.result.nodes)):
            raise GraphConnectionError("Result Graph is not connected, Please resize n_size")

    def _check_tree(self):
        if self.result.number_of_nodes() - self.result.number_of_edges() != 1:
            raise GraphConnectionError("Result Graph is not connected, Please resize n_size")

    def is_node_connected(self, n1, n2, edges):
        child1 = self.node_to_obj[n1]
        child2 = self.node_to_obj[n2]

        for c1, c2 in product(*[child1, child2]):
            e = (c1, c2)
            if (c1, c2) in edges or (c2, c1) in edges:
                return True
        return False