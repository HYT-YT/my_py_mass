import time
import os

def test_1():#浮点运算
    c1=0
    time1=time.time()
    while True:
        c1=c1+1
        t1=9999;t2=t1**9999
        time2=time.time();timea=time2-time1
        if timea>2:
            break
    fen=c1/timea
    return fen

def test_2(n):#cpu与内存交互,n为填充多少MB(不要超过物理内存大小)
    size=1024*1024*n
    time1=time.time()
    data = [0] * size#创建大小为size的列表,填充数据0,size:1MB=1024*1024...
    time2=time.time();timea=time2-time1
    del data#释放内存
    fen=10/timea
    return fen
    
def test_3(file_path,size_mb):
    size=int(1024*1024*size_mb)
    time1=time.time()
    with open(file_path, 'wb') as f:
        f.write(b'\0' * size)
    time2=time.time();timea=time2-time1
    os.remove(file_path)
    fen=size_mb/timea
    return fen

def test_4(file_path):
    time1=time.time()
    with open(file_path,'r') as file:
        file.read()
    time2=time.time();timea=time2-time1
    fen=100/timea
    os.remove(file_path)
    return fen

def write(file_path,size_mb):
    size=int(1024*1024*size_mb)
    with open(file_path, 'wb') as file:
        file.write(b'\0' * size)


print("开始检测:")
fen1=test_1()
print("浮点运算得分: ",fen1)
fen2=test_2(10)#参数为占用内存大小(输入100,一般占用700MB)
print("内存填充速度得分: ",fen2)
fen3=test_3("c://users/test_write_speed.txt",100);fen3=round(fen3,2)
print("磁盘填充速度:  ",fen3,"(MB/S)")
write("c://users/test_write_speed.txt",100)
fen4=test_4("c://users/test_write_speed.txt");fen4=round(fen4,2)
print("磁盘读取速度(伪):  ",fen4,"(MB/S)")
print("检测结束")
os.system("pause>nul")
