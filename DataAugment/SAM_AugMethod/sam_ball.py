"""
SAM分割球demo测试代码
"""

from ultralytics import SAM
import numpy as np
from PIL import Image, ImageDraw
import cv2

DEBUG = 0
def extract_region_from_mask(image, mask):
    """
    根据掩码从原始图像中提取特定区域，其他部分设置为白色。

    :param image: 原始图像
    :param mask: 二值化掩码
    :return: 提取后的图像
    """
    # 创建一个全白的图像
    result = np.ones_like(image) * 255  # 创建全白图像

    # 获取图像的高度和宽度
    height, width = mask.shape

    # 遍历每个像素
    for y in range(height):
        for x in range(width):
            if mask[y, x] == 255:  # 如果掩码为白色
                if DEBUG : print(str(x) + "  " + str(y))
                result[y, x] = image[y, x]  # 保留原图像的像素

    return result

def cv_create_binary_mask_from_points(points, image_size):
    """
    根据给定的点坐标生成二值化的掩码。

    :param points: 点坐标列表，格式为 [(x1, y1), (x2, y2), ...]
    :param image_size: 图像大小，格式为 (宽, 高)
    :return: 二值化的掩码图像
    """
    # 创建全黑的图像
    mask = np.zeros(image_size, dtype=np.uint8)  # 图像模式为单通道（灰度）

    # 将点坐标转换为整数类型
    points = np.array(points, dtype=np.int32)

    # 填充多边形
    cv2.fillPoly(mask, [points], 255)  # 255 表示白色

    return mask
def merge_masks(masks):
    """
    合并多个二值化掩码。

    :param masks: 掩码列表
    :return: 合并后的掩码
    """
    merged_mask = np.zeros_like(masks[0])  # 创建一个与第一个掩码相同大小的空白掩码
    for mask in masks:
        merged_mask = cv2.bitwise_or(merged_mask, mask)  # 合并掩码
    return merged_mask
def mask_post_process(model, image_path, save_extracted_image_path, save_merged_mask_path=None):
    # 使用 SAM 模型进行分割
    image = cv2.imread(image_path)
    h, w = image.shape[:2]
    try:
        results = model(image_path,points=[[w//2,h//2],[w//6,h//2],[w//6*5,h//2],[w//2,h//6],[w//2,h//6*5]],labels=[1,1,1,1,1])
    except:
        print("Error in processing image:", image_path)
        return 
    for result in results:
        masks = result.masks  # Masks object for segmentation masks outputs
        if DEBUG: print(len(masks.xy)) # mask数量
        
        binary_masks = [] # 将点集表示的mask转换成二值图表示的mask
        for i in range(len(masks.xy)):
            mask = masks.xy[i]
            binary_mask = cv_create_binary_mask_from_points(mask, (w,h))
            binary_masks.append(binary_mask)
        
        # 将多张二值图合并
        merged_mask = merge_masks(binary_masks)

        # 保存二值图
        if save_merged_mask_path is not None:
            cv2.imwrite(save_merged_mask_path, merged_mask)
        # 根据二值图从原始图像中提取目标
        extracted_image = extract_region_from_mask(image, merged_mask)
        # 保存目标图像
        cv2.imwrite(save_extracted_image_path, extracted_image)


if __name__ == "__main__":
    # Load a model
    model = SAM("sam_b.pt")
    # Display model information (optional)
    model.info()

    path = "/home/sxm/HomeWorkSpace/ballTrack/DataAugment/SAM_AugMethod/baidu_ball_output/1a1209e65c1b877c1c237efc672d2f69._ball_0.jpg"
    image = cv2.imread(path)
    h, w = image.shape[:2]

    # Segment with point prompt
    # results = model(path, points=[[960,530], [1340, 980], [1880,1170], [1160,1230],[880,520]], labels=[1,1,1,0,0])
    results = model(path,points=[[w//2,h//2],[w//6,h//2],[w//6*5,h//2],[w//2,h//6],[w//2,h//6*5]],labels=[1,1,1,1,1])
    # results = model(path)

    mask_post_process(results,"./save1.png","./test.png")