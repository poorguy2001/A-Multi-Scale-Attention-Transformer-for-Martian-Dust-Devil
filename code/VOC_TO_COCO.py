# 仅依赖XML转JSON
import os
import json
import xml.etree.ElementTree as ET


# 将VOC格式的XML文件转换为COCO格式的JSON文件
def voc_to_coco(voc_dir, output_json):
    # 初始化COCO格式的字典结构
    coco = {
        "images": [],  # 存储图片的元数据信息
        "annotations": [],  # 存储目标物体的标注信息
        "categories": []  # 存储类别信息
    }

    # 类别名称到ID的映射字典
    category_set = {}
    category_item_id = 0
    annotation_id = 0
    image_id = 0

    # 函数：增加类别
    def add_category_item(name):
        nonlocal category_item_id
        category_item = {
            "supercategory": "none",  # 超类别（可不填）
            "id": category_item_id + 1,  # 类别ID（从1开始）
            "name": name  # 类别名称
        }
        coco['categories'].append(category_item)
        category_set[name] = category_item_id + 1
        category_item_id += 1

    # 函数：增加图片元数据
    def add_image_item(file_name, size):
        nonlocal image_id
        image_item = {
            "id": image_id + 1,  # 图片ID
            "file_name": file_name,  # 图片文件名
            "width": size['width'],  # 图片宽度
            "height": size['height']  # 图片高度
        }
        coco['images'].append(image_item)
        image_id += 1
        return image_id

    # 函数：增加目标物体的标注信息
    def add_annotation_item(image_id, category_id, bbox):
        nonlocal annotation_id
        annotation_item = {
            "id": annotation_id + 1,  # 标注ID
            "image_id": image_id,  # 对应的图片ID
            "category_id": category_id,  # 类别ID
            "bbox": bbox,  # 边界框（左上角x, 左上角y, 宽度, 高度）
            "area": bbox[2] * bbox[3],  # 面积
            "iscrowd": 0  # 是否为拥挤目标
        }
        coco['annotations'].append(annotation_item)
        annotation_id += 1

    # 读取所有XML文件
    for xml_file in os.listdir(voc_dir):
        if not xml_file.endswith('.xml'):
            continue

        # 解析XML文件
        xml_path = os.path.join(voc_dir, xml_file)
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # 获取图片的文件名
        file_name = root.find('filename').text

        # 获取图片的尺寸
        size = {
            'width': int(root.find('size/width').text),
            'height': int(root.find('size/height').text)
        }

        # 增加图片条目
        current_image_id = add_image_item(file_name, size)

        # 遍历每个目标物体
        for obj in root.findall('object'):
            # 获取目标物体的类别名称
            category_name = obj.find('name').text

            # 如果类别还没有出现在字典中，则添加类别
            if category_name not in category_set:
                add_category_item(category_name)

            category_id = category_set[category_name]

            # 获取目标物体的边界框（xmin, ymin, xmax, ymax）
            bbox = obj.find('bndbox')
            xmin = int(bbox.find('xmin').text)
            ymin = int(bbox.find('ymin').text)
            xmax = int(bbox.find('xmax').text)
            ymax = int(bbox.find('ymax').text)

            # 计算边界框的格式为 (左上角x, 左上角y, 宽度, 高度)
            o_width = xmax - xmin
            o_height = ymax - ymin
            bbox = [xmin, ymin, o_width, o_height]

            # 增加标注条目
            add_annotation_item(current_image_id, category_id, bbox)

    # 将转换结果保存为JSON文件
    with open(output_json, 'w') as f:
        json.dump(coco, f, indent=4)


# 指定VOC格式XML文件所在目录和输出的COCO格式JSON文件路径
voc_dir = ""
output_json = ""
voc_to_coco(voc_dir, output_json)
