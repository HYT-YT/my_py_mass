import text
def txt_read_line(f,n):#读取文件---f为文件路径,n为要读取的第N行
    txt=text.txt_read_line(f,n)
    return txt
def txt_write_add(f,txt):#追加写入---f为文件路径,txt为要输入的内容
    text.writetxta(f,txt)
def txt_write_cover(f,txt):#覆盖写入---f为文件路径,txt为要输入的内容
    text.writetxtw(f,txt)
def txt_read_all(f):#读取文本所有内容
    text.txt_read_all(f)
def txt_del(f):#删除一个文本
    m=text.txt_del(f)
    return m
def txt_del_line(f,n):#删除文本某一行
    text.txt_del_line(f, n)
def txt_add_behind_line(f,n,txt):#某一行后面追加文本
    text.txt_add_behind_line(f,n,txt)














