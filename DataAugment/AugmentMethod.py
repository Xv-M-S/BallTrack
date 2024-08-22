from PIL import Image,ImageFilter
import numpy as np
import imageio
"""
椭球化图片
@ param image_path: 原始图片路径
@ param output_path: 输出图片路径
@ param ratio: 宽压缩比例
@ param angle: 旋转角度
@ return rotated_img: 旋转后的图片
"""
def ellipse_image(image_path, output_path,ratio=0.5,angle=30):
    # 加载原始图片
    img = Image.open(image_path)

    # 计算变换后图像的尺寸
    new_width = img.width
    new_height = int(img.height / ratio + 1)

    # 创建一个新图像，尺寸与变换后的图像相同
    new_img = Image.new('RGB', (img.width * 10, img.height * 10), (255, 255, 255))

    # 定义透视变换矩阵，压缩y轴
    transform_matrix = (
        1, 0, 0,
        0, ratio, 0,
        0, 0, 1
    )

    # 使用transform方法应用变换
    transformed_img = img.transform((new_width, new_height), Image.Transform.AFFINE, transform_matrix[:6], resample=Image.BICUBIC)
    # 裁剪图片
    cropped_img = transformed_img.crop((0, 0, new_width, new_height))
    # 保存裁剪后的图片
    # 缩放图片，保持长宽比
    max_size = (int(new_width*ratio), int(new_height*ratio))
    cropped_img.thumbnail(max_size, Image.Resampling.LANCZOS)
    # cropped_img.save(output_path)
    # 旋转图片
    rotated_img = cropped_img.rotate(angle, expand=True)
    rotated_img.save(output_path)
    return rotated_img

"""
灰度图添加高斯噪声
@ param image_path: 原始图片路径
@ param output_path: 输出图片路径
@ param mean: 均值
@ param std_dev: 标准差
@ return noisy_img: 噪声添加后的图片
"""
def add_gaussian_noise(image_path, output_path, mean=0, std_dev=15):
    # 加载图片
    img = Image.open(image_path).convert('L')  # 转换为灰度图像以便处理
    img_array = np.array(img)

    # 生成与图像尺寸相同的高斯噪声
    noise = np.random.normal(mean, std_dev, img_array.shape).astype('uint8')

    # 将噪声添加到图像上
    noisy_img_array = np.clip(img_array + noise, 0, 255).astype('uint8')

    # 将数组转换回图像并保存
    noisy_img = Image.fromarray(noisy_img_array)
    noisy_img.save(output_path)
    return noisy_img

"""
彩色图片添加高斯噪声
@ param image_path: 原始图片路径
@ param output_path: 输出图片路径
@ param mean: 均值
@ param std_dev: 标准差
@ return noisy_img: 噪声添加后的图片
"""
def add_gaussian_noise_color(image_path, output_path, mean=0, std_dev=15):
    # 加载彩色图像
    img = Image.open(image_path)

    # 将图像转换为numpy数组
    img_array = np.array(img)

    # 获取图像的高度、宽度和通道数
    height, width, channels = img_array.shape

    # 为每个通道生成高斯噪声
    noise = np.random.normal(mean, std_dev, size=(height, width, channels))

    # 将噪声添加到图像上
    noisy_img_array = np.clip(img_array + noise, 0, 255)

    # 将数组转换回uint8类型
    noisy_img_array = noisy_img_array.astype(np.uint8)

    # 将数组转换回图像并保存
    noisy_img = Image.fromarray(noisy_img_array)
    noisy_img.save(output_path)
    return noisy_img

"""
模糊图片
@ param image_path: 原始图片路径
@ param output_path: 输出图片路径
@ return blurred_img: 模糊后的图片
"""
def blur_image(image_path, output_path):
    # 打开图片
    img = Image.open(image_path)
    # 定义一个3x3的模糊核
    blur_kernel = [
        [1/9, 1/9, 1/9],
        [1/9, 1/9, 1/9],
        [1/9, 1/9, 1/9]
    ]
    blur_kernel_flattened = [item for sublist in blur_kernel for item in sublist]
    # 应用模糊滤镜
    blurred_img = img.filter(ImageFilter.Kernel(size=(3, 3), kernel=blur_kernel_flattened, scale=1))

    # 保存模糊后的图片
    blurred_img.save(output_path)
    return blurred_img

"""
高斯核模糊图片
@ param image_path: 原始图片路径
@ param output_path: 输出图片路径
@ radius: 模糊半径
@ return blurred_img: 模糊后的图片
"""
def Gaussian_blur_image(image_path, output_path,radius=5):
    img = Image.open(image_path)
    blurred_img = img.filter(ImageFilter.GaussianBlur(radius=radius))  # radius可以根据需要调整
    blurred_img.save(output_path)
    return blurred_img

"""
多层次模糊图片
@ param image_path: 原始图片路径
@ param output_path: 输出图片路径
@ num blurs: 模糊次数
@ return image: 模糊后的图片
"""
def apply_multiple_blurs(image_path, output_path, num_blurs=5):
    # 打开图片
    image = Image.open(image_path)
    for _ in range(num_blurs):
        image = image.filter(ImageFilter.BLUR)
    image.save(output_path)
    return image

"""
创建GIF
@ param image_list: 图片列表
@ param gif_name: GIF文件名
@ param duration: GIF播放时间间隔
"""
def create_gif(image_list, gif_name, duration=1.0):
    frames = []
    for image in image_list:
        frames.append(image)
    imageio.mimsave(gif_name, frames, 'GIF', duration=duration)
    return 

"""
用于将图像调整到相同大小的函数
@ param img: 原始图片
@ param size: 输出图片的大小
@ return new_img: 调整后的图片
"""
def pad_image(img, size=(200, 200), color=(255, 255, 255)):
    x, y = img.size
    new_img = Image.new('RGB', size, color)
    new_img.paste(img, ((size[0]-x)//2, (size[1]-y)//2))
    return new_img

if __name__ == "__main__":
    # 放缩和旋转处理
    ellipse_image('./TestData/1.jpg', './TestData/1_ellipse.jpg', 0.3,45)
    # 加噪声处理
    add_gaussian_noise('./TestData/1.jpg', './TestData/noisy_image.jpg', mean=0, std_dev=15)
    add_gaussian_noise_color('./TestData/6.jpg', './TestData/noisy_color_image.jpg', mean=0, std_dev=40)
    # 图片模糊处理算法
    blur_image('./TestData/1.jpg', './TestData/blurred_image.jpg')
    Gaussian_blur_image('./TestData/1.jpg', './TestData/Gaussian_blurred_image.jpg',10)
    apply_multiple_blurs('./TestData/1.jpg', './TestData/multiple_blurred_image.jpg', 20)

    ellipse_img_list = list()
    add_gaussian_noise_img_list = list()
    Gaussian_blur_img_list = list()
    for i in range(1,10):
        ellipse_img = ellipse_image('./TestData/1.jpg', './TestData/ellipse_image.jpg', i/10,45)
        ellipse_img = pad_image(ellipse_img, size=(2000, 2000), color=(255, 255, 255))
        ellipse_img_list.append(ellipse_img)
        print("fine")
    for i in range(1,180,10):
        ellipse_img = ellipse_image('./TestData/1.jpg', './TestData/ellipse_image.jpg', 0.4,i)
        ellipse_img = pad_image(ellipse_img, size=(2000, 2000), color=(255, 255, 255))
        ellipse_img_list.append(ellipse_img)
    
    for i in range(0,200,10):
        add_gaussian_noise_img = add_gaussian_noise_color('./TestData/6.jpg', './TestData/add_gaussian_noise_image.jpg', mean=0, std_dev=i)
        add_gaussian_noise_img_list.append(add_gaussian_noise_img)
    for i in range(0,30,1):
        gaussian_blur_img = Gaussian_blur_image('./TestData/1.jpg', './TestData/Gaussian_blur_image.jpg',i)
        Gaussian_blur_img_list.append(gaussian_blur_img)
    create_gif(ellipse_img_list, r'ellipse.gif')
    create_gif(add_gaussian_noise_img_list, r'add_gaussian_noise.gif')
    create_gif(Gaussian_blur_img_list, r'Gaussian_blur.gif')




