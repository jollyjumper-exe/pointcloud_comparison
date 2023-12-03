import sys
import open3d as o3d
import numpy as np

# Load a point cloud from file (replace "your_point_cloud_file.ply" with your actual file)
point_cloud_file = f"pointclouds/{sys.argv[1]}"
pcd = o3d.io.read_point_cloud(point_cloud_file)

# Check if the point cloud has normals; if not, compute normals
if not pcd.has_normals():
    pcd.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30)
    )

# Create a triangle mesh from the point cloud
#mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, 1)

mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
    pcd, depth=8, width=0, scale=1.1, linear_fit=False, n_threads=-1
)


# Visualize the point cloud and mesh
o3d.visualization.draw_geometries([mesh])
o3d.io.write_triangle_mesh(f"models/{sys.argv[2]}", mesh)

