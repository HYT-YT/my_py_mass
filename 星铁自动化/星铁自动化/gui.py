import tkinter as tk

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





































