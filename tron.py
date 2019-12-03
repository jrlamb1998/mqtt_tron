########################################
#  tron.py - Written by Jack Lamb and Rees Parker for ME 100, Fall 2019
#  Adapted from a snake game from pythonspot.com: https://pythonspot.com/snake-with-pygame/
#  But really we only ended up using the structure, almost everything else was changed/added/replaced.

from pygame.locals import *
from random import randint
import pygame
import time
import numpy as np

class Player:
    x = []
    y = []
    dx = 0
    dy = 0
    angle = 0
    direction = 0
    speed = 5

    
    
    def __init__(self,x,y):
        self.x = [x]
        self.y = [y]
        pass

    def update(self):
        
        # update position of head of snake
        if self.direction == 0 and (self.x[0] < windowWidth):
            self.angle = 0
        elif self.direction == 1 and (self.x[0] > 0):
            self.angle = np.pi
        elif self.direction == 2 and (self.y[0] > 0):
            self.angle = 1.5*np.pi
        elif self.direction == 3 and (self.y[0] < windowHeight):
            self.angle = 0.5*np.pi
        
        self.dx = self.speed * np.cos(self.angle)
        self.dy = self.speed * np.sin(self.angle)
        if self.x[0] > windowWidth or self.x[0] < 0:
            self.dx = 0
        if self.y[0] > windowHeight or self.y[0] < 0:
            self.dy = 0
        
        self.x = np.append([self.x[0] + self.dx],self.x)
        self.y = np.append([self.y[0] + self.dy],self.y)


    def moveRight(self):
        self.direction = 0
    
    def moveLeft(self):
        self.direction = 1
    
    def moveUp(self):
        self.direction = 2
    
    def moveDown(self):
        self.direction = 3
    
    def draw(self, surface, image):
        surface.blit(image,(self.x[0],self.y[0]))

class Game:
    def isCollision(self,x1,y1,x2,y2,bsize):
        if x1 >= x2 and x1 <= x2 + bsize:
            if y1 >= y2 and y1 <= y2 + bsize:
                return True
        return False

class App:
    
    global windowWidth
    global windowHeight
    player = 0
    apple = 0
    collision_threshhold = 4
    
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image1_surf = None
        self.image2_surf = None
        self._apple_surf = None
        self.textSurface = None
        self.TextRect = None
        self.game = Game()
        self.player1 = Player(100,100)
        self.player2 = Player(100,400)
    
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((windowWidth,windowHeight), pygame.HWSURFACE)
        
        pygame.display.set_caption('Jr. Mints ME 100')
        self._running = True
        self._image1_surf = pygame.image.load("red.jpg").convert()
        self._image2_surf = pygame.image.load("blue.jpg").convert()

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        self.player1.update()
        self.player2.update()
    
        for i in range(1,len(self.player1.x),1):
            #print(np.abs(self.player1.x[0] - self.player1.x[i]) + np.abs(self.player1.y[0] - self.player1.y[i]) < self.collision_threshhold)
            if np.abs(self.player1.x[0] - self.player1.x[i]) + np.abs(self.player1.y[0] - self.player1.y[i]) < self.collision_threshhold or \
                np.abs(self.player1.x[0] - self.player2.x[i]) + np.abs(self.player1.y[0] - self.player2.y[i]) < self.collision_threshhold:
                self.player1.speed = 0
                self.player2.speed = 0
                self.on_menu(0)
            if np.abs(self.player2.x[0] - self.player1.x[i]) + np.abs(self.player2.y[0] - self.player1.y[i]) < self.collision_threshhold or \
                np.abs(self.player2.x[0] - self.player2.x[i]) + np.abs(self.player2.y[0] - self.player2.y[i]) < self.collision_threshhold:
                self.player1.speed = 0
                self.player2.speed = 0
                self.on_menu(1)
        
    def on_menu(self, winner):
        self._display_surf.fill((0,0,0))
        
        font = pygame.font.Font('freesansbold.ttf', 32)
        self.textSurface = font.render('Press ENTER to start new game', True, (0,255,0))
        self.TextRect = self.textSurface.get_rect()
        self.TextRect.center = ((windowWidth//2),(windowHeight//2))
        self._display_surf.blit(self.textSurface, self.TextRect)
    
        if winner == 1:
            self.winnerTextSurface = font.render('Red wins!',True,(255,0,0))
        else:
            self.winnerTextSurface = font.render('Blue wins!',True,(0,0,255))
        self.winnerTextRect = self.winnerTextSurface.get_rect()
        self.winnerTextRect.center = ((windowWidth//2),(windowHeight//4))
        self._display_surf.blit(self.winnerTextSurface, self.winnerTextRect)
    
    def on_restart(self):
        self._display_surf.fill((0,0,0))
        self.player1 = Player(100,100)
        self.player2 = Player(100,400)
    
    def on_render(self):
        self.player1.draw(self._display_surf, self._image1_surf)
        self.player2.draw(self._display_surf, self._image2_surf)

        pygame.display.flip()
    
    def on_cleanup(self):
        pygame.quit()
    
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        
        self.on_menu
        while( self._running ):
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            
            if (keys[K_RIGHT]):
                self.player1.moveRight()
            if (keys[K_LEFT]):
                self.player1.moveLeft()
            if (keys[K_UP]):
                self.player1.moveUp()
            if (keys[K_DOWN]):
                self.player1.moveDown()
            if (keys[K_d]):
                self.player2.moveRight()
            if (keys[K_a]):
                self.player2.moveLeft()
            if (keys[K_w]):
                self.player2.moveUp()
            if (keys[K_s]):
                self.player2.moveDown()

            if (keys[K_RETURN]):
                self.on_restart()
            
            if (keys[K_ESCAPE]):
                self._running = False
            
            self.on_loop()
            self.on_render()
            
            time.sleep (20 / 1000.0);
        self.on_cleanup()


windowWidth = 800
windowHeight = 600
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
