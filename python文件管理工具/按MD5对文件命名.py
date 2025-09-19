import os
import hashlib

def get_file_md5_prefix(file_path, prefix_length=16, chunk_size=4096):  # 16位MD5前缀
    """计算文件的MD5值并返回前N位"""
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            md5_hash.update(chunk)
    full_md5 = md5_hash.hexdigest()
    return full_md5[:prefix_length]  # 返回前16位

def main():
    # 获取当前脚本的文件名（用于排除自身）
    script_name = os.path.basename(__file__)
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 存储已生成的文件名（用于检测重复）
    used_names = set()
    
    # 遍历目录下的所有文件
    for file_name in os.listdir(current_dir):
        # 排除自身
        if file_name == script_name:
            continue
        
        file_path = os.path.join(current_dir, file_name)
        # 只处理文件（不处理目录）
        if not os.path.isfile(file_path):
            continue
        
        # 获取文件扩展名
        _, ext = os.path.splitext(file_name)
        
        # 计算MD5前16位
        md5_prefix = get_file_md5_prefix(file_path)
        new_name = f"{md5_prefix}{ext}"  # 新文件名（MD5前16位+原扩展名）
        new_path = os.path.join(current_dir, new_name)
        
        # 检查是否重复
        if new_name in used_names:
            print(f"警告：文件名重复！文件 '{file_name}' 计算出的MD5前16位为 '{md5_prefix}'，与已存在文件冲突，请手动处理")
            continue
        
        # 执行重命名
        os.rename(file_path, new_path)
        print(f"已重命名：'{file_name}' -> '{new_name}'")
        used_names.add(new_name)

if __name__ == "__main__":
    main()
    
