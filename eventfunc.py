import sqlite3
import pygame
import sys
import math
import random

import value

pygame.init()
import os

speedx=20
card_move_time=-1
card_x_before=[[0]*10,[0]*10]
card_x_after=[[0]*10,[0]*10]

width=pygame.image.load(f"image/card1-1.png").convert().get_width()

def event(a):
    global card_move_time
    if a==0:
        value.t=39
        value.event_turn+=1
        value.eventnum=0
    else:
        card_move_time=-1
        value.eventnum=a
        value.event_t=0

def eventfunc(a):
    value.t=41
    if a==1:
        handeath()
    if a>=2:
        if value.event_t==20:
            if a==2:
                value.card_dcost[0]-=1
                value.card_dcost[1]-=1
            if a==3:
                value.card_dcost[0]+=1
                value.card_dcost[1]+=1
        for i in range(10):
            value.card_dy[0][i]=(20-abs(20-value.event_t))*10
            value.card_dy[1][i]=(20-abs(20-value.event_t))*10
        if value.event_t==40:
            value.eventnum=-1
    value.event_t+=1
        
def handeath():
    global card_x_before
    global card_x_after
    global card_move_time
    global card_select_base
    if card_move_time==-1:
        card_move_time=20
        j=0
        card_select_base=[]
        card_select_base.append(random.randint(0,len(value.hands)))
        card_select_base.append(random.randint(0,len(value.hands2)))
        #カード間隔
        if len(value.hands)-1<6:
            value.spacing_after=120
        elif len(value.hands)-1<8:
            value.spacing_after=80
        else:
            value.spacing_after=50
        if len(value.hands2)-1<6:
            value.spacing2_after=120
        elif len(value.hands2)-1<8:
            value.spacing2_after=80
        else:
            value.spacing2_after=50

        for i in range(len(value.hands)):
            card_x_before[0][i] = 639.5 - ((value.spacing * (len(value.hands) - 1)+width) / 2) + i * value.spacing
            card_x_after[0][i] = 639.5 - ((value.spacing_after * (len(value.hands) - 2)+width) / 2) + j * value.spacing_after
            if i!=card_select_base[0]:
                j+=1
        for i in range(len(value.hands2)):
            card_x_before[1][i] = 639.5 - ((value.spacing2 * (len(value.hands2) - 1)+width) / 2) + i * value.spacing2
            card_x_after[1][i] = 639.5 - ((value.spacing2_after * (len(value.hands2) - 2)+width) / 2) + j * value.spacing2_after
            if i!=card_select_base[1]:
                j+=1

    for i in range(9, -1, -1):
        if i==card_select_base[0]:
            value.card_dx[0][i]=(20-card_move_time)*speedx
            if card_move_time==0:
                del value.hands[i]
        else:
            value.card_dx[0][i]=(card_x_after[0][i]-card_x_before[0][i])/20*(20-card_move_time)
        if i==card_select_base[1]:
            value.card_dx[1][i]=(20-card_move_time)*speedx
            if card_move_time==0:
                del value.hands2[i]
        else:
            value.card_dx[1][i]=(card_x_after[1][i]-card_x_before[1][i])/20*(20-card_move_time)
    if card_move_time==0:
        value.card_dx=[[0]*10,[0]*10]
        value.card_dy=[[0]*10,[0]*10]
        value.eventnum=-1
    if card_move_time>0:card_move_time-=1

