import ctypes
import tkinter as tk
import winsound
import threading
import time
import subprocess
import keyboard
import os

def check():# 充电中返回0，未充电返回1
    class _PowerStatus(ctypes.Structure):
        _fields_ = [("ACLineStatus", ctypes.c_byte)]
    status = _PowerStatus()
    ctypes.windll.kernel32.GetSystemPowerStatus(ctypes.byref(status))
    return 0 if status.ACLineStatus == 1 else 1

def max_volume():#设置最大声音
    VK_VOLUME_UP = 0xAF
    ctypes.windll.user32.keybd_event(VK_VOLUME_UP, 0, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(VK_VOLUME_UP, 0, 0x0002, 0)
    for _ in range(50):#模拟案件增加音量（里面填次数）
        ctypes.windll.user32.keybd_event(VK_VOLUME_UP, 0, 0, 0)
        time.sleep(0.01)
        ctypes.windll.user32.keybd_event(VK_VOLUME_UP, 0, 0x0002, 0)


cover_window = None     #遮挡窗口全局变量
_alarm_playing = False  #报警声音全局变量

def show_cover():  # 显示遮挡窗口
    global cover_window
    if cover_window:
        cover_window.destroy()
    cover_window = tk.Tk()
    cover_window.overrideredirect(True)
    cover_window.geometry(f"{cover_window.winfo_screenwidth()}x{cover_window.winfo_screenheight()}+0+0")
    cover_window.configure(bg="#FF0000")
    cover_window.attributes("-topmost", True)
    
    # 核心修改：拦截并忽略窗口关闭事件（包括Alt+F4）
    cover_window.protocol("WM_DELETE_WINDOW", lambda: None)
    
    frame = tk.Frame(cover_window, bg="#FF0000")
    frame.place(relx=0.5, rely=0.5, anchor="center")
    tk.Label(
        frame,
        text="电脑已锁定",
        font=("微软雅黑", 80, "bold"),
        bg="#FF0000",
        fg="#000000"
    ).pack()
    tk.Label(frame, text="", bg="#FF0000").pack()
    tk.Label(
        frame,
        text="已打开定位",
        font=("微软雅黑", 40, "bold"),
        bg="#FF0000",
        fg="#000000"
    ).pack()
    
    cover_window.update()

def hide_cover():  # 关闭遮挡窗口
    global cover_window
    if cover_window:
        cover_window.destroy()
        cover_window = None



def start_alarm():#报警声音
    global _alarm_playing
    if not _alarm_playing:
        _alarm_playing = True
        threading.Thread(target=_loop_play, daemon=True).start()

def _loop_play():#报警声音线程（忽视勿动）
    while _alarm_playing:
        winsound.PlaySound("报警.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)  
        time.sleep(3)  

def stop_alarm():#结束报警声音
    global _alarm_playing
    _alarm_playing = False
    winsound.PlaySound(None, winsound.SND_PURGE)

def open_power_control():#打开电源管理以方便手动禁用电源按钮
    subprocess.Popen("control powercfg.cpl")
    


def check_key_pressed(key):# 检测按键是否被按下，返回1（按下）或0（未按下）
    if keyboard.is_pressed(key):
        return 1
    else:
        return 0


if __name__ == "__main__":
    #初始化
    subprocess.Popen('control.exe powercfg.cpl')
    while True:
        check_num=check()
        if check_num==0:#开发者测试（space键模拟拔出）
            check_num=check_key_pressed('space')
        if check_num==1:
            #准备锁机
            max_volume()
            show_cover()
            os.popen('start /b cmd /c 禁止关机.bat')
            #持续报警，保持窗口响应
            while True:
                start_alarm()
                # 保持窗口响应性，防止被系统判定为无响应
                if cover_window:
                    cover_window.update_idletasks()
                    cover_window.update()
                time.sleep(0.1)
                stop_num=check_key_pressed("Enter")
                if stop_num==1:
                    break
            #解除锁机
            stop_alarm()
            hide_cover()
            os.popen('start /b cmd /c 恢复关机.bat')
            break
        time.sleep(0.1)#巡警状态更新频率
