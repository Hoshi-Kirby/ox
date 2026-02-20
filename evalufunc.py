import pygame
import sys
import math
import copy
import itertools

import value
import skillcardfunccpu
import skillcardfunccpu3
import random
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

def number(p):
    n=0
    for i in range(5):
        for j in range(5):
            if value.board[i][j]==p:
                n+=1
            if value.board[i][j]==3-p:
                n-=0.9
    return n

def fullhands(p):
    if p==1:
        if len(value.hands)==9:
            return 1
        if len(value.hands)==10:
            return 2
    if p==2:
        if len(value.hands2)==9:
            return 1
        if len(value.hands2)==10:
            return 2
    return 0

#カードの価値
def cardvalue(s,p):
    if s==11:
        c1=3
        sum=0
        for x in range(1,4):
            for y in range(1,4):
                if value.board[x][y]==3-p:
                    sum+=1
        r=(reach(3-p)+reach2(3-p))*c1+sum
    return r


# 評価関数
c1,c2,c3,c4= 2 , 1 , 0.1 , 2
def evalufunc(p):
    if p==1:
        r=(len(reach(p))+len(reach2(p)))*c1
        +number(p)*c2
        +(len(value.hands)-len(value.hands2))*c3
        -fullhands(1)*c4
    else:
        r=(len(reach(p))+len(reach2(p)))*c1+number(p)*c2+(len(value.hands2)-len(value.hands))*c3-fullhands(2)*c4
    return r

def bestmove(p):
    max=evalufunc(p)
    copyboard=copy.deepcopy(value.board)
    copyboard2=copy.deepcopy(value.board2)
    copyhands=copy.deepcopy(value.hands)
    copyhands2=copy.deepcopy(value.hands2)
    copyblock=copy.deepcopy(value.block)
    copy404=copy.deepcopy(value.turn404)
    copydcost=copy.deepcopy(value.card_dcost)
    x=0
    maxi=[-1]
    if p==2:
        for i in range (len(value.hands2)):
            skillnum=value.deck[value.decks2][value.hands2[i]]
            if len(value.hands2)>value.cost[skillnum]+value.card_dcost[p-1]:
                skillcardfunccpu.riset(i)
                value.gamestep=3
                while value.gamestep!=1:
                    skillcardfunccpu.portal(skillnum)
                    value.t+=1
                x=evalufunc(p)
                if x > max:
                    max = x
                    maxi = [i]
                elif x == max:
                    maxi.append(i)
                value.board=copy.deepcopy(copyboard)
                value.board2=copy.deepcopy(copyboard2)
                value.hands=copy.deepcopy(copyhands)
                value.hands2=copy.deepcopy(copyhands2)
                value.block=copy.deepcopy(copyblock)
                value.turn404=copy.deepcopy(copy404)
                value.card_dcost=copy.deepcopy(copydcost)
                
    return random.choice(maxi)



#op,ch
def opset(p, skillnum):
    SKILL_OP = {
        11: [1,4,1,4],
        12: [1,4,1,4],
        13: lambda p: [0, len(value.hands2)] if p == 1 else [0, len(value.hands)],
        21: [0,5,0,5],
        22: [1,4,1,4],#1or3
        23: [1,4,1,4],
        25: [1,4,1,4],
        31: [1,4,1,4],
        32: [0,4],
        41: [0,5,0,5,0,5,0,5],
        42: [0,5,0,5,0,5,0,5],
        43: [1,4,1,4,0,2],
        44: [0,5,0,5]
    }
    op = SKILL_OP[skillnum]
    return op(p) if callable(op) else op

def can_use(skillnum, p, i):
    SKILL_COND = {
        11: lambda p, i: value.board[i[0]][i[1]]==3-p or value.board[i[0]][i[1]]==3,
        12: lambda p, i: 1<=value.board[i[0]][i[1]] or 1<=value.board[i[0]-1][i[1]] or 1<=value.board[i[0]][i[1]-1] or 1<=value.board[i[0]+1][i[1]] or 1<=value.board[i[0]][i[1]+1],
        13: lambda p, i: True,
        21: lambda p, i: value.board[i[0]][i[1]]==0 and (i[0]==0 or i[0]==4 or i[1]==0 or i[1]==4),
        22: lambda p, i: i[0]!=2 and i[1]!=2 and(value.board2[i[0]][i[1]]==0 or value.board2[i[0]][i[1]]==3-p),
        23: lambda p, i: value.board[i[0]][i[1]]==3-p,
        25: lambda p, i: value.board[i[0]][i[1]]==0,
        31: lambda p, i: value.board[i[0]][i[1]]==0,
        32: lambda p, i: value.board2[1][1]==0 and value.board2[3][1]==0 and i[0]==0
                      or value.board2[1][3]==0 and value.board2[3][3]==0 and i[0]==1
                      or value.board2[1][1]==0 and value.board2[1][3]==0 and i[0]==2
                      or value.board2[3][1]==0 and value.board2[3][3]==0 and i[0]==3,
        41: lambda p, i: value.board[i[0]][i[1]]==p and value.board[i[2]][i[3]]==3-p,
        42: lambda p, i: value.board[i[0]][i[1]]==p and value.board[i[2]][i[3]]==0,
        43: lambda p, i: value.board[i[0]][i[1]]==3-p,
        44: lambda p, i: value.board[i[0]][i[1]]==3-p
    }
    return SKILL_COND[skillnum](p, i)



def bestmove3(p,sknum):
    max = -10**18
    maxi = []
    copyboard=copy.deepcopy(value.board)
    copyboard2=copy.deepcopy(value.board2)
    copyhands=copy.deepcopy(value.hands)
    copyhands2=copy.deepcopy(value.hands2)
    copyblock=copy.deepcopy(value.block)
    copy404=copy.deepcopy(value.turn404)
    copydcost=copy.deepcopy(value.card_dcost)
    x=0
    op=opset(p,sknum)
    if p==2:#opは選択できる[最小値,最大値]配列
        for cpui in itertools.product(*(range(op[i], op[i+1])for i in range(0, len(op), 2))):
            if can_use(sknum, p, cpui):
                skillcardfunccpu3.riset(0)
                value.gamestep=3
                while value.gamestep!=1:
                    skillcardfunccpu3.portal(sknum,cpui)
                    value.t+=1
                x=evalufunc(p)
                if x > max:
                    max = x
                    maxi = [cpui]
                elif x == max:
                    maxi.append(cpui)

                value.board=copy.deepcopy(copyboard)
                value.board2=copy.deepcopy(copyboard2)
                value.hands=copy.deepcopy(copyhands)
                value.hands2=copy.deepcopy(copyhands2)
                value.block=copy.deepcopy(copyblock)
                value.turn404=copy.deepcopy(copy404)
                value.card_dcost=copy.deepcopy(copydcost)
                
    return random.choice(maxi)