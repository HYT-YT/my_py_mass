import find_similar_img as find_img
#在整个屏幕寻找模版照片---i:模版照片路径,s:阀值,返回xy坐标与(m=0:不存在,m=1:存在)
def find_img_1(i,s):
    x,y,m=find_img.f1(i,s)
    return x,y,m
#在指定区域寻找模版照片---region:区域(x1,y1,x2,y2),i:模版照片路径,s:阀值,返回xy坐标与(m=0:不存在,m=1:存在)
def find_img_2(region,i,s):
    x,y,m=find_img.f2(region,i,s)
    return x,y,m












