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

## 编译与运行

### 1. 编译工作空间
```bash
cd ~/ros2_ws
colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release
source install/setup.bash
