import threading
import os
import time

def fun1():
  os.system('python /content/stable-diffusion-webui/webui.py')
def fun2():
  os.system('python /content/stable-diffusion-webui/webuiapi_test.py')
thread1 = threading.Thread(name='t1',target=fun1,args=())
thread2 = threading.Thread(name='t2',target=fun2,args=())
thread1.start()   #启动线程1
time.sleep(60)
thread2.start()   #启动线程2

