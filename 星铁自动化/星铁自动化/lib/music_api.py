import music
def ring(hz,t):#响起指定频率,时间的响声,hz:频率,t:时间
    music.ring(hz,t)
def music_start(url,vol,postion,loop):#开始播放--mus_url音乐路径,vol音量(0-1),loop(-1:无限循环,0:不播放,N:重复放N次),postion开始播放的位置,返回mus
    mus=music.music_start(url,vol,postion,loop)
    return mus
def music_pause():#暂停播放
    music.music_pause()
def music_unpause():#继续播放
    music.music_unpause()
def music_stop():#结束播放
    music.music_stop()
def music_set_pos(n):#跳转到指定秒速播放
    music.music_set_pos(n)
def music_set_vol(vol):#设置音量
    music.music_set_vol(vol)
def check_music():#获取音乐信息m=(0:未播放,1:正在播放),postion:正在播放的位置,vol:音量(通常为小数,需要[乘法,int,然后除法])
    m,postion,vol=music.check_music()
    return m,postion,vol

