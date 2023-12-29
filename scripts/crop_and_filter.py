import open3d as o3d
import numpy as np

def load_point_cloud(filename):
    pcd = o3d.io.read_point_cloud(filename)
    return pcd

def center_point_cloud(pointcloud):
    
    points_np = np.asarray(pointcloud.points)
    print(points_np.shape)
    mean_point = np.median(points_np, axis=0)
    centered_points = points_np - mean_point

    pointcloud.points = o3d.utility.Vector3dVector(centered_points)
    return pointcloud

def radial_crop(pointcloud, radius=1):

    points_np = np.asarray(pointcloud.points)
    colors_np = np.array([])
    if pointcloud.colors is not None:
        colors_np = np.asarray(pointcloud.colors)

    threshold_distance = np.float64(radius)
    distances_to_mean = np.linalg.norm(points_np, axis=1)

    filtered_indices = distances_to_mean <= threshold_distance
    filtered_points_np = points_np[filtered_indices]
    filtered_pcd = o3d.geometry.PointCloud()
    filtered_pcd.points = o3d.utility.Vector3dVector(filtered_points_np)

    if(colors_np.size != 0): 
        filtered_colors_np = colors_np[filtered_indices]
        filtered_pcd.colors = o3d.utility.Vector3dVector(filtered_colors_np)

    return filtered_pcd

def filter_point_cloud(pointcloud, radius, neighbors):
    print("Removing outliers... (This might take a while)")
    filtered_pcd, _ = pointcloud.remove_radius_outlier(nb_points=neighbors, radius=radius)
    return filtered_pcd