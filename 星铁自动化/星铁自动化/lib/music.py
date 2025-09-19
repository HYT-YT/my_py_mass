import time


def ring(hz,t):#响起指定频率的声音,传入hz:声音频率,t:时间(毫秒,1000ms=1s)
    import winsound
    winsound.Beep(hz,t)
def ring1():#长段播放
    import winsound
    import threading
    ring1_1 = threading.Thread(target=ring1_1_1) #设置线程所对应函数
    ring1_1.start()
def ring1_1_1():
    # 定义旋律(前面为赫兹,声音频率--后面为持续时间,毫秒,1000ms=1s)
    notes = [  
    (500,100),
    (1000,100),
    (1500,100),
    (2000,100),
    (2500,100),
    (3000,100),
    (3500,100),
    ]  
    # 播放旋律  
    for frequency, duration in notes:  
        winsound.Beep(frequency, duration)

#开始播放--mus_url音乐路径,vol音量(0-1),loop(-1:无限循环,0:不播放,N:重复放N次),postion开始播放的位置,返回mus
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

