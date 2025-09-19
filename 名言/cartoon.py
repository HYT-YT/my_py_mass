import tkinter as tk
from tkinter import font
from PIL import ImageTk, Image
import time
import threading
import os
import ctypes
import winsound
import random
import basic as b

def x(command):
    os.system(command)

#动画1:
#描述:有一些图片随机时间从屏幕左上角滑动至屏幕右上角(较低y轴),然后消失
#举例:流星划过天际

#方案1:(较稀疏的图片较长时间维持效果)
def c1_1_1(main1):
    t=0
    for i in range(5):#总图片数
        m = random.randint(0,700)#图片之间随机间隔时间
        t=m+int(i*300)#数字为2张相邻图片最短间隔时间
        main1.update()
        main1.after(t,c1_1,main1)
#方案2:(较多的图片较短时间爆发出来)
def c1_1_2(main1):
    t=0
    for i in range(40):#总图片数
        m = random.randint(0,2000)#图片之间随机间隔时间
        t=m+int(i*600)#数字为2张相邻图片最短间隔时间
        main1.update()
        main1.after(t,c1_1,main1)
def c1_1(main1):
    r1 = random.randint(0,70)#起始x
    r2 = random.randint(0,50)#起始y
    r3 = random.randint(950,1000)#终点x
    r4 = random.randint(55,200)#终点y
    r5 = random.randint(100,150)#流畅度
    r6 = random.randint(1,5)#速度
    b.pic_move_l(main1,f="dll/pic/2.jpg",w=80,h=45,x1=r1,y1=r2,x2=r3,y2=r4,n=r5,s=r6)


#动画2:
#描述:图片A与图片B从屏幕底端移动至屏幕顶端,图片A较多,且间隔更离散,图片B较少,且间隔时间较为集中;图片A为底部随机到顶部随机,B为底部随机但笔直向上
#应用举例:水泡(A)与物品(B)随水面上升;烟花

def c2_1_1(main1,pica,picb,picbg):
    t=0
    for i in range(20):#图片A数量
        m = random.randint(0,300)#图片间隔时间随机
        t=m+int(i*100)#图片最短间隔
        main1.update()
        main1.after(t,c2_1,main1,pica)
    for i in range(5):#图片B数量
        m = random.randint(0,300)#图片间隔时间随机
        t=m+int(i*100)#图片最短间隔
        main1.update()
        main1.after(t,c2_2,main1,picb)
    c2_3(main1,picbg)

def c2_1(main1,pica):#执行图片A行为
    r1 = random.randint(0,1000)#起始x
    r2 = random.randint(570,600)#起始y
    r3 = random.randint(0,1000)#终点x
    r4 = random.randint(0,30)#终点y
    r5 = random.randint(100,130)#流畅度
    r6 = random.randint(12,20)#速度
    b.pic_move_l(main1,f=pica,w=80,h=80,x1=r1,y1=r2,x2=r3,y2=r4,n=r5,s=r6)

def c2_2(main1,picb):#图片B行为
    r1 = random.randint(0,1000)#起始x
    r2 = random.randint(570,600)#起始y
    r4 = random.randint(0,30)#终点y
    r5 = random.randint(90,120)#流畅度
    r6 = random.randint(15,17)#速度
    b.pic_move_l(main1,f=picb,w=30,h=90,x1=r1,y1=r2,x2=r1,y2=r4,n=r5,s=r6)

def c2_3(main1,picbg):#背景图片
    b.pic_move_l(main1,f=picbg,w=80,h=80,x1=400,y1=60,x2=600,y2=60,n=20,s=100)




#动画3
#描述:大量图片向中间聚拢,等待一定时间后再分开
#举例:加载动画,过渡动画

def c3_1_1(main1):
    b.pic_move_back(main1,f="dll/pic/11.jpg",w=1000,h=600,x1=0,y1=-600,x2=0,y2=0,s=1,n=60,t=4000)
    main1.after(1000,c3_1_1_1,main1)
def c3_1_1_1(main1):
    for i in range(12):
        m = random.randint(0,800)
        t=m+int(i*50)
        main1.update()
        main1.after(t,c3_1,main1)
        main1.after(t,c3_2,main1)



def c3_1(main1):
    r1 = random.randint(0,10)#起始x
    r2 = random.randint(-50,410)#起始y
    r3 = random.randint(-20,450);r3=int(r1+r3)#终点x(偏差)
    r4 = random.randint(-10,10);r4=int(r2+r4)#终点y(偏差)
    
    r5 = random.randint(20,20)#流畅度
    r6 = random.randint(1,1)#速度
    r7 = random.randint(400,500)#等待时间
    b.pic_move_back(main1,f="dll/pic/27.jpg",w=100,h=100,x1=r1,y1=r2,x2=r3,y2=r4,s=r6,n=r5,t=r7)
    

def c3_2(main1):
    r1 = random.randint(910,970)#起始x
    r2 = random.randint(-50,410)#起始y
    r3 = random.randint(40,600);r3=int(r1-r3)#终点x(偏差)
    r4 = random.randint(-10,10);r4=int(r2+r4)#终点y(偏差)
    
    r5 = random.randint(20,20)#流畅度
    r6 = random.randint(1,1)#速度
    r7 = random.randint(400,500)#等待时间
    b.pic_move_back(main1,f="dll/pic/27.jpg",w=100,h=100,x1=r1,y1=r2,x2=r3,y2=r4,s=r6,n=r5,t=r7)


#动画4
#描述:大量图片从底部到顶部然后消失
#举例:烟花
def c4_1_1(main1):
    t=0
    for i in range(20):#总图片数
        m = random.randint(0,700)#图片之间随机间隔时间
        t=m+int(i*500)#数字为2张相邻图片最短间隔时间
        main1.update()
        main1.after(t,c4_1,main1)
def c4_1(main1):
    r1 = random.randint(0,990)#起始x
    r2 = random.randint(570,600)#起始y
    r3 = random.randint(-30,30);r3=int(r3+r1)#终点x(偏差)
    r4 = random.randint(530,570);r4=int(r2-r4)#终点y(偏差)
    r5 = random.randint(100,100)#流畅度
    r6 = random.randint(1,2)#速度
    b.pic_move_l(main1,f="dll/pic/18.jpg",w=40,h=40,x1=r1,y1=r2,x2=r3,y2=r4,n=r5,s=r6)


#动画5
#描述:大量图片从顶部到底部然后消失
#举例:下雨
def c5_1_1(main1):
    t=0
    for i in range(20):#总图片数
        m = random.randint(0,500)#图片之间随机间隔时间
        t=m+int(i*500)#数字为2张相邻图片最短间隔时间
        main1.update()
        main1.after(t,c5_1,main1)
def c5_1(main1):
    r1 = random.randint(0,990)#起始x
    r2 = random.randint(-10,10)#起始y
    r3 = random.randint(-30,30);r3=int(r3+r1)#终点x(偏差)
    r4 = random.randint(570,580);r4=int(r2+r4)#终点y(偏差)
    r5 = random.randint(60,60)#流畅度
    r6 = random.randint(1,2)#速度
    b.pic_move_l(main1,f="dll/pic/15.jpg",w=30,h=30,x1=r1,y1=r2,x2=r3,y2=r4,n=r5,s=r6)






































































































