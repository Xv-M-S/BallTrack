"""
函数作用：
给定一个数据集，根据标注的YOLOv8标签裁剪出球，并将裁剪出来的球存储到指定的路径中。
"""


import os
from PIL import Image

def crop_balls_from_yolo(images_path, labels_path, output_path):
    """
    根据 YOLOv8 标签裁剪出球并保存到指定路径。

    :param images_path: 原始图像路径
    :param labels_path: YOLOv8 标签路径
    :param output_path: 裁剪结果保存路径
    """
    # 确保输出目录存在
    os.makedirs(output_path, exist_ok=True)

    # 遍历标签文件
    for image_file in os.listdir(images_path):
        if True:
            # 获取图片文件名
            label_file = image_file.rsplit('.', 1)[0] + ".txt"
            image_path = os.path.join(images_path, image_file)
            
            # 打开图片
            image = Image.open(image_path)
            
            # 读取标签文件
            with open(os.path.join(labels_path, label_file), 'r') as f:
                for line in f:
                    # YOLO格式：class x_center y_center width height
                    try:
                        class_id, x_center, y_center, width, height = map(float, line.strip().split())
                    except:
                        print(f"Error parsing label file: {label_file}.")
                        continue
                    
                    # 计算裁剪区域
                    img_width, img_height = image.size
                    x_center *= img_width
                    y_center *= img_height
                    width *= img_width
                    height *= img_height
                    
                    # 计算左上角和右下角坐标
                    x1 = int(x_center - width / 2)
                    y1 = int(y_center - height / 2)
                    x2 = int(x_center + width / 2)
                    y2 = int(y_center + height / 2)
                    
                    # 裁剪并保存
                    cropped_ball = image.crop((x1, y1, x2, y2))
                    cropped_ball.save(os.path.join(output_path, f'{image_file[:-4]}_ball_{int(class_id)}.jpg'))

    print("裁剪完成！")

# 示例调用
# crop_balls_from_yolo('/data01/migu/soccer-track/BallDataSets/ballIn_and_ballOut/test/images', '/data01/migu/soccer-track/BallDataSets/ballIn_and_ballOut/test/labels', './ball_output')
# crop_balls_from_yolo('/data01/migu/soccer-track/Yolov8_Formatted_DataSets/Roboflow/test/images', '/data01/migu/soccer-track/Yolov8_Formatted_DataSets/Roboflow/test/labels', './robo_ball_output')
crop_balls_from_yolo('/data01/migu/soccer-track/Yolov8_Formatted_DataSets/百度飞桨/final_dataset/images/val', '/data01/migu/soccer-track/Yolov8_Formatted_DataSets/百度飞桨/final_dataset/labels/val' ,'./baidu_ball_output')