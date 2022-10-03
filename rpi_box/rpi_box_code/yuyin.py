import os
from tkinter import EXCEPTION
from aip import AipSpeech

def yuyin(outstr):

    """ 你的 APPID AK SK """
    # 请自行替换
    APP_ID = '26032630'
    API_KEY = 'C2Kfa93OcZ6NM3HqD5Y9Dh6Y'
    SECRET_KEY = 'sfX3P51N9fOjQXGwee5ER6iiiRza5jwT'

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    result  = client.synthesis(outstr, 'zh', 1, {'vol':8,'per':5})
    
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open('audio.mp3', 'wb+') as f:
            f.write(result)

    cmdline = 'mplayer audio.mp3'
    os.system(cmdline)
    return True

yuyin("本次导航结束")
