# masterprojekt

## Evaluation
This branch is dedicated to an automated evaluation. The following readme contains the instructions.

## Prerequisites

To install the necessary requirements, use the .yaml file.

```pip install -r req.yaml```

Make sure you have Python 3.6+ installed.

You can find all the research associated with this [here](https://gitlab.bht-berlin.de/s87298/masterprojekt/-/wikis/Research/Evaluation-Framework).

### 1. Load your files
Place your point clouds, that you want to evaluate into the input folder. For this, you need to create a subfolder subfolder, inside the input folder, which contains the scene name. That subfolder should also contain a subfolder itself, called reference in which you should place the reference file for that scene. E.g., for a scene, named test, the structure should look like this:


``` 
├── input
│   ├── test
│   │   ├── reference
|   |   | ├──reference.ply
|   ├── *.ply
```

### 2. Evaluate point clouds and create metrices 

After setting up the input folder, you can use the app.py to evaluate the point clouds and create the metrices.

```python .\app.py <scene name>```

- scene name: The scene name needs to be identical to the scene name of the folder.

### 3. Show Distance between meshes
Finally, you can show the distances of a specific model.

```python .\show_plot.py <scene name> <model name>```

- scene name: The scene name needs to be identical to the scene name of the folder.
- model name: Name of the specific model you want to display. Look up ```output/<scene name>/metric.csv``` for the model names.

## About 
This Repo contains any code, files and information needed to understand and reconstruct this project. 
You can find our researches in the Wiki under ['Research'](https://gitlab.bht-berlin.de/s87298/masterprojekt/-/wikis/Research).

