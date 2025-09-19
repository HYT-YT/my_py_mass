import os
import shutil

# 获取当前目录
current_dir = os.getcwd()

# 获取所有txt文件
txt_files = [file for file in os.listdir(current_dir) if file.endswith(".txt")]

for txt_file in txt_files:
    # 获取文件名和扩展名
    file_name, file_extension = os.path.splitext(txt_file)

    # 寻找类似的文件
    similar_files = [file for file in os.listdir(current_dir) if file.startswith(file_name + "_") and file.endswith(file_extension)]

    if similar_files:
        # 创建新目录
        new_dir = os.path.join(current_dir, file_name + "_files")
        os.makedirs(new_dir, exist_ok=True)

        # 移动文件
        for file in [txt_file] + similar_files:
            file_path = os.path.join(current_dir, file)
            new_file_path = os.path.join(new_dir, file)
            shutil.move(file_path, new_file_path)
