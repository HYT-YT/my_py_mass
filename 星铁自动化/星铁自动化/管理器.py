import time
import os
import subprocess
import star_rail_start as star_start



def start_main(order):
    m=star_start.xt_start(f"{order}")
    if m==1:
        pass
    else:
        exit()
    #运行主程序,运行完毕后再执行下一行
    subprocess.call(["python", "main.pyw"])


def check_file_plan():#检测是否存在以plan命名的
    directory = './plan/'
    m = 0
    for filename in os.listdir(directory):
        if filename.startswith('need_') and filename.endswith('.txt'):
            m = 1
            break
    return m


def read_second_line(file_path):#读取那个浏览器
    with open(file_path, 'r', encoding='ANSI') as f:
        lines = f.readlines()
        return lines[1].strip()


if __name__=="__main__":
    subprocess.call(["change_day_pre.bat"])#每天重置
    while True:
        time.sleep(1)
        subprocess.call(["change.bat"])#刷新任务
        time.sleep(1)
        order=read_second_line("plan_use_exe.txt")
        start_main(order)
        m=check_file_plan()#检测是否完成当天全部计划
        if m==0:#不存在,全部完成
            break
    exit()



