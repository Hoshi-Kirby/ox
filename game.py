import pygame
import sys
import math

import value
import random
import skillcardfunc
pygame.init()

#壁紙
pekin = pygame.image.load("image/neon_city.png").convert()
original_width, original_height = pekin.get_size()
pekin = pygame.transform.scale_by(pekin,value.WINDOW_HEIGHT/original_height)
widhe_skew=(value.WINDOW_WIDTH-original_width*value.WINDOW_HEIGHT/original_height)/2-2

black_pekin=pygame.image.load("image/rightwipe.png").convert()
black_pekin.set_colorkey((255, 255, 255))
black_pekin.set_alpha(180)
black_x ,black_y =662,-400
black_x2,black_y2=795,650

#フレーム
frame_size=1
frame=pygame.image.load("image/frame4.png").convert_alpha()
frame = pygame.transform.scale_by(frame,frame_size)
w, h = frame.get_size()

for y in range(h):
    for x in range(w):
        r, g, b, a = frame.get_at((x, y))
        # 白さの平均を計算
        whiteness = (r + g + b)-255*2
        if whiteness<0:whiteness=0
        # 白いほど透明に（255→0）
        alpha = 255 - int(whiteness)
        frame.set_at((x, y), (0, g, b, alpha))


frame.set_alpha(180)

framex,framey=-360,20
frame2x,frame2y,frame2y2=900,25,700

#駒
tokensize=1
token=[]
token.append(pygame.image.load("image/maru.png").convert())
token.append(pygame.image.load("image/batu.png").convert())
token.append(pygame.image.load("image/unuse.png").convert())
for i in range(3):
    token[i] = pygame.transform.scale_by(token[i],tokensize)
    token[i].set_colorkey((255, 255, 255))

font =pygame.font.SysFont("Meiryo UI", 36)

#線
linesize=0.8
img = pygame.image.load("image/neon_line.png").convert_alpha()
w, h = img.get_size()
line = pygame.Surface((w, h), pygame.SRCALPHA)
line2 = pygame.Surface((w, h), pygame.SRCALPHA)
line3 = pygame.Surface((w, h), pygame.SRCALPHA)

for y in range(h):
    for x in range(w):
        r, g, b, a = img.get_at((x, y))
        # 白さの平均を計算
        whiteness = (r + g + b)/3
        if whiteness<0:whiteness=0
        # 白いほど透明に（255→0）
        alpha = 255 - int(whiteness)
        if r==0 and g==255:
            line.set_at((x, y), (255,b,255))
            line2.set_at((x,y),(255,255,255))
            line3.set_at((x,y),(90+100*b/255,170*b/255,15+140*b/255))
        else:
            line.set_at((x, y), (255, 0, 255, alpha))
            line2.set_at((x, y), (255, 255, 255, alpha))
            line3.set_at((x, y), (90, 0, 15, alpha))
line = pygame.transform.scale_by(line,linesize)
line2 = pygame.transform.scale_by(line2,linesize)
line3 = pygame.transform.scale_by(line3,linesize)
line_x=-100
line_y=-110
line2y=90
line2yy=360

#橋
bridge_image=[]
bridge_image.append(pygame.image.load("image/bridge-.png").convert())
bridge_image.append(pygame.image.load("image/bridgel.png").convert())
for i in range(2):
    bridge_image[i].set_colorkey((255, 255, 255))
    bridge_image[i].set_alpha(180)

#Turn End
turnend=pygame.image.load("image/Turn End.png").convert_alpha()
turnend2=pygame.image.load("image/Turn End.png").convert_alpha()

for x in range(turnend.get_width()):
    for y in range(turnend.get_height()):
        r, g, b, a = turnend.get_at((x, y))
        if r == 255 and g == 255 and b == 255:
            turnend2.set_at((x, y), (255, 255, 255, 0))
        else:
            # 白に近づける（例：平均値をとる）
            r = min(255, int((r + 255/2) / 1.5))
            g = min(255, int((g + 255/2) / 1.5))
            b = min(255, int((b + 255/2) / 1.5))
            turnend2.set_at((x, y), (r, g, b, a))

turnend.set_colorkey((255, 255, 255))
turnendx,turnendy=900,350
turnend2.set_alpha(220)
turnend.set_alpha(220)
turnend_rect=turnend.get_rect(topleft=(turnendx,turnendy))

#枚数
mai=[]
for i in range(10):
    mai.append(pygame.image.load(f"image/{i}.png").convert())
    mai[i].set_colorkey((255, 255, 255))
mai10=pygame.image.load("image/1-.png").convert()
mai20=pygame.image.load("image/2-.png").convert()
rest=pygame.image.load("image/rest.png").convert()
mai10.set_colorkey((255, 255, 255))
mai20.set_colorkey((255, 255, 255))
rest.set_colorkey((255, 255, 255))
omaix=900
omaiy=700
xmaiy=30
maix=omaix+200
maimai_distance=10
restx=omaix+100


#メニュー
menu_size=0.2
menu_icon=pygame.image.load("image/menu.png").convert()
menu_icon = pygame.transform.scale_by(menu_icon,menu_size)
menux,menuy=20,20
menu_icon_rect=menu_icon.get_rect(topleft=(menux, menuy))

#のターン
sturn=pygame.image.load("image/'s turn.png").convert()
sturn.set_colorkey((255, 255, 255))
sturny=120

#説明
detail_image={}
for i in (11,12,13,21,22,23,24,25,31,32,33,41,42,43,44,45):
    detail_image[i]=pygame.image.load(f"image/detail{i}.png").convert_alpha()
    detail_image[i].set_colorkey((255, 255, 255))
detailx=20
detaily=250

#イベント
no_event=pygame.image.load("image/noevent.png").convert()
no_event.set_colorkey((255, 255, 255))
no_event_y=600
no_event= pygame.transform.scale_by(no_event,0.8)

#文字
ready_text=font.render("Ready?", True, (255, 255, 255))
font_size_max=200
font_size=60
ready_time=240
ready_time2=100
start_text=font.render("Start!", True, (255, 255, 255))
start_time=150
start_time2=50
finish_text=font.render("Finish!", True, (255, 255, 255))
finish_time=150
finish_time2=50

finish=False
finisht=0



#text.get_rect(center=(295, 300))

#カード
all_cards_image={}
card_size=2
for i in (11,12,13,21,22,23,24,25,31,32,33,41,42,43,44,45):
    all_cards_image[i]=pygame.image.load(f"image/card{i // 10}-{i % 10}.png").convert()
    all_cards_image[i]=pygame.transform.scale_by(all_cards_image[i],card_size)

value.spacing = 120  # カード間のスペース
value.spacing2 = 120  # カード間のスペース
width=all_cards_image[11].get_width()
cardx_move=0
cardx_move2=0
card_select=-1
skillcard=0
hand_max=9

#コスト
cost_image=[]
for i in range(11):
    cost_image.append(pygame.image.load(f"image/cost{i}.png").convert())
    cost_image[i].set_colorkey((255, 255, 255))
    cost_image[i]=pygame.transform.scale_by(cost_image[i],card_size)
card_dcost_mode=False

#先行一ターン目
first=True

def draw_lines():
    for i in range(1, value.BOARD_ROWS):
        if value.block[i-1]>=0:
            value.screen.blit(line3, (value.OFFSET_X+line_x, value.OFFSET_Y + i * value.SQUARE_SIZE+line_y))
        else:
            value.screen.blit(line, (value.OFFSET_X+line_x, value.OFFSET_Y + i * value.SQUARE_SIZE+line_y))
    for i in range(1, value.BOARD_COLS):
        if value.block[i+1]>=0:
            value.screen.blit(pygame.transform.rotate(line3, -90), (value.OFFSET_X + i * value.SQUARE_SIZE+line_y, value.OFFSET_Y+line_x))
        else:
            value.screen.blit(pygame.transform.rotate(line, -90), (value.OFFSET_X + i * value.SQUARE_SIZE+line_y, value.OFFSET_Y+line_x))

def draw_token(col, row, ox, step):
    if step==0:
        x = value.OFFSET_X + (col-1) * value.SQUARE_SIZE
        y = value.OFFSET_Y + (row-1) * value.SQUARE_SIZE
    else:
        x = value.OFFSET_X + col * value.SQUARE_SIZE/2
        y = value.OFFSET_Y + row * value.SQUARE_SIZE/2
    margin = value.SQUARE_SIZE // 2  # 余白を調整

    dy=15

    if ox==2:
        value.screen.blit(token[0], (x-margin,y))
        value.screen.blit(token[1], (x-margin,y))
    elif ox==3:
        value.screen.blit(token[2], (x-margin,y))
    elif ox==4:
        value.screen.blit(token[1], (x-margin,y))
        value.screen.blit(bridge_image[value.bridge_direct[col][row]], (x-margin,y))
        value.screen.blit(token[0], (x-margin,y-dy))
    elif ox==5:
        value.screen.blit(token[0], (x-margin,y))
        value.screen.blit(bridge_image[value.bridge_direct[col][row]], (x-margin,y))
        value.screen.blit(token[1], (x-margin,y-dy))
    else:
        value.screen.blit(token[ox], (x-margin,y))

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
    else:
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
    for i in range(2):
        if 0<=x+dx*i<5 and 0<=y+dy*i<5:
            if value.board[x+dx*i][y+dy*i]==p or value.board[x+dx*i][y+dy*i]==3 or 5<=value.board[x+dx*i][y+dy*i]<=6:
                ch+=1
    
    if blockch2(x,y,dx,dy,p):
        ch+=1
    if ch==3:
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

def handsadd(h,n,m):
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
        
def detail(x,xx,yy):
    value.detail_check=True
    value.screen.blit(detail_image[x], (xx,yy))

        

def gameb():
    global font_size
    global cardx_move
    global cardx_move2
    
    
    global first
    global finish
    #スタート変数
    value.spacing = 120  # カード間のスペース
    value.spacing2 = 120  # カード間のスペース
    first=True
    value.board = [[0 for _ in range(5)] for _ in range(5)]
    value.board2 = [[0 for _ in range(5)] for _ in range(5)]
    value.turn404 = [[0 for _ in range(5)] for _ in range(5)]
    value.bridge_direct=[[0 for _ in range(5)] for _ in range(5)]  #0=横
    value.block=[-1]*4
    finish=False
    value.winner=0

    value.screen.blit(pekin, (widhe_skew,0))
    draw_lines()
    for i in range(5):
        for j in range(5):
            match value.board[i][j]:
                case (1|2|3|4|5|6):
                    draw_token(i,j,value.board[i][j]-1,0)
                case _:
                    pass
            match value.board2[i][j]:
                case (1|2):
                    draw_token(i,j,value.board2[i][j]-1,1)
                case _:
                    pass
    if 50>value.t:
        value.screen.blit(frame, (framex-(50-value.t)*4,framey))
    else:
        value.screen.blit(frame, (framex,framey))
        
    
    if value.t<ready_time:
        font_size=font_size_max
    elif value.t<ready_time+ready_time2:
        font_size=int((ready_time+ready_time2-value.t)*font_size_max/ready_time2)  # 毎フレーム1ずつ小さく
    elif value.t<start_time+ready_time+ready_time2:
        font_size=font_size_max
    elif value.t<start_time+start_time2+ready_time+ready_time2:
        font_size=int((start_time+start_time2-value.t+ready_time+ready_time2)*font_size_max/start_time2)
    font = pygame.font.SysFont("Meiryo UI", font_size)
    if value.t<ready_time+ready_time2:
        ready_text = font.render("Ready?", True, (255, 160, 160))
        value.screen.blit(ready_text, ready_text.get_rect(center=(639.5, 400)))
    elif value.t<start_time+start_time2+ready_time+ready_time2:
        start_text = font.render("Start!", True, (255, 160, 160))
        value.screen.blit(start_text, start_text.get_rect(center=(639.5, 400)))

    if value.t<60:
        value.screen.blit(token[value.player-1], (detailx+math.sin(value.t/10*math.pi)*10,sturny))
    else:
        value.screen.blit(token[value.player-1], (detailx,sturny))

    value.screen.blit(menu_icon,(menux,menuy))

    value.screen.blit(sturn, (detailx+100,sturny))
    #イベント
    value.screen.blit(no_event, (detailx,no_event_y))

    value.screen.blit(line2,(detailx-50,line2y))
    value.screen.blit(line2,(detailx-50,line2y+line2yy))

    if 50>value.t:
        y=(50-value.t)*4
    else:
        y=0
    value.screen.blit(black_pekin,(black_x+y,black_y-y))
    value.screen.blit(black_pekin,(black_x2+y,black_y2+y))
    value.screen.blit(token[0],(omaix,xmaiy))
    value.screen.blit(token[1],(omaix,omaiy))
    value.screen.blit(rest,(restx,omaiy))
    value.screen.blit(rest,(restx,xmaiy))
    if len(value.hands2)==0:
        value.screen.blit(mai20,(maix,xmaiy))
        value.screen.blit(mai[0],(maix+maimai_distance+10,xmaiy))
    else:
        value.screen.blit(mai10,(maix,xmaiy))
        value.screen.blit(mai[10-len(value.hands2)],(maix+maimai_distance,xmaiy))
        
    if len(value.hands)==0:
        value.screen.blit(mai20,(maix,omaiy))
        value.screen.blit(mai[0],(maix+maimai_distance+10,omaiy))
    else:
        value.screen.blit(mai10,(maix,omaiy))
        value.screen.blit(mai[10-len(value.hands)],(maix+maimai_distance,omaiy))

    cardx,cardy,cardy2 = 639.5 - ((value.spacing * (len(value.hands) - 1)+width) / 2),630,10
    j=0
    x = cardx+cardx_move/10 * value.spacing/2
    x2 = cardx+cardx_move2/10 * value.spacing*20
    for i in value.hands:
        card_rect = all_cards_image[11].get_rect(topleft=(x + j * value.spacing, cardy))
        y = cardy - 10 if card_rect.collidepoint(pygame.mouse.get_pos()) else cardy
        cardnumber=value.deck[value.decks][i]
        if j==len(value.hands):
            value.screen.blit(all_cards_image[cardnumber], (x2 + j * value.spacing, y))
            value.screen.blit(cost_image[max(0,value.cost[cardnumber]+value.card_dcost[0])], (x2 + j * value.spacing, y))
        else:
            value.screen.blit(all_cards_image[cardnumber], (x + j * value.spacing, y))
            value.screen.blit(cost_image[max(0,value.cost[cardnumber]+value.card_dcost[1])], (x + j * value.spacing, y))
        if card_rect.collidepoint(pygame.mouse.get_pos()):
            detail(cardnumber,detailx,detaily)
        j+=1
    j=0
    for i in value.hands2:
        card_rect = all_cards_image[11].get_rect(topleft=(x + j * value.spacing, cardy2))
        y = cardy2 + 10 if card_rect.collidepoint(pygame.mouse.get_pos()) else cardy2
        cardnumber=value.deck[value.decks2][i]
        if j==len(value.hands2):
            value.screen.blit(all_cards_image[cardnumber], (x2 + j * value.spacing, y))
            value.screen.blit(cost_image[value.cost[cardnumber]], (x2 + j * value.spacing, y))
        else:
            value.screen.blit(all_cards_image[cardnumber], (x + j * value.spacing, y))
            value.screen.blit(cost_image[value.cost[cardnumber]], (x + j * value.spacing, y))
        if card_rect.collidepoint(pygame.mouse.get_pos()):
            detail(cardnumber,detailx,detaily)
        j+=1
    
    value.screen.blit(turnend,(turnendx,turnendy))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    if value.t>start_time+start_time2+ready_time+ready_time2:
        value.gamestep=1
                     
    if value.fade_out:
        value.fade_alpha += 20  # フェード速度（調整可）
        if value.fade_alpha >= 255:
            value.fade_alpha = 255
            if value.nextstep==3:
                value.fade_out = False
                value.fade_in = True

        value.fade_surface.set_alpha(value.fade_alpha)
        value.screen.blit(value.fade_surface, (0, 0))

    if value.fade_in:
        value.t=0
        value.fade_alpha -= 20  # フェード速度（調整可）
        if value.fade_alpha <= 0:
            value.fade_alpha = 0

            value.fade_in = False

        value.fade_surface.set_alpha(value.fade_alpha)
        value.screen.blit(value.fade_surface, (0, 0))

    for j in range(value.handsize_change[value.Startinghandsize]+1):
        if value.t>0 and value.handsize_change[value.Startinghandsize]>0 and (ready_time)*j/(value.handsize_change[value.Startinghandsize])<=value.t<(ready_time)*j/(value.handsize_change[value.Startinghandsize])+1:
            handsadd(1,value.decks,1)
            handsadd(2,value.decks2,1)
            cardx_move=10
            cardx_move2=30

    if cardx_move>0:cardx_move-=1
    if cardx_move2>0:cardx_move2-=1
    value.t+=1
    pygame.display.update()




def game():
    global card_rect
    global card_select
    global skillcard
    global finisht
    global finish
    
    value.screen.blit(pekin, (widhe_skew,0))
    draw_lines()
    for i in range(5):
        for j in range(5):
            match value.board[i][j]:
                case (1|2|3|4|5|6):
                    draw_token(i,j,value.board[i][j]-1,0)
                case _:
                    pass
            match value.board2[i][j]:
                case (1|2):
                    draw_token(i,j,value.board2[i][j]-1,1)
                case _:
                    pass
    

    value.screen.blit(frame, (framex,framey))
    value.screen.blit(token[value.player-1], (detailx,sturny))
    value.screen.blit(sturn, (detailx+100,sturny))
    
    value.screen.blit(no_event, (detailx,no_event_y))

    value.screen.blit(line2,(detailx-50,line2y))
    value.screen.blit(line2,(detailx-50,line2y+line2yy))
    
    value.screen.blit(menu_icon,(menux,menuy))


    value.screen.blit(black_pekin,(black_x,black_y))
    value.screen.blit(black_pekin,(black_x2,black_y2))
    value.screen.blit(token[0],(omaix,xmaiy))
    value.screen.blit(token[1],(omaix,omaiy))
    value.screen.blit(rest,(restx,omaiy))
    value.screen.blit(rest,(restx,xmaiy))
    if len(value.hands2)==0:
        value.screen.blit(mai20,(maix,xmaiy))
        value.screen.blit(mai[0],(maix+maimai_distance+10,xmaiy))
    else:
        value.screen.blit(mai10,(maix,xmaiy))
        value.screen.blit(mai[10-len(value.hands2)],(maix+maimai_distance,xmaiy))
        
    if len(value.hands)==0:
        value.screen.blit(mai20,(maix,omaiy))
        value.screen.blit(mai[0],(maix+maimai_distance+10,omaiy))
    else:
        value.screen.blit(mai10,(maix,omaiy))
        value.screen.blit(mai[10-len(value.hands)],(maix+maimai_distance,omaiy))

    
    cardx,cardx2,cardy,cardy2 = 639.5 - ((value.spacing * (len(value.hands) - 1)+width) / 2), 639.5 - ((value.spacing2 * (len(value.hands2) - 1)+width) / 2),630,10
    card_select=-1
    card_select_any=-1
    for i in range(len(value.hands)):
        j=len(value.hands)-i-1
        card_rect = all_cards_image[11].get_rect(topleft=(cardx + j * value.spacing, cardy))
        if card_rect.collidepoint(pygame.mouse.get_pos()):
            if value.player==1:
                card_select=j
            card_select_any=j
            detail(value.deck[value.decks][value.hands[j]],detailx,detaily)
            break
    j=0
    for i in value.hands:
        card_rect = all_cards_image[11].get_rect(topleft=(cardx + j * value.spacing, cardy))
        y = cardy
        if card_select_any==j:
            y-=10
        cardnumber=value.deck[value.decks][i]
        value.screen.blit(all_cards_image[cardnumber], (cardx + j * value.spacing, y))
        value.screen.blit(cost_image[max(0,value.cost[cardnumber]+value.card_dcost[0])], (cardx + j * value.spacing, y))
        j+=1

    card_select_any=-1
    for i in range(len(value.hands2)):
        j=len(value.hands2)-i-1
        card_rect = all_cards_image[11].get_rect(topleft=(cardx2 + j * value.spacing2, cardy2))
        if card_rect.collidepoint(pygame.mouse.get_pos()):
            if value.player==2:
                card_select=j
            card_select_any=j
            detail(value.deck[value.decks2][value.hands2[j]],detailx,detaily)
            break
    j=0
    for i in value.hands2:
        card_rect = all_cards_image[11].get_rect(topleft=(cardx2 + j * value.spacing2, cardy2))
        y = cardy2
        if card_select_any==j:
            y+=10
        cardnumber=value.deck[value.decks2][i]
        value.screen.blit(all_cards_image[cardnumber], (cardx2 + j * value.spacing2, y))
        value.screen.blit(cost_image[max(0,value.cost[cardnumber]+value.card_dcost[1])], (cardx2 + j * value.spacing2, y))
        j+=1

    if turnend_rect.collidepoint(pygame.mouse.get_pos()):
        value.screen.blit(turnend2,(turnendx,turnendy))
    else:
        value.screen.blit(turnend,(turnendx,turnendy))

    #event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if turnend_rect.collidepoint(pygame.mouse.get_pos()):
                value.player = 2 if value.player == 1 else 1
                value.gamestep=2
                value.t=0
            if card_select>=0:
                if (value.player==1 and len(value.hands)>value.cost[value.deck[value.decks][value.hands[card_select]]]+value.card_dcost[0]) or (value.player==2 and len(value.hands2)>value.cost[value.deck[value.decks2][value.hands2[card_select]]]+value.card_dcost[1]):
                    if value.player==1:
                        skillcard=value.deck[value.decks][value.hands[card_select]]
                    else:
                        skillcard=value.deck[value.decks2][value.hands2[card_select]]
                    value.gamestep=3
                    value.skillstep=0
                    value.card_dy_mode=True
                    skillcardfunc.riset(card_select)
            if menu_icon_rect.collidepoint(pygame.mouse.get_pos()):
                value.step=1

            # mouseX, mouseY = event.pos
            # if value.OFFSET_X <= mouseX < value.OFFSET_X + value.BOARD_SIZE and value.OFFSET_Y <= mouseY < value.OFFSET_Y + value.BOARD_SIZE:
            #     clicked_row = (mouseY - value.OFFSET_Y) // value.SQUARE_SIZE
            #     clicked_col = (mouseX - value.OFFSET_X) // value.SQUARE_SIZE
            #     if 0<=clicked_row<3 and 0<=clicked_col<3:
            #         if value.board[clicked_row][clicked_col] == 0:
            #             value.board[clicked_row][clicked_col] = value.player
            #                 draw_token(i,j,value.player-1)
            #                 print(f"value.player {value.player} wins!")
            #                 value.game_over = True

            #             value.player = 2 if value.player == 1 else 1
    
    if len(value.hands)<6:
        value.spacing=120
    elif len(value.hands)<8:
        value.spacing=80
    else:
        value.spacing=50
    if len(value.hands2)<6:
        value.spacing2=120
    elif len(value.hands2)<8:
        value.spacing2=80
    else:
        value.spacing2=50

    #勝ち
    if check_win(1):
        value.winner=1
    if check_win(2):
        value.winner=2
    if value.winner>0:
        if not finish:
            finisht=value.t
            finish=True
        if value.t<finish_time+finisht:
            font_size=font_size_max
        elif value.t<finish_time+finish_time2+finisht:
            font_size=int((finish_time+finish_time2+finisht-value.t)*font_size_max/finish_time2)
            value.fade_out=True
            value.nextstep=1
        if value.t<finish_time+finish_time2+finisht:
            font = pygame.font.SysFont("Meiryo UI", font_size)
            if value.t<finish_time+finish_time2:
                finish_text = font.render("Finish!", True, (255, 160, 160))
                value.screen.blit(finish_text, finish_text.get_rect(center=(639.5, 400)))


    if value.fade_out:
        value.fade_alpha += 20  # フェード速度（調整可）
        if value.fade_alpha >= 255:
            value.fade_alpha = 255
            if value.nextstep==1:
                #step=5
                value.step=0
                value.fade_out = False
                value.fade_in = True

        value.fade_surface.set_alpha(value.fade_alpha)
        value.screen.blit(value.fade_surface, (0, 0))

    if value.fade_in:
        value.fade_alpha -= 20  # フェード速度（調整可）
        if value.fade_alpha <= 0:
            value.fade_alpha = 0

            value.fade_in = False

        value.fade_surface.set_alpha(value.fade_alpha)
        value.screen.blit(value.fade_surface, (0, 0))

    value.t+=1
    pygame.display.update()

def change():
    global font_size
    global cardx_move
    global cardx_move2
    global first
    global card_dcost_mode
    value.screen.blit(pekin, (widhe_skew,0))
    draw_lines()
    for i in range(5):
        for j in range(5):
            match value.board[i][j]:
                case (1|2|3|4|5|6):
                    draw_token(i,j,value.board[i][j]-1,0)
                case _:
                    pass
            match value.board2[i][j]:
                case (1|2):
                    draw_token(i,j,value.board2[i][j]-1,1)
                case _:
                    pass
    
    value.screen.blit(frame, (framex,framey))

    if value.t<60:
        value.screen.blit(token[value.player-1], (detailx+math.sin(value.t/10*math.pi)*10,sturny))
    else:
        value.screen.blit(token[value.player-1], (detailx,sturny))
    value.screen.blit(sturn, (detailx+100,sturny))
    
    value.screen.blit(no_event, (detailx,no_event_y))
    
    value.screen.blit(line2,(detailx-50,line2y))
    value.screen.blit(line2,(detailx-50,line2y+line2yy))
    
    value.screen.blit(menu_icon,(menux,menuy))

    value.screen.blit(black_pekin,(black_x,black_y))
    value.screen.blit(black_pekin,(black_x2,black_y2))
    value.screen.blit(token[0],(omaix,xmaiy))
    value.screen.blit(token[1],(omaix,omaiy))
    value.screen.blit(rest,(restx,omaiy))
    value.screen.blit(rest,(restx,xmaiy))
    if len(value.hands2)==0:
        value.screen.blit(mai20,(maix,xmaiy))
        value.screen.blit(mai[0],(maix+maimai_distance+10,xmaiy))
    else:
        value.screen.blit(mai10,(maix,xmaiy))
        value.screen.blit(mai[10-len(value.hands2)],(maix+maimai_distance,xmaiy))
        
    if len(value.hands)==0:
        value.screen.blit(mai20,(maix,omaiy))
        value.screen.blit(mai[0],(maix+maimai_distance+10,omaiy))
    else:
        value.screen.blit(mai10,(maix,omaiy))
        value.screen.blit(mai[10-len(value.hands)],(maix+maimai_distance,omaiy))

    #カード
    j=0
    cardx,cardx2,cardy,cardy2 = 639.5 - ((value.spacing * (len(value.hands) - 1)+width) / 2),639.5 - ((value.spacing2 * (len(value.hands2) - 1)+width) / 2),630,10
    x = cardx+cardx_move/20 * value.spacing/2
    x2 = cardx+cardx_move2/20 * value.spacing*20
    x3 = cardx2+cardx_move/20 * value.spacing2/2
    x4 = cardx2+cardx_move2/20 * value.spacing2*20
    
    card_select_any=-1
    for i in range(len(value.hands)):
        j=len(value.hands)-i-1
        card_rect = all_cards_image[11].get_rect(topleft=(x + j * value.spacing, cardy))
        if card_rect.collidepoint(pygame.mouse.get_pos()):
            card_select_any=j
            detail(value.deck[value.decks][value.hands[j]],detailx,detaily)
            break
    j=0
    for i in value.hands:
        card_rect = all_cards_image[11].get_rect(topleft=(x + j * value.spacing, cardy))
        y = cardy
        y+=value.card_dy[0][j]
        if card_select_any==j:
            y-=10
        cardnumber=value.deck[value.decks][i]
        if value.player==1:
            if j==len(value.hands):
                value.screen.blit(all_cards_image[cardnumber], (x2 + j * value.spacing, y))
                value.screen.blit(cost_image[max(0,value.cost[cardnumber]+value.card_dcost[0])], (x2 + j * value.spacing, y))
            else:
                value.screen.blit(all_cards_image[cardnumber], (x + j * value.spacing, y))
                value.screen.blit(cost_image[max(0,value.cost[cardnumber]+value.card_dcost[0])], (x + j * value.spacing, y))
        else:
            value.screen.blit(all_cards_image[cardnumber], (cardx+j * value.spacing, y))
            value.screen.blit(cost_image[max(0,value.cost[cardnumber]+value.card_dcost[1])], (cardx+j * value.spacing, y))
        j+=1

    card_select_any=-1
    for i in range(len(value.hands2)):
        j=len(value.hands2)-i-1
        card_rect = all_cards_image[11].get_rect(topleft=(x3 + j * value.spacing2, cardy2))
        if card_rect.collidepoint(pygame.mouse.get_pos()):
            if value.player==2:
                card_select=j
            card_select_any=j
            detail(value.deck[value.decks2][value.hands2[j]],detailx,detaily)
            break
    j=0
    for i in value.hands2:
        card_rect = all_cards_image[11].get_rect(topleft=(x3 + j * value.spacing2, cardy2))
        y = cardy2
        y-=value.card_dy[1][j]
        if card_select_any==j:
            y+=10
        cardnumber=value.deck[value.decks2][i]
        if value.player==2:
            if j==len(value.hands2):
                value.screen.blit(all_cards_image[cardnumber], (x4 + j * value.spacing2, y))
                value.screen.blit(cost_image[max(0,value.cost[cardnumber]+value.card_dcost[1])], (x4 + j * value.spacing2, y))
            else:
                value.screen.blit(all_cards_image[value.deck[value.decks2][i]], (x3 + j * value.spacing2, y))
                value.screen.blit(cost_image[max(0,value.cost[cardnumber]+value.card_dcost[1])], (x3 + j * value.spacing2, y))
        else:
            value.screen.blit(all_cards_image[value.deck[value.decks2][i]], (cardx2 + j * value.spacing2, y))
            value.screen.blit(cost_image[max(0,value.cost[cardnumber]+value.card_dcost[0])], (cardx2 + j * value.spacing2, y))
        j+=1

    
    #ターンエンド
    value.screen.blit(turnend,(turnendx,turnendy))

    #pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if len(value.hands)<6:
        value.spacing=120
    elif len(value.hands)<8:
        value.spacing=80
    else:
        value.spacing=50
    if len(value.hands2)<6:
        value.spacing2=120
    elif len(value.hands2)<8:
        value.spacing2=80
    else:
        value.spacing2=50
    
    if value.t>60:
        value.gamestep=1

    if value.t==1 or ((not first) and value.t==40):
        if value.player==1:
            if len(value.hands)<10:
                handsadd(1,value.decks,1)
                cardx_move=10
                cardx_move2=30
        else:
            if len(value.hands2)<10:
                handsadd(2,value.decks2,1)
                cardx_move=10
                cardx_move2=30

    #一度だけ
    if value.t==40:
        first=False
        value.card_dy=[[0]*10,[0]*10]
        card_dcost_mode=False
        for i in range(5):
            for j in range(5):
                if value.turn404[i][j]>0:
                    value.turn404[i][j]-=1
                elif value.turn404[i][j]==0:
                    value.board[i][j]=0
                    value.turn404[i][j]=-1
        
        for i in range(5):
            for j in range(5):
                if value.bridge_direct[i][j]==0 and value.board[i][j]==5 or value.bridge_direct[i][j]==1 and value.board[i][j]==6:
                    if j>1:value.board2[2+(i-2)*2][2+(j-2)*2-1]=7
                    if j<1:value.board2[2+(i-2)*2][2+(j-2)*2+1]=7
                    if i>1:value.board2[2+(i-2)*2-1][2+(j-2)*2]=8
                    if i<1:value.board2[2+(i-2)*2+1][2+(j-2)*2]=8
                elif value.bridge_direct[i][j]==1 and value.board[i][j]==5 or value.bridge_direct[i][j]==0 and value.board[i][j]==6:
                    if j>1:value.board2[2+(i-2)*2][2+(j-2)*2-1]=8
                    if j<1:value.board2[2+(i-2)*2][2+(j-2)*2+1]=8
                    if i>1:value.board2[2+(i-2)*2-1][2+(j-2)*2]=7
                    if i<1:value.board2[2+(i-2)*2+1][2+(j-2)*2]=7

        for i in range(4):
            if value.block[i]>0:
                value.block[i]-=1
                if i==0:
                    for j in range(5):
                        value.board2[j][1]=9
                if i==1:
                    for j in range(5):
                        value.board2[j][3]=9
                if i==2:
                    for j in range(5):
                        value.board2[1][j]=9
                if i==3:
                    for j in range(5):
                        value.board2[3][j]=9
            elif value.block[i]==0:
                if i==0:
                    for j in range(5):
                        value.board2[j][1]=0
                if i==1:
                    for j in range(5):
                        value.board2[j][3]=0
                if i==2:
                    for j in range(5):
                        value.board2[1][j]=0
                if i==3:
                    for j in range(5):
                        value.board2[3][j]=0
                value.block[i]=-1
                

    if (value.card_dcost[2-value.player]!=0 or card_dcost_mode)and value.t<40:
        for i in range(10):
            value.card_dy[2-value.player][i]=(20-abs(20-value.t))*10
        if value.t==20:value.card_dcost[2-value.player]=0
        card_dcost_mode=True


    if cardx_move>0:cardx_move-=1
    if cardx_move2>0:cardx_move2-=1
    value.t+=1
    pygame.display.update()













def skillbase():
    global card_rect
    global card_select
    global skillcard

    value.detail_check=False
    
    value.screen.blit(pekin, (widhe_skew,0))
    draw_lines()
    for i in range(5):
        for j in range(5):
            match value.board[i][j]:
                case (1|2|3|4|5|6):
                    draw_token(i,j,value.board[i][j]-1,0)
                case _:
                    pass
            match value.board2[i][j]:
                case (1|2):
                    draw_token(i,j,value.board2[i][j]-1,1)
                case _:
                    pass
    

    value.screen.blit(frame, (framex,framey))
    value.screen.blit(token[value.player-1], (detailx,sturny))
    value.screen.blit(sturn, (detailx+100,sturny))
    
    value.screen.blit(no_event, (detailx,no_event_y))

    value.screen.blit(line2,(detailx-50,line2y))
    value.screen.blit(line2,(detailx-50,line2y+line2yy))
    
    value.screen.blit(menu_icon,(menux,menuy))

    #枚数
    value.screen.blit(black_pekin,(black_x,black_y))
    value.screen.blit(black_pekin,(black_x2,black_y2))
    value.screen.blit(token[0],(omaix,xmaiy))
    value.screen.blit(token[1],(omaix,omaiy))
    value.screen.blit(rest,(restx,omaiy))
    value.screen.blit(rest,(restx,xmaiy))
    if len(value.hands2)==0:
        value.screen.blit(mai20,(maix,xmaiy))
        value.screen.blit(mai[0],(maix+maimai_distance+10,xmaiy))
    else:
        value.screen.blit(mai10,(maix,xmaiy))
        value.screen.blit(mai[10-len(value.hands2)],(maix+maimai_distance,xmaiy))
        
    if len(value.hands)==0:
        value.screen.blit(mai20,(maix,omaiy))
        value.screen.blit(mai[0],(maix+maimai_distance+10,omaiy))
    else:
        value.screen.blit(mai10,(maix,omaiy))
        value.screen.blit(mai[10-len(value.hands)],(maix+maimai_distance,omaiy))

    #手札カード
    cardx,cardx2,cardy,cardy2 = 639.5 - ((value.spacing * (len(value.hands) - 1)+width) / 2), 639.5 - ((value.spacing2 * (len(value.hands2) - 1)+width) / 2),630,10
    
    value.card_select_base=[-1]*2
    if value.player==1:
        card_select_any=card_select
    else:
        card_select_any=-1
    for i in range(len(value.hands)):
        j=len(value.hands)-i-1
        card_rect = all_cards_image[11].get_rect(topleft=(cardx + j * value.spacing, cardy))
        if card_rect.collidepoint(pygame.mouse.get_pos()):
            value.card_select_base[0]=j
            detail(value.deck[value.decks][value.hands[j]],detailx,detaily)
            break
    j=0
    for i in value.hands:
        card_rect = all_cards_image[11].get_rect(topleft=(cardx + j * value.spacing, cardy))
        y = cardy
        y+=value.card_dy[0][j]
        if card_select_any==j:
            y-=30
        elif value.card_select_base[0]==j and value.card_dy_mode:
            y-=10
        cardnumber=value.deck[value.decks][i]
        value.screen.blit(all_cards_image[cardnumber], (cardx+value.card_dx[0][j] + j * value.spacing, y))
        value.screen.blit(cost_image[max(0,value.cost[cardnumber]+value.card_dcost[0])], (cardx+value.card_dx[0][j] + j * value.spacing, y))
        j+=1

    if value.player==2:
        card_select_any=card_select
    else:
        card_select_any=-1
    for i in range(len(value.hands2)):
        j=len(value.hands2)-i-1
        card_rect = all_cards_image[11].get_rect(topleft=(cardx2 + j * value.spacing2, cardy2))
        if card_rect.collidepoint(pygame.mouse.get_pos()):
            value.card_select_base[1]=j
            detail(value.deck[value.decks2][value.hands2[j]],detailx,detaily)
            break
    j=0
    for i in value.hands2:
        card_rect = all_cards_image[11].get_rect(topleft=(cardx2 + j * value.spacing2, cardy2))
        y = cardy2
        y-=value.card_dy[1][j]
        if card_select_any==j:
            y+=30
        elif value.card_select_base[1]==j and value.card_dy_mode:
            y+=10
        cardnumber=value.deck[value.decks2][i]
        value.screen.blit(all_cards_image[cardnumber], (cardx2+value.card_dx[1][j] + j * value.spacing2, y))
        value.screen.blit(cost_image[max(0,value.cost[cardnumber]+value.card_dcost[1])], (cardx2+value.card_dx[1][j] + j * value.spacing2, y))
        j+=1

    #ターンエンド
    value.screen.blit(turnend,(turnendx,turnendy))



    #event
    value.click=0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            value.click=event.button



    if len(value.hands)<6:
        value.spacing=120
    elif len(value.hands)<8:
        value.spacing=80
    else:
        value.spacing=50
    if len(value.hands2)<6:
        value.spacing2=120
    elif len(value.hands2)<8:
        value.spacing2=80
    else:
        value.spacing2=50

    #それぞれ
    skillcardfunc.portal(skillcard)


    value.t+=1
    pygame.display.update()