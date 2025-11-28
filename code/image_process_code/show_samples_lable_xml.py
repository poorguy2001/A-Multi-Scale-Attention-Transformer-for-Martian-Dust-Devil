import os
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image
from PIL import ImageDraw
from skimage import io


def convert_annotation(img_xml_1):
    in_file = open(img_xml_1, encoding='utf-8')

    tree = ET.parse(in_file)
    root = tree.getroot()
    b_list = []
    for obj in root.iter('object'):
        difficult = 0
        if obj.find('difficult') != None:
            difficult = obj.find('difficult').text
        cls = obj.find('name').text

        xmlbox = obj.find('bndbox')
        b = (int(float(xmlbox.find('xmin').text)), int(float(xmlbox.find('ymin').text)),
             int(float(xmlbox.find('xmax').text)), int(float(xmlbox.find('ymax').text)), 0)
        # list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str("0"))
        b_list.append(b)
    return b_list


if __name__ == "__main__":


    root_directory = ""
    xml_ori_path = root_directory + '/Annotations'
    img_ori_path = root_directory + '/JPEGImages'
    # 获取图片的 .jpg 和 xml 文件的列表
    img_list = os.listdir(img_ori_path)
    xml_list = os.listdir(xml_ori_path)

    # 获取.jpg 和 xml 文件的地址
    xml_list_path = [xml_ori_path + '/' + i for i in xml_list]
    img_list_path = [img_ori_path + '/' + i for i in img_list]

    # 是否以图片的形式显示标签
    show_effect = True
    # print("img_list_path", img_list_path)
    save_path = root_directory + '/label_show'

    # ############  生成标签显示的图片
    if show_effect:
        for i_index, i in enumerate(img_list):  # i 是单张图片的名字

            i_path = img_ori_path + '/' + i # 单张图片的路径
            j = i.split('.')[0]     # 获取单张。jpg 前的名字
            xml_path_i = xml_ori_path + '/' + j + '.xml'
            xml = convert_annotation(xml_path_i)    # 获取对应图片的标签的位置信息

            img = io.imread(i_path)
            img_nrm = (img - np.min(img)) / (np.max(img) - np.min(img))  # 归一化处理
            # #array 转Image 对象
            img = Image.fromarray(np.uint8(255 * img_nrm))
            ##############################################################
            img = img.convert('RGB')

            progress = round(i_index * 100 / (len(img_list) + 1), 2)  # 计算整除用来计算进度
            bar = '=' * (int(progress) // 5) + '>' + ' ' * (20 - int(progress) // 5)  # 将进度分为20份，再逐步填充
            print('\rProgress:[{}] {} %'.format(bar, progress), end='', flush=True)  # flush 为 True 表示 清空缓存

            for i in xml:
                # ########## 圈定位置 ########################################################################
                draw = ImageDraw.Draw(img)

                # 图上画圆圈 左上角的坐标作为(0, 0)点，也就是cut_size[0], cut_size[1], i其实也就是坑的[x min, y min, x max, y max, 0]
                draw.rectangle((i[0], i[1], i[2], i[3]), fill=None, outline='red', width=2)  # 这是在截取图片的基础上画图的,p[2]是半径
            # print(img.size)

            img.save(save_path + '/' + j + '.jpg')  # 保存文件的名字的标签


