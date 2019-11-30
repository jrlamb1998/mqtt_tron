#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONTROLLER CLIENT
Jr Mints Final Project
Jack Lamb and Rees Parker
"""

from mqttclient import MQTTClient




session = "jr_mints"
BROKER = "mqtt.eclipse.org"
mqtt = MQTTClient(BROKER)

angle = 1.5 ##### angle of tilt calculated from the IMU, between 0 and 2pi
ready = 1   ##### ready to play

topic = "{}/final/controller1".format(session)
data = str(angle) + "," + str(ready)
mqtt.publish(topic, data)