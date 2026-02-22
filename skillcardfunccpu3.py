import pygame
import sys
import value
import random
import math
import cpu
pygame.init()

speedx=20
hand_max=10
cardx_move=0
cardx_move2=0
card_x_before=[0]*10
card_x_after=[0]*10

click_x=-1
click_y=-1
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
    # card_select=[0]*10
    # card_select_skillnum=[]
    # card_select[card_select_before]=2
    card_move_time=-1
    # value.card_dx=[[0]*10,[0]*10]
    # value.card_dy=[[0]*10,[0]*10]

def bridgech(x,y,n):
    old = value.board2[x][y]
    value.changes.append(("board2", x, y, old))

    if old == 9:
        return
    if old == 15 - n:
        value.board2[x][y] = 9
    else:
        value.board2[x][y] = n


def portal(skillnum,cpui):
    global card_select 
    global card_select_skillnum
    global card_move_time
    global card_x_before
    global card_x_after
    if value.skillstep==0:
        value.skillstep=1
        # card_select_number=0
        # for i in range(10):
        #     value.card_dy[value.player-1][i]=0
        #     value.card_dy[2-value.player][i]=0
        #     if card_select[i]>=1:
        #         value.card_dy[value.player-1][i]=-15
        #         card_select_number+=1

        # if card_select_number==max(1,value.cost[skillnum]+1+value.card_dcost[value.player-1]) or card_move_time>=0:
        #     #初回時
        #     if card_move_time==-1:
        #         card_move_time=0
        #         j=0
        #         #カード間隔
        #         if len(value.hands)-card_select_number<6:
        #             value.spacing_after=120
        #         elif len(value.hands)-card_select_number<8:
        #             value.spacing_after=80
        #         else:
        #             value.spacing_after=50
        #         if len(value.hands2)-card_select_number<6:
        #             value.spacing2_after=120
        #         elif len(value.hands2)-card_select_number<8:
        #             value.spacing2_after=80
        #         else:
        #             value.spacing2_after=50

        #         if value.player==1:
        #             for i in range(len(value.hands)):
        #                 card_x_before[i] = 639.5 - ((value.spacing * (len(value.hands) - 1)+width) / 2) + i * value.spacing
        #                 card_x_after[i] = 639.5 - ((value.spacing_after * (len(value.hands) - 1-card_select_number)+width) / 2) + j * value.spacing_after
        #                 if card_select[i]==0:
        #                     j+=1
        #         else:
        #             for i in range(len(value.hands2)):
        #                 card_x_before[i] = 639.5 - ((value.spacing2 * (len(value.hands2) - 1)+width) / 2) + i * value.spacing2
        #                 card_x_after[i] = 639.5 - ((value.spacing2_after * (len(value.hands2) - 1-card_select_number)+width) / 2) + j * value.spacing2_after
        #                 if card_select[i]==0:
        #                     j+=1

        #     for i in range(9, -1, -1):
        #         if card_select[i]>=1:
        #             value.card_dx[value.player-1][i]=(20-card_move_time)*speedx
        #             if card_move_time==0:
        #                 if value.player==1:
        #                     del value.hands[i]
        #                 else:
        #                     del value.hands2[i]
        #         else:
        #             value.card_dx[value.player-1][i]=(card_x_after[i]-card_x_before[i])/20*(20-card_move_time)
        #     if card_move_time==0:
        #         value.skillstep=1
        #         value.t=0
        #         value.card_dx=[[0]*10,[0]*10]
        #         value.card_dy=[[0]*10,[0]*10]
        #         card_move_time=-2
        # #CPU
        # elif  value.play_number==0 and value.cput==0:
        #     value.card_select_base[value.player-1]=cpu.card_select_base(card_select)
        #     if value.card_select_base[value.player-1]>=0:
        #         if card_select[value.card_select_base[value.player-1]]<2:
        #             if card_select[value.card_select_base[value.player-1]]==0:
        #                 card_select[value.card_select_base[value.player-1]]=1
        #             elif card_select[value.card_select_base[value.player-1]]==1:
        #                 card_select[value.card_select_base[value.player-1]]=0
        #             value.cput=0
        # if card_move_time>0:card_move_time-=1
    else:
        globals()[f"skill{skillnum}"](cpui)
        #仮

#value.click==1の時クリックされてる
#skillstepは初めは0
#新たな表示と操作による動きのみ作成する
def skill11(cpui):#deleteキー
    if value.skillstep==1:
        click_x,click_y=-1,-1
        ch=0
        for i in range(0,5):
            for j in range(0,5):
                if value.board[j][i]==3-value.player or value.board[j][i]==3:
                    ch=1
        if  value.play_number==0 and value.cput==0 and ch==1:
            click_x,click_y=cpui
            value.cput=0
            value.skillstep=2
        if ch==0:
            value.skillstep=0
            value.gamestep=1
    if value.skillstep==2:
        old = value.board[click_x][click_y]
        value.board[click_x][click_y] = 0
        value.changes.append(("board", click_x, click_y, old))
        
        value.skillstep=0
        value.gamestep=1
        

def skill12(cpui):
    if value.skillstep==1:
        click_x,click_y=-1,-1
        ch=0
        for i in range(1,4):
            for j in range(1,4):
                if 1<=value.board[j][i] or 1<=value.board[j-1][i] or 1<=value.board[j][i-1] or 1<=value.board[j+1][i] or 1<=value.board[j][i+1]:
                    ch=1
        if  value.play_number==0 and value.cput==0 and ch==1:
            click_x,click_y=cpui
            value.cput=0
            value.skillstep=2
        if ch==0:
            value.skillstep=0
            value.gamestep=1
    if value.skillstep==2:
        if 1 <= value.board[click_x][click_y]:
            old = value.board[click_x][click_y]
            value.board[click_x][click_y] = 0
            value.changes.append(("board", click_x, click_y, old))

        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            cx, cy = click_x+dx, click_y+dy
            if 1 <= value.board[cx][cy]:
                old = value.board[cx][cy]
                value.board[cx][cy] = 0
                value.changes.append(("board", cx, cy, old))

        value.skillstep=0
        value.gamestep=1
        

def skill13(cpui):
    global card_move_time
    global card_select_base
    if value.skillstep==1:
        card_move_time=-1
        
        if value.player==1 and len(value.hands2)==0 or value.player==2 and len(value.hands)==0:
            value.skillstep=0
            value.gamestep=1
        
        if  value.play_number==0 and value.cput==0 and value.skillstep==1:
                card_select_base=cpui[0]
                value.skillstep=2
    if value.skillstep==2:
        #初回時
        if card_move_time==-1:
            card_move_time=0

        for i in range(9, -1, -1):
            if i==card_select_base:
                if card_move_time==0:
                    if value.player == 2:
                        old = value.hands[:]  # shallow copy でOK
                        value.changes.append(("hands", old))
                        del value.hands[i]
                    else:
                        old = value.hands2[:]
                        value.changes.append(("hands2", old))
                        del value.hands2[i]
        if card_move_time==0:
            value.skillstep=0
            value.gamestep=1
            value.t=0
    if card_move_time>0:card_move_time-=1
        

def skill21(cpui):
    if value.skillstep==1:
        ch=0
        click_x,click_y=-1,-1
        for i in (0,4):
            for j in range(0,5):
                if value.board[j][i]==0:
                    ch=1
        for i in range(1,4):
            for j in (0,4):
                if value.board[j][i]==0:
                    ch=1
        if  value.play_number==0 and value.cput==0 and ch==1:
            click_x,click_y=cpui
            value.cput=0
            value.skillstep=2
        if ch==0:
            value.skillstep=0
            value.gamestep=1
    if value.skillstep==2:
        old = value.board[click_x][click_y]
        value.board[click_x][click_y] = value.player
        value.changes.append(("board", click_x, click_y, old))

        value.skillstep=0
        value.gamestep=1
        

def skill22(cpui):
    if value.skillstep==1:
        ch=0
        click_x,click_y=-1,-1
        for i in (1,3):
            for j in (1,3):
                if value.board2[j][i]==0 or value.board2[j][i]==3-value.player:
                    ch=1
        if  value.play_number==0 and value.cput==0 and ch==1:
            click_x,click_y=cpui
            value.cput=0
            value.skillstep=2
        if ch==0:
            value.skillstep=0
            value.gamestep=1
    if value.skillstep==2:
        old = value.board2[click_x][click_y]
        value.board2[click_x][click_y] = value.player
        value.changes.append(("board2", click_x, click_y, old))

        value.skillstep=0
        value.gamestep=1
        

def skill23(cpui):
    if value.skillstep==1:
        ch=0
        click_x,click_y=-1,-1
        for i in range(1,4):
            for j in range(1,4):
                if value.board[j][i]==3-value.player:
                    ch=1
        if  value.play_number==0 and value.cput==0 and ch==1:
            click_x,click_y=cpui
            value.cput=0
            value.skillstep=2
        if ch==0:
            value.skillstep=0
            value.gamestep=1
    if value.skillstep==2:
        old = value.board[click_x][click_y]
        value.board[click_x][click_y] = 3
        value.changes.append(("board", click_x, click_y, old))

        value.skillstep=0
        value.gamestep=1
        

def skill24(cpui):
    global cardx_move
    global cardx_move2
    if value.player == 1:
        old = value.hands[:]
        value.changes.append(("hands", old))
    else:
        old = value.hands2[:]
        value.changes.append(("hands2", old))

    handsadd(value.player,1)

    value.skillstep=0
    value.gamestep=1

def skill25(cpui):
    if value.skillstep==1:
        ch=0
        click_x,click_y=-1,-1
        for i in range(1,4):
            for j in range(1,4):
                if value.board[j][i]==0:
                    ch=1
        if  value.play_number==0 and value.cput==0 and ch==1:
            click_x,click_y=cpui
            value.cput=0
            value.skillstep=2
        if ch==0:
            value.skillstep=0
            value.gamestep=1
    if value.skillstep==2:
        old = value.board[click_x][click_y]
        value.board[click_x][click_y] = value.player
        value.changes.append(("board", click_x, click_y, old))

        value.skillstep=0
        value.gamestep=1
        

def skill31(cpui):
    if value.skillstep==1:
        ch=0
        click_x,click_y=-1,-1
        for i in range(1,4):
            for j in range(1,4):
                if value.board[j][i]==0:
                    ch=1
        if  value.play_number==0 and value.cput==0 and ch==1:
            click_x,click_y=cpui
            value.cput=0
            value.skillstep=2
        if ch==0:
            value.skillstep=0
            value.gamestep=1
    if value.skillstep==2:
        # board の変更ログ
        old = value.board[click_x][click_y]
        value.board[click_x][click_y] = 4
        value.changes.append(("board", click_x, click_y, old))

        # turn404 の変更ログ
        old404 = value.turn404[click_x][click_y]
        value.turn404[click_x][click_y] = 3
        value.changes.append(("turn404", click_x, click_y, old404))

        value.skillstep=0
        value.gamestep=1
        

def skill32(cpui):
    if value.skillstep==1:
        ch=0
        click_x=-1
        alpha_t=50+100*math.sin(value.t/20)
        if value.board2[1][1]==0 and value.board2[3][1]==0:
            ch=1
        if value.board2[1][3]==0 and value.board2[3][3]==0:
            ch=1
        if value.board2[1][1]==0 and value.board2[1][3]==0:
            ch=1
        if value.board2[3][1]==0 and value.board2[3][3]==0:
            ch=1
        if  value.play_number==0 and value.cput==0 and ch==1:
            click_x=cpui[0]
            value.cput=0
            value.skillstep=2
        if ch==0:
            value.skillstep=0
            value.gamestep=1
    if value.skillstep==2:
        # board2 の変更ログ（1列 or 1行）
        if click_x == 0:
            for i in range(5):
                old = value.board2[i][1]
                value.board2[i][1] = 9
                value.changes.append(("board2", i, 1, old))
        if click_x == 1:
            for i in range(5):
                old = value.board2[i][3]
                value.board2[i][3] = 9
                value.changes.append(("board2", i, 3, old))
        if click_x == 2:
            for i in range(5):
                old = value.board2[1][i]
                value.board2[1][i] = 9
                value.changes.append(("board2", 1, i, old))
        if click_x == 3:
            for i in range(5):
                old = value.board2[3][i]
                value.board2[3][i] = 9
                value.changes.append(("board2", 3, i, old))
        # block の変更ログ
        old_block = value.block[click_x]
        value.block[click_x] = 5
        value.changes.append(("block", click_x, old_block))

        value.skillstep=0
        value.gamestep=1
        

def skill33(cpui):
    old = value.card_dcost[2-value.player]
    value.card_dcost[2-value.player] += 1
    value.changes.append(("cost", 2-value.player, old))

    value.skillstep=0
    value.gamestep=1
        

def skill41(cpui):
    global click_x
    global click_y
    if value.skillstep==1:
        ch=0
        ch2=0
        click_x,click_y=-1,-1
        for i in range(0,5):
            for j in range(0,5):
                if value.board[j][i]==value.player:
                    ch=1
                if value.board[j][i]==3-value.player:
                    ch2=1
        if  value.play_number==0 and value.cput==0 and ch==1 and ch2==1:
            click_x,click_y=cpui[:2]#最初２つ
            value.cput=0
            value.skillstep=2
        if ch==0 or ch2==0:
            value.skillstep=0
            value.gamestep=1

    if value.skillstep==2:
        click2_x,click2_y=-1,-1
        for i in range(0,5):
            for j in range(0,5):
                if value.board[j][i]==3-value.player:
                    ch=1
        if  value.play_number==0:
            click2_x,click2_y=cpui[-2:]#最後２つ
            value.cput=0
            value.skillstep=3

    if value.skillstep==3:
        old1 = value.board[click2_x][click2_y]
        old2 = value.board[click_x][click_y]
        value.board[click2_x][click2_y] = value.player
        value.board[click_x][click_y] = 3-value.player
        value.changes.append(("board", click2_x, click2_y, old1))
        value.changes.append(("board", click_x, click_y, old2))

        value.skillstep=0
        value.gamestep=1
        

def skill42(cpui):
    global click_x
    global click_y
    if value.skillstep==1:
        ch=0
        ch2=0
        click_x,click_y=-1,-1
        for i in range(0,5):
            for j in range(0,5):
                if value.board[j][i]==value.player:
                    ch=1
                if value.board[j][i]==0:
                    ch2=1
        if  value.play_number==0 and value.cput==0 and ch==1 and ch2==1:
            click_x,click_y=cpui[:2]#最初２つ
            value.cput=0
            value.skillstep=2
        if ch==0 or ch2==0:
            value.skillstep=0
            value.gamestep=1

    if value.skillstep==2:
        click2_x,click2_y=-1,-1
        for i in range(1,4):
            for j in range(1,4):
                if value.board[j][i]==0:
                    ch=1
        if  value.play_number==0:
            click2_x,click2_y=cpui[-2:]#最後２つ
            value.cput=0
            value.skillstep=3

    if value.skillstep==3:
        old1 = value.board[click_x][click_y]
        old2 = value.board[click2_x][click2_y]
        value.board[click_x][click_y] = 0
        value.board[click2_x][click2_y] = value.player
        value.changes.append(("board", click_x, click_y, old1))
        value.changes.append(("board", click2_x, click2_y, old2))

        value.skillstep=0
        value.gamestep=1
        

def skill43(cpui):
    if value.skillstep==1:
        ch=0
        click_x,click_y=-1,-1
        for i in range(1,4):
            for j in range(1,4):
                if value.board[j][i]==3-value.player:
                    ch=1
        if  value.play_number==0 and value.cput==0 and ch==1:
            click_x,click_y,value.bridge_direct_n=cpui
            value.cput=0
            value.skillstep=2
        if ch==0:
            value.skillstep=0
            value.gamestep=1
    if value.skillstep==2:
        old_dir = value.bridge_direct[click_x][click_y]
        value.bridge_direct[click_x][click_y] = value.bridge_direct_n
        value.changes.append(("bridge_direct", click_x, click_y, old_dir))

        old = value.board[click_x][click_y]
        value.board[click_x][click_y] = 4 + value.player
        value.changes.append(("board", click_x, click_y, old))

        if value.bridge_direct[click_x][click_y]==0 and value.player==1 or value.bridge_direct[click_x][click_y]==1 and value.player==2:
            if click_y>1:bridgech(2+(click_x-2)*2,2+(click_y-2)*2-1,7)
            if click_y<3:bridgech(2+(click_x-2)*2,2+(click_y-2)*2+1,7)
            if click_x>1:bridgech(2+(click_x-2)*2-1,2+(click_y-2)*2,8)
            if click_x<3:bridgech(2+(click_x-2)*2+1,2+(click_y-2)*2,8)
        else:
            if click_y>1:bridgech(2+(click_x-2)*2,2+(click_y-2)*2-1,8)
            if click_y<3:bridgech(2+(click_x-2)*2,2+(click_y-2)*2+1,8)
            if click_x>1:bridgech(2+(click_x-2)*2-1,2+(click_y-2)*2,7)
            if click_x<3:bridgech(2+(click_x-2)*2+1,2+(click_y-2)*2,7)
        value.skillstep=0
        value.gamestep=1
        

def skill44(cpui):
    if value.skillstep==1:
        ch=0
        click_x,click_y=-1,-1
        for i in range(0,5):
            for j in range(0,5):
                if value.board[j][i]==3-value.player:
                    ch=1
        if value.click==1:
            if click_x!=-1 and click_y!=-1:
                value.skillstep=2
        if  value.play_number==0 and value.cput==0 and ch==1:
            click_x,click_y=cpui
            value.cput=0
            value.skillstep=2
        if ch==0:
            value.skillstep=0
            value.gamestep=1
    if value.skillstep==2:
        old = value.board[click_x][click_y]
        value.board[click_x][click_y] = value.player
        value.changes.append(("board", click_x, click_y, old))

        value.skillstep=0
        value.gamestep=1
        

def skill45(cpui):
    old = value.card_dcost[value.player-1]
    value.card_dcost[value.player-1] -= 1
    value.changes.append(("cost", value.player-1, old))

    value.skillstep=0
    value.gamestep=1
    return


        