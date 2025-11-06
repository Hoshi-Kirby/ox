import pygame
import sys
import random

import game
import value
import title
import menu
import gameset
import make
import save_load
pygame.init()

value.player = 1
value.game_over = False
for i in range(1,4):
    save_load.load(i)
while True:
    while value.step==0:
        title.title()
    while value.step==1:
        if value.menustep==0:
            menu.menu()
        if value.menustep==1:
            menu.menu2()
    if value.step==2:
        value.t=0
        value.hold_deck=value.deck[value.make_deck_ka][:]
    while value.step==2:
        make.make()
    if value.step==4:
        value.gamereset=False
        value.t=0
        value.gamestep=0
        value.hands=[]
        value.hands2=[]
        value.firstfirst=True
        value.nextevent=random.randint(0,3)
        if value.firstplayer==0:
            value.player=random.randint(1,2)
        else:
            value.player=value.firstplayer
    while value.step==4 and (not value.gamereset):
        if value.gamestep==0:
            game.gameb()
        if value.gamestep==1:
            game.game()
        if value.gamestep==2:
            game.change()
        if value.gamestep==3:
            game.skillbase()
    
    while value.step==5:
        gameset.gameset()