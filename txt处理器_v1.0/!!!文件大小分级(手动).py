import os
import shutil

# 获取当前目录
current_dir = os.getcwd()

# 设置文件大小阈值（单位：KB）
threshold_size_kb = 50

# 获取所有txt文件
txt_files = [file for file in os.listdir(current_dir) if file.endswith(".txt")]
for txt_file in txt_files:
    # 获取文件大小
    file_size_kb = os.path.getsize(os.path.join(current_dir, txt_file)) / 1024

    # 如果文件大小小于阈值，移动文件到对应大小的目录
    if file_size_kb < threshold_size_kb:
        # 创建对应大小的目录
        target_dir = os.path.join(current_dir, f"{int(threshold_size_kb)}kb")
        os.makedirs(target_dir, exist_ok=True)

        # 移动文件
        file_path = os.path.join(current_dir, txt_file)
        new_file_path = os.path.join(target_dir, txt_file)
        shutil.move(file_path, new_file_path)
