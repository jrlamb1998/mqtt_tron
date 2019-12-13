#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONTROLLER CLIENT
Jr Mints Final Project
Jack Lamb and Rees Parker
"""

from machine import Pin, PWM
import machine
import time

######################## BOOT AND GET WIFI ########################
from network import WLAN, STA_IF
from network import mDNS

#esp_wifi_disconnect()
#esp_wifi_stop()
#espw_wifi_denit()

wlan = WLAN(STA_IF)
wlan.active(True)

#wlan.connect('EE49-2.4', '122Hesse', 5000)
wlan.connect('jack', 'z6thn815ikmnh', 5000)


while not wlan.isconnected():
    print("Waiting for wlan connection")
    time.sleep(1)

print("WiFi connected at", wlan.ifconfig()[0])

# Advertise as 'hostname', alternative to IP address
try:
    hostname = 'jr_mints'
    mdns = mDNS(wlan)
    mdns.start(hostname, "MicroPython REPL")
    mdns.addService('_repl', '_tcp', 23, hostname)
    print("Advertised locally as {}.local".format(hostname))
except OSError:
    print("Failed starting mDNS server - already started?")

# start telnet server for remote login
from network import telnet

print("start telnet server")
telnet.start(user='jr_mints', password='jr_mints')

# fetch NTP time
from machine import RTC

print("inquire RTC time")
rtc = RTC()
rtc.ntp_sync(server="pool.ntp.org")

timeout = 10
for _ in range(timeout):
    if rtc.synced():
        break
    print("Waiting for rtc time")
    time.sleep(1)

if rtc.synced():
    print(time.strftime("%c", time.localtime()))
else:
    print("could not get NTP time")

######################################################


############# IMU STUFF #################
#from bno055_base import BNO055_BASE
from bno055 import *
from board import SDA, SCL

i2c = machine.I2C(0, scl=machine.Pin(SCL), sda=machine.Pin(SDA), freq=12500)
imu = BNO055(i2c)
time.sleep(0.5)
#print(imu.euler())


############# BUTTON PRESS  #################
from board import A8

button = Pin(A8, mode=Pin.IN, pull=Pin.PULL_UP, debounce=500000)

ready = int(0)   ##### ready to play


############# MQTT PUBLISH DATA #################
from mqttclient import MQTTClient

session = "jr_mints"
BROKER = "mqtt.eclipse.org"
mqtt = MQTTClient(BROKER)

controller_topic = "{}/final/controller1".format(session)

####################################

################ TONES ################

C3 = 131
CS3 = 139
D3 = 147
DS3 = 156
E3 = 165
C5 = 523
CS5 = 554
D5 = 587
DS5 = 622
E5 = 659
E6 = 1319

from board import A10

speaker = Pin(A10, mode=Pin.OUT) #may need to be switched to OUT_OD

pwm0 = PWM(speaker, freq=5000, duty=0, timer = 0) #timer needed

start = [E5,1,1,1,E5,1,1,1,E5,1,1,1,E6,E6,E6,E6,1]

win = [C5,CS5,D5,DS5,E5,E5,E5,E5,1,1]

loss = [E3,DS3,D3,CS3,C3,C3,C3,C3,1,1]

################ MQTT GAMESTATE DOWNLOAD ###############
# Define function to execute when a message is recieved on a subscribed topic.
def mqtt_callback(topic, msg):
    global ready
    global gamestate
    old_gamestate = gamestate[:]
    message = msg.decode('utf-8')
    gamestate = [int(x) for x in message.split(',')]
    if (gamestate[0] == 3):
        ready = int(0)
        if old_gamestate[0] == 0:
            #PLAY START MUSIC
            pwm0.duty(30)
            for i in start:
                pwm0.freq(i)
                time.sleep(0.2) #in seconds
            pwm0.duty(0)
    if (gamestate[0] == 1) and (old_gamestate[0] != 1):
        ###### PLAY WINNING MUSIC
        pwm0.duty(30)
        for i in win:
            pwm0.freq(i)
            time.sleep(0.2) #in seconds
        pwm0.duty(0)
    if (gamestate[0] == 2) and (old_gamestate[0] != 2):
        ###### PLAY LOSING MUSIC
            pwm0.duty(30)
            for i in lose:
                pwm0.freq(i)
                time.sleep(0.2) #in seconds
            pwm0.duty(0)


# Set callback function
mqtt.set_callback(mqtt_callback)
# Set a topic you will subscribe too. Publish to this topic via web client and watch microcontroller recieve messages.
mqtt.subscribe(session + "/final/gamestate")

############## LOGIC LOOP ###########
gamestate = []
while True:
    if ready == 0:
        if button() == 0:
            ready = int(1)
    orientation = imu.euler()
    pitch = str(orientation[1])
    roll = str(orientation[2])
    #print(pitch,roll,ready)
    mqtt.check_msg()
    #print(gamestate)
    data = pitch + ',' + roll + "," + str(ready)
    mqtt.publish(controller_topic, data)
    time.sleep(25/1000)
