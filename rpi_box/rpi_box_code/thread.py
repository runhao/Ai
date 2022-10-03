import threading
from HC_SR04 import warning
from photo_server import photo_server
from avoid_ob import avoid_ob
import time


def ph():
    photo_server()

def wa():
    warning(1000)

def av():
    avoid_ob(1000)

if __name__ == '__main__':
    p1 = threading.Thread(target=ph,args=())
    p2 = threading.Thread(target=av,args=())
    p3 = threading.Thread(target=wa,args=())
    p1.start()
    time.sleep(1)
    p2.daemon = True
    p2.start()
    time.sleep(1)
    p3.daemon = True
    p3.start()
    
'''if __name__ == '__main__':
    p1 = multiprocessing.Process(target=ph,args=())
    p2 = multiprocessing.Process(target=wa,args=())
    p3 = multiprocessing.Process(target=av,args=())
    p1.start()
    p2.start()
    p3.start()'''