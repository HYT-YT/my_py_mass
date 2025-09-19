import keyboard 
import time
import tkinter as tk
from tkinter import font
import mouse
import ctypes
import os
import dll
import function as fun

#开启提示窗口
def ts_on(txt):
    ts1.title(txt)
    tk_on(ts1)

#关闭提示窗口
def ts_off():
    tk_off(ts1)


#show通知
def show(txt,t,bg,fg):
    tk_on(show1)
    l = tk.Label(show1,text=txt,bg=bg,fg=fg,font=字体1)
    l.place(x=0,y=0,width=1400,height=800)
    show1.update()
    time.sleep(t)
    tk_off(show1)



#-----------通用模块------------

#按左键
def press_1():
    mouse.press(button="left")
    mouse.release(button="left")

#按键"R"
def press_2():
    keyboard.press("r")
    time.sleep(0.001)
    keyboard.release("r")


def m_esc():
    show(txt="已关闭程序",t=0.5,bg="red",fg="green")
    exit()





#初始化
#初始化show模块
show1,字体1=dll.pre_show()
#初始化ts窗口
ts=dll.pre_ts()
dll.show(show1,字体1,txt="主页已启动",t=0.4,bg="black",fg="white")
dll.cx_off()
while True:
    time.sleep(0.1)
    if keyboard.is_pressed("tab"):
        i=0
        fun.m1(ts)
    if keyboard.is_pressed("f2"):
        i=0
        fun.m2(show1,ts,字体1)
    if keyboard.is_pressed("f9"):
        i=0
        fun.m9(show1,ts)
    if keyboard.is_pressed("f11"):
        i=0
        fun.ai_1(show1,ts)
    """
    if keyboard.is_pressed("t"):
        i=0
        fun.m4()
    """
    if keyboard.is_pressed("esc") and keyboard.is_pressed("ctrl"):
        dll.m_esc(show1,字体1)









