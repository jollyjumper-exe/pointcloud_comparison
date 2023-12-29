import sys
import os
import open3d as o3d
import glob
import json

module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'scripts'))
sys.path.append(module_path)
import crop_and_filter as crop
import point_cloud_distance as distance
import point_clouds as pc

scene_name = sys.argv[1]
input_folder = f'input/{scene_name}/pointclouds/'
reference_folder = f'input/{scene_name}/reference'
filtered_folder = f'input/{scene_name}/pointclouds/filtered'
output_folder = f'output/{scene_name}/'
output_folder_plots = f'output/{scene_name}/plots'

limit = 10000 #this is for testing. Might remove it or turn it into an cmd argument

# create necessary folders and files

if not os.path.exists(filtered_folder):
    os.makedirs(filtered_folder)

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

if not os.path.exists(f'{output_folder}/metric.csv'):
    with open(f'{output_folder}/metric.csv', 'w') as file:
        file.write('name;sampled points;Max;Min;Mean;RMS')

if not os.path.exists(f'{output_folder}/plots.json'):
    with open(f'{output_folder}/plots.json', 'w') as file:
        json.dump({"plots" : []}, file)

# Get reference file
reference_file = glob.glob(f'{reference_folder}/*')[0]

if(len(glob.glob(f'{reference_folder}/*')) > 1): 
    print("Make sure that only one file is in the reference directory")

reference = pc.load_point_cloud(reference_file)
if(limit != 0):
    reference = pc.limit_point_cloud(reference,limit)

# Get input files
input_files = glob.glob(f'{input_folder}/*.ply')

#create filtered pointclouds
for file in input_files:
    pcd = crop.load_point_cloud(file)
    pcd = crop.center_point_cloud(pcd)
    filtered_pcd = crop.radial_crop(pcd, radius=1)
    filtered_pcd = pcd
    filename = file.split('\\')[-1].split('.')[0]
    o3d.io.write_point_cloud(f'{filtered_folder}/{filename}_cropped.ply', filtered_pcd)
    #o3d.visualization.draw_geometries([filtered_pcd])

# Get all filtered point clouds
input_files = glob.glob(f'{filtered_folder}/*.ply')

for file in input_files:
    # Load & limit point cloud
    cloud = pc.load_point_cloud(file)
    if(limit != 0):
        cloud = pc.limit_point_cloud(cloud, limit)

    points, distances, scaled_distances = distance.hausdorff_distance(reference, cloud)
    sampled_points, min_d, max_d, mean, rms = distance.hausdorff_distance_metric(distances)


    modelname = file.split('\\')[-1].split('.')[0].split('_')[0]
    with open(f'{output_folder}/metric.csv', 'a') as ofile:
        ofile.write('\n' + f'{modelname};{sampled_points};{max_d};{min_d};{mean};{rms}')

    data = {"model" : modelname,
            "points" : points.tolist(),
            "scaled_distances" : scaled_distances.tolist(),
            "metric" : {
                "Sampled Points" : sampled_points,
                "Min" : min_d,
                "Max" : max_d,
                "Mean" : mean,
                "RMS" : rms
                }
            }

    with open(f'{output_folder}/plots.json', 'r+') as ofile:
        file_data = json.load(ofile)
        file_data["plots"].append(data)
        ofile.seek(0)
        json.dump(file_data, ofile)
