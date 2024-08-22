from PIL import Image
import cv2
import numpy as np

def resize_and_pad(image_path, output_size=(32, 32)):
    """
    将图片等比例缩放并补充空白至指定尺寸。
    
    参数:
    image_path (str): 输入图片的文件路径
    output_size (tuple): 输出图片的尺寸，默认为 (32, 32)
    
    返回:
    numpy.ndarray: 处理后的图片数据
    """
    # 读取图片
    image = cv2.imread(image_path)
    
    # 计算缩放比例
    height, width, _ = image.shape
    scale = min(output_size[0] / width, output_size[1] / height)
    new_size = (int(width * scale), int(height * scale))
    
    # 缩放图片
    resized_image = cv2.resize(image, new_size, interpolation=cv2.INTER_LANCZOS4)
    
    # 创建新的图片并填充空白
    new_image = np.full((output_size[1], output_size[0], 3), 255, dtype=np.uint8)
    x = (output_size[0] - new_size[0]) // 2
    y = (output_size[1] - new_size[1]) // 2
    new_image[y:y+new_size[1], x:x+new_size[0]] = resized_image
    
    return new_image