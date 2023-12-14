import sys
import open3d as o3d
import numpy as np

def crop_and_filter(filename, radius=1, filter_ply=False):
    point_cloud_file = filename
    pcd = o3d.io.read_point_cloud(point_cloud_file)

    points_np = np.asarray(pcd.points)
    colors_np = np.array([])
    if pcd.colors is not None:
        colors_np = np.asarray(pcd.colors)

    mean_point = np.mean(points_np, axis=0)

    threshold_distance = np.float64(radius)

    distances_to_mean = np.linalg.norm(points_np - mean_point, axis=1)

    filtered_indices = distances_to_mean <= threshold_distance
    filtered_points_np = points_np[filtered_indices]
    filtered_pcd = o3d.geometry.PointCloud()
    filtered_pcd.points = o3d.utility.Vector3dVector(filtered_points_np)

    if(colors_np.size != 0): 
        filtered_colors_np = colors_np[filtered_indices]
        filtered_pcd.colors = o3d.utility.Vector3dVector(filtered_colors_np)

    if(filter_ply):
        print("Removing outliers... (This might take a while)")
        radius = 0.1  
        min_neighbors = 5  
        filtered_pcd, _ = filtered_pcd.remove_radius_outlier(nb_points=min_neighbors, radius=radius)

    return filtered_pcd