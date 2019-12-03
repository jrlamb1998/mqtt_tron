#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONTROLLER CLIENT
Jr Mints Final Project
Jack Lamb and Rees Parker
"""

from board import A21
from machine import Pin
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
from bno055_base import BNO055_BASE
import numpy as np

i2c = machine.I2C(-1, scl=machine.Pin(2), sda=machine.Pin(0))
imu = BNO055_BASE(i2c)
time.sleep(0.5)
print(imu.euler())
orientation = imu.euler()
pitch = np.radians(orientation[1])
roll = np.radians(orientation[2])

angle = np.atan(np.sin(pitch)/np.sin(roll))

button = Pin(A21, mode=Pin.IN, pull=Pin.PULL_UP, debounce=500000)

ready = 0   ##### ready to play


############# MQTT PUBLISH DATA #################
from mqttclient import MQTTClient

session = "jr_mints"
BROKER = "mqtt.eclipse.org"
mqtt = MQTTClient(BROKER)

controller_topic = "{}/final/controller1".format(session)

####################################

################ MQTT GAMESTATE DOWNLOAD ###############
# Define function to execute when a message is recieved on a subscribed topic.
def mqtt_callback(topic, msg):
    global ready
    global gamestate
    message = msg.decode('utf-8')
    gamestate = [int(x) for x in message.split(',')]
    if gamestate[0] == 3:
        ready = 0
    
    
# Set callback function
mqtt.set_callback(mqtt_callback)
# Set a topic you will subscribe too. Publish to this topic via web client and watch microcontroller recieve messages.
mqtt.subscribe(session + "/final/gamestate")


############## LOGIC LOOP ###########

while True:
    if ready == 0:
        ready = button()
    data = str(angle) + "," + str(ready)
    mqtt.publish(controller_topic, data)
    time.sleep(25/1000)