import os
import shutil
import hashlib
import threading
import sys  # 新增：导入sys模块
from queue import Queue
from collections import defaultdict

# 控制线程数量（建议设为CPU核心数的1-2倍）
THREAD_NUM = 8
file_queue = Queue()
md5_dict = defaultdict(list)
lock = threading.Lock()
# 存储重复文件组（用于后续处理）
duplicate_groups = []

def calculate_md5(file_path, block_size=65536):
    """计算文件的MD5值"""
    md5_hash = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(block_size):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()
    except (IOError, OSError) as e:
        print(f"无法读取文件 {file_path}: {e}")
        return None

def process_files():
    """线程处理函数：从队列获取文件并计算MD5"""
    while True:
        file_path = file_queue.get()
        if file_path is None:  # 终止信号
            break
        md5 = calculate_md5(file_path)
        if md5:
            with lock:
                md5_dict[md5].append(file_path)
        file_queue.task_done()

def scan_target_directory():
    """扫描程序所在的目录及所有子目录（修复路径问题）"""
    # 关键修复：获取程序实际运行的目录（.exe所在目录或脚本所在目录）
    current_dir = os.path.dirname(os.path.abspath(sys.executable))
    print(f"开始扫描目录: {current_dir}...")
    
    for dirpath, _, filenames in os.walk(current_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if os.path.isfile(file_path):
                file_queue.put(file_path)

def main():
    global duplicate_groups
    # 修复：获取程序实际运行的目录
    current_dir = os.path.dirname(os.path.abspath(sys.executable))
    
    # 启动扫描和计算线程
    scan_thread = threading.Thread(target=scan_target_directory)  # 注意函数名已修改
    scan_thread.start()

    threads = []
    for _ in range(THREAD_NUM):
        t = threading.Thread(target=process_files)
        t.start()
        threads.append(t)

    scan_thread.join()
    file_queue.join()

    # 发送终止信号
    for _ in range(THREAD_NUM):
        file_queue.put(None)
    for t in threads:
        t.join()

    # 整理重复文件组
    print("\n===== 重复文件列表 =====")
    duplicate_count = 0
    for md5, file_paths in md5_dict.items():
        if len(file_paths) > 1:
            duplicate_count += 1
            duplicate_groups.append(file_paths)  # 保存组信息
            print(f"\n重复组 {duplicate_count} (MD5: {md5}):")
            for path in file_paths:
                print(f"  - {path}")

    if duplicate_count == 0:
        print("未发现重复文件")
        input("\n按回车键退出...")
        return
    else:
        print(f"\n扫描完成，共发现 {duplicate_count} 组重复文件")

    # 第一次用户选择：是否移动文件
    while True:
        choice = input("\n是否将重复文件移动到「相同文件_待处理」文件夹？(Y/N): ").strip().upper()
        if choice in ['Y', 'N']:
            break
        print("请输入 Y 或 N")

    if choice == 'Y':
        # 创建目标文件夹（基于程序实际目录）
        target_dir = os.path.join(current_dir, "相同文件_待处理")
        os.makedirs(target_dir, exist_ok=True)
        print(f"\n已创建文件夹: {target_dir}")

        # 移动并重命名文件
        for group_idx, file_paths in enumerate(duplicate_groups, 1):
            print(f"\n处理第 {group_idx} 组文件...")
            for file_idx, file_path in enumerate(file_paths, 1):
                # 获取文件名和后缀
                file_name = os.path.basename(file_path)
                file_ext = os.path.splitext(file_name)[1] if '.' in file_name else ''
                
                # 构建新文件名（组号_序号+后缀）
                new_name = f"组{group_idx}_{file_idx}{file_ext}"
                new_path = os.path.join(target_dir, new_name)

                # 处理文件名冲突（按Windows规则）
                counter = 1
                while os.path.exists(new_path):
                    new_name = f"组{group_idx}_{file_idx}_{counter}{file_ext}"
                    new_path = os.path.join(target_dir, new_name)
                    counter += 1

                # 移动文件
                try:
                    shutil.move(file_path, new_path)
                    print(f"  已移动: {file_name} -> {new_name}")
                except Exception as e:
                    print(f"  移动失败 {file_name}: {e}")

        print("\n所有文件移动完成")

        # 第二次用户选择：是否自动删除
        while True:
            del_choice = input("\n是否在每组中仅保留一个文件，删除其余文件？(Y/N): ").strip().upper()
            if del_choice in ['Y', 'N']:
                break
            print("请输入 Y 或 N")

        if del_choice == 'Y':
            # 保留每组第一个文件，删除其余
            deleted_count = 0
            for group_idx, file_paths in enumerate(duplicate_groups, 1):
                # 原文件路径已失效，重新获取移动后的文件路径
                moved_files = [f for f in os.listdir(target_dir) if f.startswith(f"组{group_idx}_")]
                if len(moved_files) <= 1:
                    continue
                
                # 保留第一个，删除其他
                for file in moved_files[1:]:
                    file_to_del = os.path.join(target_dir, file)
                    try:
                        os.remove(file_to_del)
                        deleted_count += 1
                        print(f"已删除: {file}")
                    except Exception as e:
                        print(f"删除失败 {file}: {e}")

            print(f"\n处理完成，共删除 {deleted_count} 个重复文件")
        else:
            print("\n已取消删除操作，文件保留在「相同文件_待处理」文件夹中")
    else:
        print("\n已取消移动操作，文件保持原位")

    input("\n按回车键退出...")

if __name__ == "__main__":
    main()
    os.system("pause")
