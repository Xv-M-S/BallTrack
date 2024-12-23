import cv2
import json
from BallRule import BallTracker
from ultralytics import YOLO

# 加载Rule类
rule = BallTracker(distance_threshold=60, ratio_threshold=0.2)

# 加载模型
# model = YOLO('./models/newest.pt')  # 替换为您的模型文件路径
# model = YOLO('/home/sxm/HomeWorkSpace/ballTrack/testDemo/models/train42-11m/weights/best.pt')
model = YOLO('/home/sxm/HomeWorkSpace/MiguBallTrack/ballTrack/testDemo/models/train33-v11m/weights/best.pt')
# 打开视频文件
video_path = './test_video/index.ts'  # 替换为您的视频文件路径
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
output_path = './results/rule.mp4'  # 替换为您想要保存的路径
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 编码格式
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# 打开文本文件以写入边界框信息
output_file = "./res_file/rule.jsonl"
with open(output_file, 'w') as f:
    frame_index = 0  # 帧索引
    # 逐帧处理视频
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # 视频结束

        # 使用模型进行推理
        # results = model(frame)
        results = model.predict(source=frame, conf=0.6)

        # 处理结果
        for result in results:
            frame_data = []
            print(len(result.boxes))
            if hasattr(result, 'boxes') and len(result.boxes) > 0:
                boxes = result.boxes.xyxy  # 获取边界框,以左上角坐标和右下角坐标的形式
                boxes_list = boxes.tolist()
                if len(boxes_list) == 0:
                    continue
                # for box in boxes:
                box = rule.update_tracking(boxes_list)
                # try:
                #     x1, y1, x2, y2, conf, cls = box  # 解包边界框
                # except:
                #     x1, y1, x2, y2 = box
                x1, y1, x2, y2 = box[0], box[1], box[2], box[3]
                # x1, y1, x2, y2 = box  # 解包边界框
                # conf, cls = 0 , 0
                # 绘制边界框
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                # 可以添加标签等
                # cv2.putText(frame, f'Class: {int(cls)}, Conf: {conf:.2f}', (int(x1), int(y1) - 5),
                            # cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                cv2.putText(frame, f'ball', (int(x1), int(y1) - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                # 写入边界框信息到文本文件
                if output_file.endswith('.txt'):
                    f.write(f'{frame_index} {x1} {y1} {x2} {y2}\n')
            
                if output_file.endswith('.jsonl'):
                    frame_data.append({
                        "number": "football",  # 固定检测到的对象类别为 "football"
                        "coord": box  # 保持浮点格式的边界框坐标
                    })
            # 生成jsonl格式的输出
            json_line = {"data": frame_data, "frame_id": frame_index}
            f.write(json.dumps(json_line) + '\n')

        # 写入输出视频
        out.write(frame)
        frame_index += 1  # 更新帧索引

# 释放视频对象
cap.release()
out.release()
cv2.destroyAllWindows()
print("视频处理完毕，结果已保存至", output_path)