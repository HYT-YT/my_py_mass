import os

# 获取当前路径下的所有txt文件
txt_files = [f for f in os.listdir('.') if f.endswith('.txt')]

for txt_file in txt_files:
    # 打开文件，读取第一行
    #------------------------此处修改文件编码---------------
    with open(txt_file, 'r', encoding='ANSI') as f:
        line = f.readline().strip()
    
    # 将读取的字符串去除符号<与>
    new_name = line.replace('<', '').replace('>', '')
    
    # 处理重复文件名
    name_suffix = 1
    new_file_name = new_name + '.txt'
    while os.path.exists(new_file_name):
        new_file_name = f'{new_name}_{name_suffix}.txt'
        name_suffix += 1
    
    # 重命名文件
    os.rename(txt_file, new_file_name)
    
    print(f'{txt_file}改名为{new_file_name}')
