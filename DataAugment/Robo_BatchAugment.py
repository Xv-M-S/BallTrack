import os
import random
from PIL import Image
import numpy as np
from pathlib import Path
from AugmentMethod import *
import cv2
import numpy as np


def process_dataset(data_dir, output_dir, times=1):
    """处理数据集并进行数据增强"""
    image_dir = os.path.join(data_dir, 'images')
    label_dir = os.path.join(data_dir, 'labels')
    output_image_dir = os.path.join(output_dir, 'images')
    output_label_dir = os.path.join(output_dir, 'labels')

    if not os.path.exists(output_image_dir):
        os.makedirs(output_image_dir)
    if not os.path.exists(output_label_dir):
        os.makedirs(output_label_dir)

      

    for img_file in os.listdir(image_dir):
        img_path = os.path.join(image_dir, img_file)
        label_path = os.path.join(label_dir, os.path.splitext(img_file)[0] + '.txt')
        output_img_path = os.path.join(output_image_dir, img_file)
        

        # 读取标注
        with open(label_path, 'r') as f:
            labels = [line.strip().split() for line in f.readlines()]

        # 对每个目标区域进行数据增强
        for _ in range(times):
            for label in labels:
                # 读取图像
                image = Image.open(img_path)
                # 裁剪区域
                wh, ht = image.size
                # print(label)
                bx,by,sx,sy = float(label[1]),float(label[6]),float(label[3]),float(label[4])
                class_id, x, y, w, h = int(label[0]),float(bx+sx)/2,float(by+sy)/2,float(bx-sx),float(by-sy)
                x, y, w, h = int(x * wh), int(y * ht), int(w * wh), int(h * ht)
                bbox = (x - w // 2, y - h // 2, w, h)
                # 裁剪图像
                left,top,right,bottom = bbox[0],bbox[1],bbox[0]+bbox[2],bbox[1]+bbox[3]
                cropped_image = image.crop((left, top, right, bottom))
                cropped_image = cropped_image.convert("RGB")
                opencv_image = cv2.cvtColor(np.array(cropped_image), cv2.COLOR_RGB2BGR)
                cv2.imwrite('output_image.jpg', opencv_image)

                # 应用数据增强
                aug_func = random.choice([
                    ellipse_image, add_gaussian_noise, add_gaussian_noise_color,
                    blur_image, Gaussian_blur_image, apply_multiple_blurs,add_random_patch
                ])
                try:
                    fill_color = (
                        (image.getpixel((left + 2, top + 2))[0] + image.getpixel((right - 2, bottom - 2))[0]) // 2,
                        (image.getpixel((left + 2, top + 2))[1] + image.getpixel((right - 2, bottom - 2))[1]) // 2,
                        (image.getpixel((left + 2, top + 2))[2] + image.getpixel((right - 2, bottom - 2))[2]) // 2
                    )
                except:
                    fill_color = (0,128,0)
                # print("fill_color:" + str(fill_color))
                if aug_func == ellipse_image:
                    # print("aug_func:" + str(aug_func))
                    aug_func("output_image.jpg", "aug_output_image.jpg",fill_color)
                else:
                    aug_func("output_image.jpg", "aug_output_image.jpg")

                # 保存增强后的图像和标注
                img = Image.open("aug_output_image.jpg")
                width, height = img.size

                aug_img_name = f"{Path(img_file).stem}_{random.randint(0, 99999)}.jpg"
                aug_img_path = os.path.join(output_image_dir, aug_img_name)
                output_label_name = f"{Path(aug_img_name).stem}.txt"
                output_label_path = os.path.join(output_label_dir, output_label_name)
                # print(aug_img_path)
                # print(output_label_path)
                black_rectangle = Image.new("RGB", (right - left, bottom - top), (0, 0, 0))
                image.paste(black_rectangle, (left, top))
                image.paste(img, (x-width//2, y-height//2))
                opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                cv2.imwrite(aug_img_path, opencv_image)
                
                line = f"{class_id} {x / wh} {y / ht} {width / wh} {height / ht}\n"
                with open(output_label_path, 'w') as f:
                    f.write(line)

if __name__ == '__main__':
    data_dir = '/data01/migu/soccer-track/Yolov8_Formatted_DataSets/Roboflow/valid'
    output_dir = '/data01/migu/soccer-track/Yolov8_Formatted_DataSets_Augmented/Roboflow/valid'
    process_dataset(data_dir, output_dir, times=1)
    os.system("rm output_image.jpg aug_output_image.jpg")