import os
import shutil
from glob import glob
from PIL import Image
import numpy as np
from multiprocessing import Pool, cpu_count

# 配置参数
SIMILARITY_THRESHOLD = 5  # 哈希值差异阈值（越小越严格，建议3-5）
TARGET_FOLDER = "相似图片_待处理"
IMAGE_EXTENSIONS = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.gif"]
MAX_PROCESSES = cpu_count()  # 多进程数量（使用全部CPU核心）


def get_image_paths():
    """获取当前目录下所有图片路径"""
    image_paths = []
    for ext in IMAGE_EXTENSIONS:
        image_paths.extend(glob(ext))
    return list(set(image_paths))  # 去重


def average_hash(img_path, size=8):
    """计算图片的平均哈希值"""
    try:
        # 打开图片并转为灰度图
        with Image.open(img_path) as img:
            # 缩小尺寸并转为灰度
            img = img.resize((size, size), Image.LANCZOS).convert('L')
            # 计算像素平均值
            pixels = np.array(img)
            avg = pixels.mean()
            # 生成哈希值（大于平均值为1，否则为0）
            hash_array = (pixels > avg).flatten()
            return hash_array, img_path
    except Exception as e:
        print(f"处理 {img_path} 时出错: {e}")
        return None, img_path


def hamming_distance(hash1, hash2):
    """计算两个哈希值的汉明距离（差异位数）"""
    return np.sum(hash1 != hash2)


def group_similar_images(hashes, paths, threshold):
    """将相似图片分组（同一组内的图片互相相似）"""
    groups = []
    processed = set()  # 记录已分组的图片索引

    for i in range(len(hashes)):
        if i in processed:
            continue
        # 新建组，以当前图片为起点
        group = [paths[i]]
        processed.add(i)
        # 寻找与当前图片相似的其他图片
        for j in range(i + 1, len(hashes)):
            if j in processed:
                continue
            distance = hamming_distance(hashes[i], hashes[j])
            if distance <= threshold:
                group.append(paths[j])
                processed.add(j)
        # 只保留包含多张相似图片的组
        if len(group) >= 2:
            groups.append(group)
    return groups


def main():
    image_paths = get_image_paths()
    if len(image_paths) < 2:
        print("当前目录下图片数量不足，无法对比")
        return

    print(f"发现 {len(image_paths)} 张图片，正在计算哈希值（多进程加速）...")

    # 多进程计算所有图片的哈希值
    with Pool(processes=MAX_PROCESSES) as pool:
        hash_results = pool.map(average_hash, image_paths)

    # 过滤无效结果
    valid_hashes = [(h, p) for h, p in hash_results if h is not None]
    if len(valid_hashes) < 2:
        print("有效图片不足，无法对比")
        return

    hashes, paths = zip(*valid_hashes)

    # 按组划分相似图片
    print(f"开始对比哈希值（共 {len(valid_hashes)} 张有效图片）...")
    similar_groups = group_similar_images(hashes, paths, SIMILARITY_THRESHOLD)

    if not similar_groups:
        print("未发现达到阈值的相似图片组")
        return

    # 显示分组结果
    print("\n发现以下相似图片组：")
    for i, group in enumerate(similar_groups, 1):
        print(f"组 {i}（共 {len(group)} 张）: {[os.path.basename(p) for p in group]}")

    # 创建目标文件夹
    os.makedirs(TARGET_FOLDER, exist_ok=True)
    print(f"\n正在将相似图片移动到 {TARGET_FOLDER}（数字前缀命名以聚拢显示）...")

    # 按组重命名并移动图片 - 数字前缀确保Windows排序时聚拢
    for group_idx, group in enumerate(similar_groups, 1):
        # 为组内每张图片编号（001, 002... 确保排序正确）
        for img_idx, img_path in enumerate(group, 1):
            # 获取原文件扩展名
            ext = os.path.splitext(img_path)[1].lower()
            # 新文件名（如 "1_001.jpg"、"1_002.png"、"2_001.jpg"）
            # 数字前缀确保在Windows中按名称排序时同一组图片聚集在一起
            new_name = f"{group_idx}_{img_idx:03d}{ext}"
            dest_path = os.path.join(TARGET_FOLDER, new_name)

            # 处理可能的重名
            counter = 1
            while os.path.exists(dest_path):
                new_name = f"{group_idx}_{img_idx:03d}_{counter}{ext}"
                dest_path = os.path.join(TARGET_FOLDER, new_name)
                counter += 1

            # 移动并改名
            try:
                shutil.move(img_path, dest_path)
                print(f"已移动：{os.path.basename(img_path)} → {new_name}")
            except Exception as e:
                print(f"移动 {os.path.basename(img_path)} 失败: {e}")

    print("\n处理完成。相似图片已按组以数字前缀命名，在Windows中按名称排序会自动聚拢。")


if __name__ == "__main__":
    main()
