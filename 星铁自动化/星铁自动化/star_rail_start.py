import time
import os
import pyautogui
import sys
sys.path.append("./lib")
import find_similar_img_api as find_img
import operate_api as operate

def write_log(txt):
    time_now=time.time();time_now=round(time_now,1)
    txt_write_add(f="log.txt",txt=f"{time_now}---{txt}")
def txt_write_add(f,txt):#追加写入
    with open(f,"a",encoding="utf-8") as file:
        file.write(f"\r\n{txt}")
def chick_pos(x,y):
    operate.mouse_moveto(x,y,t=0)
    operate.click_left()
def find_and_chick(i,s):
    x,y,m=find_img.find_img_1(i,s)
    if m==1:
        chick_pos(x,y)



#主函数
def xt_start(order):
    bl1=0
    os.system(f'"start "{order}" "https://cg.163.com/#/mobile"')
    time.sleep(3)
    for i in range(300):#关闭网易云广告,以及确认是否打开
        time.sleep(0.5)
        x1,y1,m1=find_img.find_img_1(i="img2/6.jpg",s=0.9)
        xo5,yo5,mo5=find_img.find_img_1(i="img2/5.jpg",s=0.8)
        if m1==1:
            chick_pos(x1,y1)
        else:
            if mo5==1:
                time.sleep(3)
                find_and_chick(i="img2/6.jpg",s=0.9)
                bl1=1;break
    if bl1==0:#如果没有打开,处理办法
        write_log("网易云很久没有打开");exit()
    operate.mouse_moveto(xo5,yo5,t=0)#校准鼠标,以免出现滚动的列表不是想要的
    chick_pos(xo5,yo5)#校准鼠标,确定目前属于浏览器窗口
    for i in range(120):#寻找开始按钮
        time.sleep(0.5)
        x1,y1,m1=find_img.find_img_1(i="img2/1.jpg",s=0.8)
        if m1==1:
            x2,y2,m2=find_img.find_img_2(region=(int(x1-80),int(y1),int(x1+80),int(y1+240)),i="img2/2.jpg",s=0.8)
            if m2==1:
                chick_pos(x2,y2)
                break
        pyautogui.scroll(-200)#模拟鼠标滚轮下滑
    time.sleep(4)
    for i in range(400):#处理打开时网易云抽风
        time.sleep(0.5)
        x1,y1,m1=find_img.find_img_1(i="img2/13.jpg",s=0.9)
        x2,y2,m2=find_img.find_img_1(i="img2/11.jpg",s=0.9)
        x3,y3,m3=find_img.find_img_1(i="img2/3.jpg",s=0.8)
        x4,y4,m4=find_img.find_img_1(i="img2/6.jpg",s=0.9)
        x5,y5,m5=find_img.find_img_1(i="img2/7.jpg",s=0.9)
        x6,y6,m6=find_img.find_img_1(i="img2/8.jpg",s=0.65)
        if m1==1:
            time.sleep(2)
            find_and_chick(i="img2/14.jpg",s=0.9)
        if m2==1:
            time.sleep(2)
            find_and_chick(i="img2/12.jpg",s=0.9)
        if m3==1:
            time.sleep(2)
            find_and_chick(i="img2/4.jpg",s=0.9)
        if m4==1:
            time.sleep(4)
            x4,y4,m4=find_img.find_img_1(i="img2/6.jpg",s=0.9)
            chick_pos(x4,y4)
        if m5==1:
            time.sleep(2)
            x5,y5,m5=find_img.find_img_1(i="img2/7.jpg",s=0.9)
            chick_pos(x5,y5)
        if m6==1:
            time.sleep(4)
            x6,y6,m6=find_img.find_img_1(i="img2/8.jpg",s=0.5)
            chick_pos(x6,y6)
            break
    time.sleep(5)
    for i in range(60):#进入加载页面后,确定是否在主界面
        time.sleep(1)
        x1,y1,m1=find_img.find_img_1(i="img2/9.jpg",s=0.7)
        x2,y2,m2=find_img.find_img_1(i="img2/10.jpg",s=0.7)
        if m1==1 or m2==1:
            write_log("星铁成功启动")
            break
    m=1;return m
