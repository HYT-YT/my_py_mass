import time
import keyboard 
import mouse
import pyautogui
def click_left():#左击
    mouse.press(button="left")
    mouse.release(button="left")
def click_right():#右击
    mouse.press(button="right")
    mouse.release(button="right")
def press(x):#点按x键
    keyboard.press(x)
    keyboard.release(x)
def press_on(x):#按住x键
    keyboard.press(x)
def press_off(x):#放开x键
    keyboard.release(x)
def input(txt):#输入文本
    pyautogui.typewrite(txt)
def mouse_moveto(x,y,t):#鼠标位置移至,t为花费时间
    pyautogui.moveTo(x,y,duration=t)
def screen_wh_get():#获取屏幕分辨率
    w,h=pyautogui.size()
    return w,h
def screen_keep(f):#保存屏幕截屏,f为路径
    screenshot=pyautogui.screenshot()
    screenshot.save(f)
def mouse_drato(x,y,t):#从当前位置拖拽至,t为花费时间
    pyautogui.dragTo(x,y,duration=t)
def mouse_postion_get():#获取当前鼠标位置
    x,y=pyautogui.position()
    return x,y
def check_keyboard(x):#检测当前某个键位是否按下,返回m=0未按住,m=1正在按住
    if keyboard.is_pressed(x):
        m=1;return m
    else:
        m=0;return m

