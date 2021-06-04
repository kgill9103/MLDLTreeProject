import argparse, sys
import os

sys.path.append(f'{os.getcwd()}/3DFeatures')

from objFeatureExtraction import *
from fileToArray import *
from build_obj_graph import *
from utils import *
import networkx as nx

def main(argv):

    parser=argparse.ArgumentParser()

    parser.add_argument('--f', help='Write obj or pcd File name in obj_data')
    parser.add_argument('--n_size', help='Write voxel max length')

    args=parser.parse_args()

    filename = './obj_data/tree.obj'
    if args.f is not None:
        filename = f'./obj_data/{args.f}'

    ext = filename.split('.')[-1]
    if ext == 'obj':
        objToArray = ObjtoArray(filename)
    else:
        objToArray = PCDtoArray(filename)

    x, y, z = objToArray.xyz
    faces = objToArray.faces
    pairs = objToArray.pairs

    n_size = 50
    if args.n_size is not None:
        n_size = int(args.n_size)

    objGraph = BuildObjGraph(x, y, z, faces, pairs=pairs, n_size=n_size)

    resultGraph = objFeatureDiGraph(objGraph)

    # write result

    result = resultGraph.result
    node_distance_map = resultGraph.node_distance_map
    nodes = convert_attributes_format(nx.get_node_attributes(result, 'thickness'), 'thickness')
    f = open('result3d.txt', 'w')
    f.write(str(nodes))
    f.write('\n')
    f.write(str(list(result.edges)))
    f.write('\n')
    f.write(str(node_distance_map))
    f.close()



if __name__ == "__main__":
    main(sys.argv)