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


############# IMU STUFF #################
from bno055 import *
i2c = machine.I2C(1)
# ESP8266 soft I2C
# i2c = machine.I2C(-1, scl=machine.Pin(2), sda=machine.Pin(0))
imu = BNO055(i2c)
time.sleep(0.5)
print(imu.accel())

button = Pin(A21, mode=Pin.IN, pull=Pin.PULL_UP, debounce=500000)

angle = 0 ##### angle of tilt calculated from the IMU, between 0 and 2pi
ready = 0   ##### ready to play


############# MQTT PUBLISH DATA #################
from mqttclient import MQTTClient

session = "jr_mints"
BROKER = "mqtt.eclipse.org"
mqtt = MQTTClient(BROKER)

controller_topic = "{}/final/controller1".format(session)

####################################

############## LOGIC LOOP ###########

while True:
    if ready == 0:
        ready = button()
    data = str(angle) + "," + str(ready)
    mqtt.publish(controller_topic, data)
    time.sleep(25/1000)