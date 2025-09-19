import tkinter as tk
from tkinter import font
import mouse
import keyboard
import time

#参数设置:
model_choose_time=0.14#模式判断时间-----------(按下按钮后,超过这个值还保持按压,则进入长按模式)(过小:无法进入自动模式:可作为战斗模式)(过大:等待时间过长,不灵敏)
press_wait_time=0.01#连点时间间隔
common_wait_time=0.02#待机循环刷新时间---------------(越小,待机模式下更灵敏,但是对cpu消耗更大)
enter_wait_time=0.1#进入模式后人体反应时间
exit_wait_time=0.1#退出模式后人体反应时间--------------(仅仅针对自动模式,长按模式取消按下即退出)
ts_color_change_n=30#提示悬浮窗颜色改变频率----------------(连点多少次后改变一次颜色)
keys_list_enter = ["tab","alt","up"]#为判断键列表,任意一个键被按下,即可(进入/退出)连点
keys_list_f=["f"]#自动拾取的打开按钮


#基础
def tk_on(window):
    window.deiconify()
def tk_off(window):
    window.withdraw()
def press_left():#按左键
    mouse.press(button="left")
    mouse.release(button="left")
def press(x):#点按x键
    keyboard.press(x)
    keyboard.release(x)
def msg(txt,fg):
    l_msg.config(text=txt,fg=fg)
    tk_on(msg_box)
    msg_box.update()
def msg_star():
    global msg_star_bl
    tk_on(msg_box)
    colors = ["#EE6363", "black", "#8B2500", "blue", "yellow", "#CD1076", "#A020F0", "green", "#00FF7F", "white", "red"]#列表
    l_msg.config(fg=colors[msg_star_bl])
    msg_star_bl = (msg_star_bl + 1) % len(colors)#其中,%是求余数,这里用作限制范围,在colors中反复遍历
    msg_box.update()

def m1():#自动模式,开启后自动连点
    msg(txt="███自动模式███",fg="blue")
    bl_jc=0
    time.sleep(enter_wait_time)
    while True:
        press_left()
        time.sleep(press_wait_time)
        if any(keyboard.is_pressed(key) for key in keys_list_enter):
            tk_off(msg_box)
            time.sleep(exit_wait_time)
            break
        bl_jc=bl_jc+1
        if bl_jc==ts_color_change_n:
            msg_star();bl_jc=0

def m2():#长按模式,长按以保持连点状态
    msg(txt="███长按模式███",fg="blue")
    bl_jc=0
    while True:
        if any(keyboard.is_pressed(key) for key in keys_list_enter):
            press_left()
        else:
            tk_off(msg_box)
            time.sleep(exit_wait_time)
            break
        time.sleep(press_wait_time)
        bl_jc=bl_jc+1
        if bl_jc==ts_color_change_n:
            msg_star();bl_jc=0


def m3():#自动拾取模式(按f)
    msg(txt="█拾取追加..",fg="red")
    while True:
        if any(keyboard.is_pressed(key) for key in keys_list_f):
            press("f")
            time.sleep(0.05)
        else:
            tk_off(msg_box)
            break


#主函数
if __name__ in "__main__":
    global msg_star_bl;msg_star_bl=0
    msg_box=tk.Tk();字体1=font.Font(family='SimHei',size=20)
    xo=msg_box.winfo_screenwidth();yo=msg_box.winfo_screenheight()
    w=int(xo*0.21);h=int(yo*0.04);x=int(xo*0.4);y=0;msg_box.geometry(f"{w}x{h}");msg_box.geometry(f"+{x}+{y}")
    msg_box.attributes("-transparentcolor","#F8F8FF")#设置透明颜色
    msg_box.configure(bg="#F8F8FF")#设置背景颜色
    msg_box.attributes("-topmost", True)#窗口顶置
    msg_box.overrideredirect(True)#无边框
    l_msg=tk.Label(msg_box,text="提示",font=字体1,bg="#F8F8FF",fg="black",width=int(xo*0.015));l_msg.place(x=0,y=0)
    msg(txt="连点器就绪",fg="green")
    while True:
        if any(keyboard.is_pressed(key) for key in keys_list_enter):
            time.sleep(model_choose_time)
            if any(keyboard.is_pressed(key) for key in keys_list_enter):#在制定时间后来判断是进入(自动/长按)模式
                m2()
            else:
                m1()
        if any(keyboard.is_pressed(key) for key in keys_list_f):#拾取模式判断
            time.sleep(0.1)
            if any(keyboard.is_pressed(key) for key in keys_list_f):
                m3()
        if keyboard.is_pressed("ctrl") and keyboard.is_pressed("esc"):
            msg(txt="即将关闭..",fg="red")
            time.sleep(2);exit()
        time.sleep(0.1)







