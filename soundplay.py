import pygame
import sys
import math

import value

se=[]
se.append(pygame.mixer.Sound("sound/decision fo-n.wav"))#0
se[-1].set_volume(0.1)
se.append(pygame.mixer.Sound("sound/decision syui-n.wav"))#1
se[-1].set_volume(0.4)
se.append(pygame.mixer.Sound("sound/cursor kasha.wav"))#2
se[-1].set_volume(0.4)
se.append(pygame.mixer.Sound("sound/back futt.wav"))#3
se[-1].set_volume(0.4)
se.append(pygame.mixer.Sound("sound/decision ka.wav"))#4
se[-1].set_volume(0.5)
se.append(pygame.mixer.Sound("sound/decision tururun.wav"))#5
se[-1].set_volume(0.5)
se.append(pygame.mixer.Sound("sound/flip pera.wav"))#6
se[-1].set_volume(0.5)

def bgm_play(x):
    if value.bgm_track != x:
        match(x):
            case 1:
                pygame.mixer.music.load(f"sound/op.mp3")
                pygame.mixer.music.set_volume(0.1)
            case 2:
                pygame.mixer.music.load(f"sound/mm.mp3")
                pygame.mixer.music.set_volume(0.05)
            case 3:
                pygame.mixer.music.load(f"sound/vs.mp3")
                pygame.mixer.music.set_volume(0.05)  
            case 4:
                pygame.mixer.music.load(f"sound/mk.mp3")
                pygame.mixer.music.set_volume(0.07)
        pygame.mixer.music.play(-1)
        value.bgm_track=x

def se_play(x):
    se[x].play()