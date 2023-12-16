import open3d as o3d
import numpy as np

def load_point_cloud(file_path):
    pcd = o3d.io.read_point_cloud(file_path)
    points = np.asarray(pcd.points)
    return points

def center_point_cloud(pc):
    return pc - np.mean(pc, axis=0)

def limit_point_cloud(pc, x):
    return pc[:x]