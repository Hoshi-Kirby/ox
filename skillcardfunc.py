import pygame
import sys
import value
import random
pygame.init()

speedx=20
hand_max=10
cardx_move=0
cardx_move2=0
card_x_before=[0]*10
card_x_after=[0]*10
width=pygame.image.load(f"image/card1-1.png").convert().get_width()
def handsadd(h,m):
    check=[0]*20
    if h==1:
        for i in range(len(value.hands)):
            check[value.hands[i]]=1
        if len(value.hands)>hand_max:
            m=0
    elif h==2:
        for i in range(len(value.hands2)):
            check[value.hands2[i]]=1   
        if len(value.hands2)>hand_max:
            m=0
    for i in range(m):
        if h==1:
            a=random.randint(0,19-len(value.hands))
        elif h==2:
            a=random.randint(0,19-len(value.hands2))
        addnum=0
        while check[addnum]==1:
            addnum+=1
        for j in range(a):
            addnum+=1
            while check[addnum]==1:
                addnum+=1
        if h==1:
            value.hands.append(addnum)
        elif h==2:
            value.hands2.append(addnum)

def riset(card_select_before):
    global card_select
    global card_select_skillnum
    global card_move_time
    card_select=[0]*10
    card_select_skillnum=[]
    card_select[card_select_before]=2
    card_move_time=-1
    value.card_dx=[[0]*10,[0]*10]
    value.card_dy=[[0]*10,[0]*10]




def portal(skillnum):
    global card_select 
    global card_select_skillnum
    global card_move_time
    global card_x_before
    global card_x_after
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
        if card_select_number==value.cost[skillnum]+1 or card_move_time>=0:
            #初回時
            if card_move_time==-1:
                card_move_time=20
                j=0
                #カード間隔
                if len(value.hands)-card_select_number<6:
                    value.spacing_after=120
                elif len(value.hands)-card_select_number<8:
                    value.spacing_after=80
                else:
                    value.spacing_after=50
                if len(value.hands2)-card_select_number<6:
                    value.spacing2_after=120
                elif len(value.hands2)-card_select_number<8:
                    value.spacing2_after=80
                else:
                    value.spacing2_after=50

                if value.player==1:
                    for i in range(len(value.hands)):
                        card_x_before[i] = 639.5 - ((value.spacing * (len(value.hands) - 1)+width) / 2) + i * value.spacing
                        card_x_after[i] = 639.5 - ((value.spacing_after * (len(value.hands) - 1-card_select_number)+width) / 2) + j * value.spacing_after
                        if card_select[i]==0:
                            j+=1
                else:
                    for i in range(len(value.hands2)):
                        card_x_before[i] = 639.5 - ((value.spacing2 * (len(value.hands2) - 1)+width) / 2) + i * value.spacing2
                        card_x_after[i] = 639.5 - ((value.spacing2_after * (len(value.hands2) - 1-card_select_number)+width) / 2) + j * value.spacing2_after
                        if card_select[i]==0:
                            j+=1

            for i in range(9, -1, -1):
                if card_select[i]>=1:
                    value.card_dx[value.player-1][i]=(20-card_move_time)*speedx
                    if card_move_time==0:
                        if value.player==1:
                            card_select_skillnum.append(value.deck[value.decks][value.hands[i]])
                            del value.hands[i]
                        else:
                            card_select_skillnum.append(value.deck[value.decks2][value.hands2[i]])
                            del value.hands2[i]
                else:
                    value.card_dx[value.player-1][i]=(card_x_after[i]-card_x_before[i])/20*(20-card_move_time)
            if card_move_time==0:
                value.skillstep=1
                value.t=0
        if card_move_time>0:card_move_time-=1
    else:
        globals()[f"skill{skillnum}"]()
        #仮

#value.click==1の時クリックされてる
#skillstepは初めは0
#新たな表示と操作による動きのみ作成する
def skill11():
    
        value.skillstep=0
        value.gamestep=1
        

def skill12():
    
        value.skillstep=0
        value.gamestep=1
        

def skill13():
    
        value.skillstep=0
        value.gamestep=1
        

def skill21():
    
        value.skillstep=0
        value.gamestep=1
        

def skill22():
    
        value.skillstep=0
        value.gamestep=1
        

def skill23():
    
        value.skillstep=0
        value.gamestep=1
        

def skill24():
    global cardx_move
    global cardx_move2
    if value.t==1:
        handsadd(value.player,1)
        cardx_move=10
        cardx_move2=30
    if value.player==1:
        for i in range(len(value.hands)-1):
            value.card_dx[0][i] = cardx_move/20 * value.spacing/2
        value.card_dx[0][len(value.hands)-1] = cardx_move2/20 * value.spacing*20
    else:
        for i in range(len(value.hands2)-1):
            value.card_dx[1][i] = cardx_move/20 * value.spacing2/2
        value.card_dx[1][len(value.hands2)-1] = cardx_move2/20 * value.spacing2*20
    if cardx_move>0:cardx_move-=1
    if cardx_move2>0:cardx_move2-=1
    if value.t>30:
        value.skillstep=0
        value.gamestep=1

def skill25():
    
        value.skillstep=0
        value.gamestep=1
        

def skill31():
    
        value.skillstep=0
        value.gamestep=1
        

def skill32():
    
        value.skillstep=0
        value.gamestep=1
        

def skill33():
    
        value.skillstep=0
        value.gamestep=1
        

def skill41():
    
        value.skillstep=0
        value.gamestep=1
        

def skill42():
    
        value.skillstep=0
        value.gamestep=1
        

def skill43():
    
        value.skillstep=0
        value.gamestep=1
        

def skill44():
    
        value.skillstep=0
        value.gamestep=1
        

def skill45():
    if value.t==20:
        value.card_dcost[value.player-1]=-1
    for i in range(10):
        value.card_dy[value.player-1][i]=(20-abs(20-value.t))*10
    if value.t==40:
        value.skillstep=0
        value.gamestep=1
        
    

