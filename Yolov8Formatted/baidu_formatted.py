import os
import xml.etree.ElementTree as ET
import shutil

# 定义类别字典
labels_dict = {
    'football': 0
}
# 输入和输出目录
input_dir = '/data01/migu/soccer-track/BallDataSets/百度飞桨/strong_dataset'
output_dir = '/data01/migu/soccer-track/Yolov8_Formatted_DataSets/百度飞桨/strong_dataset'

# 创建输出目录结构
os.makedirs(os.path.join(output_dir, 'images', 'train'), exist_ok=True)
os.makedirs(os.path.join(output_dir, 'images', 'val'), exist_ok=True)
os.makedirs(os.path.join(output_dir, 'labels', 'train'), exist_ok=True)
os.makedirs(os.path.join(output_dir, 'labels', 'val'), exist_ok=True)

# 读取训练和验证列表
with open(os.path.join(input_dir, 'train_list.txt'), 'r') as f:
    train_list = [line.strip().split() for line in f]
with open(os.path.join(input_dir, 'val_list.txt'), 'r') as f:
    val_list = [line.strip().split() for line in f]

# 转换标注格式并保存
for img_path, anno_path in train_list:
    img_name = os.path.basename(img_path)
    new_img_path = os.path.join(output_dir, 'images', 'train', img_name)
    new_label_path = os.path.join(output_dir, 'labels', 'train', os.path.splitext(img_name)[0] + '.txt')
    
    # 复制图片文件
    try:
        shutil.copy2(os.path.join(input_dir, img_path), new_img_path)
    except FileNotFoundError:
        print(f"Error copying file: {img_path}")
        continue
    
    # 转换标注格式并保存
    tree = ET.parse(os.path.join(input_dir, anno_path))
    root = tree.getroot()
    width = int(root.find('size/width').text)
    height = int(root.find('size/height').text)
    with open(new_label_path, 'w') as f:
        for obj in root.findall('object'):
            class_name = obj.find('name').text
            class_id = int(labels_dict[class_name])
            xmin = int(obj.find('bndbox/xmin').text)
            ymin = int(obj.find('bndbox/ymin').text)
            xmax = int(obj.find('bndbox/xmax').text)
            ymax = int(obj.find('bndbox/ymax').text)
            x = (xmin + xmax) / 2 / width
            y = (ymin + ymax) / 2 / height
            w = (xmax - xmin) / width
            h = (ymax - ymin) / height
            f.write(f'{class_id} {x:.6f} {y:.6f} {w:.6f} {h:.6f}\n')

# 验证集处理
for img_path, anno_path in val_list:
    img_name = os.path.basename(img_path)
    new_img_path = os.path.join(output_dir, 'images', 'val', img_name)
    new_label_path = os.path.join(output_dir, 'labels', 'val', os.path.splitext(img_name)[0] + '.txt')
    
    # 复制图片文件
    try:
        shutil.copy2(os.path.join(input_dir, img_path), new_img_path)
    except FileNotFoundError:
        print(f"Error copying file: {img_path}")
        continue
    
    # 转换标注格式并保存
    tree = ET.parse(os.path.join(input_dir, anno_path))
    root = tree.getroot()
    width = int(root.find('size/width').text)
    height = int(root.find('size/height').text)
    with open(new_label_path, 'w') as f:
        for obj in root.findall('object'):
            class_name = obj.find('name').text
            class_id = int(labels_dict[class_name])
            xmin = int(obj.find('bndbox/xmin').text)
            ymin = int(obj.find('bndbox/ymin').text)
            xmax = int(obj.find('bndbox/xmax').text)
            ymax = int(obj.find('bndbox/ymax').text)
            x = (xmin + xmax) / 2 / width
            y = (ymin + ymax) / 2 / height
            w = (xmax - xmin) / width
            h = (ymax - ymin) / height
            f.write(f'{class_id} {x:.6f} {y:.6f} {w:.6f} {h:.6f}\n')