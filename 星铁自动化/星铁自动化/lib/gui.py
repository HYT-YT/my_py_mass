import tkinter as tk
from tkinter import font
from PIL import ImageTk, Image
import time
import threading
import ctypes
#默认参数含义(如未注明):
#txt-内容 t-时间 n-次数(行) f-url s-(移动)速度
#x/y-坐标 w/h-宽/高 x1/y1/x2/y2-起始终点坐标 size-字体大小
#默认顺序:window,f,w,h,x,y,bg,fg,size,txt,s,n...
#时间,速度...这样设计时间的参数,均以毫秒做单位
def destroy_x(x):
    x.destroy()
#隐藏tk窗口
def tk_off(window):
    window.withdraw()
#显示tk窗口
def tk_on(window):
    window.deiconify()
#获取屏幕长宽
def get_screen_wh():
    import tkinter as tk
    get_screen_wh_window=tk.Tk()
    w = get_screen_wh_window.winfo_screenwidth()
    h = get_screen_wh_window.winfo_screenheight()
    return w,h

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

#显示文本
def echo_txt(window,w,h,x,y,bg,fg,size,txt):
    字体1 = font.Font(family='SimHei', size=size)
    l = tk.Label(window,text=txt,bg=bg,fg=fg,font=字体1,width=w,height=h) #标签内容设置
    l.place(x=x,y=y)
    return l


def clear_window(window):#清除目标窗口所有部件
    children = window.winfo_children()
    # 遍历子组件并删除
    for child in children:
        child.destroy()


#输入框
def entry_input_2_1(window,x,y,w,font,bg,fg,e):
    txt=e.get()
    l = tk.Label(window,text=txt,bg=bg,fg=fg,font=font,width=w);l.place(x=x,y=y)
    window.update()
    window.after(1000,destroy_x,l)
def entry_input(window,x,y,w,font,bg,fg,show):#x,y,w为坐标,宽,font的字体大小用于调节高度,bg,fg为背景文字颜色,show(0:密码框,1:明文框,2:密码框(有按钮查看密码))
    if show==0:
        e=tk.Entry(window,show="*",bg=bg,fg=fg,width=w,font=font);e.place(x=x,y=y)#密码输入框(show可以指定输入的样式)
    if show==1:
        e=tk.Entry(window,bg=bg,fg=fg,width=w,font=font);e.place(x=x,y=y)##明文输入框
    if show==2:
        e=tk.Entry(window,show="*",bg=bg,fg=fg,width=w,font=font);e.place(x=x,y=y)#密码输入框(show可以指定输入的样式)
        b=tk.Button(window,width=3,bg=bg,fg=fg,text="T",command=lambda: entry_input_2_1(window,x,y,w,font,bg,fg,e));b.place(x=int(x+w*21.3),y=y)
    return e

#弹出窗口,让用户选择文件
def get_file_path(title,variety,allow_m,allow):#variety=0:单选,=1:多选,allow格式:allow=(("文本文件","*.txt"), ("所有文件","*.*")..),allow_m=0,无限制,allow_m=1,有限制
    from tkinter import filedialog  #用于弹出文件选择对话框
    if allow_m==1:#有限制
        if variety==0:
            file_path = filedialog.askopenfilename(title=title,filetypes=allow)
        if variety==1:
            file_path = filedialog.askopenfilenames(title=title,filetypes=allow)
    else:#无限制
        if variety==0:
            file_path = filedialog.askopenfilename(title=title)
        if variety==1:
            file_path = filedialog.askopenfilenames(title=title)
    return file_path
#弹出窗口,让用户选择目录
def get_files_path(title):
    from tkinter import filedialog  #用于弹出文件选择对话框
    dir_path = filedialog.askdirectory(title=title)  # 弹出目录选择对话框，获取用户选择的目录路径
    return dir_path

#----------------滚动条-------画布--------------
def creat_canvas_update(c1):
    c1.config(scrollregion=c1.bbox("all"))
#sx,cx..等为滚动条(s),画布(c)的xy坐标,wh长宽,bg为画布背景颜色
#sf为滚动条方向:sf="x",水平,,sf="y",垂直,,,,cf为画布方向:sf="x",水平,,cf="y"垂直
def creat_canvas_move(window,sx,sy,sw,sh,sf,cx,cy,cw,ch,cf,bg):
    if sf=="y":
        s1 = tk.Scrollbar(window)#垂直创建滚动条
    if sf=="x":
        s1 = tk.Scrollbar(window,orient=tk.HORIZONTAL)# 创建滚动条,orient=tk.HORIZONTAL代表设置为水平方向
    s1.place(x=sx,y=sy,width=sw,height=sh)
    if cf=="y":
        c1 = tk.Canvas(window,yscrollcommand=s1.set,bg=bg)#创建画布
    if cf=="x":
        c1 = tk.Canvas(window,xscrollcommand=s1.set,bg=bg)#创建画布
    c1.place(x=cx,y=cy,width=cw,height=ch)
    if cf=="y":
        s1.config(command=c1.yview)# 将滚动条与画布关联
    if cf=="x":
        s1.config(command=c1.xview)# 将滚动条与画布关联
    window.after(110,creat_canvas_update,c1)#本来需要布局好部件后更新才能使用滚动条,这里利用after自动更新,等待时间过短会导致滚动条无法加载
    #!!!!!!在主程序需要加入的:!!!!!!!
    #c1.create_window(x,y,window=部件名称)
    return c1,s1

"""
#滚动条示例
root=tk.Tk()
root.geometry("800x600")
c1,s1=creat_canvas_move(window=root,sx=0,sy=500,sw=400,sh=20,sf="x",cx=0,cy=0,cw=600,ch=400,cf="y",bg="green")
for i in range(20):
    b1 = tk.Button(c1, text=f"按钮{i+1}")
    c1.create_window(0,50+i*60,window=b1)
root.mainloop()
"""





#----------------快速提示通知----------------
def pre_show():#准备工作-全屏显示提示,创建相关窗口,然后隐藏,返回窗口与字体,可用新名字来接受窗口与字体
    show=tk.Tk()
    show.geometry("1400x800")
    show.geometry("+0+0")
    show.overrideredirect(True)
    show.attributes("-alpha",1)
    show_font = font.Font(family='SimHei', size=70)
    tk_off(show)
    return show,show_font
def pre_ts():#准备工作-创建任务栏图标以提示,创建相关窗口,然后隐藏,返回窗口,可用新名字来接受窗口
    ts = tk.Tk()
    ts.geometry("1x1")
    ts.geometry("+9000+9000")
    ts.title("No Date")
    tk_off(ts)
    return ts
def show(window,show_font,txt,t,bg,fg):#全屏通知,传入(窗口,字体,文本,显示时间,背景颜色,文字颜色)
    tk_on(window)
    l = tk.Label(window,text=txt,bg=bg,fg=fg,font=show_font)
    l.place(x=0,y=0,width=1400,height=800)
    window.update()
    time.sleep(t)
    tk_off(window)
def ts_on(window,txt):#开启提示窗口,传入(要修改名称的窗口,文本)
    window.title(txt)
    tk_on(window)
def ts_off(window):#关闭提示窗口,隐藏窗口
    tk_off(window)



#读取图片
def pic(f,w,h):
    image = Image.open(f)
    img=image.resize((w,h))
    my_img=ImageTk.PhotoImage(img)
    return my_img

#显示图片
def pic_echo(window,f,w,h,x,y):
    my_img=pic(f,w,h)
    l=tk.Label(window,image=my_img)
    l.image=my_img
    l.place(x=x,y=y)
    return l

#图片移动:n为移动次数(越大越精细)
#方式1(移动后图片消失)
def pic_move_l(window,f,w,h,x1,y1,x2,y2,s,n):
    my_img=pic(f,w,h)
    l=tk.Label(window,image=my_img)
    l.image=my_img
    l.place(x=x1,y=y1)
    xs=(x2-x1)/n;ys=(y2-y1)/n
    move_3(window,l,xs,ys,x1,y1,n,s,i=0)
def move_3(window,l,xs,ys,x1,y1,n,s,i):
    if i<n:
        i=i+1
        x1=x1+xs;y1=y1+ys
        l.place(x=int(x1),y=int(y1))
        window.update()
        window.after(s,move_3,window,l,xs,ys,x1,y1,n,s,i)
    elif i==n:
        l.destroy()
#方式2(移动后图片保留)
def pic_move_k(window,f,w,h,x1,y1,x2,y2,s,n):
    my_img=pic(f,w,h)
    l=tk.Label(window,image=my_img)
    l.image=my_img
    l.place(x=x1,y=y1)
    xs=(x2-x1)/n;ys=(y2-y1)/n
    limg=move_4(window,l,xs,ys,x1,y1,n,s,i=0)
    return limg
def move_4(window,l,xs,ys,x1,y1,n,s,i):
    if i<n:
        i=i+1
        x1=x1+xs;y1=y1+ys
        l.place(x=int(x1),y=int(y1))
        window.update()
        window.after(s,move_4,window,l,xs,ys,x1,y1,n,s,i)
    elif i==n:
        return l

#-----------------------基础---------结束---------------------



#顶部消息框:x/y:出现于x轴,从顶部下滑至y轴,t:移动至制定位置后等待时间,s为速度,bg,fg为背景/文字颜色
def msg_txt_s1(window,w,h,x,y,bg,fg,size,t,s,txt):
    字体1 = font.Font(family='SimHei', size=size)
    text = tk.Label(window, text=txt, font=字体1,width=w,height=h,bg=bg,fg=fg)
    x1=x;y1=-50
    text.place(x=x1,y=y1)
    move_1(window,t,y,x1,y1,s,text,i=0)
def move_1(window,t,y,x1,y1,s,text,i):
    i=i+1
    m=2*y+5
    if i<y:
        y1=y1+1
        text.place(x=x1,y=y1)
        window.update()
        window.after(s,move_1,window,t,y,x1,y1,s,text,i)
    elif i==y:
        i=i+1
        window.after(t,move_1,window,t,y,x1,y1,s,text,i)
    elif i==m:
        text.destroy()
    elif i>y:
        y1=y1-1
        text.place(x=x1,y=y1)
        window.update()
        window.after(s,move_1,window,t,y,x1,y1,s,text,i)


def msg_txt_s2(window,w,h,x,y,bg,fg,size,t,s,txt):
    字体1 = font.Font(family='SimHei', size=size)
    text = tk.Label(window, text=txt, font=字体1,width=w,height=h)
    x1=x;y1=-20
    text.place(x=x1,y=y1)
    while y1<y:
        time.sleep(s)
        y1=y1+1
        text.place(x=x1,y=y1)
        window.update()
    time.sleep(t)
    while y1>-20:
        time.sleep(s)
        y1=y1-1
        text.place(x=x1,y=y1)
        window.update()
    text.destroy()


#渐变文字(白-黑-白)t:转为黑色后停留时间;n:数字越大最后越黑;s:变化速度
#渐变1(after循环mainloop)
def echo_txt_s1(window,w,h,x,y,size,txt,t,s,n):
    字体1 = font.Font(family='SimHei', size=size) 
    text = tk.Label(window,text=txt, font=字体1,width=w,height=h);text.place(x=x,y=y)
    n0=0;n1=255;n2=255;n3=255
    echo_txt_s1_1(window,n,n0,n1,n2,n3,text,s,t,i=0)
def echo_txt_s1_1(window,n,n0,n1,n2,n3,text,s,t,i):
    i=i+1
    m=2*n+10
    if i<n:
        n0 +=1;n1 -=1;n2 -=1;n3 -=1
        text.config(foreground=f"#{int(n1):02x}{int(n2):02x}{int(n3):02x}")
        window.update()
        window.after(s,echo_txt_s1_1,window,n,n0,n1,n2,n3,text,s,t,i)
    elif i==n:
        n0=0;n1=255-n;n2=255-n;n3=255-n
        window.after(t,echo_txt_s1_1,window,n,n0,n1,n2,n3,text,s,t,i)
    elif i==m:
        text.destroy()
    elif i>n:
        n0 +=1;n1 +=1;n2 +=1;n3 +=1
        text.config(foreground=f"#{int(n1):02x}{int(n2):02x}{int(n3):02x}")
        window.update()
        window.after(s,echo_txt_s1_1,window,n,n0,n1,n2,n3,text,s,t,i)

#渐变2(阻塞线程)t:转为黑色后停留时间;n:数字越大最后越黑;s:变化速度
def echo_txt_s2(window,w,h,x,y,size,txt,t,s,n):
    字体1 = font.Font(family='SimHei', size=size) 
    text = tk.Label(window, text=txt, font=字体1,width=w,height=h);text.place(x=x,y=y)
    n0=0;n1=255;n2=255;n3=255;s=s/1000
    while n0<n:
        n0 +=1;n1 -=1;n2 -=1;n3 -=1
        text.config(foreground=f"#{int(n1):02x}{int(n2):02x}{int(n3):02x}")
        window.update();time.sleep(s)
    n0=0;n1=255-n;n2=255-n;n3=255-n
    t=int(t/1000)
    time.sleep(t)
    while n0<n:
        n0 +=1;n1 +=1;n2 +=1;n3 +=1
        text.config(foreground=f"#{int(n1):02x}{int(n2):02x}{int(n3):02x}")
        window.update();time.sleep(s)
    text.destroy()

#淡入显示文本,no1/2/3:初始三原色
def echo_txt_s3(window,w,h,x,y,size,txt,s,no1,no2,no3,nl1,nl2,nl3,ns,bg):
    字体1 = font.Font(family='SimHei', size=size) 
    l=tk.Label(window,text=txt, font=字体1,width=w,height=h,bg=bg);l.place(x=x,y=y)
    ns1=(nl1-no1)/ns;ns2=(nl2-no2)/ns;ns3=(nl3-no3)/ns;i=0
    echo_txt_s3_1(window,s,no1,no2,no3,ns1,ns2,ns3,i,ns,l)
def echo_txt_s3_1(window,s,no1,no2,no3,ns1,ns2,ns3,i,ns,l):
    i=i+1
    if i<ns:
        n1=no1+ns1;n2=no2+ns2;n3=no3+ns3;no1=n1;no2=n2;no3=n3;n1=int(n1);n2=int(n2);n3=int(n3)
        l.config(foreground=f"#{int(n1):02x}{int(n2):02x}{int(n3):02x}")
        window.update()
        window.after(s,echo_txt_s3_1,window,s,no1,no2,no3,ns1,ns2,ns3,i,ns,l)
    if i==ns:
        return l



#图片移动并返回n:移动的总次数,f为路径,s为每次移动停顿时间(毫秒),t为移动到制定位置后的等待时间
def pic_move_back(window,f,w,h,x1,y1,x2,y2,s,n,t):
    my_img=pic(f,w,h)
    l=tk.Label(window,image=my_img)
    l.image=my_img
    l.place(x=x1,y=y1)
    xsg=(x2-x1)/n;ysg=(y2-y1)/n;xsb=(x1-x2)/n;ysb=(y1-y2)/n
    pic_move_back_1(window,x1,y1,x2,y2,xsg,ysg,xsb,ysb,s,n,t,l,i=0)
def pic_move_back_1(window,x1,y1,x2,y2,xsg,ysg,xsb,ysb,s,n,t,l,i):
    i=i+1;m=2*n
    if i<n:
        x1=int(x1+xsg);y1=int(y1+ysg)
        l.place(x=x1,y=y1)
        window.update()
        window.after(s,pic_move_back_1,window,x1,y1,x2,y2,xsg,ysg,xsb,ysb,s,n,t,l,i)
    elif i==n:
        window.after(t,pic_move_back_1,window,x1,y1,x2,y2,xsg,ysg,xsb,ysb,s,n,t,l,i)
    elif i==m:
        l.destroy()
    elif i>n:
        x1=int(x1+xsb);y1=int(y1+ysb)
        l.place(x=x1,y=y1)
        window.update()
        window.after(s,pic_move_back_1,window,x1,y1,x2,y2,xsg,ysg,xsb,ysb,s,n,t,l,i)
        
    

#gif播放winodws:窗口名,f:路径,x,y:坐标(左上)
def gif_echo(window,f,x,y):
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
    l=Lgif(window)
    l.place(x=x,y=y)
    l.load(f)
    return l

#设置gui界面，bk=0无边框,title标题,w,h,x,y,bg为属性,tm为透明属性(0-1),
#top_m为顶置属性(=1时将永远顶置于其他窗口上)
#tp="某种颜色",这种颜色将在这个窗口(包括部件)内被替换为透明,(最好将16进制颜色设为透明)
#tp应用需要tp_m=1
def set_gui(window,bk,title,tm,w,h,x,y,bg,top_m,tp_m,tp):
    window.configure(bg=bg)
    window.attributes("-alpha", tm)
    if bk==0:
        window.overrideredirect(True)
    if top_m==1:
        window.attributes("-topmost", True)#窗口顶置
    if tp_m==1:
        window.attributes("-transparentcolor",tp)#将某种颜色设置为透明
    window.title(title) 
    window.geometry(f"{w}x{h}")
    window.geometry(f"+{x}+{y}")
    return window


