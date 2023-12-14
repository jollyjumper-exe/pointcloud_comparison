import sys
import pathlib
import numpy as np
from scipy.spatial.distance import cdist
import open3d as o3d
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def load_point_cloud(file_path):
    pcd = o3d.io.read_point_cloud(file_path)
    points = np.asarray(pcd.points)
    return points

def visualize_hausdorff_distance(set1, set2):
    # Calculate distances from each point in set2 to the nearest point in set1
    distances_to_set1 = np.min(cdist(set2, set1), axis=1)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Scale the distances to be in the range [0, 1] for colormap mapping
    if(not (distances_to_set1.max() - distances_to_set1.min())==0):
        scaled_distances = (distances_to_set1 - distances_to_set1.min()) / (distances_to_set1.max() - distances_to_set1.min())
    else:
        print("It is the same pointcloud!")
        scaled_distances = np.zeros(distances_to_set1.shape[0])

    # Use a colormap to map distances to colors
    scatter = ax.scatter(set2[:, 0], set2[:, 1], set2[:, 2], c=scaled_distances, cmap='viridis', marker='s', label='Set 2 - Hausdorff Distance')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    sampled_points = set1.shape[0]
    min_d = round(min(distances_to_set1),5)
    max_d = round(max(distances_to_set1),5)
    mean = round(np.mean(distances_to_set1),5)
    RMS = round(np.sqrt(np.mean(np.square(distances_to_set1))),5)
    fig.text(0.0, 0.7,  
         f"Sampled points: {sampled_points}\nMin: {min_d}\nMax: {max_d}\nMean: {mean}\nRMS: {RMS}",   
         fontsize = 15)

    print(f'Sampled Points: {sampled_points}')
    print(f'Min: {min_d}')
    print(f'Max: {max_d}')
    print(f'Mean: {mean}')
    print(f'RMS: {RMS}')

    plt.savefig('plots/3DPlot.png')
    plt.show()

# Load point clouds

cloud1 = load_point_cloud(f"pointclouds/{sys.argv[1]}")
cloud2 = load_point_cloud(f"pointclouds/{sys.argv[2]}")

x = 5000 # x = -1 to load full set
if(x != -1):
    cloud1 = cloud1[:x]
    cloud2 = cloud2[:x]

cloud1 = cloud1 - np.mean(cloud1, axis=0)
cloud2 = cloud2 - np.mean(cloud2, axis=0)



# Visualize Hausdorff distance
visualize_hausdorff_distance(cloud1, cloud2)