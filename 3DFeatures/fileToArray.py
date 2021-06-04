import matplotlib.pyplot as plt
from time import time
from tqdm.auto import tqdm
import numpy as np
import plotly.graph_objects as go
import math
import networkx as nx
from utils import *
from itertools import product
import open3d as o3d
from sklearn.neighbors import KDTree, BallTree

class ObjtoArray:

    def __init__(self, filename):
        f = open(filename, 'r')
        obj_data = f.read()
        f.close()
        vertices, faces = self._obj_data_to_mesh3d(obj_data)
        self.vertices = vertices
        self.faces = faces
        self.xyz = vertices[:,:3].T
        self.pairs = None

    def _obj_data_to_mesh3d(self, odata):
        # odata is the string read from an obj file
        vertices = []
        faces = []
        lines = odata.splitlines()   
    
        for line in lines:
            slist = line.split()
            if slist:
                if slist[0] == 'v':
                    vertex = np.array(slist[1:], dtype=float)
                    vertices.append(vertex)
                elif slist[0] == 'f':
                    face = []
                    for k in range(1, len(slist)):
                        face.append([int(s) for s in slist[k].replace('//','/').split('/')])
                    if len(face) > 3: # triangulate the n-polyonal face, n>3
                        faces.extend([[face[0][0]-1, face[k][0]-1, face[k+1][0]-1] for k in range(1, len(face)-1)])
                    else:    
                        faces.append([face[j][0]-1 for j in range(len(face))])
                else: pass
        
        
        return np.array(vertices), np.array(faces)

class PCDtoArray:
    def __init__(self, filename):
        pcd = o3d.io.read_point_cloud(filename) 

        distances = pcd.compute_nearest_neighbor_distance()
        avg_dist = np.mean(distances)
        self.radius = 2 * avg_dist

        pts = np.asarray(pcd.points)

        new_array = [tuple(row) for row in pts]
        pts = np.unique(new_array, axis=0)

        self.pts = pts

        g = self._graph(self.pts)
        nodes = list(g.nodes)
        self.xyz = zip(*nodes)
        self.pairs = self._pairs(g, nodes)
        self.faces = None

    def _graph(self, pts):
        tree = BallTree(pts, leaf_size=2) 
        ind = tree.query_radius(pts, r=self.radius)

        edges = []
        for i, neighbors in enumerate(ind):
            for neighbor in neighbors:
                if i != neighbor:
                    edges.append((tuple(pts[i]),tuple(pts[neighbor])))
        edges = set(edges)

        g = nx.Graph()
        for node in pts:
            g.add_node(tuple(node))
        for edge in edges:
            g.add_edge(edge[0], edge[1])

        # g 를 구성하는 그룹
        components = list(nx.connected_components(g))

        # 그룹마다의 크기
        len_components = list(map(len, components))

        # 그룹 평균 크기
        mean_len = np.mean(len_components)

        # 평균 크기 보다 큰 그룹
        max_components = list(filter(lambda x: len(x) > mean_len, components))

        # 평균 크기 보다 작은 그룹
        min_components = list(filter(lambda x: len(x) <= mean_len, components))

        # 작은 그룹에 들어간 노드들은 삭제
        for cs in min_components:
            for c in cs:
                g.remove_node(c)

        # 노드를 좌표로 변환
        components_pts = []
        for component in max_components:
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
                g.add_edge(x, y)
                G.add_edge(a, b)
            if nx.is_connected(G):
                break
        
        if not nx.is_connected(g):
            raise GraphConnectionError("Graph is not connected, Please resize n_size")
        
        return g

    def _pairs(self, g, nodes):
        node_to_idx = dict()
        for idx, node in enumerate(nodes):
            node_to_idx[node] = idx

        pairs = []
        for edge in g.edges():
            p1, p2 = node_to_idx[edge[0]], node_to_idx[edge[1]]
            pairs.append((p1, p2))
        
        return set(pairs)
