import tkinter as tk
import time
from tkinter import font
from PIL import ImageTk, Image
import basic as b
from tkinter import font
import cartoon as ct
import random
import sys
import os


main1 = tk.Tk()
main1.overrideredirect(True)
main1.attributes("-alpha", 0.9)
main1.title("名言") 
main1.geometry("1000x600")
main1.geometry("+20+50")
main1.configure(bg="white")
字体1 = font.Font(family='SimHei', size=20)





#关闭窗口事件
def close():
    clear(main1)
    b.pic_echo(main1,"dll/pic/25.jpg",w=1000,h=600,x=0,y=0)
    b.msg_txt_s1(main1,w=20,h=1,x=300,y=70,bg="#228B22",fg="white",size=30,t=1000,s=3,txt="要离开吗?")
    b1=tk.Button(main1,text="离开",width=8,height=1,bg="white",fg="red",font=字体1,command=close_1)
    b1.place(x=250,y=400)
    b1=tk.Button(main1,text="返回",width=8,height=1,bg="white",fg="black",font=字体1,command=close_2)
    b1.place(x=650,y=400)
def close_1():
    clear(main1)
    b.gif_echo(main1,f="dll/gif/2.gif",x=0,y=0)
    main1.after(1400,close_3)
def close_2():
    clear(main1)
    m1()
def close_3():
    os.system("start c://windows/explorer.exe")
    exit()
main1.protocol("WM_DELETE_WINDOW", close)

#清空部件
def clear(window):  
    for widget in window.winfo_children():  
        widget.destroy()


def m1():
    b.echo_txt_s2(main1,txt="启动",x=280,y=200,w=0,h=0,size=120,t=300,n=100,s=0)
    b.gif_echo(main1,f="dll/gif/1.gif",x=100,y=130)
    main1.after(2500,m2)

def m2():
    main1.attributes("-alpha", 0.9)
    b.pic_echo(main1,f="dll/pic/1.jpg",w=1000,h=600,x=0,y=0)
    main1.update()
    time.sleep(0.3)
    b.pic_echo(main1,f="dll/1.jpg",w=800,h=500,x=100,y=50)
    main1.update()
    time.sleep(0.1)
    b1=tk.Button(main1,text="下一页",width=6,height=1,bg="yellow",fg="black",font=字体1,command=m3)
    b1.place(x=900,y=550)
    ct.c1_1_1(main1)
    b.msg_txt_s1(main1,txt="什么是勇气",t=2000,x=250,y=80,w=30,h=2,s=5,size=20,bg="#F4A460",fg="black")

def m3():
    clear(main1)
    b.gif_echo(main1,f="dll/gif/4.gif",x=0,y=0)
    b.pic_echo(main1,"dll/2.jpg",w=850,h=400,x=50,y=100)
    b.msg_txt_s1(main1,txt="勇气:名言",t=2000,x=250,y=80,w=30,h=2,s=5,size=20,bg="#F4A460",fg="black")
    b1=tk.Button(main1,text="下一页",width=6,height=1,bg="yellow",fg="black",font=字体1,command=m4)
    b1.place(x=900,y=550)
    ct.c4_1_1(main1)

def m4():
    clear(main1)
    ct.c3_1_1(main1)
    main1.after(5500,m5)

def m5():
    b.pic_echo(main1,"dll/3.jpg",w=1000,h=600,x=0,y=0)
    b.msg_txt_s1(main1,txt="第一句的含义",t=2000,x=250,y=80,w=30,h=2,s=5,size=20,bg="#F4A460",fg="black")
    b1=tk.Button(main1,text="下一页",width=6,height=1,bg="yellow",fg="black",font=字体1,command=m6)
    b1.place(x=900,y=550)

def m6():
    main1.overrideredirect(False)
    clear(main1)
    ct.c5_1_1(main1)
    b.pic_echo(main1,"dll/4.jpg",w=1000,h=600,x=0,y=0)
    b.msg_txt_s1(main1,txt="第二句的含义",t=2000,x=250,y=80,w=30,h=2,s=3,size=20,bg="#F4A460",fg="black")
    b1=tk.Button(main1,text="演示完毕",width=6,height=1,bg="yellow",fg="red",font=字体1,command=m7)
    b1.place(x=900,y=550)

def m7():
    clear(main1)
    b.gif_echo(main1,f="dll/gif/5.gif",x=0,y=0)
    b.msg_txt_s1(main1,txt="感谢观看整huo",t=1000,x=250,y=80,w=30,h=2,s=5,size=20,bg="#F4A460",fg="black")
    b1=tk.Button(main1,text="结束退出",width=12,height=2,bg="yellow",fg="black",font=字体1,command=close)
    b1.place(x=380,y=240)

os.system("taskkill /f /im explorer.exe")
m1()


main1.mainloop()















