# MLDLTreeProject

- Machine Learning and Deep Learning for Data Science (GSDS 2021-1) Sixth Sensor

## run.py usage

### obj_data

+ tree.obj (Simple tree)
+ tree_hard.obj (Complex tree)

f : obj to load, name of the pcd (default : tree.obj)
n_size : voxel size (default : 50)

```
python3 run.py --f=tree.obj
```



## show3d.py usage

Display result from run.py

only_node : display only nodes, 'T' or 'F' (default=F)

```
python3 show3d.py --only_node=T
```



## showPCD.py usage

Visualize pcd file

f : pcd to load (default : tree_10.pcd)

```
python3 showPCD.py --f=tree_1.pcd
```

