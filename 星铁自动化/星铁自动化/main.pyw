import time
import sys
sys.path.append("./lib")
import find_similar_img_api as find_img
import operate_api as operate

#基本参数设置
order_txt="plan.txt"#计划表文件位置
f_phone="img/phone"
f_jixing="img/phone/jixing"
f_cailiaoweituo="img/phone/cailiao_weituo"
f_pre_fight="img/pre_fight"
f_menu="img/menu"
f_suaben="img/menu/suaben"
f_meiriweituo="img/menu/meiri_weituo"
f_suaben_cailiao="img/menu/suaben/cailiao"
f_suaben_cailiao_1="img/menu/suaben/cailiao/1"#基础材料
f_suaben_cailiao_2="img/menu/suaben/cailiao/2"#行迹材料
f_suaben_cailiao_3="img/menu/suaben/cailiao/3"#圣遗物
f_img="img"

def write_log(txt):
    time_now=time.time();time_now=round(time_now,1)
    txt_write_add(f="log.txt",txt=f"{time_now}---{txt}")
def cx_exit():
    write_log("--------------程序结束运行---------------")
    exit()
def pc_shutdown():#关机
    import os
    write_log("--------------关机---------------")
    os.system("shutdown -s -t 3")
    exit()

def txt_read_line(f,n):#读取文件---f为文件路径,n为要读取的第N行
    with open(f,"r",encoding="utf-8") as file:
        txt = file.readlines()[n-1].strip()
        return txt

def txt_write_add(f,txt):#追加写入
    with open(f,"a",encoding="utf-8") as file:
        file.write(f"\r\n{txt}")
def txt_write_all(f,txt):#覆盖写入
    with open(f,"w",encoding="utf-8") as file:
        file.write(txt)
def chick_pos(x,y):#点击制定位置
    operate.mouse_moveto(x=x,y=y,t=0)
    operate.click_left()
def find_and_chick(i,s):#点击制定位置图片
    x,y,m=find_img.find_img_1(i=i,s=s)
    if m==1:
        chick_pos(x=x,y=y)
def drato_down(i,n,t,s):#下滑(从某张图片出,向上拖拽一段距离)(n:y轴距离)(t:时间)(s:相似度)
    x,y,m=find_img.find_img_1(i,s)
    if m==1:
        operate.mouse_moveto(x=x,y=y,t=0)
        operate.mouse_drato(x=x,y=int(y-n),t=t)


#在列表内查找某图片,然后传送(会在列表下翻)(目标目录以连续的数字命名图片)(目录后不含/)
def find_img_in_list_and_chick(d,n,dl):#刷本_行迹材料(n:为第n个)(d:目标目录)(n:目标目录下的第N个)(dl:下滑距离)(dt下滑时间)(ut刷新缓冲时间)
    #参数设置:(dra_long下滑距离)(dra_time下滑时间)(dra_sim下滑定位点相似度)(enter_sim目的照片相似度)(update_time下滑刷新时间)
    dra_long=dl;dra_time=0.5;dra_sim=0.7;enter_sim=0.9;update_time=0.2
    for i in range(1,999,1):
        x1,y1,m1=find_img.find_img_1(i=f"{d}/{n}.JPG",s=enter_sim)
        if m1==1:#找到了--开始
            x2,y2,m2=find_img.find_img_2(region=(int(x1),int(y1-50),int(x1+1000),int(y1+50)),i="img/1.JPG",s=enter_sim)
            chick_pos(x=x2,y=y2)
            break
        else:#没找到---下滑
            for i1 in range(1,999,1):
                x3,y3,m3=find_img.find_img_1(i=f"{d}/{i1}.JPG",s=dra_sim)
                if m3==1:#找到可下滑点,下滑
                    drato_down(i=f"{d}/{i1}.JPG",n=dra_long,t=dra_time,s=dra_sim)
                    i2=i1#保存此次下滑点
                    break
                else:#找不到下滑点
                    i1=i2#还原上次下滑点位置
                    x3,y3,m3=find_img.find_img_1(i=f"{d}/{i1}.JPG",s=dra_sim)#查找上次下滑点
                    if m3==1:#如果上次下滑点在屏幕中存在,下滑
                        drato_down(i=f"{d}/{i1}.JPG",n=dra_long,t=dra_time,s=dra_sim)
                        break
                    else:#如果上次下滑点不存在,查找以下的下滑点
                        for i3 in range(1,999,1):
                            i4=i2+i3
                            x4,y4,m4=find_img.find_img_1(i=f"{d}/{i4}.JPG",s=dra_sim)
                            if m4==1:#如果这次能找到下方的下滑点,下滑,没有则继续查找下一个
                                drato_down(i=f"{d}/{i4}.JPG",n=dra_long,t=dra_time,s=dra_sim)
                                break
                        break
        time.sleep(update_time)

#项目录专属列表查询(克隆上一个函数)
def find_img_in_list_and_chick_1(d,n,dl):
    dra_long=dl;dra_time=0.5;dra_sim=0.7;enter_sim=0.9;update_time=0.2
    for i in range(1,999,1):
        xk1,yk1,mk1=find_img.find_img_1(i=f"{d}/{n}.JPG",s=enter_sim)
        if mk1==1:
            chick_pos(x=xk1,y=yk1)
            break
        else:
            for i1 in range(1,999,1):
                xk3,yk3,mk3=find_img.find_img_1(i=f"{d}/{i1}.JPG",s=dra_sim)
                if mk3==1:
                    drato_down(i=f"{d}/{i1}.JPG",n=dra_long,t=dra_time,s=dra_sim)
                    i2=i1
                    break
                else:
                    i1=i2
                    xk3,yk3,mk3=find_img.find_img_1(i=f"{d}/{i1}.JPG",s=dra_sim)
                    if mk3==1:
                        drato_down(i=f"{d}/{i1}.JPG",n=dra_long,t=dra_time,s=dra_sim)
                        break
                    else:
                        for i3 in range(1,999,1):
                            i4=i2+i3
                            xk4,yk4,mk4=find_img.find_img_1(i=f"{d}/{i4}.JPG",s=dra_sim)
                            if mk4==1:
                                drato_down(i=f"{d}/{i4}.JPG",n=dra_long,t=dra_time,s=dra_sim)
                                break
                        break
        time.sleep(update_time)

def exit_now_page():#关闭当前页面
    x,y,m=find_img.find_img_1(i="img/exit.jpg",s=0.8)
    if m==0:
        operate.press("G")
    if m==1:
        chick_pos(x=x,y=y)

def return_main_page():#重置界面,返回主界面
    for i in range(1,20,1):
        m=test_if_in_main_page(s=0.8)
        if m==1:
            break
        else:
            time.sleep(0.7)
            find_and_chick(i=f"{f_img}/exit.jpg",s=0.8)
    m=test_if_in_main_page(s=0.8)
    if m==0:
        for i1 in range(80,40,-5):
            i2=i1/100
            m1=test_if_in_main_page(s=i2)
            if m1==1:
                break
            else:
                time.sleep(0.7)
                find_and_chick(i=f"{f_img}/exit.jpg",s=i2)
        
    

def test_if_in_main_page(s):#检测是否位于主界面(位于主界面:返回1)(否:返回0)
    xt1,yt1,mt1=find_img.find_img_1(i=f"{f_phone}/1.jpg",s=s)
    xt2,yt2,mt2=find_img.find_img_1(i=f"{f_phone}/2.jpg",s=s)
    if mt1==1 or mt2==1:
        m=1;return m
    else:
        m=0;return m

def among_fight():#接管"正在战斗界面"
    for i in range(1200):
        x1,y1,m1=find_img.find_img_1(i=f"{f_pre_fight}/fight_fail_1.JPG",s=0.95)
        x2,y2,m2=find_img.find_img_1(i=f"{f_pre_fight}/fight_success.JPG",s=0.95)
        m3=test_if_in_main_page(s=0.9)#检测是否回到主界面(与大世界普通怪物战斗不会出现刷本胜利选项)
        if m1==1:
            write_log("战斗失败")
            break
        if m2==1:
            write_log("战斗成功")
            break
        if m3==1:
            return
        if i>600:
            write_log("挑战时间大于10分钟")
        if i>900:
            write_log("挑战时间大于15分钟,可能程序出现异常")
        if i>1200:
            write_log("挑战时间大于20分钟,程序出现异常,可能没有开启自动战斗,即将退出此次战斗")
            find_img.find_img_1(i=f"{f_pre_fight}/pause.JPG",s=0.6)
            find_img.find_img_1(i=f"{f_pre_fight}/leave.JPG",s=0.6)
            return
        time.sleep(1)
    if m1==1:
        find_and_chick(i=f"{f_pre_fight}/fight_fail_2.JPG",s=0.9)
    if m2==1:
        find_and_chick(i=f"{f_pre_fight}/exit_fight.JPG",s=0.9)
    return_main_page()


def initialize_fight():#初始化"正在战斗界面"
    time.sleep(0.5)
    for ii1 in range(100,70,-1):
        si=ii1/100
        x1,y1,m1=find_img.find_img_1(i=f"{f_pre_fight}/beishu_close.JPG",s=si)
        x2,y2,m2=find_img.find_img_1(i=f"{f_pre_fight}/beishu_open.JPG",s=si)
        print(m1,m2)
        if m1==1:
            if m2==0:
                find_and_chick(i=f"{f_pre_fight}/beishu_close.JPG",s=si)
                break
        if m2==1:
            if m1==0:
                break
        if m1==1:
            if m2==1:
                write_log("倍数判断错误:既是打开也是关闭的")
                break
    time.sleep(0.5)
    find_and_chick(i=f"{f_pre_fight}/auto_close.JPG",s=0.3)
    among_fight()

def initialize_fight_1():#检测是否进入"正在战斗界面"
    for i in range(40):
        time.sleep(0.5)
        x1,y1,m1=find_img.find_img_1(i=f"{f_pre_fight}/beishu_close.JPG",s=0.8)
        x2,y2,m2=find_img.find_img_1(i=f"{f_pre_fight}/beishu_open.JPG",s=0.8)
        x3,y3,m3=find_img.find_img_1(i=f"{f_pre_fight}/auto_close.JPG",s=0.8)
        x4,y4,m4=find_img.find_img_1(i=f"{f_pre_fight}/auto_open.JPG",s=0.8)
        if m1==1 or m2==1 or m3==1 or m4==1:
            break
    initialize_fight()

def pre_fight(n,helper):#配置"刷本战斗配置界面"(n:几次)(helper=[0:不支援,1:支援])
    if n>1:
        for i in range(n-1):
            time.sleep(0.3)
            find_and_chick(i=f"{f_pre_fight}/add.JPG",s=0.8)
    time.sleep(0.5)
    find_and_chick(i=f"{f_pre_fight}/fight.JPG",s=0.8)
    time.sleep(2)
    if helper==1:
        find_and_chick(i=f"{f_pre_fight}/helper.JPG",s=0.6)
        time.sleep(1.5)
        find_and_chick(i=f"{f_pre_fight}/join_team.JPG",s=0.6)
        time.sleep(1)
    find_and_chick(i=f"{f_pre_fight}/begin_fight.JPG",s=0.8)
    initialize_fight_1()


def pre_fight_1(n,helper):#检测是否进入"刷本战斗配置界面"
    for i in range(60):
        time.sleep(1)
        x,y,m=find_img.find_img_1(i=f"{f_pre_fight}/fight.JPG",s=0.8)
        if m==1:
            pre_fight(n=n,helper=helper)
            break

def open_phone():#打开手机
    return_main_page()
    x1,y1,m1=find_img.find_img_1(i=f"{f_phone}/1.jpg",s=0.8)
    if m1==1:
        chick_pos(x=x1,y=y1)
    else:
        x2,y2,m2=find_img.find_img_1(i=f"{f_phone}/2.jpg",s=0.8)
        if m2==1:
            chick_pos(x=x2,y=y2)
        else:
            operate.press("P")
    time.sleep(2)
def open_menu():#打开菜单
    open_phone()
    find_and_chick(i=f"{f_menu}/1.jpg",s=0.8)
    time.sleep(2)
def open_menu_sb():#菜单_打开刷本
    open_menu()
    find_and_chick(i=f"{f_suaben}/cailiao_close.JPG",s=0.8)
    find_and_chick(i=f"{f_suaben}/cailiao_open.JPG",s=0.8)
    time.sleep(1)
def finish_meiriweituo():#完成每日委托
    open_menu()
    find_and_chick(i=f"{f_meiriweituo}/weituo_close.JPG",s=0.9)
    find_and_chick(i=f"{f_meiriweituo}/weituo_open.JPG",s=0.9)
    time.sleep(1)
    for i in range(8):
        time.sleep(0.3)
        find_and_chick(i=f"{f_meiriweituo}/get_rewards.JPG",s=0.9)
    find_and_chick(i=f"{f_meiriweituo}/get_reward_1.jpg",s=0.75)
    time.sleep(2)
    find_and_chick(i=f"{f_meiriweituo}/1.jpg",s=0.4)
    write_log("已完成每日委托")
    return_main_page()
def finish_cailiao_weituo():#完成材料委托
    open_phone()
    find_and_chick(i=f"{f_cailiaoweituo}/1.jpg",s=0.95)
    find_and_chick(i=f"{f_cailiaoweituo}/2.jpg",s=0.95)
    time.sleep(2)
    for i in range(5):
        find_and_chick(i=f"{f_cailiaoweituo}/get.jpg",s=0.95)
        time.sleep(1)
        find_and_chick(i=f"{f_cailiaoweituo}/hand_out.jpg",s=0.95)
        time.sleep(2.5)
    write_log("已完成材料委托")
    return_main_page()
def finish_jixing():#完成纪行
    open_phone()
    time.sleep(2)
    find_and_chick(i=f"{f_jixing}/1.jpg",s=0.6)
    time.sleep(1)
    for i in range(6):
        time.sleep(0.6)
        find_and_chick(i=f"{f_jixing}/2.jpg",s=0.9)
    time.sleep(1)
    find_and_chick(i=f"{f_jixing}/3.jpg",s=0.8)
    time.sleep(1)
    find_and_chick(i=f"{f_jixing}/4.jpg",s=0.8)
    write_log("已完成纪行")
    return_main_page()
def menu_sb_1(n):#刷本_花萼金
    open_menu_sb()
    find_img_in_list_and_chick_1(d=f"{f_suaben_cailiao}",n=1,dl=50);time.sleep(1)
    find_img_in_list_and_chick(d=f"{f_suaben_cailiao_1}",n=n,dl=60)
def menu_sb_2(n):#刷本_花萼赤
    open_menu_sb()
    find_img_in_list_and_chick_1(d=f"{f_suaben_cailiao}",n=2,dl=50);time.sleep(1)
    find_img_in_list_and_chick(d=f"{f_suaben_cailiao_2}",n=n,dl=80)
def menu_sb_3(n):#刷本_圣遗物
    open_menu_sb()
    find_img_in_list_and_chick_1(d=f"{f_suaben_cailiao}",n=3,dl=50);time.sleep(1)
    find_img_in_list_and_chick(d=f"{f_suaben_cailiao_3}",n=n,dl=80)





if __name__=="__main__":
    write_log("--------------开始运行---------------")
    for num_m in range(2,999999,1):
        order=txt_read_line(f=order_txt,n=num_m);order=str(order)#注意,第一行有不可见字符,不要用第一行为命令行
        #-------------------函数区-------------------
        if order=="打开菜单":
            open_menu()
        elif order=="打开手机":
            open_phone()
        elif order=="打开刷本":
            open_menu_sb()
        elif order=="完成每日委托":
            finish_meiriweituo()
        elif order=="完成材料委托":
            finish_cailiao_weituo()
        elif order=="完成纪行":
            finish_jixing()
        elif order=="关闭":
            exit_now_page()
        elif order=="返回主界面":
            return_main_page()
        #-------------------读取区-------------------
        elif order=="花萼金":
            order=txt_read_line(f=order_txt,n=int(num_m+1));order=int(order)
            menu_sb_1(order)
        elif order=="花萼赤":
            order=txt_read_line(f=order_txt,n=int(num_m+1));order=int(order)
            menu_sb_2(order)
        elif order=="圣遗物":
            order=txt_read_line(f=order_txt,n=int(num_m+1));order=int(order)
            menu_sb_3(order)
        elif order=="准备战斗":
            order1=txt_read_line(f=order_txt,n=int(num_m+1));order1=int(order1)
            order2=txt_read_line(f=order_txt,n=int(num_m+2))
            if order2=="是":
                helper=1
            else:
                helper=0
            pre_fight_1(order1,helper)
        elif order=="接管战斗":
            initialize_fight_1()
        #-------------------命令区-------------------
        elif order=="exit":
            cx_exit()
        elif order=="wait":
            order=txt_read_line(f=order_txt,n=int(num_m+1));order=int(order)
            time.sleep(order)
        elif order=="shutdown":
            pc_shutdown()





