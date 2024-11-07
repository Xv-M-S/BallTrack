from PIL import Image
import os
import random
from PIL import Image
DEBUG = True
def put_ball_everywhere(ball_image_path,background_image_path,output_image_path,box):
    # 加载球的图片
    ball_image = Image.open(ball_image_path).convert("RGBA")  # 确保使用 RGBA 模式

    # 等比例缩小为32像素
    ball_image.thumbnail((16, 16))

    # 读取1920x1080的背景图像
    # background_image_path = './data/background/b1.jpg'  # 替换为您的背景图像路径
    background = Image.open(background_image_path).convert("RGBA")  # 确保使用 RGBA 模式

    # 随机选择粘贴位置
    ad_x, ad_y, ad_width, ad_height = box[0],box[1],box[2],box[3]
    max_x = ad_width - ball_image.width
    max_y = ad_height - ball_image.height
    random_x = random.randint(0, max_x)
    random_y = random.randint(0, max_y)

    # 粘贴球的图片到背景图像，保持透明度
    background.paste(ball_image, (ad_x + random_x, ad_y + random_y), ball_image)

    # 保存结果图像
    # output_image_path = 'output_image.png'  # 输出图像路径
    # background.save(output_image_path)
    background = background.convert("RGB")
    background.save(output_image_path, format="JPEG")

    if DEBUG : print(f"球的图片已随机粘贴到位置: ({random_x}, {random_y})")
    
    # 保存结果图像
    background.save(output_image_path)

    # 计算 YOLO 格式
    ball_x,ball_y = random_x + ad_x, random_y + ad_y
    x_center = (ball_x + ball_image.width / 2) / background.width
    y_center = (ball_y + ball_image.height / 2) / background.height
    width = ball_image.width / background.width
    height = ball_image.height / background.height

    # 打印或保存 YOLO 格式标注
    yolo_annotation = f"{0} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
    if DEBUG : print(yolo_annotation)
    return yolo_annotation


"""
将广告的图片粘贴到背景图像上，并返回广告图片在背景中的位置和背景的大小。
返回广告图片在球场中的位置。
广告大小如果超过480，则resize到480
"""
def put_advertise_everywhere(advertise_image_path,background_image_path,output_image_path):
    # 加载广告的图片
    advertise_image = Image.open(advertise_image_path).convert("RGBA")  # 确保使用 RGBA 模式
    # 获取当前大小
    width, height = advertise_image.size
    # 检查是否需要调整大小
    if width > 480 or height > 480:
        # 计算新的宽高
        if width > height:
            new_width = 480
            new_height = int((480 / width) * height)
        else:
            new_height = 480
            new_width = int((480 / height) * width)
        
        # 调整图像大小
        advertise_image = advertise_image.resize((new_width, new_height), Image.LANCZOS)
    # 读取1920x1080的背景图像
    background = Image.open(background_image_path).convert("RGBA")  # 确保使用 RGBA 模式

    # 随机选择粘贴位置
    max_x = background.width - advertise_image.width
    max_y = background.height - advertise_image.height
    random_x = random.randint(0, max_x)
    random_y = random.randint(0, max_y)

    # 粘贴广告的图片到背景图像，保持透明度
    background.paste(advertise_image, (random_x, random_y), advertise_image)

    # 保存结果图像
    background = background.convert("RGB")
    background.save(output_image_path, format="JPEG")

    if DEBUG : print(f"广告的图片已随机粘贴到位置: ({random_x}, {random_y})")
    
    # 保存结果图像
    background.save(output_image_path)

    # 返回广告图片在球场中的位置
    box = (random_x,random_y,advertise_image.width,advertise_image.height)
    return box
    
"""
读取背景文件夹的所有图片，对于每个背景图片，随机从球文件夹中random选择一张球图片,
然后调用put_ball_everywhere函数，得到增强后的图片和yolo标注，将增强后的图片和标注
分别存储到输出图片文件夹和标注文件夹
"""
def process_images(background_folder, ball_folder, ad_folder,output_image_folder, output_annotation_folder):
    # 确保输出文件夹存在
    os.makedirs(output_image_folder, exist_ok=True)
    os.makedirs(output_annotation_folder, exist_ok=True)

    # 获取所有背景图像路径
    background_images = [f for f in os.listdir(background_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

    # 获取所有球图像路径
    ball_images = [f for f in os.listdir(ball_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

    # 获取所有广告图片
    ad_images = [f for f in os.listdir(ad_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

    for background_image in background_images:
        # 随机选择一张球图片
        ball_image = random.choice(ball_images)
        # 随机选择一张广告图片
        ad_image = random.choice(ad_images)

        # 构建完整路径
        background_image_path = os.path.join(background_folder, background_image)
        ball_image_path = os.path.join(ball_folder, ball_image)
        ad_image_path = os.path.join(ad_folder, ad_image)

        # 输出路径
        output_ad_path = "./data/temp/tmp.png"
        output_image_path = os.path.join(output_image_folder, background_image)
        output_annotation_path = os.path.join(output_annotation_folder, f"{os.path.splitext(background_image)[0]}.txt")

        # 获取广告合成图片及其位置
        box = put_advertise_everywhere(ad_image_path, background_image_path, output_ad_path)
        # 调用函数并获取 YOLO 标注
        yolo_annotation = put_ball_everywhere(ball_image_path, output_ad_path, output_image_path, box)

        # 保存 YOLO 标注到文件
        with open(output_annotation_path, 'w') as f:
            f.write(yolo_annotation + '\n')

if __name__ == "__main__":
    # 单独测试 put_advertise_everywhere
    # box = put_advertise_everywhere('./data/advertise/test_ReCTS_task3_and_task_4_001332.jpg','./data/background/b1.jpg','mixback_image.png')
    # put_ball_everywhere("./data/ball/1.png",'mixback_image.png','output_image.png',box)
    # 批量生成
    # 示例调用
    background_folder = '/data01/migu/soccer-track/BallDataSets/ballIn_and_ballOut/train/images/'  # 背景图片文件夹
    ball_folder = './data/ball'              # 球图片文件夹
    ad_folder = '/data01/migu/soccer-track/Yolov8_Formatted_DataSets/ReCTS_test_part1/Task3_and_Task4/img' # 广告图片文件夹
    output_image_folder = './ad_output/images'   # 输出图片文件夹
    output_annotation_folder = './ad_output/labels'  # 输出标注文件夹

    process_images(background_folder, ball_folder, ad_folder, output_image_folder, output_annotation_folder)