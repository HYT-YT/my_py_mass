import tkinter as tk
from tkinter import font
from PIL import ImageTk, Image
import time
import threading
import os
import ctypes
import winsound

def x(command):
    os.system(command)

#默认参数含义(如未注明):
#txt-内容 t-时间 n-次数(行) f-url s-(移动)速度
#x/y-坐标 w/h-宽/高 x1/y1/x2/y2-起始终点坐标 size-字体大小
#默认顺序:main1,f,w,h,x,y,bg,fg,size,txt,s,n...
#时间,速度...这样设计时间的参数,均以毫秒做单位



#------------------------基础---------------------
#隐藏tk窗口
def tk_off(main1):
    main1.withdraw()

#显示tk窗口
def tk_on(main1):
    main1.deiconify()


#文档操作
def readtxt(f,n):#读取文档第n行
    with open("C:\\1.txt", "r") as file:
        txt = file.readlines()[n-1].strip()
        return txt
def writetxta(f,txt):#追加写入
    with open(f,"a") as f:
        f.write(txt)
def writetxtw(f,txt):#覆盖写入
    with open(f,"w") as f:
        f.write(txt)

#显示文本
def echo_txt(main1,w,h,x,y,bg,fg,size,txt):
    字体1 = font.Font(family='SimHei', size=size)
    l = tk.Label(main1,text=txt,bg=bg,fg=fg,font=字体1,width=w,height=h) #标签内容设置
    l.place(x=x,y=y)
    return l


#读取图片
def pic(f,w,h):
    image = Image.open(f)
    img=image.resize((w,h))
    my_img=ImageTk.PhotoImage(img)
    return my_img

#显示图片
def pic_echo(main1,f,w,h,x,y):
    my_img=pic(f,w,h)
    l=tk.Label(main1,image=my_img)
    l.image=my_img
    l.place(x=x,y=y)

#图片移动:n为移动次数(越大越精细)
#方式1(移动后图片消失)
def pic_move_l(main1,f,w,h,x1,y1,x2,y2,s,n):
    my_img=pic(f,w,h)
    l=tk.Label(main1,image=my_img)
    l.image=my_img
    l.place(x=x1,y=y1)
    xs=(x2-x1)/n;ys=(y2-y1)/n
    move_3(main1,l,xs,ys,x1,y1,n,s,i=0)
def move_3(main1,l,xs,ys,x1,y1,n,s,i):
    if i<n:
        i=i+1
        x1=x1+xs;y1=y1+ys
        l.place(x=int(x1),y=int(y1))
        main1.update()
        main1.after(s,move_3,main1,l,xs,ys,x1,y1,n,s,i)
    elif i==n:
        l.destroy()
#方式2(移动后图片保留)
def pic_move_k(main1,f,w,h,x1,y1,x2,y2,s,n):
    my_img=pic(f,w,h)
    l=tk.Label(main1,image=my_img)
    l.image=my_img
    l.place(x=x1,y=y1)
    xs=(x2-x1)/n;ys=(y2-y1)/n
    move_4(main1,l,xs,ys,x1,y1,n,s,i=0)
def move_4(main1,l,xs,ys,x1,y1,n,s,i):
    if i<n:
        i=i+1
        x1=x1+xs;y1=y1+ys
        l.place(x=int(x1),y=int(y1))
        main1.update()
        main1.after(s,move_4,main1,l,xs,ys,x1,y1,n,s,i)
    elif i==n:
        time.sleep(0)

#-----------------------基础---------结束---------------------



#顶部消息框:x/y:出现于x轴,从顶部下滑至y轴
def msg_txt_s1(main1,w,h,x,y,bg,fg,size,t,s,txt):
    字体1 = font.Font(family='SimHei', size=size)
    text = tk.Label(main1, text=txt, font=字体1,width=w,height=h,bg=bg,fg=fg)
    x1=x;y1=-50
    text.place(x=x1,y=y1)
    move_1(main1,t,y,x1,y1,s,text,i=0)
def move_1(main1,t,y,x1,y1,s,text,i):
    i=i+1
    m=2*y+5
    if i<y:
        y1=y1+1
        text.place(x=x1,y=y1)
        main1.update()
        main1.after(s,move_1,main1,t,y,x1,y1,s,text,i)
    elif i==y:
        i=i+1
        main1.after(t,move_1,main1,t,y,x1,y1,s,text,i)
    elif i==m:
        text.destroy()
    elif i>y:
        y1=y1-1
        text.place(x=x1,y=y1)
        main1.update()
        main1.after(s,move_1,main1,t,y,x1,y1,s,text,i)


def msg_txt_s2(main1,w,h,x,y,bg,fg,size,t,s,txt):
    字体1 = font.Font(family='SimHei', size=size)
    text = tk.Label(main1, text=txt, font=字体1,width=w,height=h)
    x1=x;y1=-20
    text.place(x=x1,y=y1)
    while y1<y:
        time.sleep(s)
        y1=y1+1
        text.place(x=x1,y=y1)
        main1.update()
    time.sleep(t)
    while y1>-20:
        time.sleep(s)
        y1=y1-1
        text.place(x=x1,y=y1)
        main1.update()
    text.destroy()


#渐变文字(白-黑-白)t:转为黑色后停留时间;n:数字越大最后越黑;s:变化速度
#渐变1(after循环mainloop)
def echo_txt_s1(main1,w,h,x,y,size,txt,t,s,n):
    字体1 = font.Font(family='SimHei', size=size) 
    text = tk.Label(main1, text=txt, font=字体1,width=w,height=h);text.place(x=x,y=y)
    n0=0;n1=255;n2=255;n3=255
    move_2(main1,n,n0,n1,n2,n3,text,s,t,i=0)
def move_2(main1,n,n0,n1,n2,n3,text,s,t,i):
    i=i+1
    m=2*n+10
    if i<n:
        n0 +=1;n1 -=1;n2 -=1;n3 -=1
        text.config(foreground=f"#{int(n1):02x}{int(n2):02x}{int(n3):02x}")
        main1.update()
        main1.after(s,move_2,main1,n,n0,n1,n2,n3,text,s,t,i)
    elif i==n:
        n0=0;n1=255-n;n2=255-n;n3=255-n
        main1.after(t,move_2,main1,n,n0,n1,n2,n3,text,s,t,i)
    elif i==m:
        text.destroy()
    elif i>n:
        n0 +=1;n1 +=1;n2 +=1;n3 +=1
        text.config(foreground=f"#{int(n1):02x}{int(n2):02x}{int(n3):02x}")
        main1.update()
        main1.after(s,move_2,main1,n,n0,n1,n2,n3,text,s,t,i)

#渐变2(阻塞线程)
def echo_txt_s2(main1,w,h,x,y,size,txt,t,s,n):
    字体1 = font.Font(family='SimHei', size=size) 
    text = tk.Label(main1, text=txt, font=字体1,width=w,height=h);text.place(x=x,y=y)
    n0=0;n1=255;n2=255;n3=255;s=s/1000
    while n0<n:
        n0 +=1;n1 -=1;n2 -=1;n3 -=1
        text.config(foreground=f"#{int(n1):02x}{int(n2):02x}{int(n3):02x}")
        main1.update();time.sleep(s)
    n0=0;n1=255-n;n2=255-n;n3=255-n
    t=int(t/1000)
    time.sleep(t)
    while n0<n:
        n0 +=1;n1 +=1;n2 +=1;n3 +=1
        text.config(foreground=f"#{int(n1):02x}{int(n2):02x}{int(n3):02x}")
        main1.update();time.sleep(s)
    text.destroy()



#音乐1
def sound_1():
    sound_1 = threading.Thread(target=sound_1_1) #设置线程所对应函数
    sound_1.start()
def sound_1_1():
    # 定义旋律
    notes = [  
    (659, 500),
    (759, 500),
    ]  
    # 播放旋律  
    for frequency, duration in notes:  
        winsound.Beep(frequency, duration)


#图片移动并返回
def pic_move_back(main1,f,w,h,x1,y1,x2,y2,s,n,t):
    my_img=pic(f,w,h)
    l=tk.Label(main1,image=my_img)
    l.image=my_img
    l.place(x=x1,y=y1)
    xsg=(x2-x1)/n;ysg=(y2-y1)/n;xsb=(x1-x2)/n;ysb=(y1-y2)/n
    pic_move_back_1(main1,x1,y1,x2,y2,xsg,ysg,xsb,ysb,s,n,t,l,i=0)
def pic_move_back_1(main1,x1,y1,x2,y2,xsg,ysg,xsb,ysb,s,n,t,l,i):
    i=i+1;m=2*n
    if i<n:
        x1=int(x1+xsg);y1=int(y1+ysg)
        l.place(x=x1,y=y1)
        main1.update()
        main1.after(s,pic_move_back_1,main1,x1,y1,x2,y2,xsg,ysg,xsb,ysb,s,n,t,l,i)
    elif i==n:
        main1.after(t,pic_move_back_1,main1,x1,y1,x2,y2,xsg,ysg,xsb,ysb,s,n,t,l,i)
    elif i==m:
        l.destroy()
    elif i>n:
        x1=int(x1+xsb);y1=int(y1+ysb)
        l.place(x=x1,y=y1)
        main1.update()
        main1.after(s,pic_move_back_1,main1,x1,y1,x2,y2,xsg,ysg,xsb,ysb,s,n,t,l,i)
        
    





#gif播放
def gif_echo(main1,f,x,y):
    import tkinter as tk
    from PIL import Image, ImageTk
    from itertools import count

    class Lgif(tk.Label):
        def load(self, im):
            if isinstance(im, str):
                im = Image.open(im)
            self.loc = 0
            self.frames = []

            try:
                for i in count(1):
                    self.frames.append(ImageTk.PhotoImage(im.copy()))
                    im.seek(i)
            except EOFError:
                pass

            try:
                self.delay = im.info['duration']
            except:
                self.delay = 100#默认间隔时间



            if len(self.frames) == 1:
                self.config(image=self.frames[0])
            else:
                self.next_frame()

        def unload(self):
            self.config(image="")
            self.frames = None

        def next_frame(self):
            if self.frames:
                self.loc += 1
                self.loc %= len(self.frames)
                self.config(image=self.frames[self.loc])
                self.after(self.delay, self.next_frame)
    l=Lgif(main1)
    l.place(x=x,y=y)
    l.load(f)
    return l











































































