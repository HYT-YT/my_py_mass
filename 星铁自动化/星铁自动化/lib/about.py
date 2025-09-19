def txt_read_line(f,n):
    with open(f, "r",encoding='utf-8') as file:
        txt = file.readlines()[n-1].strip()
        return txt
def version_get():
    version=txt_read_line(f="version.txt",n=1)
    version = version.replace('\ufeff', '')#txt带有一个不可见的字符,需要删除
    version=float(version)
    return version
def model_get():
    model=txt_read_line(f="version.txt",n=2)
    model=str(model)
    return model

def not_suit_version():
    file_path = "version_refuse.txt"
    result = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip().replace('\ufeff', '')  # 删除不可见的字符
            result.append(float(line))
    return result


def version_check(v_u):
    v_u=float(v_u)
    v_n=version_get()
    not_suit=not_suit_version()
    if v_u in not_suit:
        m=0;return m
    if v_n>v_u:
        m=1;return m
    if v_n<v_u:
        m=2;return m
    if v_n==v_u:
        m=3;return m



if __name__=="__main__":
    print("说明:")
    print("   本文件夹中,后面加_api的文件,内部装载了成品函数和说明,调用_api文件即可")
    print("本库的调用方法:")
    print("     调用本库的version_get函数,即可获取版本信息")
    print("     调用version_check,传递你自己的参数,即可检测是否兼容")
    print("     如果version_check返回的值为(0:不兼容,1:兼容,2:目前库文件版本较低,部分功能受限,3:版本匹配)")
    print("     调用model_get,查看型号")
    print("目前版本:")
    v=version_get();print("     ",v)
    print("目前型号:")
    m=model_get();print("     ",m)
    while True:
        print("--------------------------------------------")
        v_u=input("可以输入你的要测试的版本,来确认是否与此版本兼容: ")
        m=version_check(v_u)
        print("结果如下:")
        if m==0:
            print("      不兼容")
        elif m==1:
            print("      兼容")
        elif m==2:
            print("      目前库文件版本较低,部分功能受限")
        elif m==3:
            print("      版本相同")
        else:
            print("      未知错误,可能受篡改")










