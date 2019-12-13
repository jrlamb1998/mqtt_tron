############# DOWNLOAD FROM SERVER #####################

import time
import numpy as np
import paho.mqtt.client as paho
session = "jr_mints"
BROKER = "mqtt.eclipse.org"
qos = 0
mqtt = paho.Client()
mqtt.connect(BROKER, 1883)

data1 = [0,0,0]
data2 = [0,0,0]
ready1 = 0
ready2 = 0
gamestate = 0
speed = 5.
x1 = 100.
y1 = 100.
x2 = 100.
y2 = 400.

player1_list = np.array([[0,0],[0,0]])
player2_list = np.array([[0,0],[0,0]])

def controller1_reader(c, u, message):
    global data1 ### data has the fields [pitch,roll,ready]
    msg = message.payload.decode('ascii')
    data1 = [ float(x) for x in msg.split(',') ]

def controller2_reader(c, u, message):
    global data2  #### data has the fields [pitch,roll,ready]
    msg = message.payload.decode('ascii')
    data2 = [ float(x) for x in msg.split(',') ]

controller1_topic = "{}/final/controller1".format(session, qos)
controller2_topic = "{}/final/controller2".format(session, qos)
mqtt.subscribe(controller1_topic)
mqtt.subscribe(controller2_topic)

mqtt.message_callback_add(controller1_topic, controller1_reader)
mqtt.message_callback_add(controller2_topic, controller2_reader)
mqtt.loop_start()

############# UPLOAD TO SERVER #####################
gamestate_topic = "{}/final/gamestate".format(session)
players_topic = "{}/final/players".format(session)

while True:
    
    ########### Calculate gamestate
    ready1_old = ready1
    ready2_old = ready2
    
    ready1 = int(data1[2])
    ready2 = int(data2[2])
    
    ### Start the game
    if not (ready1_old and ready2_old):
        if ready1 and ready2:
            gamestate_data_ready = str(gamestate) + "," + str(ready1) + "," + str(ready2)
            mqtt.publish(gamestate_topic, gamestate_data_ready, qos)
            time.sleep(0.5)
            gamestate = 3
            gamestate_data = str(gamestate) + "," + str(ready1) + "," + str(ready2)
            players_data = str(int(x1)) + "," + str(int(y1)) + "," + str(int(x2)) + "," + str(int(y2))
            mqtt.publish(gamestate_topic, gamestate_data, qos)
            time.sleep(4)
         
    if gamestate == 3:
        ############ Calculate positions
        pitch1 = np.radians(data1[0])
        roll1 = np.radians(data1[1])
        angle1 = np.arctan2(np.sin(roll1),np.sin(pitch1))
        
        pitch2 = np.radians(data2[0])
        roll2 = np.radians(data2[1])
        
        angle2 = np.arctan2(np.sin(roll2), np.sin(pitch2))
        
        x1 += speed * np.cos(angle1)
        y1 += speed * np.sin(angle1)
        x2 += speed * np.cos(angle2)
        y2 += speed * np.sin(angle2)
        
    ### Check for edge
        if x1 > 800:
            x1 = 800
        if x2 > 800:
            x2 = 800
        if y1 > 600:
            y1 = 600
        if y2 > 600:
            y2 = 600
            
        if x1 < 0:
            x1 = 0
        if x2 < 0:
            x2 = 0
        if y1 < 0:
            x2 = 0
        if y2 < 0:
            y2 = 0

    ### check for collisions 
        for i in range(len(player2_list)):
            distance = np.sqrt( (player2_list[i,0]-x1)**2 + (player2_list[i,1] - y1)**2)
            if distance <= 0.9*float(speed):
                gamestate = 2     
                time.sleep(2)
        for i in range(len(player1_list)-1):
            distance = np.sqrt( (player1_list[i,0]-x1)**2 + (player1_list[i,1] - y1)**2)
            if distance <= 0.9*float(speed):
                gamestate = 2
                time.sleep(2)
                
        for i in range(len(player1_list)):
            distance = np.sqrt( (player1_list[i,0]-x2)**2 + (player1_list[i,1] - y2)**2)
            if distance <= 0.9*speed:
                gamestate = 1
                time.sleep(2)
        for i in range(len(player2_list)-1):
            distance = np.sqrt( (player2_list[i,0]-x2)**2 + (player2_list[i,1] - y2)**2)
            if distance <= 0.9*speed:
                gamestate = 1
                time.sleep(2)
        
        player1_list = np.vstack((player1_list,[x1,y1]))
        player2_list = np.vstack((player2_list,[x2,y2]))
    
    else:
        x1 = 100.
        y1 = 100.
        x2 = 100.
        y2 = 400.
        player1_list = np.array([[0,0],[0,0]])
        player2_list = np.array([[0,0],[0,0]])
        
        
    
    gamestate_data = str(gamestate) + "," + str(ready1) + "," + str(ready2)
    players_data = str(int(x1)) + "," + str(int(y1)) + "," + str(int(x2)) + "," + str(int(y2))
    mqtt.publish(gamestate_topic, gamestate_data, qos)
    mqtt.publish(players_topic, players_data, qos)
    time.sleep(100/1000)