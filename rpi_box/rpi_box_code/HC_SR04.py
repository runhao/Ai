#导入 GPIO库
from yuyin import yuyin
import RPi.GPIO as GPIO
import time
#设置 GPIO 模式为 BCM

#定义 GPIO 引脚
#GPIO_TRIGGER = 20#右
#GPIO_ECHO = 21
#GPIO_TRIGGER = 13#左
#GPIO_ECHO = 26
#GPIO_TRIGGER = 18#前
#GPIO_ECHO = 19
#设置 GPIO 的工作方式 (IN / OUT)

def distance(GPIO_TRIGGER, GPIO_ECHO):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    # 发送高电平信号到 Trig 引脚
    GPIO.output(GPIO_TRIGGER, True)
    # 持续 10 us
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    start_time = time.time()
    stop_time = time.time()
    # 记录发送超声波的时刻1
    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()
        # 记录接收到返回超声波的时刻2
    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()
        # 计算超声波的往返时间 = 时刻2 - 时刻1
        time_elapsed = stop_time - start_time
        # 声波的速度为 343m/s， 转化为 34300cm/s。
        distance = (time_elapsed * 34300) / 2
        #dist = distance
    return float(format(distance))

def warning(n):
    for i in range(n):
        try:
            if distance(18,19) <= 50.0:
                print('前方:'+str(distance(18,19)))
                #yuyin('前方报警！')
                #time.sleep(0.5)
            if distance(13,26) <= 50.0:
                print('左侧:'+str(distance(13,26)))
                #yuyin('左侧报警！')
                time.sleep(0.5)
            if distance(20,21) <= 50.0:
                print('右侧:'+str(distance(20,21)))
                #yuyin('右侧报警！')
                time.sleep(0.5)
            time.sleep(1)
        except Exception as e:
            print(e)
    GPIO.cleanup()
    return 1
warning(100) 