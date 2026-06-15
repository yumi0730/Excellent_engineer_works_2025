import cv2
import sys
import time
from pathlib import Path

sys.path.insert(0, r"E:\Windows_Desktop\yolov13-main")
from ultralytics import YOLO

# ========== 可配置区域 ==========
# 1) 模型路径：用你训练好的 best.pt，或者先用官方权重测试（yolov8n.pt）
MODEL_PATH = r"E:\项目\vision_car\goodstest_train\yolov13n.pt"  # 改成你的路径；未训练可先用 "yolov8n.pt"

# 2) 输入源：
#    - 摄像头：0（或 1/2…）
#    - 本地视频：r"D:\path\to\video.mp4"
SOURCE = 0

# 3) 置信度与 IoU 阈值
CONF_THRES = 0.25
IOU_THRES = 0.45

# 4) 是否使用半精度（需要支持的 NVIDIA GPU）
HALF = False

# 5) 窗口标题
WINDOW_NAME = "YOLOv13 Realtime Detection"
# =================================

# 兼容导入：优先使用 Ultralytics 的 YOLO API
try:
    from ultralytics import YOLO
except Exception as e:
    print("未安装 ultralytics，或环境异常：", e)
    print("请先执行：pip install ultralytics opencv-python")
    sys.exit(1)


def open_capture(source):
    """
    更健壮地打开视频源（摄像头/文件）。
    Windows 上用 CAP_DSHOW 可减少初始化卡顿。
    """
    if isinstance(source, int):
        cap = cv2.VideoCapture(source, cv2.CAP_DSHOW)
    else:
        # 文件/RTSP/HTTP 流
        cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise RuntimeError(f"无法打开视频源：{source}")
    return cap


def main():
    # 检查模型文件（若是本地路径）
    if isinstance(MODEL_PATH, str) and MODEL_PATH.endswith(".pt"):
        p = Path(MODEL_PATH)
        if not p.exists() and p.name != "yolov8n.pt":
            print(f"[警告] 模型文件不存在：{MODEL_PATH}")
            print("如果你还没训练，先把 MODEL_PATH 改为 'yolov8n.pt' 以测试流程。")

    # 加载模型
    print("加载模型中……")
    model = YOLO(MODEL_PATH)

    # 推理设置
    model.overrides["conf"] = CONF_THRES
    model.overrides["iou"] = IOU_THRES
    model.overrides["half"] = HALF  # 半精度（需要 CUDA + 支持的 GPU）
    # 你也可以设置 classes 只检测某几类，例如：model(overrides={"classes":[0,2]})

    # 打开视频源
    cap = open_capture(SOURCE)
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

    # 计算 FPS 用
    t0 = time.time()
    frames = 0

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                print("读取到视频结尾或摄像头断开。")
                break

            # 使用 stream=True 实时逐帧推理，保持低延迟
            results = model.predict(source=frame, stream=True, verbose=False)
            # results 是一个生成器，这里只取当前帧的第一个结果对象
            result = next(results)

            # 使用 Ultralytics 自带的绘制工具
            # result.plot() 返回已绘制框与标签的 np.ndarray 图像
            annotated = result.plot()

            # 计算并显示 FPS
            frames += 1
            if frames % 10 == 0:
                dt = time.time() - t0
                fps = frames / dt if dt > 0 else 0.0
            else:
                # 简单平滑：不每帧都重算
                fps = None

            if fps is not None:
                cv2.putText(
                    annotated,
                    f"FPS: {fps:.1f}",
                    (12, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA,
                )

            cv2.imshow(WINDOW_NAME, annotated)

            key = cv2.waitKey(1) & 0xFF
            if key in (27, ord('q')):  # ESC 或 q 退出
                break

    except KeyboardInterrupt:
        print("收到中断，正在退出…")
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
