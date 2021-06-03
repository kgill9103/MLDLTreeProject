import argparse, sys
import os

sys.path.append(f'{os.getcwd()}/3DFeatures')

from objFeatureExtraction import *
from build_obj_graph import *
from utils import *
import networkx as nx

def main(argv):

    parser=argparse.ArgumentParser()

    parser.add_argument('--obj', help='Write obj File name in obj_data')
    parser.add_argument('--n_size', help='Write voxel max length')

    args=parser.parse_args()

    filename = './obj_data/tree.obj'
    if args.obj is not None:
        filename = f'./obj_data/{args.obj}'

    f = open(filename, 'r')
    obj_data = f.read()
    f.close()

    objToArray = ObjtoArray(obj_data)

    x, y, z = objToArray.xyz
    faces = objToArray.faces

    n_size = 50
    if args.n_size is not None:
        n_size = args.n_size

    objGraph = BuildObjGraph(x, y, z, faces, n_size)

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




# module이 아닌 main으로 실행된 경우 실행된다
if __name__ == "__main__":
    main(sys.argv)