import pygame
import sys
import math

import value
import random
import evalufunc
pygame.init()

def blockch(x,y,dx,dy,p):
    if 0<=x*2-2+dx<5 and 0<=y*2-2+dy<5:
        if value.board2[x*2-2+dx][y*2-2+dy]==0 or value.board2[x*2-2+dx][y*2-2+dy]==9-p:
            return True
    else:
        return True
    return False

def blockch2(x,y,dx,dy,p):
    if 0<=x*2-2+dx<5 and 0<=y*2-2+dy<5:
        if value.board2[x*2-2+dx][y*2-2+dy]==p:
            return True
    return False

def tokench(x,y,dx,dy,p):
    ch=0
    for i in range(3):
        if 0<=x+dx*i<5 and 0<=y+dy*i<5:
            if value.board[x+dx*i][y+dy*i]==p or value.board[x+dx*i][y+dy*i]==3 or 5<=value.board[x+dx*i][y+dy*i]<=6:
                ch+=1
    
    for i in range(2):
        if 0<=x+dx*i<5 and 0<=y+dy*i<5:
            if blockch(x+dx*i,y+dy*i,dx,dy,p):
                ch+=1
    if ch==5:
        return True
    return False

def tokench2(x,y,dx,dy,p):
    ch=0
    ch2=0
    for i in range(2):
        if 0<=x+dx*i<5 and 0<=y+dy*i<5:
            if value.board[x+dx*i][y+dy*i]==p or value.board[x+dx*i][y+dy*i]==3 or 5<=value.board[x+dx*i][y+dy*i]<=6:
                ch+=1
                if i==0:
                    ch2+=1
    
    if blockch2(x,y,dx,dy,p):
        ch+=1
        ch2+=1
    if blockch2(x,y,-dx,-dy,p):
        ch2+=1
    if ch==3 or ch2==3:
        return True
    return False

def check_win(p):
    for row in range(5):
        for col in range(5):
            for i in range(4):
                dx=0
                dy=0
                match i:
                    case 0:
                        dx=1
                    case 1:
                        dx=1
                        dy=1
                    case 2:
                        dy=1
                    case 3:
                        dx=-1
                        dy=1
                if tokench(row,col,dx,dy,p) or tokench2(row,col,dx,dy,p):
                    return True
    return False

#リーチ
def check_reach(p,x,y):
    hold = value.board[x][y]
    value.board[x][y] = p 

    result = check_win(p)

    value.board[x][y] = hold
    return result

def check_reach2(p,x,y):
    hold = value.board2[x][y]
    value.board2[x][y] = p 

    result = check_win(p)

    value.board2[x][y] = hold
    return result

def reach(p):
    spots=[]
    for i in range(5):
        for j in range(5):
            if check_reach(p,i,j):
                spots.append((i, j))
    
    return spots
def reach2(p):
    spots=[]
    for i in range(2):
        for j in range(2):
            if check_reach(p,i*2+1,j*2+1):
                spots.append((i*2+1,j*2+1))
    
    return spots

#カード使用　-1はパス
def card_select():

    r=evalufunc.bestmove(2)
    
    for x,y in reach(2):
        if value.board[x][y]==0 and 0<x<4 and 0<y<4:#cout<<
            if len(value.hands2)>max(0,value.cost[25]+value.card_dcost[1]):
                for i in range(len(value.hands2)):
                    if value.hands2[i]==25:
                        r=i
                        break
        elif value.board[x][y]==0:#外れ値
            if len(value.hands2)>max(0,value.cost[21]+value.card_dcost[1]):
                for i in range(len(value.hands2)):
                    if value.hands2[i]==21:
                        r=i
                        break
        if value.board[x][y]==3-value.player and 0<x<4 and 0<y<4:#ダブルダウン:立体交差
            if len(value.hands2)>max(0,value.cost[23]+value.card_dcost[1]):
                for i in range(len(value.hands2)):
                    if value.hands2[i]==23:
                        r=i
                        break
            if len(value.hands2)>max(0,value.cost[43]+value.card_dcost[1]):
                for i in range(len(value.hands2)):
                    if value.hands2[i]==43:
                        r=i
                        break
        if value.board[x][y]==3-value.player:#中割り
            if len(value.hands2)>max(0,value.cost[23]+value.card_dcost[1]):
                for i in range(len(value.hands2)):
                    if value.hands2[i]==23:
                        r=i
                        break
    for x,y in reach2(2):#囲碁
        if len(value.hands2)>max(0,value.cost[22]+value.card_dcost[1]):
            for i in range(len(value.hands2)):
                if value.hands2[i]==22:
                    r=i
                    break

    return r

#カード使用　捨てるカード
def card_select_base(card_s):
    while True:
        r=random.randint(0,len(value.hands2)-1)
        if card_s[r]==0:
            break
    return r

def cpu11():
    r1,r2=evalufunc.bestmove3(2,11)
    value.cput=60
    return r1,r2
def cpu12():
    r1,r2=evalufunc.bestmove3(2,12)
    value.cput=60
    return r1,r2
def cpu13():
    r=evalufunc.bestmove3(2,13)[0]
    return r
def cpu21():
    r1,r2=evalufunc.bestmove3(2,21)
    for x,y in reach(2):
        if value.board[x][y]==0 and (x==0 or x==4 or y==0 or y==4):
            r1,r2=x,y
            break
    value.cput=60
    return r1,r2
def cpu22():
    r1,r2=evalufunc.bestmove3(2,22)
    for x,y in reach2(2):
        if value.board2[x][y]==0 or value.board2[x][y]==3-value.player:
            r1,r2=x,y
            break
    value.cput=60
    return r1,r2
def cpu23():
    r1,r2=evalufunc.bestmove3(2,23)
    for x,y in reach(2):
        if value.board[x][y]==3-value.player and 0<x<4 and 0<y<4:
            r1,r2=x,y
            break
    value.cput=60
    return r1,r2
def cpu25():
    r1,r2=evalufunc.bestmove3(2,25)
    for x,y in reach(2):
        if value.board[x][y]==0 and 0<x<4 and 0<y<4:
            r1,r2=x,y
            break
    value.cput=60
    return r1,r2
def cpu31():
    r1,r2=evalufunc.bestmove3(2,31)
    value.cput=60
    return r1,r2
def cpu32():
    r=evalufunc.bestmove3(2,32)[0]
    value.cput=60
    return r

def cpu41():
    r1,r2=evalufunc.bestmove3(2,41)[:2]
    value.cput=60
    return r1,r2
def cpu41_2():
    r1,r2=evalufunc.bestmove3(2,41)[-2:]
    value.cput=60
    return r1,r2
def cpu42():
    r1,r2=evalufunc.bestmove3(2,42)[:2]
    value.cput=60
    return r1,r2
def cpu42_2():
    r1,r2=evalufunc.bestmove3(2,42)[-2:]
    value.cput=60
    return r1,r2
def cpu43():
    r1,r2,r3=evalufunc.bestmove3(2,43)
    value.cput=60
    return r1,r2,r3
def cpu44():
    r1,r2=evalufunc.bestmove3(2,44)
    for x,y in reach(2):
        if value.board[x][y]==3-value.player:
            r1,r2=x,y
            break
    value.cput=60
    return r1,r2