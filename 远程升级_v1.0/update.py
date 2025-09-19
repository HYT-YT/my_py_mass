#place: c:\my\program\update\

import os
import zmail
import time
import wget
import ctypes
SW_HIDE = 0
if __name__ == "__main__":
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), SW_HIDE)
    
def x(command):
    os.system(command)




def begin():
    print("进行一次循环:")
    #配置邮箱
    server = zmail.server('upook.com', 'q78')
    #读取本地版本数:version_local
    with open("c:/my/program/update/version.txt") as f:
        version_1 = f.read(1000)
        version_local=int(version_1)
    #获取邮件
    latest_mail = server.get_latest()
    mail = server.get_latest()
    print("邮件主题：", mail['Subject'])
    print("邮件发送时间：", mail['Date'])
    print("发送者：", mail['From'])
    print("接收者：", mail['To'])
    print("内容：", mail['content_text'])
    txtmain = mail['content_text']
    version_net_1 = mail['Subject']
    version_net = int(version_net_1)
    #比较版本数
    if version_net>version_local:
        #进行更新
        print("需要更新")
        #删除上一次的更新包
        x("start c:/my/program/update/del_last_package.bat")
        time.sleep(1)
        with open("c:/my/program/update/reachplace.txt","w") as f:
            f.write(str(txtmain))
        fresh_txt_netplace()
        download_update_zip()
        x("start c:/my/program/update/release.bat")
        print("更新成功")
        time.sleep(100)
        begin()
        
    else:
        #不更新
        time.sleep(60)
        begin()






#重新整理更新包网络位置
def fresh_txt_netplace():
    print("已进行txt网络更新包位置整理")
    with open("c:/my/program/update/reachplace.txt") as f:
        txta = f.read(1000)
        txtb=txta.replace("'","")
        txtc=txtb.replace("[","")
        txtd=txtc.replace("]","")
    with open("c:/my/program/update/reachplace.txt", "w") as file:
        file.write(txtd)



#开始下载更新包
def download_update_zip():
    print("开始下载安装包")
    with open("c:/my/program/update/reachplace.txt") as f:
        txta = f.read(1000)
    url=txta
    path="c:/my/temp/"
    wget.download(url,path)





begin()





    

