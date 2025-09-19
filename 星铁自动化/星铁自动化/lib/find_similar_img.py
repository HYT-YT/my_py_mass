import time
import cv2  #图片识别
import numpy as np  #图片识别灰度
from PIL import ImageGrab  #截取屏幕图像

#基本
def find_similar_img_1(image_path):#模版照片处理,输入路径
    image = cv2.imread(image_path)#读取图片文件
    image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)#转换为灰度图
    w,h = image_gray.shape[::-1]#获取模板图片的宽度和高度
    return image_gray,w,h
def find_similar_img_2():#截屏照片处理
    screen = np.array(ImageGrab.grab())#截屏转换
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)#屏幕图像转换灰度图
    return screen_gray
def find_similar_img_3(image_gray,w,h,screen_gray,threshold):#全屏搜索(处理后的模版,处理后的截屏,模版的宽高,阀值)
    #匹配
    res = cv2.matchTemplate(screen_gray, image_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)#寻找
    if max_val >= threshold:#超过阀值
        #计算坐标
        mean_x = max_loc[0] + int(w / 2)
        mean_y = max_loc[1] + int(h / 2)
        m=1
        return mean_x,mean_y,m
    else:#未超过阀值
        x=0;y=0;m=0
        return x,y,m
def find_similar_img_4(region,image_gray,w,h,screen_gray,threshold):#区域搜索(区域坐标(x1,y1,x2,y2),处理后的模版,处理后的截屏,模版的宽高,阀值)
    #匹配
    res = cv2.matchTemplate(screen_gray[region[1]:region[3], region[0]:region[2]], image_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)#寻找
    if max_val >= threshold:#超过阀值
        #计算坐标
        mean_x = max_loc[0] + int(w / 2)+region[0]
        mean_y = max_loc[1] + int(h / 2)+region[1]
        m=1
        return mean_x,mean_y,m
    else:#未超过阀值
        x=0;y=0;m=0
        return x,y,m
#成品
def f1(i,s):#在整个屏幕寻找模版照片---i:模版照片路径,s:阀值,返回xy坐标与(m=0:不存在,m=1:存在)
    image_gray,w,h=find_similar_img_1(image_path=i)
    screen_gray=find_similar_img_2()
    x,y,m=find_similar_img_3(image_gray,w,h,screen_gray,threshold=s)
    return x,y,m
def f2(region,i,s):#在指定区域寻找模版照片---region:区域(x1,y1,x2,y2),i:模版照片路径,s:阀值,返回xy坐标与(m=0:不存在,m=1:存在)
    image_gray,w,h=find_similar_img_1(image_path=i)
    screen_gray=find_similar_img_2()
    x,y,m=find_similar_img_4(region,image_gray,w,h,screen_gray,threshold=s)
    return x,y,m

