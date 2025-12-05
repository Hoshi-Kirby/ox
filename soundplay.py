import pygame
import sys
import math

import value
pygame.init()
pygame.mixer.init()

se=[]
se.append(pygame.mixer.Sound("sound/decision_fo-n.wav"))#0
se[-1].set_volume(0.16)
se.append(pygame.mixer.Sound("sound/decision_syui-n.wav"))#1
se[-1].set_volume(0.4)
se.append(pygame.mixer.Sound("sound/cursor_kasha.wav"))#2
se[-1].set_volume(0.4)
se.append(pygame.mixer.Sound("sound/back_futt.wav"))#3
se[-1].set_volume(0.4)
se.append(pygame.mixer.Sound("sound/decision_ka.wav"))#4
se[-1].set_volume(0.3)
se.append(pygame.mixer.Sound("sound/decision_tururun.wav"))#5
se[-1].set_volume(0.5)
se.append(pygame.mixer.Sound("sound/flip_pera.wav"))#6
se[-1].set_volume(0.5)
se.append(pygame.mixer.Sound("sound/draw_pera.wav"))#7
se[-1].set_volume(0.4)
se.append(pygame.mixer.Sound("sound/windou_buonwi-n.wav"))#8
se[-1].set_volume(0.4)
se.append(pygame.mixer.Sound("sound/disappear_hyu.wav"))#9
se[-1].set_volume(0.5)
se.append(pygame.mixer.Sound("sound/event_whowa-n.wav"))#10
se[-1].set_volume(0.2)
se.append(pygame.mixer.Sound("sound/selectcard_pisi.wav"))#11
se[-1].set_volume(0.4)
se.append(pygame.mixer.Sound("sound/K.O._ka-n.wav"))#12
se[-1].set_volume(0.3)
se.append(pygame.mixer.Sound("sound/result_pi-.wav"))#13
se[-1].set_volume(0.4)
se.append(pygame.mixer.Sound("sound/disp_don.wav"))#14
se[-1].set_volume(0.3)
se.append(pygame.mixer.Sound("sound/canselcard_za.wav"))#15
se[-1].set_volume(0.6)
se.append(pygame.mixer.Sound("sound/menu_ponnporo.wav"))#16
se[-1].set_volume(0.3)
se.append(pygame.mixer.Sound("sound/delete_hyu-w.wav"))#17
se[-1].set_volume(0.3)
se.append(pygame.mixer.Sound("sound/explosion_do-n.wav"))#18
se[-1].set_volume(0.2)
se.append(pygame.mixer.Sound("sound/shot_dyukushu.wav"))#19
se[-1].set_volume(0.3)
se.append(pygame.mixer.Sound("sound/put_bisi.wav"))#20
se[-1].set_volume(0.3)
se.append(pygame.mixer.Sound("sound/up_kui-n.wav"))#21
se[-1].set_volume(0.3)
se.append(pygame.mixer.Sound("sound/down_down.wav"))#22
se[-1].set_volume(0.7)
se.append(pygame.mixer.Sound("sound/backcard1_syu.wav"))#23
se[-1].set_volume(0.5)
se.append(pygame.mixer.Sound("sound/backcard2_syusyu.wav"))#24
se[-1].set_volume(0.7)

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