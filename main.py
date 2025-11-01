import pygame
import sys
import random

import game
import value
import title
import menu
pygame.init()

value.player = 1
value.game_over = False
while True:
    while value.step==0:
        title.title()
    while value.step==1:
        if value.menustep==0:
            menu.menu()
        if value.menustep==1:
            menu.menu2()
    if value.step==4:
        value.t=0
        value.gamestep=0
        value.hands=[]
        value.hands2=[]
        if value.firstplayer==0:
            value.player=random.randint(1,2)
        else:
            value.player=value.firstplayer
    while value.step==4:
        if value.gamestep==0:
            game.gameb()
        if value.gamestep==1:
            game.game()
        if value.gamestep==2:
            game.change()
        if value.gamestep==3:
            game.skillbase()
    
    while value.step==5:
        pass