# 小车控制系统

基于 AprilTag 码巡航和 YOLO 物体识别的小车控制系统。

## 项目结构

```
.
├── src/                    # 源代码目录
│   ├── main.py            # 主程序入口
│   ├── camera.py          # 摄像头和 AprilTag 检测模块
│   ├── servo.py           # 舵机控制模块（PWM）
│   ├── motor.py           # 电机控制模块（封装左右电机）
│   ├── display.py         # OLED 显示模块
│   ├── yolo.py            # YOLO 物体识别模块
│   └── start.py           # 启动按钮检测模块
├── resources/             # 资源文件目录
│   ├── fonts/            # 字体文件
│   │   └── NotoSerifCJKsc-Regular.otf
│   └── models/           # 模型文件
│       └── best-3.pt     # YOLO 模型文件
├── requirements.txt       # Python 依赖库清单
├── .gitignore            # Git 忽略配置
└── README.md             # 本文件
```

## 功能说明

- **AprilTag 码检测与巡航**：通过摄像头检测 AprilTag 码，实现自动巡航功能
- **物体识别**：使用 YOLO 模型识别物体（花露水、益达、英吉利、肯德基、屁股、纸巾）
- **OLED 显示**：在 OLED 屏幕上显示识别结果和任务状态
- **电机控制**：通过 PWM 控制左右电机实现前进、后退、转向

## 安装说明

### 1. 安装 Python 依赖库

```bash
pip install -r requirements.txt
```

### 2. 确保资源文件存在

确保以下文件存在：
- `resources/fonts/NotoSerifCJKsc-Regular.otf` - 中文字体文件
- `resources/models/best-3.pt` - YOLO 模型文件

### 3. 硬件要求

- Linux 系统（推荐 Ubuntu 或 Debian）
- 摄像头（USB 摄像头或 CSI 摄像头）
- OLED 显示屏（SSD1306，I2C 接口）
- GPIO 按钮（用于启动）
- PWM 控制的电机驱动模块

**注意**：
- `python-periphery` 库需要 Linux 系统支持，Windows 系统无法使用 GPIO 和 PWM 功能
- 如果需要在 Windows 上测试，可以创建硬件模拟层或使用其他替代方案

## 运行方式

### 基本运行

```bash
cd src
python main.py
```

### 测试单个模块

```bash
# 测试摄像头
python src/camera.py

# 测试电机控制
python src/motor.py

# 测试 OLED 显示
python src/display.py

# 测试 YOLO 检测
python src/yolo.py
```

## 代码优化说明

### 主要改进

1. **代码结构优化**
   - 统一类命名规范（PascalCase）
   - 统一函数命名规范（snake_case）
   - 添加详细的文档字符串和注释

2. **错误处理**
   - 添加异常处理机制
   - 资源自动释放（使用 `try-finally` 和 `__del__`）
   - 友好的错误提示信息

3. **代码重构**
   - 消除重复代码
   - 提取魔法数字为常量
   - 改进函数职责划分

4. **Bug 修复**
   - 修复 `motor.py` 中的时间计算错误
   - 修复 `camera.py` 中的参数传递错误
   - 改进资源管理

5. **可维护性**
   - 模块化设计，职责清晰
   - 便于测试和扩展
   - 代码可读性大幅提升

## 依赖库清单

详细依赖库版本请查看 `requirements.txt` 文件，主要包含：

- **opencv-python** - 计算机视觉处理
- **numpy** - 数值计算
- **Pillow** - 图像处理
- **apriltag** - AprilTag 码检测
- **ultralytics** - YOLO 物体检测
- **luma.oled** - OLED 显示驱动
- **python-periphery** - GPIO 和 PWM 控制（仅 Linux）

## 配置说明

### 相机参数

在 `src/camera.py` 中可以修改相机内参和畸变系数：
- `camera_matrix` - 相机内参矩阵
- `dist_coeffs` - 相机畸变系数
- `tag_size` - AprilTag 标签尺寸（米）

### 导航参数

在 `src/main.py` 中可以修改导航参数：
- `DETECTION_DISTANCE` - 检测距离阈值
- `NAVIGATION_DISTANCE` - 导航目标距离
- `FORWARD_DISTANCE` - 前进目标距离
- `TAG_ID_LEFT` / `TAG_ID_RIGHT` - 左右标签 ID

### OLED 配置

在 `src/display.py` 中可以修改：
- `i2c_port` - I2C 端口号（默认 5）

### GPIO 配置

在 `src/start.py` 中可以修改：
- `gpio_chip` - GPIO 芯片路径（默认 `/dev/gpiochip3`）
- `gpio_line` - GPIO 线号（默认 1）

## 故障排除

### 1. 无法打开摄像头

- 检查摄像头是否连接
- 检查摄像头权限（Linux 下可能需要加入 `video` 用户组）
- 尝试修改 `camera_index` 参数

### 2. GPIO 权限错误

```bash
# 以 root 权限运行
sudo python src/main.py

# 或添加用户到 gpio 组
sudo usermod -a -G gpio $USER
```

### 3. 模型文件未找到

- 确保 `resources/models/best-3.pt` 文件存在
- 检查文件路径是否正确

### 4. 字体文件未找到

- 确保 `resources/fonts/NotoSerifCJKsc-Regular.otf` 文件存在
- 检查文件路径是否正确

## 开发说明

### 代码风格

- 使用 Python 3.7+ 语法
- 遵循 PEP 8 代码规范
- 使用类型提示（可选）

### 扩展开发

如需添加新功能，建议：
1. 在对应模块中添加新方法
2. 保持模块职责单一
3. 添加适当的错误处理
4. 更新文档字符串

## 许可证

本项目仅供学习和研究使用。

## 联系方式

如有问题或建议，请提交 Issue 或 Pull Request。