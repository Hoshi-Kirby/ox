import pygame
import sys
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
    while value.step==4:
        game.game()