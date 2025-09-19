import operate
def click_left():#左击
    operate.click_left()
def click_right():#右击
    operate.click_right()
def press(x):#点按x键
    operate.press(x)
def press_on(x):#按住x键
    operate.press_on(x)
def press_off(x):#放开x键
    operate.press_off(x)
def input_txt(txt):#输入文本
    operate.input(txt)
def mouse_moveto(x,y,t):#鼠标位置移至,t为花费时间
    operate.mouse_moveto(x,y,t)
def mouse_drato(x,y,t):#从当前位置拖拽至,t为花费时间
    operate.mouse_drato(x,y,t)
def mouse_postion_get():#获取当前鼠标位置
    operate.mouse_postion_get()
def check_keyboard(x):#检测当前某个键位是否按下,返回m=0未按住,m=1正在按住
    m=operate.check_keyboard(x)
    return m













