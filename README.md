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

## tree+tree_hard merged.ipynb usage
1. Import nodes from txt file
```
root, nodes, encoding = initialize_graph('result3d-1.txt') # for complex
root, nodes, encoding = initialize_graph('result3d.txt') # for simple
```
2. Change parameters and train
```
algorithm_param = {'max_num_iteration':1000,\
                   'population_size':100,\
                   'mutation_probability':0.1,\
                   'elit_ratio': 0.01,\
                   'crossover_probability': 0.5,\
                   'parents_portion': 0.3,\
                   'crossover_type':'uniform',\
                   'max_iteration_without_improv':500}

model=ga(function=fitness, dimension=len(nodes), variable_type='bool', algorithm_parameters=algorithm_param)
model.run()
```
3. Show plot
prunedPlot()

## Structure of txt file that contains information of the nodes
[nodes as (x, y, z)]\n
[(node1, node2) as ((x1, y1, z1), (x2, y2, z2))]\n
{node:distance from root as (x, y, z):dist}

