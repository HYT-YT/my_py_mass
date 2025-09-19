#适合小文件,一次性读取所有内容
def txt_read_line(f,n):#读取文件---f为文件路径,n为要读取的第N行
    with open(f, "r") as file:
        txt = file.readlines()[n-1].strip()
        return txt

#适合大文件,逐行读取
def txt_read_line_1(f,n):#读取文件---file_path为文件路径,n为要读取的第N行
    file_path=f
    with open(file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i == n - 1:
                return line.strip()
    return None




def writetxta(f,txt):#追加写入---f为文件路径,txt为要输入的内容
    with open(f,"a") as file:
        file.write(txt)
def writetxtw(f,txt):#覆盖写入---f为文件路径,txt为要输入的内容
    with open(f,"w") as file:
        file.write(txt)
def txt_read_all(f):#读取文本所有内容
    with open(f,"r") as file:
        txt=file.read(file)
        return txt
def txt_del(f):#删除一个文本
    if os.path.exists(f):
        os.remove(f)
    else:#不存在文件
        m=0
        return m

def txt_del_line(f, n):#删除文本某一行
    with open(f, 'r') as file:
        lines = file.readlines()
    with open(f, 'w') as file:
        for index, line in enumerate(lines):
            if index != n - 1:
                file.write(line)

def txt_add_behind_line(f,n,txt):#某一行后面追加文本
    with open(f, 'r') as file:
        lines = file.readlines()
    with open(f, 'w') as file:
        for index, line in enumerate(lines):
            if index == n - 1:
                line += txt + '\n'
            file.write(line)










