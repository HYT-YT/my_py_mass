import keyboard 
import time
import tkinter as tk
from tkinter import font
import mouse
import ctypes
import os
import keyboard 
import dll
import mouse

def press_1():#按左键
    mouse.press(button="left")
    mouse.release(button="left")
def press_2():#按键"R"
    keyboard.press("r")
    time.sleep(0.001)
    keyboard.release("r")
def m1(ts):#快速连点
    dll.ts_on(ts,txt="快速连点")
    i=0
    time.sleep(0.1)
    while i<1:
        time.sleep(0.01)
        press_1()
        if keyboard.is_pressed("tab"):
            time.sleep(0.1)
            dll.ts_off(ts)
            break
def m2(show1,ts,字体1):#输入账密
    import pyautogui
    dll.ts_on(ts,txt="输入中..")
    dll.show(show1,字体1,txt="键盘已占用:1-3账号 q-r密码",t=0.3,bg="white",fg="black")
    for i in range(1000):
        if keyboard.is_pressed("1"):
            pyautogui.press('backspace')
            pyautogui.typewrite('2305931805@qq.com')
            time.sleep(0.2)
        if keyboard.is_pressed("2"):
            pyautogui.press('backspace')
            pyautogui.typewrite('wbms84@163.com')
            time.sleep(0.2)
        if keyboard.is_pressed("3"):
            pyautogui.press('backspace')
            pyautogui.typewrite('15828279979')
            time.sleep(0.2)
        if keyboard.is_pressed("q"):
            pyautogui.press('backspace')
            pyautogui.typewrite('aa474920')
            time.sleep(0.2)
        if keyboard.is_pressed("w"):
            pyautogui.press('backspace')
            pyautogui.typewrite('aa47492000')
            time.sleep(0.2)
        if keyboard.is_pressed("e"):
            pyautogui.press('backspace')
            pyautogui.typewrite('hyt474920')
            time.sleep(0.2)
        if keyboard.is_pressed("r"):
            pyautogui.press('backspace')
            pyautogui.typewrite('hyt47492000')
            time.sleep(0.2)
        time.sleep(0.01)
    dll.show(show1,字体1,txt="主页",t=0.3,bg="black",fg="white")
    dll.ts_off(ts)
def m_esc():#退出
    show(txt="已关闭程序",t=0.5,bg="red",fg="green")
    exit()
def m9(show1,ts):#自动挂机
    import pyautogui
    #确定浏览器窗口
    pyautogui.moveTo(5,600)
    press_1()
    #打开菜单
    keyboard.press("esc")
    keyboard.release("esc")
    time.sleep(0.3)
    #打开后台挂机
    pyautogui.moveTo(850,185)
    press_1()
    time.sleep(1)
    #输入时间
    keyboard.press("1")
    time.sleep(0.01)
    keyboard.release("1")
    time.sleep(0.01)
    keyboard.press("0")
    time.sleep(0.01)
    keyboard.release("0")
    #确定
    time.sleep(0.4)
    pyautogui.moveTo(682,478)
    time.sleep(0.3)
    press_1()





def mai1(region,i,s):
    print("进入场景：按f")
    image_gray,w,h=dll.find_similar_img_1(image_path=i)
    while True:
        screen_gray=dll.find_similar_img_2()
        x,y,m=dll.find_similar_img_4(region,image_gray,w,h,screen_gray,threshold=s)
        if keyboard.is_pressed("f11"):
            break
        if m==1:
            for i in range(2):
                time.sleep(0.07)
                keyboard.press("f")
                keyboard.release("f")
        else:
            print("场景变更,退出")
            break
        time.sleep(0.1)


def ai_sure(region,i,s,f):
    print("对场景识别中..")
    x,y,m=dll.find_similar_img_f2(region,i,s)
    if m==1:
        #属于场景f,即将转入
        eval(f+"(region,i,s)")



def ai_1(show1,ts):#智能模式
    dll.ts_on(ts,txt="智能模式")
    time.sleep(0.3)
    while True:
        time.sleep(1)
        print("情景识别..")
        ai_sure(region=(0,0,200,170),i="c:\\help/dll/img/1/1.jpg",s=0.65,f="mai1")
        ai_sure(region=(0,0,200,170),i="c:\\help/dll/img/1/2.jpg",s=0.65,f="mai1")
        ai_sure(region=(0,0,200,170),i="c:\\help/dll/img/2/1.jpg",s=0.65,f="mai1")
        ai_sure(region=(0,0,200,170),i="c:\\help/dll/img/2/2.jpg",s=0.65,f="mai1")
        ai_sure(region=(0,0,200,170),i="c:\\help/dll/img/2/3.jpg",s=0.65,f="mai1")
        ai_sure(region=(0,0,200,170),i="c:\\help/dll/img/2/4.jpg",s=0.65,f="mai1")
        time.sleep(1)
        if keyboard.is_pressed("f11"):
            dll.ts_off(ts)
            time.sleep(0.8)
            break






def m11(show1,ts):
    time.sleep(0.2)
    while True:
        keyboard.press("f")
        keyboard.release("f")
        if keyboard.is_pressed("f11"):
            time.sleep(0.2)
            break
        time.sleep(0.2)
    
















def m4():#五郎速射
    i=0
    while i<1:
        #按下左键(射出一键)
        press_1()
        time.sleep(0.025)#这个地方为攻击后进入瞄准状态的等待时间(根据电脑反应速度调整)

        #按下r键(进入瞄准状态以取消后摇)
        press_2()
        time.sleep(0.02)
        #按下r键(退出瞄准状态以进行下一轮循环)
        press_2()
        #当按下键盘t时退出
        if keyboard.is_pressed("t"):
            break


