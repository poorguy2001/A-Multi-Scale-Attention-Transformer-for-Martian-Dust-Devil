

import os
import xml.etree.ElementTree as ET

# 输入路径
image_dir = r""
annotations_dir = r""
output_dir = r""
os.makedirs(output_dir, exist_ok=True)

# 类别映射
class_name = 'dust_devil'
class_id = 0  # 如果有多个类别，这里可以做一个字典映射

for filename in os.listdir(annotations_dir):
    if filename.endswith('.xml'):
        xml_file = os.path.join(annotations_dir, filename)
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # 获取图像文件名（不带后缀）
        image_filename = os.path.splitext(filename)[0]
        image_path = os.path.join(image_dir, f'{image_filename}.jpg')

        # 图像的宽和高
        width = int(root.find('size').find('width').text)
        height = int(root.find('size').find('height').text)

        # YOLO 标签保存路径
        output_path = os.path.join(output_dir, f'{image_filename}.txt')

        with open(output_path, 'w') as f_out:
            for obj in root.findall('object'):
                cls = obj.find('name').text.strip()
                # 如果有多个类别，可以用 dict 映射
                cid = class_id

                # 读取标注框
                xmin = int(float(obj.find('bndbox').find('xmin').text))
                ymin = int(float(obj.find('bndbox').find('ymin').text))
                xmax = int(float(obj.find('bndbox').find('xmax').text))
                ymax = int(float(obj.find('bndbox').find('ymax').text))

                # 保证顺序正确
                xmin, xmax = min(xmin, xmax), max(xmin, xmax)
                ymin, ymax = min(ymin, ymax), max(ymin, ymax)

                # 边界裁剪，防止超出图像范围
                xmin = max(0, min(xmin, width - 1))
                xmax = max(0, min(xmax, width - 1))
                ymin = max(0, min(ymin, height - 1))
                ymax = max(0, min(ymax, height - 1))

                # 转换成 YOLO 格式
                x_center = (xmin + xmax) / 2 / width
                y_center = (ymin + ymax) / 2 / height
                box_width = (xmax - xmin) / width
                box_height = (ymax - ymin) / height

                # 过滤掉无效框（宽高为 0 或负数）
                if box_width <= 0 or box_height <= 0:
                    print(f"⚠️ 跳过无效框: {filename}, {xmin, ymin, xmax, ymax}")
                    continue

                # 写入 YOLO 标签
                f_out.write(f"{cid} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}\n")

        print(f"✅ {image_filename}.txt 已保存到 {output_dir}")

print("🎯 所有 VOC → YOLO 标签转换完成！")
