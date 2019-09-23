#!/usr/bin/env/python
# File name   : server.py
# Production  : GWR
# Website     : www.gewbot.com
# E-mail      : gewubot@163.com
# Author      : William
# Date        : 2019/07/24

import socket
import time
import threading
import move
import Adafruit_PCA9685
import os
import FPV
import info
import servo
import LED
import findline
import switch
import ultra
import PID
from mpu6050 import mpu6050

MPU_connection = 1
try:
    sensor = mpu6050(0x68)
    print('mpu6050 connected, PT MODE ON\n检测到已连接姿态传感器，当前为云台模式。')
except:
    MPU_connection = 0
    print('mpu6050 disconnected, ARM MODE ON\n检测到未连接姿态传感器，当前为机械臂模式。')

servo_speed  = 11
functionMode = 0
dis_keep = 0.35
goal_pos = 0
tor_pos  = 1
mpu_speed = 2
init_get = 0

class Servo_ctrl(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(Servo_ctrl, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()     # 用于暂停线程的标识
        self.__flag.set()       # 设置为True
        self.__running = threading.Event()      # 用于停止线程的标识
        self.__running.set()      # 将running设置为True

    def run(self):
        global goal_pos, servo_command, init_get, functionMode
        while self.__running.isSet():
            self.__flag.wait()      # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            if functionMode != 6:
                if servo_command == 'lookleft':
                    servo.lookleft(servo_speed)
                elif servo_command == 'lookright':
                    servo.lookright(servo_speed)
                elif servo_command == 'up':
                    servo.up(servo_speed)
                elif servo_command == 'down':
                    servo.down(servo_speed)
                elif servo_command == 'lookup':
                    servo.lookup(servo_speed)
                elif servo_command == 'lookdown':
                    servo.lookdown(servo_speed)
                elif servo_command == 'grab':
                    servo.grab(servo_speed)
                elif servo_command == 'loose':
                    servo.loose(servo_speed)
                else:
                    pass

            if functionMode == 4:
                servo.ahead()
                findline.run()
                if not functionMode:
                    move.motorStop()
            elif functionMode == 5:
                servo.ahead()
                dis_get = ultra.checkdist()
                if dis_get < 0.15:
                    move.motorStop()
                    move.move(100, 'backward', 'no', 1)
                    move.motorStop()
                    move.move(100, 'no', 'left', 1)
                    time.sleep(0.2)
                    move.motorStop()
                else:
                    move.move(100, 'forward', 'no', 1)
                if not functionMode:
                    move.motorStop()
            elif functionMode == 6:
                if MPU_connection:
                    accelerometer_data = sensor.get_accel_data()
                    Y_get = accelerometer_data['y']
                    if not init_get:
                        goal_pos = Y_get
                        init_get = 1
                    if servo_command == 'up':
                        servo.up(servo_speed)
                        time.sleep(0.2)
                        accelerometer_data = sensor.get_accel_data()
                        Y_get = accelerometer_data['y']
                        goal_pos = Y_get
                    elif servo_command == 'down':
                        servo.down(servo_speed)
                        time.sleep(0.2)
                        accelerometer_data = sensor.get_accel_data()
                        Y_get = accelerometer_data['y']
                        goal_pos = Y_get
                    if abs(Y_get-goal_pos)>tor_pos:
                        if Y_get < goal_pos:
                            servo.down(int(mpu_speed*abs(Y_get - goal_pos)))
                        elif Y_get > goal_pos:
                            servo.up(int(mpu_speed*abs(Y_get - goal_pos)))
                        time.sleep(0.03)
                        continue
                else:
                    functionMode = 0
                    try:
                        self.pause()
                    except:
                        pass

            time.sleep(0.07)

    def pause(self):
        self.__flag.clear()     # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()    # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()       # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()        # 设置为False  


def info_send_client():
    SERVER_IP = addr[0]
    SERVER_PORT = 2256   #Define port serial 
    SERVER_ADDR = (SERVER_IP, SERVER_PORT)
    Info_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Set connection value for socket
    Info_Socket.connect(SERVER_ADDR)
    print(SERVER_ADDR)
    while 1:
        try:
            Info_Socket.send((info.get_cpu_tempfunc()+' '+info.get_cpu_use()+' '+info.get_ram_info()+' '+str(servo.get_direction())).encode())
            time.sleep(1)
        except:
            time.sleep(10)
            pass


def FPV_thread():
    global fpv
    fpv=FPV.FPV()
    fpv.capture_thread(addr[0])


def  ap_thread():
    os.system("sudo create_ap wlan0 eth0 AdeeptCar 12345678")


def run():
    global servo_move, speed_set, servo_command, functionMode, init_get
    servo.servo_init()
    move.setup()
    findline.setup()
    direction_command = 'no'
    turn_command = 'no'
    servo_command = 'no'
    speed_set = 100
    rad = 0.5

    info_threading=threading.Thread(target=info_send_client)    #Define a thread for FPV and OpenCV
    info_threading.setDaemon(True)                             #'True' means it is a front thread,it would close when the mainloop() closes
    info_threading.start()                                     #Thread starts


    servo_move = Servo_ctrl()
    servo_move.start()
    servo_move.pause()
    findline.setup()
    while True: 
        data = ''
        data = str(tcpCliSock.recv(BUFSIZ).decode())
        if not data:
            continue

        elif 'forward' == data:
            direction_command = 'forward'
            move.move(speed_set, direction_command, turn_command, rad)
        
        elif 'backward' == data:
            direction_command = 'backward'
            move.move(speed_set, direction_command, turn_command, rad)

        elif 'DS' in data:
            direction_command = 'no'
            move.move(speed_set, direction_command, turn_command, rad)

        elif 'left' == data:
            turn_command = 'left'
            move.move(speed_set, direction_command, turn_command, rad)

        elif 'right' == data:
            turn_command = 'right'
            move.move(speed_set, direction_command, turn_command, rad)

        elif 'TS' in data:
            turn_command = 'no'
            move.move(speed_set, direction_command, turn_command, rad)


        elif 'Switch_1_on' in data:
            switch.switch(1,1)
            tcpCliSock.send(('Switch_1_on').encode())

        elif 'Switch_1_off' in data:
            switch.switch(1,0)
            tcpCliSock.send(('Switch_1_off').encode())

        elif 'Switch_2_on' in data:
            switch.switch(2,1)
            tcpCliSock.send(('Switch_2_on').encode())

        elif 'Switch_2_off' in data:
            switch.switch(2,0)
            tcpCliSock.send(('Switch_2_off').encode())

        elif 'Switch_3_on' in data:
            switch.switch(3,1)
            tcpCliSock.send(('Switch_3_on').encode())

        elif 'Switch_3_off' in data:
            switch.switch(3,0)
            tcpCliSock.send(('Switch_3_off').encode())


        elif 'function_1_on' in data:
            servo.ahead()
            time.sleep(0.2)
            tcpCliSock.send(('function_1_on').encode())
            radar_send = servo.radar_scan()
            tcpCliSock.sendall(radar_send.encode())
            print(radar_send)
            time.sleep(0.3)
            tcpCliSock.send(('function_1_off').encode())


        elif 'function_2_on' in data:
            functionMode = 2
            fpv.FindColor(1)
            tcpCliSock.send(('function_2_on').encode())

        elif 'function_3_on' in data:
            functionMode = 3
            fpv.WatchDog(1)
            tcpCliSock.send(('function_3_on').encode())

        elif 'function_4_on' in data:
            functionMode = 4
            servo_move.resume()
            tcpCliSock.send(('function_4_on').encode())

        elif 'function_5_on' in data:
            functionMode = 5
            servo_move.resume()
            tcpCliSock.send(('function_5_on').encode())

        elif 'function_6_on' in data:
            if MPU_connection:
                functionMode = 6
                servo_move.resume()
                tcpCliSock.send(('function_6_on').encode())


        #elif 'function_1_off' in data:
        #    tcpCliSock.send(('function_1_off').encode())

        elif 'function_2_off' in data:
            functionMode = 0
            fpv.FindColor(0)
            switch.switch(1,0)
            switch.switch(2,0)
            switch.switch(3,0)
            tcpCliSock.send(('function_2_off').encode())

        elif 'function_3_off' in data:
            functionMode = 0
            fpv.WatchDog(0)
            tcpCliSock.send(('function_3_off').encode())

        elif 'function_4_off' in data:
            functionMode = 0
            servo_move.pause()
            move.motorStop()
            tcpCliSock.send(('function_4_off').encode())

        elif 'function_5_off' in data:
            functionMode = 0
            servo_move.pause()
            move.motorStop()
            tcpCliSock.send(('function_5_off').encode())

        elif 'function_6_off' in data:
            functionMode = 0
            servo_move.pause()
            move.motorStop()
            init_get = 0
            tcpCliSock.send(('function_6_off').encode())


        elif 'lookleft' == data:
            servo_command = 'lookleft'
            servo_move.resume()

        elif 'lookright' == data:
            servo_command = 'lookright'
            servo_move.resume()

        elif 'up' == data:
            servo_command = 'up'
            servo_move.resume()

        elif 'down' == data:
            servo_command = 'down'
            servo_move.resume()

        elif 'lookup' == data:
            servo_command = 'lookup'
            servo_move.resume()

        elif 'lookdown' == data:
            servo_command = 'lookdown'
            servo_move.resume()

        elif 'grab' == data:
            servo_command = 'grab'
            servo_move.resume()

        elif 'loose' == data:
            servo_command = 'loose'
            servo_move.resume()

        elif 'stop' == data:
            if not functionMode:
                servo_move.pause()
            servo_command = 'no'
            pass

        elif 'home' == data:
            servo.ahead()

        elif 'wsB' in data:
            try:
                set_B=data.split()
                speed_set = int(set_B[1])
            except:
                pass

        else:
            pass

        print(data)


def wifi_check():
    try:
        s =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(("1.1.1.1",80))
        ipaddr_check=s.getsockname()[0]
        s.close()
        print(ipaddr_check)
    except:
        ap_threading=threading.Thread(target=ap_thread)   #Define a thread for data receiving
        ap_threading.setDaemon(True)                          #'True' means it is a front thread,it would close when the mainloop() closes
        ap_threading.start()                                  #Thread starts

        LED.colorWipe(0,16,50)
        time.sleep(1)
        LED.colorWipe(0,16,100)
        time.sleep(1)
        LED.colorWipe(0,16,150)
        time.sleep(1)
        LED.colorWipe(0,16,200)
        time.sleep(1)
        LED.colorWipe(0,16,255)
        time.sleep(1)
        LED.colorWipe(35,255,35)



if __name__ == '__main__':
    servo.servo_init()
    switch.switchSetup()
    switch.set_all_switch_off()

    HOST = ''
    PORT = 10223                              #Define port serial 
    BUFSIZ = 1024                             #Define buffer size
    ADDR = (HOST, PORT)

    try:
        LED  = LED.LED()
        LED.colorWipe(255,16,0)
    except:
        print('Use "sudo pip3 install rpi_ws281x" to install WS_281x package')
        pass

    while  1:
        wifi_check()
        try:
            tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcpSerSock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            tcpSerSock.bind(ADDR)
            tcpSerSock.listen(5)                      #Start server,waiting for client
            print('waiting for connection...')
            tcpCliSock, addr = tcpSerSock.accept()
            print('...connected from :', addr)

            fpv=FPV.FPV()
            fps_threading=threading.Thread(target=FPV_thread)         #Define a thread for FPV and OpenCV
            fps_threading.setDaemon(True)                             #'True' means it is a front thread,it would close when the mainloop() closes
            fps_threading.start()                                     #Thread starts
            break
        except:
            LED.colorWipe(0,0,0)

        try:
            LED.colorWipe(0,80,255)
        except:
            pass
        run()
    try:
        run()
    except:
        servo_move.stop()
        LED.colorWipe(0,0,0)
        servo.clean_all()
        move.destroy()
