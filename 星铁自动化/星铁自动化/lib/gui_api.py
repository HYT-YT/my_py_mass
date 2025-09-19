import gui

#设置gui界面，bk=0无边框,title标题,tm为透明属性(0:完全透明-1:不透明)
#top_m=1时顶置窗口
#如果tp_m=1,那么tp="某种颜色",这种颜色将在这个窗口内替换为透明(且操作穿透),建议使用16进制颜色
def tk_set(window,bk,title,tm,w,h,x,y,bg,top_m,tp_m,tp):
    window=gui.set_gui(window,bk,title,tm,w,h,x,y,bg,top_m,tp_m,tp)
    return window


#-----基础-----
def screen_wh_get():#获取屏幕分辨率
    w,h=gui.get_screen_wh()
    return w,h
def tk_off(window):#隐藏tk窗口
    gui.tk_off(window)
def tk_on(window):#显示tk窗口
    gui.tk_on(window)
def clear_window(window):#清除目标窗口所有部件
    gui.clear_window(window)
def cx_off():#隐藏任务(黑框框)
    gui.cx_off()
def cx_on():#显示任务(黑框框)
    gui.cx_on()
def pic_read(f,w,h):#读取图片(用于照片按钮)
    img=gui.pic(f,w,h)
    return img


#-----中级-----
def echo_txt(window,w,h,x,y,bg,fg,size,txt):#显示标签
    l=gui.echo_txt(window,w,h,x,y,bg,fg,size,txt)
    return l
def pic_echo(window,f,w,h,x,y):#创建图片标签(显示图片)
    l=gui.pic_echo(window,f,w,h,x,y)
    return l
def entry_input(window,x,y,w,font,bg,fg,show):#x,y,w为坐标,宽,font的字体大小用于调节高度,bg,fg为背景文字颜色,show(0:密码框,1:明文框,2:密码框(有按钮查看密码))
    e=gui.entry_input(window,x,y,w,font,bg,fg,show)
    return e
#弹出窗口,让用户选择文件
def get_file_path(title,variety,allow_m,allow):#variety=(0/1:单/多选),当allow_m=1时,进行格式限制,allow格式:allow=(("文本文件","*.txt"), ("所有文件","*.*")..)
    file_path=gui.get_file_path(title,variety,allow_m,allow)
    return file_path
def get_files_path(title):#弹出窗口,让用户选择目录
    dir_path=gui.get_files_path(title)
    return dir_path
def gui_pic_move_die(window,f,w,h,x1,y1,x2,y2,s,n):#(移动后图片消失),n为移动次数(越大越精细)
    gui.pic_move_l(window,f,w,h,x1,y1,x2,y2,s,n)
def gui_pic_move_live(window,f,w,h,x1,y1,x2,y2,s,n):#(移动后图片保留),n为移动次数(越大越精细)
    limg=gui.pic_move_k(window,f,w,h,x1,y1,x2,y2,s,n)
    return limg


#-----高级-----
#顶部消息框:x/y:出现于x轴,从顶部下滑至y轴,t:移动至制定位置后等待时间,s为速度,bg,fg为背景/文字颜色
def gui_msg_txt_s1(window,w,h,x,y,bg,fg,size,t,s,txt):#不阻塞线程版
    gui.msg_txt_s1(window,w,h,x,y,bg,fg,size,t,s,txt)
def gui_msg_txt_s2(window,w,h,x,y,bg,fg,size,t,s,txt):#阻塞线程版
    gui.msg_txt_s2(window,w,h,x,y,bg,fg,size,t,s,txt)
#渐变文字(白-黑-白)t:转为黑色后停留时间;n:数字越大最后越黑;s:变化速度
def gui_echo_txt_jb1(window,w,h,x,y,size,txt,t,s,n):#不阻塞线程
    gui.echo_txt_s1(window,w,h,x,y,size,txt,t,s,n)
def gui_echo_txt_jb2(window,w,h,x,y,size,txt,t,s,n):#阻塞线程
    gui.echo_txt_s2(window,w,h,x,y,size,txt,t,s,n)
#渐变,no1/2/3:初始三原色,nl1/2/3:变化后三原色,ns:变化次数,返回l标签
def echo_txt_jb(window,w,h,x,y,size,txt,s,no1,no2,no3,nl1,nl2,nl3,ns,bg):
    l=gui.echo_txt_s3(window,w,h,x,y,size,txt,s,no1,no2,no3,nl1,nl2,nl3,ns,bg)
    return l
#图片移动并返回n:移动的总次数,f为路径,s为每次移动停顿时间(毫秒),t为移动到制定位置后的等待时间
def gui_pic_move_back(window,f,w,h,x1,y1,x2,y2,s,n,t):
    gui.pic_move_back(window,f,w,h,x1,y1,x2,y2,s,n,t)
#gif播放winodws:窗口名,f:路径,x,y:坐标(左上)
def gui_gif_echo(window,f,x,y):
    l=gui.gif_echo(window,f,x,y)
    return l













