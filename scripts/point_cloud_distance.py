import numpy as np
from scipy.spatial.distance import cdist
import open3d as o3d
import matplotlib.pyplot as plt


def hausdorff_distance(set1, set2, scale = .5):
    # Calculate distances from each point in set2 to the nearest point in set1
    distances_to_set1 = np.min(cdist(set2, set1), axis=1)

    scale = .05
    # Scale the distances to be in the range [0, 1] for colormap mapping
    if(not (distances_to_set1.max() - distances_to_set1.min())==0):
        scaled_distances = np.clip(distances_to_set1 / scale, None, 1)
    else:
        print("It is the same pointcloud!")
        scaled_distances = np.zeros(distances_to_set1.shape[0])
    
    return set2, distances_to_set1, scaled_distances

def hausdorff_distance_metric(distances):
    sampled_points = distances.shape[0]
    min_d = round(min(distances),5)
    max_d = round(max(distances),5)
    mean = round(np.mean(distances),5)
    RMS = round(np.sqrt(np.mean(np.square(distances))),5)
    
    return sampled_points, min_d, max_d, mean, RMS

def visualize_hausdorff_distance(points, scaled_distances, data=[]):
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    data_string = ""
    for entry in data:
        data_string += f'{entry}: {data[entry]}\n'

    fig.text(0.0, 0.7,  
        data_string,   
        fontsize = 15)
    
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], c=scaled_distances, cmap='viridis', marker='s', label='Set 2 - Hausdorff Distance')
    
    ax.set_box_aspect([np.ptp(axis) for axis in [points[:, 0], points[:, 1], points[:, 2]]])
    
    plt.show()