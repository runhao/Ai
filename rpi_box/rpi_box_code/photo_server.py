import cv2
import numpy as np
import time

def is_inside(o, i):
    ox, oy, ow, oh = o
    ix, iy, iw, ih = i
    return ox > ix and oy > iy and ox + ow < ix + iw and oy + oh < iy+ ih


def draw_person(image, person):
    x, y, w, h = person
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 255), 2)

def photo_server():
    cap=cv2.VideoCapture(0) #调用摄像头‘0'一般是打开电脑自带摄像头，‘1'是打开外部摄像头（只有一个摄像头的情况）
    width=640
    height=480
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,width)#设置图像宽度
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,height)#设置图像高度
    s = 0
    start_time = time.time()
    #显示图像
    print("start camera")
    while True: 
        ret,frame=cap.read()#读取图像(frame就是读取的视频帧，对frame处理就是对整个视频的处理)
        #cv2.imshow("frame",frame) 
        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        found, w = hog.detectMultiScale(frame)#将视频帧传入并处理
        found_filtered = []
        for ri, r in enumerate(found):
            for qi, q, in enumerate(found):
                if ri != qi and is_inside(r, q):
                    break
                else:
                    found_filtered.append(r)
            for person in found_filtered:
                    draw_person(frame, person)
        cv2.imshow("people detection", frame)
        """s = s + 1
        if s%10 == 0:
            end_time = time.time()
            print(10/(end_time-start_time))#实际帧数
            start_time = end_time"""
        input=cv2.waitKey(1) #设置帧数
        if input==ord('q'):#如过输入的是q就break，结束图像显示，鼠标点击视频画面输入字符
            break
    
    cap.release()#释放摄像头
    cv2.destroyAllWindows()#销毁窗口