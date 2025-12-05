import pygame
import sys
import value
import random
import math
import soundplay
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

#指示
direct_image={}
for i in (0,11,12,13,21,22,23,24,25,31,32,33,41,42,43,44,45):
    direct_image[i]={}
    for j in range(1,3):
        try:
            direct_image[i][j]=pygame.image.load(f"image/direction{i}-{j}.png").convert_alpha()
            direct_image[i][j].set_colorkey((255, 255, 255))
        except FileNotFoundError:
            pass

directx=20
directy=250

sq=pygame.image.load("image/sq.png").convert()
sq.set_colorkey((255, 255, 255))
ci=pygame.image.load("image/ci.png").convert()
ci.set_colorkey((255, 255, 255))

#回転
turn_size=0.2
turn=pygame.image.load("image/turn.png").convert_alpha()
turn2=pygame.image.load("image/turn.png").convert_alpha()
turn= pygame.transform.scale_by(turn,turn_size)
turn2= pygame.transform.scale_by(turn2,turn_size)

for x in range(turn.get_width()):
    for y in range(turn.get_height()):
        r, g, b, a = turn.get_at((x, y))
        if r == 255 and g == 255 and b == 255:
            turn2.set_at((x, y), (255, 255, 255, 0))
        else:
            # 白に近づける（例：平均値をとる）
            r = min(255, int((r + 255/2) / 1.5))
            g = min(255, int((g + 255/2) / 1.5))
            b = min(255, int((b + 255/2) / 1.5))
            turn2.set_at((x, y), (r, g, b, a))

turn.set_colorkey((255, 255, 255))
turnx,turny=800,360
turn2.set_alpha(220)
turn.set_alpha(220)
turn_rect=turn.get_rect(topleft=(turnx,turny))

#橋
bridge_image=[]
bridge_image.append(pygame.image.load("image/bridge-.png").convert())
bridge_image.append(pygame.image.load("image/bridgel.png").convert())
for i in range(2):
    bridge_image[i].set_colorkey((255, 255, 255))
    bridge_image[i].set_alpha(180)

#線
linesize=0.8
img = pygame.image.load("image/neon_line.png").convert_alpha()
w, h = img.get_size()
line = pygame.Surface((w, h), pygame.SRCALPHA)

for y in range(h):
    for x in range(w):
        r, g, b, a = img.get_at((x, y))
        # 白さの平均を計算
        whiteness = (r + g + b)/3
        if whiteness<0:whiteness=0
        # 白いほど透明に（255→0）
        alpha = 255 - int(whiteness)
        if r==0 and g==255:
            line.set_at((x,y),(255,255,255))
        else:
            line.set_at((x, y), (255, 255, 255, alpha))
line = pygame.transform.scale_by(line,linesize)
line_x=-100
line_y=-110
line4 = pygame.image.load("image/neon_line4.png").convert_alpha()
line4 = pygame.transform.scale_by(line4,linesize)


def draw_sq(col, row, alpha):
    global sq_rect
    sq2 = sq.convert_alpha()
    sq2.set_alpha(alpha)

    x = value.OFFSET_X+5 + (col-1) * value.SQUARE_SIZE*1
    y = value.OFFSET_Y+5 + (row-1) * value.SQUARE_SIZE*1

    value.screen.blit(sq2, (x,y))
    sq_rect=sq.get_rect(topleft=(x,y))

def draw_ci(col, row, alpha):
    global ci_rect
    ci2 = ci.convert_alpha()
    ci2.set_alpha(alpha)

    x = value.OFFSET_X+5 + col * value.SQUARE_SIZE/2
    y = value.OFFSET_Y+5 + row * value.SQUARE_SIZE/2

    value.screen.blit(ci2, (x,y))
    ci_rect=ci.get_rect(topleft=(x,y))

def draw_lines(x,alpha):#0,1,2,3 -_||
    global rect_lines
    line2=line.convert_alpha()
    line2.set_alpha(alpha)
    line4_disy=122*0.8
    line4_disx=50
    if x<2:
        if x==0:i=1
        if x==1:i=2
        value.screen.blit(line2, (value.OFFSET_X+line_x, value.OFFSET_Y + i * value.SQUARE_SIZE+line_y))
        rect_lines=line4.get_rect(topleft=(value.OFFSET_X+line_x+line4_disx, value.OFFSET_Y + i * value.SQUARE_SIZE+line_y+line4_disy))

    else:
        if x==2:i=1
        if x==3:i=2
        value.screen.blit(pygame.transform.rotate(line2, -90), (value.OFFSET_X + i * value.SQUARE_SIZE+line_y, value.OFFSET_Y+line_x))
        rect_lines=pygame.transform.rotate(line4, -90).get_rect(topleft=(value.OFFSET_X + i * value.SQUARE_SIZE+line_y+line4_disy, value.OFFSET_Y+line_x+line4_disx))
        


def direction(x,y):
    if not value.detail_check:
        value.screen.blit(direct_image[x][y], (directx,directy))

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

def bridgech(x,y,n):
    if value.board2[x][y]==15-n:
        value.board2[x][y]=9
    else:
        value.board2[x][y]=n


def portal(skillnum):
    global card_select 
    global card_select_skillnum
    global card_move_time
    global card_x_before
    global card_x_after
    if value.skillstep==0:
        card_select_number=0
        for i in range(10):
            value.card_dy[value.player-1][i]=0
            value.card_dy[2-value.player][i]=0
            if card_select[i]>=1:
                value.card_dy[value.player-1][i]=-15
                card_select_number+=1

        direction(0,1)
        if card_select_number==max(1,value.cost[skillnum]+1+value.card_dcost[value.player-1]) or card_move_time>=0:
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
                if 1<card_select_number<5:
                    soundplay.se_play(23)
                elif 5<=card_select_number:
                    soundplay.se_play(24)

            for i in range(9, -1, -1):
                if card_select[i]>=1:
                    value.card_dx[value.player-1][i]=(20-card_move_time)*speedx
                    if card_move_time==0:
                        if value.player==1:
                            del value.hands[i]
                        else:
                            del value.hands2[i]
                else:
                    value.card_dx[value.player-1][i]=(card_x_after[i]-card_x_before[i])/20*(20-card_move_time)
            if card_move_time==0:
                value.skillstep=1
                value.t=0
                value.card_dx=[[0]*10,[0]*10]
                value.card_dy=[[0]*10,[0]*10]
                card_move_time=-2
        elif value.click==1:
            if value.card_select_base[value.player-1]>=0:
                if card_select[value.card_select_base[value.player-1]]<2:
                    if card_select[value.card_select_base[value.player-1]]==0:
                        card_select[value.card_select_base[value.player-1]]=1
                        soundplay.se_play(4)
                    elif card_select[value.card_select_base[value.player-1]]==1:
                        card_select[value.card_select_base[value.player-1]]=0
                        soundplay.se_play(15)
        if card_move_time>0:card_move_time-=1
    else:
        globals()[f"skill{skillnum}"]()
        #仮

#value.click==1の時クリックされてる
#skillstepは初めは0
#新たな表示と操作による動きのみ作成する
def skill11():#deleteキー
    if value.skillstep==1:
        click_x,click_y=-1,-1
        direction(11,1)
        ch=0
        for i in range(0,5):
            for j in range(0,5):
                if value.board[j][i]==3-value.player or value.board[j][i]==3:
                    ch=1
                    draw_sq(j,i,90+40*math.sin(value.t/20))
                    if sq_rect.collidepoint(pygame.mouse.get_pos()):
                        click_x,click_y=j,i
        if value.click==1:
            if click_x!=-1 and click_y!=-1:
                value.skillstep=2
        if ch==0:
            value.skillstep=0
            value.gamestep=1
    if value.skillstep==2:
        value.board[click_x][click_y]=0
        value.skillstep=0
        value.gamestep=1
        soundplay.se_play(17)
        

def skill12():
    if value.skillstep==1:
        click_x,click_y=-1,-1
        direction(12,1)
        ch=0
        for i in range(1,4):
            for j in range(1,4):
                if 1<=value.board[j][i] or 1<=value.board[j-1][i] or 1<=value.board[j][i-1] or 1<=value.board[j+1][i] or 1<=value.board[j][i+1]:
                    ch=1
                    draw_sq(j,i,90+40*math.sin(value.t/20))
                    if sq_rect.collidepoint(pygame.mouse.get_pos()):
                        click_x,click_y=j,i
        if value.click==1:
            if click_x!=-1 and click_y!=-1:
                value.skillstep=2
        if ch==0:
            value.skillstep=0
            value.gamestep=1
    if value.skillstep==2:
        if 1<=value.board[click_x][click_y]:value.board[click_x][click_y]=0
        if 1<=value.board[click_x-1][click_y]:value.board[click_x-1][click_y]=0
        if 1<=value.board[click_x][click_y-1]:value.board[click_x][click_y-1]=0
        if 1<=value.board[click_x+1][click_y]:value.board[click_x+1][click_y]=0
        if 1<=value.board[click_x][click_y+1]:value.board[click_x][click_y+1]=0
        value.skillstep=0
        value.gamestep=1
        soundplay.se_play(18)
        

def skill13():
    global card_move_time
    global card_select_base
    if value.skillstep==1:
        direction(13,1)
        if value.click==1:
            if value.card_select_base[2-value.player]>=0:
                card_select_base=value.card_select_base[2-value.player]
                value.skillstep=2
        card_move_time=-1
        
        if value.player==1 and len(value.hands2)==0 or value.player==2 and len(value.hands)==0:
            value.skillstep=0
            value.gamestep=1
    if value.skillstep==2:
        #初回時
        if card_move_time==-1:
            card_move_time=20
            j=0
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

            if value.player==2:
                for i in range(len(value.hands)):
                    card_x_before[i] = 639.5 - ((value.spacing * (len(value.hands) - 1)+width) / 2) + i * value.spacing
                    card_x_after[i] = 639.5 - ((value.spacing_after * (len(value.hands) - 2)+width) / 2) + j * value.spacing_after
                    if i!=card_select_base:
                        j+=1
            else:
                for i in range(len(value.hands2)):
                    card_x_before[i] = 639.5 - ((value.spacing2 * (len(value.hands2) - 1)+width) / 2) + i * value.spacing2
                    card_x_after[i] = 639.5 - ((value.spacing2_after * (len(value.hands2) - 2)+width) / 2) + j * value.spacing2_after
                    if i!=card_select_base:
                        j+=1
            soundplay.se_play(19)

        for i in range(9, -1, -1):
            if i==card_select_base:
                value.card_dx[2-value.player][i]=(20-card_move_time)*speedx
                if card_move_time==0:
                    if value.player==2:
                        del value.hands[i]
                    else:
                        del value.hands2[i]
            else:
                value.card_dx[2-value.player][i]=(card_x_after[i]-card_x_before[i])/20*(20-card_move_time)
        if card_move_time==0:
            value.skillstep=0
            value.gamestep=1
            value.t=0
    if card_move_time>0:card_move_time-=1
        

def skill21():
    if value.skillstep==1:
        ch=0
        click_x,click_y=-1,-1
        direction(21,1)
        for i in (0,4):
            for j in range(0,5):
                if value.board[j][i]==0:
                    ch=1
                    draw_sq(j,i,90+40*math.sin(value.t/20))
                    if sq_rect.collidepoint(pygame.mouse.get_pos()):
                        click_x,click_y=j,i
        for i in range(1,4):
            for j in (0,4):
                if value.board[j][i]==0:
                    ch=1
                    draw_sq(j,i,90+40*math.sin(value.t/20))
                    if sq_rect.collidepoint(pygame.mouse.get_pos()):
                        click_x,click_y=j,i
        if value.click==1:
            if click_x!=-1 and click_y!=-1:
                value.skillstep=2
        if ch==0:
            value.skillstep=0
            value.gamestep=1
    if value.skillstep==2:
        value.board[click_x][click_y]=value.player
        value.skillstep=0
        value.gamestep=1
        soundplay.se_play(20)
        

def skill22():
    if value.skillstep==1:
        ch=0
        click_x,click_y=-1,-1
        direction(21,1)
        for i in (1,3):
            for j in (1,3):
                if value.board2[j][i]==0 or value.board2[j][i]==3-value.player:
                    ch=1
                    draw_ci(j,i,90+40*math.sin(value.t/20))
                    if ci_rect.collidepoint(pygame.mouse.get_pos()):
                        click_x,click_y=j,i
        if value.click==1:
            if click_x!=-1 and click_y!=-1:
                value.skillstep=2
        if ch==0:
            value.skillstep=0
            value.gamestep=1
    if value.skillstep==2:
        value.board2[click_x][click_y]=value.player
        value.skillstep=0
        value.gamestep=1
        soundplay.se_play(20)
        

def skill23():
    if value.skillstep==1:
        ch=0
        click_x,click_y=-1,-1
        direction(21,1)
        for i in range(1,4):
            for j in range(1,4):
                if value.board[j][i]==3-value.player:
                    ch=1
                    draw_sq(j,i,90+40*math.sin(value.t/20))
                    if sq_rect.collidepoint(pygame.mouse.get_pos()):
                        click_x,click_y=j,i
        if value.click==1:
            if click_x!=-1 and click_y!=-1:
                value.skillstep=2
        if ch==0:
            value.skillstep=0
            value.gamestep=1
    if value.skillstep==2:
        value.board[click_x][click_y]=3
        value.skillstep=0
        value.gamestep=1
        soundplay.se_play(20)
        

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
        soundplay.se_play(7)

def skill25():
    if value.skillstep==1:
        ch=0
        click_x,click_y=-1,-1
        direction(21,1)
        for i in range(1,4):
            for j in range(1,4):
                if value.board[j][i]==0:
                    ch=1
                    draw_sq(j,i,90+40*math.sin(value.t/20))
                    if sq_rect.collidepoint(pygame.mouse.get_pos()):
                        click_x,click_y=j,i
        if value.click==1:
            if click_x!=-1 and click_y!=-1:
                value.skillstep=2
        if ch==0:
            value.skillstep=0
            value.gamestep=1
    if value.skillstep==2:
        value.board[click_x][click_y]=value.player
        value.skillstep=0
        value.gamestep=1
        soundplay.se_play(20)
        

def skill31():
    if value.skillstep==1:
        ch=0
        click_x,click_y=-1,-1
        direction(31,1)
        for i in range(1,4):
            for j in range(1,4):
                if value.board[j][i]==0:
                    ch=1
                    draw_sq(j,i,90+40*math.sin(value.t/20))
                    if sq_rect.collidepoint(pygame.mouse.get_pos()):
                        click_x,click_y=j,i
        if value.click==1:
            if click_x!=-1 and click_y!=-1:
                value.skillstep=2
        if ch==0:
            value.skillstep=0
            value.gamestep=1
    if value.skillstep==2:
        value.board[click_x][click_y]=4
        value.skillstep=0
        value.gamestep=1
        value.turn404[click_x][click_y]=3
        soundplay.se_play(20)
        

def skill32():
    if value.skillstep==1:
        ch=0
        click_x=-1
        direction(32,1)
        alpha_t=50+100*math.sin(value.t/20)
        if value.board2[1][1]==0 and value.board2[3][1]==0:
            ch=1
            draw_lines(0,alpha_t)
            if rect_lines.collidepoint(pygame.mouse.get_pos()):
                click_x=0
        if value.board2[1][3]==0 and value.board2[3][3]==0:
            ch=1
            draw_lines(1,alpha_t)
            if rect_lines.collidepoint(pygame.mouse.get_pos()):
                if click_x!=-1:
                    click_x=-2
                else:
                    click_x=1
        if value.board2[1][1]==0 and value.board2[1][3]==0:
            ch=1
            draw_lines(2,alpha_t)
            if rect_lines.collidepoint(pygame.mouse.get_pos()):
                if click_x!=-1:
                    click_x=-2
                else:
                    click_x=2
        if value.board2[3][1]==0 and value.board2[3][3]==0:
            ch=1
            draw_lines(3,alpha_t)
            if rect_lines.collidepoint(pygame.mouse.get_pos()):
                if click_x!=-1:
                    click_x=-2
                else:
                    click_x=3
        if value.click==1:
            if click_x>=0:
                value.skillstep=2
        if ch==0:
            value.skillstep=0
            value.gamestep=1
    if value.skillstep==2:
        if click_x==0:
            for i in range(5):
                value.board2[i][1]=9
        if click_x==1:
            for i in range(5):
                value.board2[i][3]=9
        if click_x==2:
            for i in range(5):
                value.board2[1][i]=9
        if click_x==3:
            for i in range(5):
                value.board2[3][i]=9
        value.skillstep=0
        value.gamestep=1
        value.block[click_x]=5
        soundplay.se_play(8)
        

def skill33():
    if value.t==1:
        soundplay.se_play(22)
    if value.t==20:
        value.card_dcost[2-value.player]+=1
    for i in range(10):
        value.card_dy[2-value.player][i]=(20-abs(20-value.t))*10
    if value.t==40:
        value.skillstep=0
        value.gamestep=1
        

def skill41():
    global click_x
    global click_y
    if value.skillstep==1:
        ch=0
        ch2=0
        click_x,click_y=-1,-1
        direction(41,1)
        for i in range(0,5):
            for j in range(0,5):
                if value.board[j][i]==value.player:
                    ch=1
                    draw_sq(j,i,90+40*math.sin(value.t/20))
                    if sq_rect.collidepoint(pygame.mouse.get_pos()):
                        click_x,click_y=j,i
                if value.board[j][i]==3-value.player:
                    ch2=1
        if value.click==1:
            if click_x!=-1 and click_y!=-1:
                value.skillstep=2
        if ch==0 or ch2==0:
            value.skillstep=0
            value.gamestep=1

    if value.skillstep==2:
        click2_x,click2_y=-1,-1
        direction(41,2)
        for i in range(0,5):
            for j in range(0,5):
                if value.board[j][i]==3-value.player:
                    ch=1
                    draw_sq(j,i,90+40*math.sin(value.t/20))
                    if sq_rect.collidepoint(pygame.mouse.get_pos()):
                        click2_x,click2_y=j,i
        if value.click==1:
            if click2_x!=-1 and click2_y!=-1:
                value.skillstep=3

    if value.skillstep==3:
        value.board[click2_x][click2_y]=value.player
        value.board[click_x][click_y]=3-value.player
        value.skillstep=0
        value.gamestep=1
        soundplay.se_play(20)
        

def skill42():
    global click_x
    global click_y
    if value.skillstep==1:
        ch=0
        ch2=0
        click_x,click_y=-1,-1
        direction(42,1)
        for i in range(0,5):
            for j in range(0,5):
                if value.board[j][i]==value.player:
                    ch=1
                    draw_sq(j,i,90+40*math.sin(value.t/20))
                    if sq_rect.collidepoint(pygame.mouse.get_pos()):
                        click_x,click_y=j,i
                if value.board[j][i]==0:
                    ch2=1
        if value.click==1:
            if click_x!=-1 and click_y!=-1:
                value.skillstep=2
        if ch==0 or ch2==0:
            value.skillstep=0
            value.gamestep=1

    if value.skillstep==2:
        click2_x,click2_y=-1,-1
        direction(42,2)
        for i in range(1,4):
            for j in range(1,4):
                if value.board[j][i]==0:
                    ch=1
                    draw_sq(j,i,90+40*math.sin(value.t/20))
                    if sq_rect.collidepoint(pygame.mouse.get_pos()):
                        click2_x,click2_y=j,i
        if value.click==1:
            if click2_x!=-1 and click2_y!=-1:
                value.skillstep=3

    if value.skillstep==3:
        value.board[click2_x][click2_y]=value.player
        value.board[click_x][click_y]=0
        value.skillstep=0
        value.gamestep=1
        soundplay.se_play(20)
        

def skill43():
    if value.skillstep==1:
        ch=0
        click_x,click_y=-1,-1
        direction(43,1)
        value.screen.blit(bridge_image[value.bridge_direct_n],(turnx-30,turny-50))
        if turn_rect.collidepoint(pygame.mouse.get_pos()):
            value.screen.blit(turn2,(turnx,turny))
        else:
            value.screen.blit(turn,(turnx,turny))
        for i in range(1,4):
            for j in range(1,4):
                if value.board[j][i]==3-value.player:
                    ch=1
                    draw_sq(j,i,90+40*math.sin(value.t/20))
                    if sq_rect.collidepoint(pygame.mouse.get_pos()):
                        click_x,click_y=j,i
        if value.click==1:
            if click_x!=-1 and click_y!=-1:
                value.skillstep=2
            if turn_rect.collidepoint(pygame.mouse.get_pos()):
                value.bridge_direct_n=1-value.bridge_direct_n
                soundplay.se_play(4)
        if ch==0:
            value.skillstep=0
            value.gamestep=1
    if value.skillstep==2:
        value.bridge_direct[click_x][click_y]=value.bridge_direct_n
        value.board[click_x][click_y]=4+value.player
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
        soundplay.se_play(20)
        

def skill44():
    if value.skillstep==1:
        ch=0
        click_x,click_y=-1,-1
        direction(44,1)
        for i in range(0,5):
            for j in range(0,5):
                if value.board[j][i]==3-value.player:
                    ch=1
                    draw_sq(j,i,90+40*math.sin(value.t/20))
                    if sq_rect.collidepoint(pygame.mouse.get_pos()):
                        click_x,click_y=j,i
        if value.click==1:
            if click_x!=-1 and click_y!=-1:
                value.skillstep=2
        if ch==0:
            value.skillstep=0
            value.gamestep=1
    if value.skillstep==2:
        value.board[click_x][click_y]=value.player
        value.skillstep=0
        value.gamestep=1
        soundplay.se_play(20)
        

def skill45():
    if value.t==1:
        soundplay.se_play(21)
    if value.t==20:
        value.card_dcost[value.player-1]-=1
    for i in range(10):
        value.card_dy[value.player-1][i]=(20-abs(20-value.t))*10
    if value.t==40:
        value.skillstep=0
        value.gamestep=1
        
    

