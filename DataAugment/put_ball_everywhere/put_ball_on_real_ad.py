from PIL import Image
import os
import random
from PIL import Image
import sys
sys.path.append('..')
from AugmentMethod import apply_multiple_blurs, add_gaussian_noise_color
DEBUG = True

def read_annotations(file_path):
    boxes = []  # 用于存储框的列表

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()  # 读取所有行

        for line in lines:
            # 拆分行内容
            parts = line.strip().split(',')
            if len(parts) < 5:
                continue  # 跳过格式不正确的行
            
            # 解析坐标
            class_name = parts[0]  # 类别名称
            x1 = max(int(parts[1]), 0)  # 左上角 x 坐标，设置小于0的为0
            y1 = max(int(parts[2]), 0)  # 左上角 y 坐标，设置小于0的为0
            w = max(int(parts[3]), 0)  # 右下角 x 坐标，设置小于0的为0
            h = max(int(parts[4]), 0)  # 右下角 y 坐标，设置小于0的为0

            

            # 将框的信息存入 boxes 列表
            box = {
                'class': class_name,
                'x1': x1,
                'y1': y1,
                'w': w,
                'h': h
            }
            boxes.append(box)

    return boxes
    
def put_ball_everywhere(ball_image_path, background_image_path, background_label_path, output_image_path):
    # 加载球的图片
    # ball_image_path = './data/ball/4.png'  # 替换为你的球的图片路径
    ball_image = Image.open(ball_image_path).convert("RGBA")  # 确保使用 RGBA 模式
    noise_ratio = random.randint(0, 40)
    if noise_ratio <= 25: # [0,25]
        ball_image = add_gaussian_noise_color(ball_image, 0, noise_ratio)
    blur_ratio = random.randint(0, 160)
    if noise_ratio <= 120: # [10,120]
        ball_image = apply_multiple_blurs(ball_image, noise_ratio)
    # 等比例缩小为32像素
    ball_image.thumbnail((16, 16))

    # 读取1920x1080的背景图像
    # background_image_path = './data/background/b1.jpg'  # 替换为您的背景图像路径
    background = Image.open(background_image_path).convert("RGBA")  # 确保使用 RGBA 模式
    
    # 获取要copyPast的框
    boxes = read_annotations(background_label_path)
    random_box = random.choice(boxes)
    x1,y1,w,h = random_box['x1'], random_box['y1'], random_box['w'], random_box['h'] 
    # 随机选择粘贴位置
    max_x = w - ball_image.width
    max_y = h - ball_image.height
    random_x = random.randint(0, max_x) + x1
    random_y = random.randint(0, max_y) + y1

    # 粘贴球的图片到背景图像，保持透明度
    background.paste(ball_image, (random_x, random_y), ball_image)

    # 保存结果图像
    # output_image_path = 'output_image.png'  # 输出图像路径
    # background.save(output_image_path)
    background = background.convert("RGB")
    background.save(output_image_path, format="JPEG")

    if DEBUG : print(f"球的图片已随机粘贴到位置: ({random_x}, {random_y})")
    
    # 保存结果图像
    background.save(output_image_path)

    # 计算 YOLO 格式
    x_center = (random_x + ball_image.width / 2) / background.width
    y_center = (random_y + ball_image.height / 2) / background.height
    width = ball_image.width / background.width
    height = ball_image.height / background.height

    # 打印或保存 YOLO 格式标注
    yolo_annotation = f"{0} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
    if DEBUG : print(yolo_annotation)
    return yolo_annotation
    
"""
读取背景文件夹的所有图片，对于每个背景图片，随机从球文件夹中random选择一张球图片,
然后调用put_ball_everywhere函数，得到增强后的图片和yolo标注，将增强后的图片和标注
分别存储到输出图片文件夹和标注文件夹
"""
def process_images(background_folder, ball_folder, output_image_folder, output_annotation_folder):
    # 确保输出文件夹存在
    os.makedirs(output_image_folder, exist_ok=True)
    os.makedirs(output_annotation_folder, exist_ok=True)

    # 获取所有背景图像路径
    background_images = [f for f in os.listdir(background_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

    # 获取所有球图像路径
    ball_images = [f for f in os.listdir(ball_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

    for background_image in background_images:
        # 随机选择一张球图片
        ball_image = random.choice(ball_images)

        # 构建完整路径
        background_image_path = os.path.join(background_folder, background_image)
        background_label_path = os.path.join(background_folder, "../advertise_labels", os.path.splitext(background_image)[0] + '.txt')
        if not os.path.exists(background_label_path):
            print(f"{background_label_path} not exists")
            continue
        ball_image_path = os.path.join(ball_folder, ball_image)

        # 输出路径
        output_image_path = os.path.join(output_image_folder, background_image)
        output_annotation_path = os.path.join(output_annotation_folder, f"{os.path.splitext(background_image)[0]}.txt")

        # 调用函数并获取 YOLO 标注
        yolo_annotation = put_ball_everywhere(ball_image_path, background_image_path, background_label_path, output_image_path)

        # 保存 YOLO 标注到文件
        with open(output_annotation_path, 'w') as f:
            f.write(yolo_annotation + '\n')

if __name__ == "__main__":
    # 单独测试 put_ball_everywhere
    # put_ball_everywhere('./data/ball/4.png','./data/background/b1.jpg','output_image.png')
    
    # 批量生成
    # 示例调用
    background_folder = '/data01/migu/soccer-track/Yolov8_Formatted_DataSets_Augmented/Roboflow/test/images/'  # 背景图片文件夹
    ball_folder = './data/ball/white'              # 球图片文件夹
    output_image_folder = './real_ad_output10/images'   # 输出图片文件夹
    output_annotation_folder = './real_ad_output10/labels'  # 输出标注文件夹

    process_images(background_folder, ball_folder, output_image_folder, output_annotation_folder)