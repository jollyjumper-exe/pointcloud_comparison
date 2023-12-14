# masterprojekt



## Distance Visualization
This branch is dedicated to experimenting with the distance visualization, which is needed for the evaluation framework. To run distance_visualization.py, you need to install the requirements via:

```pip install -r req.yaml```

Make sure you have Python 3.6+ installed.

You can find all the research associated with this [here](https://gitlab.bht-berlin.de/s87298/masterprojekt/-/wikis/Research/Evaluation-Framework).

### 1. Crop your Pointcloud

```python .\crop_ply.py <pointcloud.ply> <radius> <use neighbor filtering> ```

- pointcloud.ply: Name of the file, inside the pointclouds/ folder
- radius: radius to remove points outside of it
- use neighbor filtering: boolean, if you want to apply neighbor filtering (cautiion: applying could take a while)

### 2. Convert your pointcloud to a mesh

```python .\ply_to_mesh.py <pointcloud.ply> <object.glb>```

- pointcloud.ply: Name of the file, inside the pointclouds/ folder
- object.glb: Name of stored file, inside the models/ folder

### 3. Show Distance between meshes

```python .\distance_visualization.py <source> <compare>```

- source: name of the source file
- compare: name of the compare file

## About 
This Repo contains any code, files and information needed to understand and reconstruct this project. 
You can find our researches in the Wiki under ['Research'](https://gitlab.bht-berlin.de/s87298/masterprojekt/-/wikis/Research).

