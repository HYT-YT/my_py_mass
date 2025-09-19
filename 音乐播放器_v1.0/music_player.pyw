import tkinter as tk
from tkinter import font
import time
import os
import pyautogui
from PIL import ImageTk, Image


def close_exit():
    print("1")
    exit()





#------------------------------------------dll库打包内容------------------------------------------

#------------------------------------------music库------------------------------------------
def music_start(url,vol,postion,loop):
    from pygame import mixer
    mixer.init()
    mus=mixer.music.load(url)
    mus=mixer.music.set_volume(vol)
    mus=mixer.music.play(loops=loop, start=postion)
    return mus
def music_pause():#暂停播放
    from pygame import mixer
    mixer.music.pause()
def music_unpause():#继续播放
    from pygame import mixer
    mixer.music.unpause()
def music_stop():#结束播放
    from pygame import mixer
    mixer.music.stop()
def music_set_pos(n):#跳转到指定秒速播放
    from pygame import mixer
    mixer.music.set_pos(n)
def music_set_vol(vol):#设置音量
    from pygame import mixer
    mixer.music.set_volume(vol)
def check_music():#获取音乐信息m=(0:未播放,1:正在播放),postion:正在播放的位置,vol:音量(通常为小数,需要[乘法,int,然后除法])
    from pygame import mixer
    mixer.init()
    if mixer.music.get_busy():
        m=1
    else:
        m=0
    postion=mixer.music.get_pos()
    vol=mixer.music.get_volume()
    return m,postion,vol

def txt_read_line(f,n):#读取文件---f为文件路径,n为要读取的第N行
    with open(f, "r") as file:
        txt = file.readlines()[n-1].strip()
        return txt

def gui_set(window,bk,title,tm,w,h,x,y,bg,top_m,tp_m,tp):
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

def gui_pic_read(f,w,h):
    image = Image.open(f)
    img=image.resize((w,h))
    my_img=ImageTk.PhotoImage(img)
    return my_img

def gui_echo_txt(window,w,h,x,y,bg,fg,size,txt):
    字体1 = font.Font(family='SimHei', size=size)
    l = tk.Label(window,text=txt,bg=bg,fg=fg,font=字体1,width=w,height=h) #标签内容设置
    l.place(x=x,y=y)
    return l

def screen_wh_get():#获取屏幕分辨率
    w,h=pyautogui.size()
    return w,h



































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

#---------------------------------------------音乐播放---------------------------------------------
def b_mus_start(url,name,artist):#播放音乐
    global mus_m;global voln;volm=voln/100
    if mus_m==1:
        music_stop();mus_m=0
    if mus_m==0:
        music_start(url=url,vol=volm,postion=0.0,loop=-1)
        msg2.config(text=f"{name}");msg3.config(text=f"{artist}");mus_m=1
        b_mus_pause_check()
#音量加(+)
def vol_add():
    global voln,mus_m,mus
    voln=int(voln+1);msg1.config(text=f"音量:{voln}%")
    if voln>100:
        voln=voln-1;msg3.config(text="音量最高了!");msg1.config(text=f"音量:{voln}%")
    if mus_m==1:
        volm=voln/100
        music_set_vol(vol=volm)
def vol_add_press():
    global root
    vol_add()
    global job_id;job_id=root.after(18,vol_add_press)
def vol_add_release():
    global root
    root.after_cancel(job_id)
#音量减(-)
def vol_reduce():
    global voln,mus_m
    voln=int(voln-1);msg1.config(text=f"音量:{voln}%")
    if voln<0:
        voln=voln+1;msg3.config(text="音量最低了!");msg1.config(text=f"音量:{voln}%")
    if mus_m==1:
        volm=voln/100
        music_set_vol(vol=volm)
def vol_reduce_press():
    global root
    vol_reduce()
    global job_id;job_id=root.after(18,vol_reduce_press)
def vol_reduce_release():
    global root
    root.after_cancel(job_id)
#---------------------------------------------暂停按钮---------------------------------------------
def b_mus_pause_check():
    global b_mus_pause_m,mus_m
    if mus_m==0:#未加载音乐状态
        b_pause_img.config(image=ico_pause);b_mus_pause_m=1
    if mus_m==1:#正在播放状态
        b_pause_img.config(image=ico_unpause);b_mus_pause_m=0
def b_mus_pause_update():
    global b_mus_pause_m
    if b_mus_pause_m==0:#改为未暂停属性
        music_unpause()
        b_pause_img.config(image=ico_unpause)
    if b_mus_pause_m==1:#改为暂停属性
        music_pause()
        b_pause_img.config(image=ico_pause)
def b_mus_pause():
    global b_mus_pause_m,mus_m
    if mus_m==0:
        msg2.config(text="音乐未播放")
    else:
        if b_mus_pause_m==0:
            b_mus_pause_m=1;b_mus_pause_update()
        else:
            b_mus_pause_m=0;b_mus_pause_update()
#---------------------------------------------结束播放音乐---------------------------------------------
def b_mus_stop():
    global mus_m
    if mus_m==0:
        msg1.config(text="结束播放")
    if mus_m==1:
        music_stop()
        msg1.config(text="结束播放");mus_m=0;b_mus_pause_check()
#-----------------------------扫描歌曲--------使用scan_mp3_files(url)[是目录名]即可添加到播放列表------------------------------
def scan_mp3_files(url):#扫描,然后启动创建列表函数
    for root, dirs, files in os.walk(url):
        for file in files:
            if file.endswith(".mp3"):
                fn = os.path.splitext(file)[0]#输出名称
                fp = os.path.join(root,fn)#输出路径和名称(不包括后缀名)
                if os.path.exists(f"{fp}.artist"):
                    artist=txt_read_line(f=f"{fp}.artist",n=1)
                else:
                    artist="未知歌手"
                creat_mp3_list(fn,fp,artist)
    #结束扫描时的工作
    b=tk.Button(main1,width=int(xo*0.055),height=int(yo*0.03),bg="green",fg="red",text="已扫描,点击退出",command=lambda:main1.destroy());b.place(x=0,y=0)
    load_music_list();msg3.config(text="已完成扫描")


def txt_add_behind_line(f, n, txt):#文本写入函数,用于支持列表创建函数
    url=f
    try:
        with open(url,'r+') as file:
            lines = file.readlines()
            if len(lines) >= n:
                lines[n-1] = txt + '\n'
            else:
                lines.extend(['\n'] * (n - len(lines) - 1))
                lines.append(txt + '\n')
            file.seek(0)
            file.writelines(lines)
    except FileNotFoundError:
        print("文件未找到")
    except PermissionError:
        print("无法写入文件")
def creat_mp3_list(fn,fp,artist):#创建列表函数
    global creat_list_num;creat_list_num=creat_list_num+1
    txt_add_behind_line(f=mus_list,n=creat_list_num,txt=f"{fp}");creat_list_num=creat_list_num+1
    txt_add_behind_line(f=mus_list,n=creat_list_num,txt=f"{fn}");creat_list_num=creat_list_num+1
    txt_add_behind_line(f=mus_list,n=creat_list_num,txt=f"{artist}")
def choose_file():
    from tkinter import filedialog  #用于弹出文件选择对话框
    os.remove(mus_list)
    with open(mus_list, 'w') as file:
        file.write('')
    file.close()
    dir_path = filedialog.askdirectory(title="选择你要加入播放列表的文件夹")
    scan_mp3_files(url=f"{dir_path}/")
def scan_file():
    global main1,creat_list_num;main1=tk.Tk();creat_list_num=0
    font_1 = font.Font(family='SimHei', size=20)
    root=gui_set(window=main1,bk=1,title="音乐扫描仪",tm=1,w=int(xo*0.4),h=int(yo*0.4),x=int(xo*0.3),y=int(yo*0.3),bg="white",top_m=1,tp_m=1,tp="#F8F8FF")
    b_choose_file=tk.Button(main1,width=int(xo*0.04),height=int(yo*0.008),font=font_1,text="选择目录",bg="green",fg="black",command=choose_file);b_choose_file.place(x=int(xo*0.03),y=int(yo*0.12))
#---------------------------------------------播放列表---------------------------------------------
def count_lines(file_path):#获取总行数
    with open(file_path, 'r') as file:
        lines = file.readlines()
        line_count = len(lines)
    return line_count
def join_mp3_list(url,line_count):#创建tk窗口的播放列表按钮
    for i in range(1,line_count,3):
        global list_num;list_num=list_num+1
        mp3_url=txt_read_line(f=mus_list,n=i)
        mp3_name=txt_read_line(f=mus_list,n=int(i+1))
        mp3_artist=txt_read_line(f=mus_list,n=int(i+2))
        #这里lambda需要转化然后传入,不然执行播放的是最后一个加载的,而不是每次传入的
        b=tk.Button(root,width=int(xo*0.01),height=0,font=font_1,text=f"{mp3_name}",bg="white",fg="green",command=lambda url=mp3_url,name=mp3_name,artist=mp3_artist: b_mus_start(f"{url}.mp3",name=f"{name}",artist=f"{artist}"));c2.create_window(0,int(list_num*yo*0.04),window=b)
def load_music_list():#加载播放列表
    global list_num;list_num=0
    line_count = count_lines(file_path=mus_list)#获取播放列表总行数,以免超出范围引发错误
    join_mp3_list(url=mus_list,line_count=line_count)#开始创建按钮







#----------------------主函数------------------------
#窗口配置
global root
root=tk.Tk()
xo,yo=screen_wh_get()
font_1 = font.Font(family='SimHei', size=20)
root=gui_set(window=root,bk=0,title="音乐播放器",tm=1,w=int(xo*0.0923),h=int(yo*0.95),x=int(xo*0.908),y=int(yo*0.025),bg="#F8F8FF",top_m=1,tp_m=1,tp="#F8F8FF")
#-------------------------------------程序变量-------------------------------------
cx_dll="C:/mh_file/program/music_player"
mus_list=f"{cx_dll}/mus_list.txt"
cx_ico=f"{cx_dll}/ico/"
ico_pause=gui_pic_read(f=f"{cx_ico}/ico_pause.jpg",w=int(xo*0.025),h=int(xo*0.025))
ico_unpause=gui_pic_read(f=f"{cx_ico}/ico_unpause.jpg",w=int(xo*0.025),h=int(xo*0.025))
ico_scan=gui_pic_read(f=f"{cx_ico}/ico_scan.jpg",w=int(xo*0.04),h=int(xo*0.04))
ico_stop=gui_pic_read(f=f"{cx_ico}/ico_stop.jpg",w=int(xo*0.025),h=int(xo*0.025))
ico_close=gui_pic_read(f=f"{cx_ico}/ico_close.jpg",w=int(xo*0.025),h=int(xo*0.025))
#关闭按钮
b=tk.Button(root,width=int(xo*0.032),height=int(xo*0.032),image=ico_close,command=close_exit);b.place(x=int(xo*0.03),y=int(yo*0.23))
#配置基础界面:标签
t=gui_echo_txt(window=root,w=int(xo*0.0066),h=0,x=0,y=0,bg="#F8F8FF",fg="red",size=20,txt="MY播放器")
msg1=gui_echo_txt(window=root,w=int(xo*0.0081),h=0,x=0,y=int(yo*0.8191),bg="#F8F8FF",fg="white",size=16,txt="50%")
msg2=gui_echo_txt(window=root,w=int(xo*0.0081),h=0,x=0,y=int(yo*0.8545),bg="#F8F8FF",fg="white",size=16,txt="---")
msg3=gui_echo_txt(window=root,w=int(xo*0.0081),h=0,x=0,y=int(yo*0.89),bg="#F8F8FF",fg="white",size=16,txt="通知栏")
global mus_m;mus_m=0#变量:是否正在播放音乐
#按钮-----音量加+
global voln;voln=50
font_1 = font.Font(family='SimHei', size=20)
b_add=tk.Button(root,width=int(xo*0.0024),height=0,font=font_1,text="+",bg="white",fg="red");b_add.place(x=0,y=int(yo*0.76))
b_add.bind("<Button-1>",lambda x:vol_add_press())
b_add.bind("<ButtonRelease-1>", lambda x:vol_add_release())
#按钮-----音量减-
b_reduce=tk.Button(root,width=int(xo*0.0024),height=0,font=font_1,text="-",bg="white",fg="red");b_reduce.place(x=int(xo*0.055),y=int(yo*0.76))
b_reduce.bind("<Button-1>",lambda x:vol_reduce_press())
b_reduce.bind("<ButtonRelease-1>", lambda x:vol_reduce_release())
#暂停
global b_mus_pause_m;b_mus_pause_m=0
b_pause_img=tk.Button(root,width=int(xo*0.025),height=int(xo*0.025),image=ico_pause,command=b_mus_pause);b_pause_img.place(x=0,y=int(yo*0.245))
#音乐结束按钮
b_stop_img=tk.Button(root,width=int(xo*0.025),height=int(xo*0.025),image=ico_stop,command=b_mus_stop);b_stop_img.place(x=int(xo*0.065),y=int(yo*0.245))
#加载扫描按钮
font_1 = font.Font(family='SimHei', size=10)
b_scan_file=tk.Button(root,width=int(xo*0.04),height=int(xo*0.04+10),image=ico_scan,font=font_1,text="歌曲扫描",compound="top",command=scan_file);b_scan_file.place(x=int(xo*0.025),y=int(yo*0.12))
#创建播放列表画布
font_1 = font.Font(family='SimHei', size=12)
global c2
c2,s2=creat_canvas_move(window=root,sx=int(xo*0.082),sy=int(yo*0.3),sw=int(xo*0.011),sh=int(yo*0.45),sf="y",cx=0,cy=int(yo*0.3),cw=int(xo*0.082),ch=int(yo*0.45),cf="y",bg="#F8F8FF")
#加载播放列表
load_music_list()
root.protocol("WM_DELETE_WINDOW", close_exit)
root.mainloop()

