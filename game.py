#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GAME CLIENT
Jr. Mints final project
Jack Lamb and Rees Parker
"""

import time

############### MQTT CODE, RETURNS p1_position, p2_position, read1, ready2
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
############# END OF MQTT #################


############ LOGIC LOOP ##################
while True:
    if gamestate == 0:
        #clearscreen
        if ready1 == 1:
            #player 1 ready
        if ready2 == 1:
            #player 2 ready
    elif gamestate == 1:
        #clearscreen
        #print player 1 wins
        if ready1 == 1:
            #player 1 ready
        if ready2 == 1:
            #player 2 ready    
    elif gamestate == 2:
        #clearscreen
        if ready1 == 1:
            #player 1 ready
        if ready2 == 1:
            #player 2 ready
    elif gamestate == 3:
        #plot current p1, p2