# MLDLTreeProject

- Machine Learning and Deep Learning for Data Science (GSDS 2021-1)

## run.py 사용법

### obj_data

+ tree.obj (간단한 이미지)
+ tree_hard.obj (복잡한 이미지)

f : 읽어들일 obj, pcd 파일 이름 (default : tree.obj)
n_size : 데이터를 옮길 voxel 사이즈 (default : 50)

```
python3 run.py --f=tree.obj
```



## show3d.py 사용법

run.py 의 결과를 표시

only_node : node 만을 표시할지에 대한 여부, 'T' or 'F' 작성 (default=F)

```
python3 show3d.py --only_node=T
```



## showPCD.py 사용법

pcd 파일을 시각화

f : 읽어들일 pcd 파일 이름 (default : tree_10.pcd)

```
python3 showPCD.py --f=tree_1.pcd
```

