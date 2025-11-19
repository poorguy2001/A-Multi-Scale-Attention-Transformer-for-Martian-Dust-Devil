import cv2
import os

def draw_labels(image, labels, class_names):
    height, width = image.shape[:2]

    for line in labels:
        parts = line.strip().split()
        class_id = int(parts[0])
        x_center = float(parts[1]) * width
        y_center = float(parts[2]) * height
        box_width = float(parts[3]) * width
        box_height = float(parts[4]) * height

        x_min = int(x_center - box_width / 2)
        y_min = int(y_center - box_height / 2)

        # 绘制矩形框
        cv2.rectangle(image, (x_min, y_min), (x_min + int(box_width), y_min + int(box_height)), (0, 255, 0), 2)

        # 绘制类别标签
        label = class_names[class_id]
        cv2.putText(image, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return image

def process_directory(img_dir, label_dir, output_dir, class_names):
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 遍历图像文件
    for img_file in os.listdir(img_dir):
        img_path = os.path.join(img_dir, img_file)
        label_path = os.path.join(label_dir, img_file.replace('.jpg', '.txt'))

        if os.path.exists(label_path):
            image = cv2.imread(img_path)
            with open(label_path, 'r') as file:
                labels = file.readlines()

            labeled_image = draw_labels(image, labels, class_names)

            # 显示图像
            # cv2.imshow('Labeled Image', labeled_image)
            # cv2.waitKey(1)

            # 或者保存图像
            output_path = os.path.join(output_dir, img_file)
            cv2.imwrite(output_path, labeled_image)

    # cv2.destroyAllWindows()

# 类别名称列表，根据实际情况修改
class_names = ['']

# 文件夹路径
img_dir = r''
label_dir = r''
output_dir = r''

# 处理目录
process_directory(img_dir, label_dir, output_dir, class_names)
