#!/usr/bin/python3
# File name   : findline.py
# Description : line tracking 
# Website     : www.gewbot.com
# Author      : William
# Date        : 2019/08/28
import RPi.GPIO as GPIO
import time
import move
import LED
'''
status     = 1          #Motor rotation
forward    = 1          #Motor forward
backward   = 0          #Motor backward

left_spd   = num_import_int('E_M1:')         #Speed of the car
right_spd  = num_import_int('E_M2:')         #Speed of the car
left       = num_import_int('E_T1:')         #Motor Left
right      = num_import_int('E_T2:')         #Motor Right
'''
line_pin_right = 20
line_pin_middle = 16
line_pin_left = 19
'''
left_R = 15
left_G = 16
left_B = 18

right_R = 19
right_G = 21
right_B = 22

on  = GPIO.LOW
off = GPIO.HIGH

spd_ad_1 = 1
spd_ad_2 = 1
'''
def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(line_pin_right,GPIO.IN)
    GPIO.setup(line_pin_middle,GPIO.IN)
    GPIO.setup(line_pin_left,GPIO.IN)
    #motor.setup()


led = LED.LED()
turn_status = 0
speed = 40 #0~70
angle_rate = 1
color_select = 0 # 0 --> white line / 1 --> black line
forword = False
def run():
    global turn_status, speed, angle_rate, color_select, led, check_true_out, backing, last_turn
    status_right = GPIO.input(line_pin_right)
    status_middle = GPIO.input(line_pin_middle)
    status_left = GPIO.input(line_pin_left)
    #print('R%d   M%d   L%d'%(status_right,status_middle,status_left))

    # if status_right == color_select and status_middle == color_select:
    #     print('fixRight')
    #     move.move(speed, 'forward', 'no', 1)
    #     time.sleep(0.2)
    #     move.move(speed, 'forward', 'right', 0.6)
    #     time.sleep(0.2)
    # elif status_left == color_select and status_middle == color_select:
    #     print('fixLeft')
    #     move.move(speed, 'forward', 'no', 1)
    #     time.sleep(0.2)
    #     move.move(speed, 'forward', 'left', 0.6)
    #     time.sleep(0.2)
    

    if status_right == color_select:
        print('right')
        forword = False
        led.colorWipe(0,0,255)
        turn_status = -1
        if forword:
            move.move(speed, 'backward', 'no', 1)
            time.sleep(0.05)
        move.move(speed+30, 'forward', 'right', 0.6)
        time.sleep(0.1)
    elif status_left == color_select:
        print('left')
        forword = False
        turn_status = 1
        led.colorWipe(0,255,0)
        if forword:
            move.move(speed, 'backward', 'no', 1)
            time.sleep(0.05)
        move.move(speed+30, 'forward', 'left', 0.6)
        time.sleep(0.1)

    elif status_middle == color_select:
        print('middle')
        forword = True
        led.colorWipe(255,255,255)
        turn_status = 0
        move.move(speed, 'forward', 'no', 1)

    else:
        print('none')
        led.colorWipe(255,0,0)
        move.move(speed, 'backward', 'no', 1)

if __name__ == '__main__':
    try:
        setup()
        move.setup()
        while 1:
            run()
            
        pass
    except KeyboardInterrupt:
        move.destroy()


# def run():
#     status_right = GPIO.input(line_pin_right)
#     status_middle = GPIO.input(line_pin_middle)
#     status_left = GPIO.input(line_pin_left)
#     #print('R%d   M%d   L%d'%(status_right,status_middle,status_left))
#     if status_middle == 1:
#         move.move(100, 'forward', 'no', 1)
#     elif status_left == 1:
#         move.move(100, 'forward', 'right', 0.6)
#     elif status_right == 1:
#         move.move(100, 'forward', 'left', 0.6)
#     else:
#         move.move(100, 'backward', 'no', 1)

