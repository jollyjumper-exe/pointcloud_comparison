import open3d as o3d
import sys

def glb_to_pointcloud(glb_path, n):
    mesh = o3d.io.read_triangle_mesh(glb_path)
    pcd = mesh.sample_points_uniformly(number_of_points=n)

    return pcd

glb_file_path = sys.argv[1]

if(len(sys.argv) <= 2):
    n = 20000
else:
    n = int(sys.argv[2])
pointcloud = glb_to_pointcloud(glb_file_path, n)

o3d.visualization.draw_geometries([pointcloud])
o3d.io.write_point_cloud(sys.argv[1].split(".")[0]+".ply", pointcloud)