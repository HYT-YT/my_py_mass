import os
import hashlib
import random
from multiprocessing import Pool, cpu_count

def calculate_md5(file_path, block_size=65536):
    """计算文件的MD5哈希值，支持大文件"""
    md5 = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            while True:
                block = f.read(block_size)  # 分块读取，避免占用过多内存
                if not block:
                    break
                md5.update(block)
        return md5.hexdigest()
    except Exception as e:
        print(f"计算文件 {file_path} 的MD5时出错: {str(e)}")
        return None

def get_all_files(exclude_file):
    """获取当前目录下所有文件（除自身外），不限制后缀名"""
    all_files = []
    for file in os.listdir('.'):
        if file == exclude_file:
            continue  # 排除脚本自身
        if os.path.isfile(file):
            all_files.append(file)
    return all_files

def process_file(file):
    """处理单个文件，返回(文件名, MD5值)"""
    md5 = calculate_md5(file)
    return (file, md5) if md5 else None

def find_duplicate_files(all_files):
    """通过MD5值查找重复文件组"""
    print(f"使用 {cpu_count()} 个进程计算文件MD5值（支持大文件）...")
    with Pool(cpu_count()) as pool:
        results = pool.map(process_file, all_files)
    
    # 过滤无效结果并构建MD5-文件映射
    file_md5 = {file: md5 for file, md5 in results if md5 is not None}
    md5_groups = {}
    for file, md5 in file_md5.items():
        if md5 not in md5_groups:
            md5_groups[md5] = []
        md5_groups[md5].append(file)
    
    # 筛选出重复文件组（包含2个及以上文件）
    duplicate_groups = [sorted(group) for group in md5_groups.values() if len(group) > 1]
    return duplicate_groups

def delete_duplicates(duplicate_groups):
    """删除重复文件，每组保留一个随机文件"""
    deleted_count = 0
    for group in duplicate_groups:
        # 随机选择一个保留，其余删除
        keep = random.choice(group)
        to_delete = [f for f in group if f != keep]
        for file in to_delete:
            try:
                os.remove(file)
                print(f"已删除: {file}")
                deleted_count += 1
            except Exception as e:
                print(f"删除文件 {file} 失败: {str(e)}")
    print(f"\n操作完成，共删除 {deleted_count} 个重复文件")

if __name__ == "__main__":
    script_name = os.path.basename(__file__)
    print(f"正在扫描当前目录所有文件（除自身 {script_name} 外）...")
    
    all_files = get_all_files(script_name)
    if not all_files:
        print("目录下没有其他文件可对比")
        exit()
    
    print(f"找到 {len(all_files)} 个文件，开始计算MD5值（大文件将自动分块处理）...")
    duplicate_groups = find_duplicate_files(all_files)
    
    if not duplicate_groups:
        print("\n未发现重复文件（所有文件MD5值均唯一）")
        exit()
    
    # 打印重复文件组
    print("\n发现以下重复文件组（MD5值相同）：")
    for i, group in enumerate(duplicate_groups, 1):
        print(f"组 {i}: {group}")
    
    # 询问用户是否删除
    while True:
        choice = input("\n是否删除每组中的多余文件（仅保留一个随机文件）？(Y/N): ").strip().upper()
        if choice in ['Y', 'N']:
            break
        print("请输入 Y（是）或 N（否）")
    
    if choice == 'Y':
        delete_duplicates(duplicate_groups)
    else:
        print("已取消删除操作")
    os.system('pause')
