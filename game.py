#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GAME CLIENT
Jr. Mints final project
Jack Lamb and Rees Parker
"""

from pygame.locals import *
from random import randint
import pygame
import time
import numpy as np


############### MQTT CODE, RETURNS p1_position, p2_position, read1, ready2
import paho.mqtt.client as paho
session = "jr_mints"
BROKER = "mqtt.eclipse.org"
qos = 0
mqtt = paho.Client()
mqtt.connect(BROKER, 1883)

p1_position = []
p2_position = []
gamestate = 2
ready1 = 1
ready2 = 1

def player_reader(c, u, message):
    global p1_position,p2_position
    msg = message.payload.decode('ascii')
    positions = [ int(x) for x in msg.split(',') ]
    p1_position = [positions[0],positions[1]]
    p2_position = [positions[2],positions[3]]

def gamestate_reader(c,u,message):
    global gamestate, ready1, ready2
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
mqtt.loop_start()

############# END OF MQTT #################


############ GAME SETUP ################
windowWidth = 800
windowHeight = 600

pygame.init()
display_surf = pygame.display.set_mode((windowWidth, windowHeight), pygame.HWSURFACE)
pygame.display.set_caption('Jr. Mints ME 100')
font = pygame.font.Font('freesansbold.ttf', 32)

######################################

############ LOGIC LOOP ##################

while True:
    if gamestate == 0:
        display_surf.fill((0,0,0))

        ready1text = font.render('Waiting...',True,(255,215,0))
        ready1TextRect = ready1text.get_rect()
        ready1TextRect.center = ((windowWidth//4),(3*windowHeight//4))
        display_surf.blit(ready1text, ready1TextRect)

        ready2text = font.render('Waiting...',True,(0,0,255))
        ready2TextRect = ready2text.get_rect()
        ready2TextRect.center = ((3*windowWidth//4),(3*windowHeight//4))
        display_surf.blit(ready2text, ready2TextRect)

        pygame.display.flip()

        while gamestate == 0:
            if ready1 == 1:
                pygame.draw.rect(display_surf,(0,0,0),ready1TextRect)
                ready1text = font.render('Ready',True,(255,215,0))
                display_surf.blit(ready1text, ready1TextRect)
            if ready2 == 1:
                pygame.draw.rect(display_surf,(0,0,0),ready2TextRect)
                ready2text = font.render('Ready',True,(0,0,255))
                display_surf.blit(ready2text, ready2TextRect)
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            if (keys[K_ESCAPE]):
                mqtt.loop_stop()
                pygame.quit()
            pygame.display.flip()
            time.sleep(25/1000)
    elif gamestate == 1:
        display_surf.fill((0,0,0))

        winnerTextSurface = font.render('Gold wins!',True,(255,215,0))
        winnerTextRect = winnerTextSurface.get_rect()
        winnerTextRect.center = ((windowWidth//2),(windowHeight//4))
        display_surf.blit(winnerTextSurface, winnerTextRect)

        ready1text = font.render('Waiting...',True,(255,215,0))
        ready1TextRect = ready1text.get_rect()
        ready1TextRect.center = ((windowWidth//4),(3*windowHeight//4))
        display_surf.blit(ready1text, ready1TextRect)

        ready2text = font.render('Waiting...',True,(0,0,255))
        ready2TextRect = ready2text.get_rect()
        ready2TextRect.center = ((3*windowWidth//4),(3*windowHeight//4))
        display_surf.blit(ready2text, ready2TextRect)
        pygame.display.flip()

        while gamestate == 1:
            if ready1 == 1:
                pygame.draw.rect(display_surf,(0,0,0),ready1TextRect)
                ready1text = font.render('Ready',True,(255,215,0))
                ready1TextRect = ready1text.get_rect()
                ready1TextRect.center = ((windowWidth//4),(3*windowHeight//4))
                display_surf.blit(ready1text, ready1TextRect)
            if ready2 == 1:
                pygame.draw.rect(display_surf,(0,0,0),ready2TextRect)
                ready2text = font.render('Ready',True,(0,0,255))
                display_surf.blit(ready2text, ready2TextRect)
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            if (keys[K_ESCAPE]):
                mqtt.loop_stop()
                pygame.quit()
            pygame.display.flip()
            time.sleep(25/1000)
    elif gamestate == 2:
        display_surf.fill((0,0,0))

        winnerTextSurface = font.render('Blue wins!',True,(0,0,255))
        winnerTextRect = winnerTextSurface.get_rect()
        winnerTextRect.center = ((windowWidth//2),(windowHeight//4))
        display_surf.blit(winnerTextSurface, winnerTextRect)

        ready1text = font.render('Waiting...',True,(255,215,0))
        ready1TextRect = ready1text.get_rect()
        ready1TextRect.center = ((windowWidth//4),(3*windowHeight//4))
        display_surf.blit(ready1text, ready1TextRect)

        ready2text = font.render('Waiting...',True,(0,0,255))
        ready2TextRect = ready2text.get_rect()
        ready2TextRect.center = ((3*windowWidth//4),(3*windowHeight//4))
        display_surf.blit(ready2text, ready2TextRect)
        pygame.display.flip()

        while gamestate == 2:
            if ready1 == 1:
                pygame.draw.rect(display_surf,(0,0,0),ready1TextRect)
                ready1text = font.render('Ready',True,(255,215,0))
                display_surf.blit(ready1text, ready1TextRect)
            if ready2 == 1:
                pygame.draw.rect(display_surf,(0,0,0),ready2TextRect)
                ready2text = font.render('Ready',True,(0,0,255))
                display_surf.blit(ready2text, ready2TextRect)
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            if (keys[K_ESCAPE]):
                mqtt.loop_stop()
                pygame.quit()
            pygame.display.flip()
            time.sleep(25/1000)

    elif gamestate == 3:
        display_surf.fill((0,0,0))
        while gamestate == 3:
            pygame.draw.circle(display_surf, (255,215,0), (p1_position[0],p1_position[1]), 5)
            pygame.draw.circle(display_surf, (0,0,255), (p2_position[0],p2_position[1]), 5)
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            if (keys[K_ESCAPE]):
                mqtt.loop_stop()
                pygame.quit()
            pygame.display.flip()
            time.sleep(5/1000)
############# END OF LOGIC LOOP ###############
