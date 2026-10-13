# 导航自主任务——建图

## 项目简介
使用 Livox Mid360 激光雷达，在 Ubuntu 22.04 + ROS2 Humble 环境下，通过 FAST-LIO 算法实时建立三维点云地图，再经离线处理生成二维占据栅格地图，并在 RViz 中同时显示。

## 环境依赖
- Ubuntu 22.04
- ROS2 Humble
- Livox-SDK2
- livox_ros_driver2
- FAST-LIO (ROS2 分支)
- Open3D, PCL, OpenCV, PyYAML

ws/ # 仓库根目录
├── maps/
│ ├── pcd_map.pcd # 三维点云地图
│ ├── occugrid_map.pgm # 二维占据栅格图片
│ └── occugrid_map.yaml # 二维栅格配置文件
├── src/
│ ├── config/ # 配置文件（mid360.yaml、MID360_config.json）
│ ├── launch/ # 启动文件（mapping.launch.py、rviz_MID360_launch.py）
│ └── scripts/ # 数据处理脚本
│ ├── extract_last_pcd.py
│ ├── pcd_to_grid.py
│ └── display_map.py
├── screenshots/
│ └── rviz_display.png # RViz 同时显示三维点云与二维栅格的截图
└── README.md
text


## 运行方法
注：如果有海康的MVS可能会导致第二个终端打不开
   原来的栅格地图有大约253万个点，运行时非常卡顿，经过降采样之后还有大约9万个点，流畅了一些
   采集样本时因为雷达断电,电脑息屏等原因多次失败，所以最终采集的样本比较简略，生成的栅格地图质量有待提高
   
   
   **************我已经把自己找到的绝对路径改为相对路径，但是可能还有疏漏，如果运行不成功，大概率是这个问题********

### 1. 安装 Python 依赖
```bash
pip install open3d numpy opencv-python pyyaml
（1）打开一个终端
bash

cd ~/ros2_ws/nav_task_repo
source /opt/ros/humble/setup.bash
python3 src/scripts/display_map.py

该节点会读取 maps/pcd_map.pcd 和 maps/occugrid_map.yaml，并持续发布：

    /cloud_registered（三维点云）

    /map（二维占据栅格）

2. 另开一个终端启动 RViz：
bash

source /opt/ros/humble/setup.bash
rviz2

在 RViz 中设置：

    Fixed Frame 改为 camera_init

    点击 Add → PointCloud2，话题选 /cloud_registered

    点击 Add → Map，话题选 /map

    调整视角，即可同时看到三维点云与二维栅格地图。

3. 若需重新生成二维栅格地图

仓库中已有三维点云 maps/pcd_map.pcd，可直接重新生成二维栅格：
bash

cd ~/ros2_ws/nav_task_repo
python3 src/scripts/pcd_to_grid.py

生成的文件会覆盖 maps/occugrid_map.pgm 和 maps/occugrid_map.yaml



###   地图保存方式


    三维点云：通过 FAST-LIO 建图后，使用 extract_last_pcd.py 从 ROS2 bag 中提取全局点云，保存为 maps/pcd_map.pcd（PCD 格式）。

    二维占据栅格：使用 pcd_to_grid.py 对三维点云进行统计离群点去除、体素降采样（0.05m）、高度过滤（0.2m~2.0m），投影到 XY 平面生成栅格，保存为 maps/occugrid_map.pgm（图片）和 maps/occugrid_map.yaml（配置文件，包含分辨率、原点、阈值等）。

注意事项


    相对路径：所有脚本和配置中的文件路径均已改为相对路径，运行时请确保在仓库根目录或对应目录下执行。

    RViz 显示：若点云太大导致卡顿，可进一步调整 voxel_size 参数。

######完成截图

注：采集样本时因为雷达断电,电脑息屏等原因多次失败，所以最终采集的样本比较简略，生成的栅格地图质量有待提高

https://screenshots/rviz_display.png
或者直接打开screenshots文件夹查看最终成果截图
