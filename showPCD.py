import argparse, sys
import os
import open3d as o3d

def main(argv):

    parser=argparse.ArgumentParser()

    parser.add_argument('--f', help='Write obj or pcd File name in obj_data')

    args=parser.parse_args()

    filename = './obj_data/tree_10.pcd'
    if args.f is not None:
        filename = f'./obj_data/{args.f}'

    pcd = o3d.io.read_point_cloud(filename) 
    o3d.visualization.draw_geometries([pcd])

if __name__ == "__main__":
    main(sys.argv)