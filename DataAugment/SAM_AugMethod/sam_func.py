"""
函数作用：
segment_balls_with_sam(input_folder, output_folder)
    对一个球文件夹中的球图片数据，使用ultralytics调用SAM模型进行分割并保存分割的结果。
    
接受一个根据分割出的mask，用随机的颜色填充mask。
"""

import os
from ultralytics import SAM
import numpy as np
from PIL import Image
from sam_ball import *
from cut_ball import *

def segment_balls_with_sam(input_folder, output_folder):
    """
    使用 Ultralytics 的 SAM 模型对球的图片进行分割并保存结果。

    :param input_folder: 输入图片文件夹路径
    :param output_folder: 输出分割结果保存路径
    """
    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)

    # 初始化 SAM 模型
    model = SAM('./models/sam_b.pt')

    # 遍历输入文件夹中的图片
    for image_file in os.listdir(input_folder):
        if image_file.endswith(('.jpg', '.png')):  # 支持的图片格式
            image_path = os.path.join(input_folder, image_file)
            save_path = os.path.join(output_folder, "sam_" + image_file)
            
            mask_post_process(model, image_path, save_extracted_image_path=save_path)


# 示例调用
# segment_balls_with_sam('./ball_output', './sam_ball')
segment_balls_with_sam('./data/baidu_ball_output', './data/sam_baidu_ball')