import sys
import os
import open3d as o3d
import glob
import numpy as np

module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'scripts'))
sys.path.append(module_path)
import crop_and_filter as crop
import point_cloud_distance as distance

def load_point_cloud(file_path):
    pcd = o3d.io.read_point_cloud(file_path)
    points = np.asarray(pcd.points)
    return points

def center_point_cloud(pc):
    return pc - np.mean(pc, axis=0)

def limit_point_cloud(pc, x):
    return pc[:x]

scene_name = sys.argv[1]
input_folder = f'input/{scene_name}/pointclouds/'
reference_folder = f'input/{scene_name}/reference'
filtered_folder = f'input/{scene_name}/pointclouds/filtered'
output_folder = f'output/{scene_name}/'
output_folder_plots = f'output/{scene_name}/plots'

limit = 5000

# Get reference file
reference_file = glob.glob(f'{reference_folder}/*')[0]

if(len(glob.glob(f'{reference_folder}/*')) > 1): 
    print("Make sure that only one file is in the reference directory")

reference = load_point_cloud(reference_file)
reference = limit_point_cloud(reference,limit)

# Get input files
input_files = glob.glob(f'{input_folder}/*.ply')

# Create filtered Folder
if not os.path.exists(filtered_folder):
    os.makedirs(filtered_folder)

#create filtered pointclouds
for file in input_files:
    filtered_pcd = crop.crop_and_filter(file)
    filename = file.split('\\')[-1].split('.')[0]
    o3d.io.write_point_cloud(f'{filtered_folder}/{filename}_cropped.ply', filtered_pcd)
    #o3d.visualization.draw_geometries([filtered_pcd])

# Get all filtered point clouds
input_files = glob.glob(f'{filtered_folder}/*.ply')

# Create filtered Folder
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Create filtered Folder
if not os.path.exists(f'{output_folder}/metric.csv'):
    with open(f'{output_folder}/metric.csv', 'w') as file:
        file.write('name;sampled points;Max;Min;Mean;RMS')

for file in input_files:
    # Load & limit point cloud
    cloud = load_point_cloud(file)
    cloud = limit_point_cloud(cloud, limit)

    sampled_points, min_d, max_d, mean, RMS = distance.visualize_hausdorff_distance(reference, cloud)

    modelname = file.split('\\')[-1].split('.')[0].split('_')[0]
    with open(f'{output_folder}/metric.csv', 'a') as ofile:
        ofile.write('\n' + f'{modelname};{sampled_points};{max_d};{min_d};{mean};{RMS}')