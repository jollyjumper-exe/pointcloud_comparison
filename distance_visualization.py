import pathlib
import struct
import numpy as np
from pygltflib import GLTF2
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def load_gltf_vertices(filepath):
    gltf = GLTF2().load(filepath)
    mesh = gltf.meshes[gltf.scenes[gltf.scene].nodes[0]]
    vertices = []
    
    for primitive in mesh.primitives:
        accessor = gltf.accessors[primitive.attributes.POSITION]
        buffer_view = gltf.bufferViews[accessor.bufferView]
        buffer = gltf.buffers[buffer_view.buffer]
        data = gltf.get_data_from_buffer_uri(buffer.uri)

        for i in range(accessor.count):
            index = buffer_view.byteOffset + accessor.byteOffset + i * 12
            vertex_data = data[index:index + 12]
            vertex = struct.unpack("<fff", vertex_data)
            vertices.append(vertex)

    return np.array(vertices)

def visualize_hausdorff_distance(set1, set2):
    # Calculate distances from each point in set2 to the nearest point in set1
    distances_to_set1 = np.min(cdist(set2, set1), axis=1)

    # Visualize the sets and Hausdorff distance as a heatmap
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Scale the distances to be in the range [0, 1] for colormap mapping
    scaled_distances = (distances_to_set1 - distances_to_set1.min()) / (distances_to_set1.max() - distances_to_set1.min())

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

    plt.savefig('plots/3DPlot.png')
    plt.show()

# Load GLTF files and extract vertices
set1 = load_gltf_vertices(pathlib.Path("models/cube.glb"))
set2 = load_gltf_vertices(pathlib.Path("models/cube_m.glb"))

# Visualize Hausdorff distance
visualize_hausdorff_distance(set1, set2)