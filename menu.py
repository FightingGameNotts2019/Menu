# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 18:17:35 2019

@author: nabid
"""

import pygame
import time
import random
import main
import gameScreen

 
def quitgame():
    pygame.quit()
    quit()

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()
 
    
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)

def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        screen.fill(white) 
        largeText = pygame.font.SysFont("comicsansms",90) 
        TextSurf, TextRect = text_objects("Smash Bros", largeText) 
        TextRect.center = ((display_width/2),(display_height*0.15)) 
        screen.blit(TextSurf, TextRect)

        button("Fight!",800,200,100,50,green,bright_green,main.gameLoop)
        button("Tutorial?",800,300,100,50,red,bright_red,quitgame)
        button("Quit",800,400,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)
    

pygame.init()
display_width = 1600
display_height = 800
screen = gameScreen.screen

black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
blue = (0,0,255)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)
 
block_color = (53,115,255)
 
car_width = 73
 
pygame.display.set_caption('Smash Bros')
clock = pygame.time.Clock()
 
carImg = pygame.draw.rect(screen,blue,(200,150,100,50))

game_intro()
game_loop()
pygame.quit()
quit()    

