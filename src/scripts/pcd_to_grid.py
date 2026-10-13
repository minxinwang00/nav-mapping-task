import open3d as o3d
import numpy as np
import cv2
import yaml

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
pcd_path = os.path.join(BASE_DIR, '../../maps/pcd_map.pcd')
output_pgm = os.path.join(BASE_DIR, '../../maps/occugrid_map.pgm')
output_yaml = os.path.join(BASE_DIR, '../../maps/occugrid_map.yaml')
resolution = 0.05          # 栅格分辨率，单位：米/像素
height_min = 0.2           # 地面以上最低高度（米）
height_max = 2.0           # 最高高度（米）

# 1. 读取点云
pcd = o3d.io.read_point_cloud(pcd_path)
print(f"原始点数：{len(pcd.points)}")

# 2. 去除无效点（NaN/Inf）
points = np.asarray(pcd.points)
mask = np.isfinite(points).all(axis=1)
points = points[mask]
print(f"去除无效点后：{len(points)}")

# 3. 统计离群点去除
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)
cl, ind = pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
pcd = pcd.select_by_index(ind)
points = np.asarray(pcd.points)
print(f"去除离群点后：{len(points)}")

# 4. 体素降采样
pcd = pcd.voxel_down_sample(voxel_size=0.05)
points = np.asarray(pcd.points)
print(f"体素降采样后：{len(points)}")

# 5. 根据高度过滤（保留地面以上、一定高度以下的点）
mask = (points[:, 2] > height_min) & (points[:, 2] < height_max)
points_2d = points[mask, :2]
print(f"高度过滤后：{len(points_2d)}")

if len(points_2d) == 0:
    print("错误：过滤后没有点，请调整 height_min / height_max")
    exit(1)

# 6. 生成二维栅格
x_min, y_min = points_2d.min(axis=0)
x_max, y_max = points_2d.max(axis=0)
width = int((x_max - x_min) / resolution) + 1
height = int((y_max - y_min) / resolution) + 1
grid = np.zeros((height, width), dtype=np.uint8)

for x, y in points_2d:
    i = int((y - y_min) / resolution)
    j = int((x - x_min) / resolution)
    if 0 <= i < height and 0 <= j < width:
        grid[i, j] = 255  # 占据

# 7. 保存为 pgm
cv2.imwrite(output_pgm, grid)
print(f"已保存 {output_pgm}，尺寸：{width}x{height}")

# 8. 保存 yaml
yaml_data = {
    'image': output_pgm,
    'resolution': resolution,
    'origin': [float(x_min), float(y_min), 0.0],
    'negate': 0,
    'occupied_thresh': 0.65,
    'free_thresh': 0.196
}
with open(output_yaml, 'w') as f:
    yaml.dump(yaml_data, f)
print(f"已保存 {output_yaml}")
