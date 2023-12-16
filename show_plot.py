import sys
import os
import numpy as np
import json

module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'scripts'))
sys.path.append(module_path)
import point_cloud_distance as distance

scene_name = sys.argv[1]
model_name = sys.argv[2]

output_folder = f'output/{scene_name}/'

with open(f'{output_folder}/plots.json', 'r') as file:
        file_contents = file.read()

obj = json.loads(file_contents)
for entry in obj["plots"]:
    if(entry["model"]==model_name):
        points = np.array(entry["points"])
        scaled_distances = np.array(entry["scaled_distances"])
        metric = entry["metric"]
        distance.visualize_hausdorff_distance(points, scaled_distances, data=metric)
        break
