import json
import laspy
import numpy as np
import open3d as o3d

def density(data):
    min_x, max_x = np.min(data.x), np.max(data.x)
    min_y, max_y = np.min(data.y), np.max(data.y)

    area = (max_x - min_x) * (max_y - min_y)
    n_points = len(data.x)

    density = n_points / area
    return density

def data2np(data):
    points = np.vstack((data.x, data.y, data.z)).transpose()
    return points

def plot_o3d(points):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    o3d.visualization.draw_geometries([pcd])


def main():
    data_golm = laspy.read("2012/golm_364806_fp.las")
    data_palais = laspy.read("2012/neuespalais362808_fp.las")

    density_golm = density(data_golm)
    density_palais = density(data_palais)

    output_density = {
        "golm": density_golm,
        "palais": density_palais
    }

    with open("density.json", "w") as f:
        json.dump(output_density, f, indent=4)

    #points_golm = data2np(data_golm)
    #points_palais = data2np(data_golm)

    #plot_o3d(points_golm)
    #plot_o3d(points_palais)

if __name__ == "__main__":
    main()
