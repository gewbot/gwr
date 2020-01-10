#!/usr/bin/python3
# File name   : setup.py
# Website     : www.gewbot.com
# E-mail      : gewubot@163.com
# Author      : William
# Date        : 2019/09/02

import os
import time

def replace_num(file,initial,new_num):  
    newline=""
    str_num=str(new_num)
    with open(file,"r") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                line = (str_num+'\n')
            newline += line
    with open(file,"w") as f:
        f.writelines(newline)

for x in range(1,4):
	if os.system("sudo apt-get update") == 0:
		break

os.system("sudo apt-get purge -y wolfram-engine")
os.system("sudo apt-get purge -y libreoffice*")
os.system("sudo apt-get -y clean")
os.system("sudo apt-get -y autoremove")

# for x in range(1,4):
# 	if os.system("sudo apt-get -y upgrade") == 0:
# 		break

for x in range(1,4):
	if os.system("sudo pip3 install -U pip") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y python-dev python-pip libfreetype6-dev libjpeg-dev build-essential") == 0:
		break

for x in range(1,4):
	if os.system("sudo -H pip3 install --upgrade luma.oled") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y i2c-tools") == 0:
		break

for x in range(1,4):
	if os.system("sudo pip3 install adafruit-pca9685") == 0:
		break

for x in range(1,4):
	if os.system("sudo pip3 install rpi_ws281x") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y python3-smbus") == 0:
		break

for x in range(1,4):
	if os.system("sudo pip3 install mpu6050-raspberrypi") == 0:
		break

try:
	replace_num("/boot/config.txt",'#dtparam=i2c_arm=on','dtparam=i2c_arm=on\nstart_x=1\n')
except:
	print('try again')


for x in range(1,4):
	if os.system("sudo pip3 install numpy") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y libopencv-dev python3-opencv") == 0:
		break

for x in range(1,4):
	if os.system("sudo pip3 install imutils zmq pybase64 psutil") == 0:   ####
		break

for x in range(1,4):
	if os.system("sudo git clone https://github.com/oblique/create_ap") == 0:
		break

try:
	os.system("cd //home/pi/gtank/create_ap && sudo make install")
except:
	pass

try:
	os.system("cd //home/pi/create_ap && sudo make install")
except:
	pass

try:
	os.system("sudo cd //home/pi/create_ap && sudo make install")
except:
	pass

for x in range(1,4):
	if os.system("sudo apt-get install -y util-linux procps hostapd iproute2 iw haveged dnsmasq") == 0:
		break
'''
try:
	os.system('sudo mkdir //home/pi/.config/autostart')
	os.system('sudo touch //home/pi/.config/autostart/car.desktop')
	with open("//home/pi/.config/autostart/car.desktop",'w') as file_to_write:
		file_to_write.write("[Desktop Entry]\n   Name=Car\n   Comment=Car\n   Exec=sudo python3 //home/pi/gtank/server/server.py\n   Icon=false\n   Terminal=false\n   MutipleArgs=false\n   Type=Application\n   Catagories=Application;Development;\n   StartupNotify=true")
except:
	pass
'''
try:
	os.system('sudo touch //home/pi/startup.sh')
	with open("//home/pi/startup.sh",'w') as file_to_write:
		file_to_write.write("#!/bin/sh\nsudo python3 //home/pi/gtank/server/server.py")
except:
	pass

os.system('sudo chmod 777 //home/pi/startup.sh')

replace_num('/etc/rc.local','fi','fi\n//home/pi/startup.sh start')

try: #fix conflict with onboard Raspberry Pi audio
	os.system('sudo touch /etc/modprobe.d/snd-blacklist.conf')
	with open("/etc/modprobe.d/snd-blacklist.conf",'w') as file_to_write:
		file_to_write.write("blacklist snd_bcm2835")
except:
	pass

print('树莓派中的程序已经安装完毕，已经断开连接并重启。\n你现在可以将树莓派断电来安装摄像头以及驱动板(Robot HAT)。\n再次开机后树莓派会自动运行程序将舵机口信号设置为使舵机转动到中间位置，方便机械组装。')

os.system("sudo reboot")
