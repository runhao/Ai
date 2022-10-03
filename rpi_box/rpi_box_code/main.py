from gaode_direction import gaode_direction
from gaode_place import gaode_place
from sp_re import sp_re
from yuyin import yuyin
import RPi.GPIO as GPIO
import time
from gps import GPS
import sys
from gaode_geocode import gaode_geocode
from avoid_ob import avoid_ob
from HC_SR04 import warning
from photo_server import photo_server
import threading

'''GPIO_TRIGGER_R = 20#右
GPIO_ECHO_R = 21
GPIO_TRIGGER_L = 13#左
GPIO_ECHO_L = 26
GPIO_TRIGGER_H = 18#前
GPIO_ECHO_H = 19'''

'''yuyin("这里是智能导盲系统,系统正在初始化")
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)   #按钮是用的是GPIO22
origin = GPS()
if origin == 0:    #检测GPS是否连接卫星
    yuyin("G P S 信号弱,请稍后再试")
    sys.exit()
yuyin("当前坐标定位:" + gaode_geocode(origin) + " 请单击按钮,并告诉我目的地")    #提示当前定位
#yuyin("请单击按钮后告诉我目的地")
while True:    #监听按钮状态
    if GPIO.input(22) == 1:
        print(GPIO.input(22))
        break
    time.sleep(0.1)
destinaton = sp_re()    #语音识别目的地
destinaton_gps = gaode_place(destinaton)    #获取目的地坐标
destinaton_gps_list = destinaton_gps.split(',')
yuyin("接下来为您导航" + gaode_geocode(destinaton_gps_list))    #播报高德目的地
origin = str(origin[0]) + ',' + str(origin[1])
direction = gaode_direction(origin,destinaton_gps)    #获取路径规划集合
s = 0
for i in direction:
    yuyin(direction[s]["instruction"])    #播报路径规划字典内容
    s = s + 1
    time.sleep(1)
avoid_ob(3)    #红外模组运行三次(n)
warning(1)    #超声波模组运行三次(3n)'''

def interactive():
    yuyin("这里是智能导盲系统,系统正在初始化")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(22, GPIO.OUT)   #按钮是用的是GPIO22
    origin = GPS()
    if origin == 0:    #检测GPS是否连接卫星
        yuyin("G P S 信号弱,请稍后再试")
        #sys.exit()
        return 0
    yuyin("当前坐标定位:" + gaode_geocode(origin) + " 请单击按钮,并告诉我目的地")    #提示当前定位
    #yuyin("请单击按钮后告诉我目的地")
    while True:    #监听按钮状态
        if GPIO.input(22) == 1:
            print(GPIO.input(22))
            break
        time.sleep(0.1)
    destinaton = sp_re()    #语音识别目的地
    destinaton_gps = gaode_place(destinaton)    #获取目的地坐标
    destinaton_gps_list = destinaton_gps.split(',')
    yuyin("接下来为您导航" + gaode_geocode(destinaton_gps_list))    #播报高德目的地
    origin = str(origin[0]) + ',' + str(origin[1])
    direction = gaode_direction(origin,destinaton_gps)    #获取路径规划集合
    s = 0
    for i in direction:
        yuyin(direction[s]["instruction"])    #播报路径规划字典内容
        s = s + 1
        time.sleep(1)
    return 1

def ph():
    photo_server()

def wa():
    warning(1000)

def av():
    avoid_ob(1000)

if __name__ == '__main__':
    interactive()
    p1 = threading.Thread(target=ph,args=())
    #p2 = threading.Thread(target=av,args=())
    p3 = threading.Thread(target=wa,args=())
    p1.start()
    time.sleep(1)
    #p2.daemon = True
    #p2.start()
    #time.sleep(1)
    p3.daemon = True
    p3.start()