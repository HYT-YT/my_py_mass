import os
import cv2
import shutil
from glob import glob

# 配置参数（可根据需要修改）
SIMILARITY_THRESHOLD = 0.7  # 相似度阈值（0-1，越高要求越相似）
TARGET_FOLDER = "相似图片_待处理"  # 存放相似图片的文件夹
IMAGE_EXTENSIONS = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.gif"]  # 支持的图片格式


def get_image_paths():
    """获取当前目录下所有图片的路径"""
    image_paths = []
    for ext in IMAGE_EXTENSIONS:
        image_paths.extend(glob(ext))
    # 去重（避免同一文件多种格式匹配）
    return list(set(image_paths))


def compare_histograms(img1_path, img2_path):
    """比较两张图片的直方图相似度"""
    try:
        # 读取图片并转换为HSV色彩空间（比RGB更适合颜色分布对比）
        img1 = cv2.imread(img1_path)
        img2 = cv2.imread(img2_path)
        if img1 is None or img2 is None:
            return 0.0  # 读取失败则视为不相似

        # 转换为HSV空间（Hue色调, Saturation饱和度, Value明度）
        hsv1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
        hsv2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)

        # 计算直方图（每个通道单独计算）
        hist1 = cv2.calcHist([hsv1], [0, 1, 2], None, [8, 8, 8], [0, 180, 0, 256, 0, 256])
        hist2 = cv2.calcHist([hsv2], [0, 1, 2], None, [8, 8, 8], [0, 180, 0, 256, 0, 256])

        # 归一化直方图（确保尺度一致）
        cv2.normalize(hist1, hist1, 0, 1, cv2.NORM_MINMAX)
        cv2.normalize(hist2, hist2, 0, 1, cv2.NORM_MINMAX)

        # 计算相关性（返回值越接近1越相似）
        return cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    except Exception as e:
        print(f"对比 {img1_path} 和 {img2_path} 时出错: {e}")
        return 0.0


def main():
    # 获取所有图片路径
    image_paths = get_image_paths()
    if len(image_paths) < 2:
        print("当前目录下图片数量不足，无法对比")
        return

    # 创建目标文件夹
    if not os.path.exists(TARGET_FOLDER):
        os.makedirs(TARGET_FOLDER)

    # 记录已处理的图片对（避免重复处理）
    processed_pairs = set()
    # 记录需要移动的图片
    to_move = set()

    print(f"发现 {len(image_paths)} 张图片，开始对比...")

    # 两两对比所有图片
    for i in range(len(image_paths)):
        for j in range(i + 1, len(image_paths)):
            img1 = image_paths[i]
            img2 = image_paths[j]
            # 避免重复对比同一对
            pair = frozenset([img1, img2])
            if pair in processed_pairs:
                continue
            processed_pairs.add(pair)

            # 计算相似度
            similarity = compare_histograms(img1, img2)
            if similarity >= SIMILARITY_THRESHOLD:
                print(f"相似图片: {img1} 和 {img2}，相似度: {similarity:.2f}")
                to_move.add(img1)
                to_move.add(img2)

    # 移动相似图片到目标文件夹
    if to_move:
        print(f"\n共发现 {len(to_move)} 张相似图片，正在移动到 {TARGET_FOLDER}...")
        for img_path in to_move:
            try:
                shutil.move(img_path, os.path.join(TARGET_FOLDER, os.path.basename(img_path)))
            except Exception as e:
                print(f"移动 {img_path} 失败: {e}")
        print("移动完成")
    else:
        print("\n未发现达到阈值的相似图片")


if __name__ == "__main__":
    main()
