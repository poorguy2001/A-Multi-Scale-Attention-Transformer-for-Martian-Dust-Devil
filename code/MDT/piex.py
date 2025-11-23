import os


img_width, img_height = 640, 640

# 标签路径
label_dirs = [
    r"E:/MDT/datasets/MDD-Human/labels/train",
    r"E:/MDT/datasets/MDD-Human/labels/val",
    r"E:/MDT/datasets/MDD-Human/labels/test"
]

# 存储所有目标框的像素面积
all_areas = []

# 遍历三个数据集文件夹
for label_dir in label_dirs:
    for file in os.listdir(label_dir):
        if file.endswith('.txt'):
            file_path = os.path.join(label_dir, file)
            with open(file_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    parts = line.strip().split()
                    if len(parts) == 5:
                        _, _, _, w_rel, h_rel = map(float, parts)
                        w_px = w_rel * img_width
                        h_px = h_rel * img_height
                        area = w_px * h_px
                        all_areas.append(area)

# 输出统计结果
if all_areas:
    min_area = min(all_areas)
    max_area = max(all_areas)
    print(f"共检测到 {len(all_areas)} 个目标。")
    print(f"最小目标像素面积：{min_area:.2f} px²")
    print(f"最大目标像素面积：{max_area:.2f} px²")
else:
    print("未检测到任何目标。")
