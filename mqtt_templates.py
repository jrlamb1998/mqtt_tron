#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jr. Mints final Project
MQTT templates
"""

############## UPLOAD FROM CONTROLLER ################

from mqttclient import MQTTClient
session = "jr_mints"
BROKER = "mqtt.eclipse.org"
mqtt = MQTTClient(BROKER)

angle = 1.5 ##### angle of tilt calculated from the IMU, between 0 and 2pi
ready = 1   ##### ready to play

topic = "{}/final/controller1".format(session)
data = str(angle) + "," + str(ready)
mqtt.publish(topic, data)


############# DOWNLOAD TO GAME CLIENT ################

import paho.mqtt.client as paho
session = "jr_mints"
BROKER = "mqtt.eclipse.org"
qos = 0
mqtt = paho.Client()
mqtt.connect(BROKER, 1883)

def player_reader(c, u, message):
    msg = message.payload.decode('ascii')
    positions = [ float(x) for x in msg.split(',') ]
    p1_position = [positions[0],positions[1]]
    p2_position = [positions[2],positions[3]]
    
def gamestate_reader(c,u,message):
    msg = message.payload.decode('ascii')
    gamestate_data = [ int(x) for x in msg.split(',') ]
    gamestate = gamestate_data[0]
    ready1 = gamestate_data[1]
    ready2 = gamestate_data[2]
    
players_topic = "{}/final/players".format(session, qos)
mqtt.subscribe(players_topic)
mqtt.message_callback_add(players_topic, player_reader)

gamestate_topic = "{}/final/gamestate".format(session, qos)
mqtt.subscribe(gamestate_topic)
mqtt.message_callback_add(gamestate_topic, gamestate_reader)

mqtt.loop_forever()

############# DOWNLOAD TO SERVER #####################

import paho.mqtt.client as paho
session = "jr_mints"
BROKER = "mqtt.eclipse.org"
qos = 0
mqtt = paho.Client()
mqtt.connect(BROKER, 1883)

def controller1_reader(c, u, message):
    msg = message.payload.decode('ascii')
    data = [ float(x) for x in msg.split(',') ]
    return data  #### data has the fields [angle1, ready1]

def controller2_reader(c, u, message):
    msg = message.payload.decode('ascii')
    data = [ float(x) for x in msg.split(',') ]
    return data  #### data has the fields [angle2, ready2]

controller1_topic = "{}/final/controller1".format(session, qos)
controller2_topic = "{}/final/controller2".format(session, qos)
mqtt.subscribe(controller1_topic)
mqtt.subscribe(controller2_topic)

mqtt.message_callback_add(controller1_topic, controller1_reader)
mqtt.message_callback_add(controller2_topic, controller2_reader)
mqtt.loop_forever()

############# UPLOAD FROM SERVER #####################

import paho.mqtt.client as paho
session = "jr_mints"
BROKER = "mqtt.eclipse.org"
qos = 0
mqtt = paho.Client()
mqtt.connect(BROKER, 1883)
gamestate_topic = "{}/final/gamestate".format(session)
players_topic = "{}/final/players".format(session)


gamestate = 1   #example - player 1 wins
ready1 = 0
ready2 = 1

x1, y1, x2, y2 = [20,30,40,50]  # example
gamestate_data = str(gamestate) + "," + str(ready1) + "," + str(ready2)
players_data = str(x1) + "," + str(y2) + "," + str(x2) + "," + str(y2)
mqtt.publish(gamestate_topic, gamestate_data, qos)
mqtt.publish(players_topic, players_data, qos)