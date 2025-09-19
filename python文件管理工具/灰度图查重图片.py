import os
import shutil
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from multiprocessing import Pool, cpu_count
import itertools

# 设置相似度阈值（0-1之间，值越高要求越相似）
SIMILARITY_THRESHOLD = 0.8
# 最大图片尺寸（用于缩放，平衡精度和性能）
MAX_IMAGE_SIZE = 1000
# 进程池大小（默认使用所有CPU核心）
POOL_SIZE = cpu_count()
# 相似图片存放文件夹
SIMILAR_FOLDER = "相似图片_待处理"

def get_image_files(exclude_file):
    """获取当前目录下所有图片文件，排除脚本自身"""
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff')
    image_files = []
    
    for file in os.listdir('.'):
        if file == exclude_file or file == SIMILAR_FOLDER:
            continue
        if file.lower().endswith(image_extensions) and os.path.isfile(file):
            image_files.append(file)
    
    return image_files

def load_image_gray(image_path):
    """加载图片并转换为灰度图，限制最大尺寸"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            raise Exception("无法读取图片内容")
        
        # 调整图片大小
        height, width = img.shape[:2]
        if height > MAX_IMAGE_SIZE or width > MAX_IMAGE_SIZE:
            scale = MAX_IMAGE_SIZE / max(height, width)
            img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    except Exception as e:
        print(f"处理图片 {image_path} 时出错: {str(e)}")
        return None

def compare_pair(args):
    """比较单对图片的相似度（供多进程调用）"""
    gray_images, file1, file2 = args
    try:
        img1 = gray_images[file1]
        img2 = gray_images[file2]
        
        # 确保尺寸相同
        if img1.shape != img2.shape:
            img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]), interpolation=cv2.INTER_AREA)
        
        similarity = ssim(img1, img2)
        return (file1, file2, similarity) if similarity >= SIMILARITY_THRESHOLD else None
    except Exception as e:
        print(f"比较 {file1} 和 {file2} 时出错: {str(e)}")
        return None

def find_similar_images(image_files):
    """多进程查找所有相似的图片组"""
    # 预加载所有图片的灰度图（单进程，I/O密集型操作不适合多进程）
    print("正在加载图片...")
    gray_images = {}
    for file in image_files:
        gray = load_image_gray(file)
        if gray is not None:
            gray_images[file] = gray
    
    # 生成所有需要比较的图片对
    files = list(gray_images.keys())
    pairs = [(gray_images, files[i], files[j]) for i in range(len(files)) for j in range(i + 1, len(files))]
    
    # 使用进程池并行比较
    print(f"使用 {POOL_SIZE} 个进程进行比较...")
    similar_pairs = []
    with Pool(POOL_SIZE) as pool:
        # 分批处理避免内存占用过高
        batch_size = max(100, len(pairs) // POOL_SIZE)
        for i in range(0, len(pairs), batch_size):
            batch = pairs[i:i+batch_size]
            results = pool.map(compare_pair, batch)
            similar_pairs.extend([r for r in results if r is not None])
    
    # 从相似对构建相似组
    similar_groups = []
    for file1, file2, _ in similar_pairs:
        found = False
        for group in similar_groups:
            if file1 in group or file2 in group:
                group.add(file1)
                group.add(file2)
                found = True
                break
        if not found:
            similar_groups.append({file1, file2})
    
    return [sorted(group) for group in similar_groups]

def move_similar_images(similar_groups):
    """创建文件夹并移动相似图片"""
    # 创建文件夹，如果已存在则不做处理
    try:
        os.makedirs(SIMILAR_FOLDER, exist_ok=True)
        print(f"\n已创建文件夹: {SIMILAR_FOLDER}")
    except Exception as e:
        print(f"创建文件夹失败: {str(e)}")
        return
    
    # 跟踪已移动的文件，避免重复移动
    moved_files = set()
    
    # 移动每组相似图片
    for i, group in enumerate(similar_groups, 1):
        print(f"\n移动第 {i} 组相似图片:")
        for file in group:
            if file not in moved_files:
                try:
                    # 构建源路径和目标路径
                    src = file
                    dst = os.path.join(SIMILAR_FOLDER, file)
                    
                    # 检查目标文件是否已存在
                    if os.path.exists(dst):
                        # 如果已存在，添加编号避免覆盖
                        name, ext = os.path.splitext(file)
                        counter = 1
                        while os.path.exists(os.path.join(SIMILAR_FOLDER, f"{name}_{counter}{ext}")):
                            counter += 1
                        dst = os.path.join(SIMILAR_FOLDER, f"{name}_{counter}{ext}")
                    
                    shutil.move(src, dst)
                    moved_files.add(file)
                    print(f"已移动: {file} -> {dst}")
                except Exception as e:
                    print(f"移动文件 {file} 失败: {str(e)}")

if __name__ == "__main__":
    script_name = os.path.basename(__file__)
    print("正在扫描图片文件...")
    image_files = get_image_files(script_name)
    
    if not image_files:
        print("未找到任何图片文件")
        os.system("pause")
        exit()
    
    print(f"找到 {len(image_files)} 个图片文件，准备比较...")
    similar_groups = find_similar_images(image_files)
    
    if similar_groups:
        print("\n找到以下相似图片组:")
        for i, group in enumerate(similar_groups, 1):
            print(f"组 {i}: {group}")
        
        # 移动相似图片到指定文件夹
        move_similar_images(similar_groups)
    else:
        print("\n未找到相似的图片")
    
    os.system("pause")
    
