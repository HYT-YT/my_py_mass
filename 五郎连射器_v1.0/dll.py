import keyboard 
import time
import tkinter as tk
from tkinter import font
import mouse
import ctypes
import os
import cv2  #图片识别
import numpy as np  #图片识别灰度
from PIL import ImageGrab  #截取屏幕图像
#隐藏tk窗口
def tk_off(window):
    window.withdraw()
#显示tk窗口
def tk_on(window):
    window.deiconify()
#隐藏任务
def cx_off():
    from ctypes import c_int, WINFUNCTYPE, windll
    from ctypes.wintypes import HWND, BOOL
    SW_HIDE = 0
    SW_RESTORE = 9
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), SW_HIDE)
#显示任务
def cx_on():
    from ctypes import c_int, WINFUNCTYPE, windll
    from ctypes.wintypes import HWND, BOOL
    SW_HIDE = 0
    SW_RESTORE = 9
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), SW_RESTORE)

#开启提示窗口
def ts_on(ts,txt):
    ts.title(txt)
    tk_on(ts)

#关闭提示窗口
def ts_off(ts):
    tk_off(ts)


#show通知
def show(show1,字体1,txt,t,bg,fg):
    tk_on(show1)
    l = tk.Label(show1,text=txt,bg=bg,fg=fg,font=字体1)
    l.place(x=0,y=0,width=1400,height=800)
    show1.update()
    time.sleep(t)
    tk_off(show1)


def pre_show():
    show1=tk.Tk()
    show1.geometry("1400x800")
    show1.geometry("+0+0")
    show1.overrideredirect(True)
    show1.attributes("-alpha",1)
    字体1 = font.Font(family='SimHei', size=70)
    tk_off(show1)
    return show1,字体1

def pre_ts():
    global ts
    ts = tk.Tk()
    ts.geometry("1x1")
    ts.geometry("+2000+700")
    tk_off(ts)
    return ts

def m_esc(show1,字体1):
    show(show1,字体1,txt="已关闭程序",t=0.5,bg="red",fg="green")
    exit()




def find_similar_img_1(image_path):#模版照片处理
    image = cv2.imread(image_path)  # 读取图片文件
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  #转换为灰度图
    w, h = image_gray.shape[::-1]  #获取模板图片的宽度和高度
    return image_gray,w,h

def find_similar_img_2():#截屏处理
    screen = np.array(ImageGrab.grab())  # 截屏转换
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)  # 屏幕图像转换灰度图
    return screen_gray

#全屏搜索
def find_similar_img_3(image_gray,w,h,screen_gray,threshold):
    #匹配
    res = cv2.matchTemplate(screen_gray, image_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)#寻找

    if max_val >= threshold:#超过阀值
        #计算坐标
        mean_x = max_loc[0] + int(w / 2)
        mean_y = max_loc[1] + int(h / 2)
        m=1
        return mean_x,mean_y,m
    else:#未超过阀值
        x=0;y=0;m=0
        return x,y,m
#区域搜索
def find_similar_img_4(region,image_gray,w,h,screen_gray,threshold):
    #匹配
    res = cv2.matchTemplate(screen_gray[region[1]:region[3], region[0]:region[2]], image_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)#寻找

    if max_val >= threshold:#超过阀值
        #计算坐标
        mean_x = max_loc[0] + int(w / 2)+region[0]
        mean_y = max_loc[1] + int(h / 2)+region[1]
        m=1
        return mean_x,mean_y,m
    else:#未超过阀值
        x=0;y=0;m=0
        return x,y,m

def find_similar_img_f1(i,s):
    image_gray,w,h=find_similar_img_1(image_path=i)
    screen_gray=find_similar_img_2()
    x,y,m=find_similar_img_3(image_gray,w,h,screen_gray,threshold=s)
    return x,y,m

def find_similar_img_f2(region,i,s):
    image_gray,w,h=find_similar_img_1(image_path=i)
    screen_gray=find_similar_img_2()
    x,y,m=find_similar_img_4(region,image_gray,w,h,screen_gray,threshold=s)
    return x,y,m






















