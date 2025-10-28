import pygame
import sys
import value
import random
pygame.init()

card_select=[0]*10
def riset(card_select_before):
    global card_select
    card_select=[0]*10
    card_select[card_select_before]=2
    value.card_dx=[[0]*10,[0]*10]
    value.card_dy=[[0]*10,[0]*10]

def portal(skillnum):
    global card_select 
    if value.skillstep==0:
        if value.click==1:
            if value.card_select_base[value.player-1]>=0:
                if card_select[value.card_select_base[value.player-1]]<2:
                    card_select[value.card_select_base[value.player-1]]=1-card_select[value.card_select_base[value.player-1]]
        card_select_number=0
        for i in range(10):
            value.card_dy[value.player-1][i]=0
            value.card_dy[2-value.player][i]=0
            if card_select[i]>=1:
                value.card_dy[value.player-1][i]=-15
                card_select_number+=1
        if card_select_number==value.cost[skillnum]+1:
            value.skillstep=1
            for i in range(9, -1, -1):
                if card_select[i]>=1:
                    if value.player==1:
                        del value.hands[i]
                    else:
                        del value.hands2[i]

    else:
        globals()[f"skill{skillnum}"]()
        #仮
        value.skillstep=0
        value.gamestep=1
        card_select=[0]*10

#value.click==1の時クリックされてる
#skillstepは初めは0
#新たな表示と操作による動きのみ作成する
def skill11():
    pass

def skill12():
    pass

def skill13():
    pass

def skill21():
    pass

def skill22():
    pass

def skill23():
    pass

def skill24():
    pass

def skill25():
    pass

def skill31():
    pass

def skill32():
    pass

def skill33():
    pass

def skill41():
    pass

def skill42():
    pass

def skill43():
    pass

def skill44():
    pass

def skill45():
    pass
    

