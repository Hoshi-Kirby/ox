import pygame
import sys
import math

import value
import random
import skillcardfunc
import eventfunc
import soundplay
pygame.init()

#カード使用　-1はパス
def card_select():
    if len(value.hands2)>5:
        r=random.randint(0,len(value.hands2)-1)
    else:
        r=-1

    return r

#カード使用
def card_select_base(card_s):
    while True:
        r=random.randint(0,len(value.hands2)-1)
        if card_s[r]==0:
            break
    return r

def cpu11():
    while True:
        r1=random.randint(1,3)
        r2=random.randint(1,3)
        if value.board[r1][r2]==3-value.player or value.board[r1][r2]==3:
            break
    value.cput=60
    return r1,r2
def cpu12():
    while True:
        r1=random.randint(1,3)
        r2=random.randint(1,3)
        if 1<=value.board[r1][r2] or 1<=value.board[r1-1][r2] or 1<=value.board[r1][r2-1] or 1<=value.board[r1+1][r2] or 1<=value.board[r1][r2+1]:
            break
    value.cput=60
    return r1,r2
def cpu13():
    r=random.randint(0,len(value.hands)-1)
    return r
def cpu21():
    while True:
        r1=random.randint(0,4)
        r2=random.randint(0,4)
        if value.board[r1][r2]==0 and (r1==0 or r1==4 or r2==0 or r2==4):
            break
    value.cput=60
    return r1,r2
def cpu22():
    while True:
        r1=random.randint(0,1)*2+1
        r2=random.randint(0,1)*2+1
        if value.board2[r1][r2]==0 or value.board2[r1][r2]==3-value.player:
            break
    value.cput=60
    return r1,r2
def cpu23():
    while True:
        r1=random.randint(1,3)
        r2=random.randint(1,3)
        if value.board[r1][r2]==3-value.player:
            break
    value.cput=60
    return r1,r2
def cpu25():
    while True:
        r1=random.randint(1,3)
        r2=random.randint(1,3)
        if  value.board[r1][r2]==0:
            break
    value.cput=60
    return r1,r2
def cpu31():
    while True:
        r1=random.randint(1,3)
        r2=random.randint(1,3)
        if  value.board[r1][r2]==0:
            break
    value.cput=60
    return r1,r2
def cpu32():
    while True:
        r=random.randint(0,4)
        if value.board2[1][1]==0 and value.board2[3][1]==0 and r==0:
                break
        if value.board2[1][3]==0 and value.board2[3][3]==0 and r==1:
                break
        if value.board2[1][1]==0 and value.board2[1][3]==0 and r==2:
                break
        if value.board2[3][1]==0 and value.board2[3][3]==0 and r==3:
                break
    value.cput=60
    return r

def cpu41():
    while True:
        r1=random.randint(0,4)
        r2=random.randint(0,4)
        if  value.board[r1][r2]==value.player:
            break
    value.cput=60
    return r1,r2
def cpu41_2():
    while True:
        r1=random.randint(0,4)
        r2=random.randint(0,4)
        if  value.board[r1][r2]==3-value.player:
            break
    value.cput=60
    return r1,r2
def cpu42():
    while True:
        r1=random.randint(0,4)
        r2=random.randint(0,4)
        if  value.board[r1][r2]==value.player:
            break
    value.cput=60
    return r1,r2
def cpu42_2():
    while True:
        r1=random.randint(0,4)
        r2=random.randint(0,4)
        if  value.board[r1][r2]==0:
            break
    value.cput=60
    return r1,r2
def cpu43():
    while True:
        r1=random.randint(1,3)
        r2=random.randint(1,3)
        r3=random.randint(0,1)
        if  value.board[r1][r2]==3-value.player:
            break
    value.cput=60
    return r1,r2,r3
def cpu44():
    while True:
        r1=random.randint(0,4)
        r2=random.randint(0,4)
        if  value.board[r1][r2]==3-value.player:
            break
    value.cput=60
    return r1,r2