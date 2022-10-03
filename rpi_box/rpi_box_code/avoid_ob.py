from yuyin import yuyin
import RPi.GPIO as GPIO
import time

'''GPIO_TRIGGER_R = 20#右
GPIO_ECHO_R = 21
GPIO_TRIGGER_L = 13#左
GPIO_ECHO_L = 26
GPIO_TRIGGER_H = 18#前
GPIO_ECHO_H = 19'''
sensor_Right=12
sensor_Left=16

def avoid_ob(n):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup((sensor_Right,sensor_Left), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    try:
        for i in range(n):
            status_R = GPIO.input(sensor_Right)
            status_L= GPIO.input(sensor_Left)
            if status_R == False and status_L == False:
                print('两侧检测到障碍物！')
                yuyin('两侧检测到障碍物！')
            elif status_R == True and status_L == False:
                print('右前方检测到障碍物！')
                yuyin('右前方检测到障碍物！')
            elif status_R == False and status_L == True:
                print('左前方检测到障碍物！')
                yuyin('左前方检测到障碍物！')
            '''elif distance(GPIO_TRIGGER_H,GPIO_ECHO_H) >= 50.0:
                print("两侧未检测到障碍物!")
                #print("前方障碍物{:.2f} cm".format(distance(GPIO_TRIGGER_H,GPIO_ECHO_H)))
                time.sleep(1)'''
            #else:
            time.sleep(0.5)
                #print("前方障碍物{:.2f} cm".format(distance(GPIO_TRIGGER_H,GPIO_ECHO_H)))

    except KeyboardInterrupt as e:
        print(e)
        GPIO.cleanup()

#avoid_ob(100)

