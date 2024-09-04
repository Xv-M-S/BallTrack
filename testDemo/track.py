import cv2
from ultralytics import YOLO

# 加载模型
model = YOLO('./models/newest.pt')  # 替换为您的模型文件路径

# 打开视频文件
video_path = './test_video/t2.mp4'  # 替换为您的视频文件路径
cap = cv2.VideoCapture(video_path)

# 检查视频是否打开成功
if not cap.isOpened():
    print("错误：无法打开视频文件")
    exit()

# 获取视频的基本信息
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# 创建 VideoWriter 对象以保存输出视频
output_path = './results/t2.mp4'  # 替换为您想要保存的路径
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 编码格式
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# 逐帧处理视频
while True:
    ret, frame = cap.read()
    if not ret:
        break  # 视频结束

    # 使用模型进行推理
    results = model(frame)

    # 处理结果
    for result in results:
        boxes = result.boxes.xyxy  # 获取边界框
        for box in boxes:
            # x1, y1, x2, y2, conf, cls = box  # 解包边界框
            x1, y1, x2, y2 = box  # 解包边界框
            conf, cls = 0 , 0
            # 绘制边界框
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            # 可以添加标签等
            # cv2.putText(frame, f'Class: {int(cls)}, Conf: {conf:.2f}', (int(x1), int(y1) - 5),
                        # cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            cv2.putText(frame, f'ball', (int(x1), int(y1) - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # 写入输出视频
    out.write(frame)

# 释放视频对象
cap.release()
out.release()
cv2.destroyAllWindows()
print("视频处理完毕，结果已保存至", output_path)