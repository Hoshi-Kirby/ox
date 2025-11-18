import pygame
import sys
import math

import value
import help

pygame.init()

maxpage=7

#壁紙
pekin2 = pygame.image.load("image/neon_city3.png").convert()
original_width2, original_height2 = pekin2.get_size()
pekin2 = pygame.transform.scale_by(pekin2,value.WINDOW_HEIGHT/original_height2)
widhe_skew2=value.WINDOW_WIDTH-original_width2*value.WINDOW_HEIGHT/original_height2

pekin = pygame.image.load("image/leftwhite.png").convert()
original_width, original_height = pekin.get_size()
pekin = pygame.transform.scale_by(pekin,value.WINDOW_HEIGHT/original_height)
pekin.set_colorkey((255, 255, 255))
pekin.set_alpha(80)

pekin3 = pygame.image.load("image/rightwhite.png").convert()
original_width, original_height = pekin3.get_size()
pekin3 = pygame.transform.scale_by(pekin3,value.WINDOW_HEIGHT/original_height)
pekin3.set_colorkey((255, 255, 255))
pekin3.set_alpha(120)

#フレーム
framesize=0.6
frame = pygame.image.load("image/frame1.png").convert()
frame = pygame.transform.scale_by(frame,framesize)
frame.set_colorkey((255, 255, 255))
frame.set_alpha(180)
framex,framey=30,120
frame_distance=120
frame_rect=[]
backx,backy=-150,650

frame2size=1.2
frame2 = pygame.image.load("image/frame2.png").convert()
frame2 = pygame.transform.scale_by(frame2,frame2size)
frame2.set_colorkey((255, 255, 255))
frame2.set_alpha(200)
frame2x,frame2y=400,70

frame3size=1
frame3 = pygame.image.load("image/frame3.png").convert()
frame3 = pygame.transform.scale_by(frame3,frame3size)
frame3.set_colorkey((255, 255, 255))
frame3.set_alpha(220)
frame3x,frame3y=600,450
frame3_rect=frame3.get_rect(topleft=(frame3x, frame3y))

frame4size=1
img = pygame.image.load("image/frame6.png").convert()
w, h = img.get_size()
frame4 = pygame.Surface((w, h), pygame.SRCALPHA)
frame5 = pygame.Surface((w, h), pygame.SRCALPHA)
for y in range(h):
    for x in range(w):
        r, g, b, a = img.get_at((x, y))
        blackness = 255-(r + g + b)/3
        if blackness<0:blackness=0
        alpha = int(255-blackness)
        r,g,b=r*1.5,g*1.5,b*1.5
        if r>255:r=255
        if g>255:g=255
        if b>255:b=255
        frame4.set_at((x, y), (r,g,b, alpha))
        r,g,b=r*1.5,g*1.5,b*1.5
        if r>255:r=255
        if g>255:g=255
        if b>255:b=255
        frame5.set_at((x, y), (r,g,b, alpha))
# frame4.set_alpha(220)
frame4 = pygame.transform.scale_by(frame4,frame4size)
frame5 = pygame.transform.scale_by(frame5,frame4size)
frame4x,frame4y=650,600
frame4_rect=frame4.get_rect(topleft=(frame4x, frame4y))

#矢印
arrowsize=1
arrow=[]
for i in range(4):
    arrow.append(pygame.image.load(f"image/arrow{i+1}.png").convert())
    arrow[i] = pygame.transform.scale_by(arrow[i],arrowsize)
    arrow[i].set_colorkey((255, 255, 255))
    arrow[i].set_alpha(255)
for i in range(4):
    arrow.append(pygame.transform.flip(arrow[i], True, False))
arrowx1,arrowx2,arrowy,arrowy_help,arrowy_distance=700,1000,200,650,100
arrow_rect1=[arrow[4].get_rect(topleft=(arrowx1, arrowy)),arrow[4].get_rect(topleft=(arrowx1, arrowy+arrowy_distance)),arrow[4].get_rect(topleft=(arrowx1, arrowy_help))]
arrow_rect2=[arrow[0].get_rect(topleft=(arrowx2, arrowy)),arrow[0].get_rect(topleft=(arrowx2, arrowy+arrowy_distance)),arrow[0].get_rect(topleft=(arrowx2, arrowy_help))]
arrow_push1=[0,0]
arrow_push2=[0,0]

def draw_arrow(x,x2,y,arrow_push1,arrow_rect1,arrow_push2,arrow_rect2):
    a=0
    if arrow_push1>0:
        a+=1
    if arrow_rect1.collidepoint(pygame.mouse.get_pos()):
        a+=2
    value.screen.blit(arrow[4+a], (x,y))
    
    a=0
    if arrow_push2>0:
        a+=1
    if arrow_rect2.collidepoint(pygame.mouse.get_pos()):
        a+=2
    value.screen.blit(arrow[a], (x2,y))

#使えないかも下線
linesize=1
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
            line.set_at((x, y), (255,b,255))
        else:
            line.set_at((x, y), (255, 0, 255, alpha))
line = pygame.transform.scale_by(line,linesize)
linex,liney=550,620

#枚数
maisu=[]
j=0
for i in value.handsize_change:
    maisu.append(pygame.image.load(f"image/{i}.png").convert())
    maisu[j] = pygame.transform.scale_by(maisu[j],arrowsize)
    maisu[j].set_colorkey((255, 255, 255))
    j+=1
Startinghandsize_size=j
maisux=arrowx1+100
maisuy=arrowy-10

#先手
sente=[]
sente.append(pygame.image.load("image/rundom.png").convert())
sente.append(pygame.image.load("image/maru.png").convert())
sente.append(pygame.image.load("image/batu.png").convert())
for i in range(3):
    sente[i] = pygame.transform.scale_by(sente[i],arrowsize)
    sente[i].set_colorkey((255, 255, 255))
firstplayer_size=3
sentex=arrowx1+100
sentey=arrowy-10+arrowy_distance

#デッキ
deck=[]
for i in range(5):
    deck.append(pygame.image.load(f"image/deck{i}.png").convert())
    deck[i] = pygame.transform.scale_by(deck[i],arrowsize*2)
    deck[i].set_colorkey((255, 255, 255))
for i in range(5):
    deck.append(pygame.image.load(f"image/deck{i}.png").convert())

for i in range(5,10):
    for x in range(deck[i].get_width()):
        for y in range(deck[i].get_height()):
            r, g, b, a = deck[i].get_at((x, y))
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)  # NTSC係数でグレースケール
            deck[i].set_at((x, y), (gray, gray, gray, a))
    
    deck[i] = pygame.transform.scale_by(deck[i],arrowsize*2)
    deck[i].set_colorkey((255, 255, 255))

decks_size=5
deckx=arrowx1+50
deckx2=arrowx1+200
decky=arrowy-10+arrowy_distance*2
deck_rect=deck[0].get_rect(topleft=(deckx,decky))
deck_rect2=deck[0].get_rect(topleft=(deckx2,decky))

#作成デッキ
make_deckx=[550,650,750,850]
make_decky=300
make_deck_rect=[]
for i in range(4):
    make_deck_rect.append(deck[0].get_rect(topleft=(make_deckx[i],make_decky)))
#変更デッキ
change_deckx=[630,710,790,870]
change_deckx2=[x + 150 for x in change_deckx]
change_decky=460
change_deck_rect=[]
for i in range(4):
    change_deck_rect.append(deck[0].get_rect(topleft=(change_deckx[i],change_decky)))
for i in range(4):
    change_deck_rect.append(deck[0].get_rect(topleft=(change_deckx2[i],change_decky)))
change = pygame.image.load("image/change.png").convert()
change.set_colorkey((255, 255, 255))
changex=deckx-10
changex2=deckx2-10
changey=decky-20


deck_push=0
deck_push2=0
mouse_check_deck_time=0
mouse_check_deck_time2=0
mouse_check_deck2=0
mouse_check_deck2=0
mouse_check_change_deck=[0,0,0,0]
mouse_check_change_deck_time=[0,0,0,0]
deck_change=False
deck_change2=False

#ありなし
ivent_size=0.6
ivent_switch=[]
ivent_switch.append(pygame.image.load("image/no.png").convert())
ivent_switch.append(pygame.image.load("image/yes.png").convert())
ivent_switch.append(pygame.image.load("image/no2.png").convert())
ivent_switch.append(pygame.image.load("image/yes2.png").convert())
for i in range(4):
    ivent_switch[i].set_colorkey((255, 255, 255))
    ivent_switch[i] = pygame.transform.scale_by(ivent_switch[i],ivent_size)
ivent_x,ivent_y=800,500
ivent_rect=ivent_switch[0].get_rect(topleft=(ivent_x,ivent_y))

#ゲームスタート
gamessize=1.5
games = pygame.image.load("image/gamestart1.png").convert()
games = pygame.transform.scale_by(games,gamessize)
games.set_colorkey((255, 255, 255))
games2 = pygame.image.load("image/gamestart2.png").convert()
games2 = pygame.transform.scale_by(games2,gamessize)
games2.set_colorkey((255, 255, 255))
gamesx,gamesy=600,600
games_rect=games.get_rect(topleft=(gamesx,gamesy))

setumei=[]
for i in range(4):
    setumei.append(pygame.image.load(f"image/1{i+1}.png").convert())
    setumei[i] = pygame.transform.scale_by(setumei[i],1)
    setumei[i].set_colorkey((255, 255, 255))

#四角
sq=pygame.image.load("image/sq.png").convert()
sq=pygame.transform.scale_by(sq,1.2)
sq.set_colorkey((255, 255, 255))

def draw_sq(i,dy, alpha):
    sq2 = sq.convert_alpha()
    sq2.set_alpha(alpha)
    value.screen.blit(sq2, (make_deckx[i],make_decky+dy))










font =pygame.font.SysFont("Meiryo UI", 36)

#文字
menu_text_list=["  ひとりで","  ふたりで","   ヘルプ","デッキ編成"]
tab=len(menu_text_list)
menu_text=[]
for i in range (len(menu_text_list)):
    menu_text.append(font.render(menu_text_list[i], True, (255, 255, 255)))

back_text = font.render("戻る", True, (255, 255, 255))

menu2_text_list=["初期手札","先手","デッキ","イベント"]
tab2=len(menu2_text_list)
menu2_text=[]
for i in range (len(menu2_text_list)):
    menu2_text.append(font.render(menu2_text_list[i], True, (255,255,255)))

menu2x,menu2y,menu2y_distance=500,200,100
sonotax=menu2x+350
sonota_rect= menu2_text[len(menu2_text_list)-1].get_rect(topleft=(sonotax,menu2y+menu2y_distance*len(menu2_text)-1))

deckselect_text = font.render("編集するデッキを選択してください", True, (255, 255, 255))
deckselect_textx,deckselect_texty=500,200

page_textx=900

#フレームムーブ
frame_move=[0]*(tab+1)
frame_move_max=3
frame_move_s=10

#ムーブトゥ
moveto1=0
moveto2=0
move_time=8
move_distance=900
framemove_distance=-0.18

ka=0
def menu():
    global moveto1
    global moveto2
    global arrow_push1
    global arrow_push2

    #壁紙
    value.screen.blit(pekin2, (widhe_skew2,0))
    
    x1=moveto1*move_distance*(framemove_distance)/move_time
    value.screen.blit(pekin, (x1,0))

    
    x2=(move_time-moveto1)*move_distance/move_time
    value.screen.blit(pekin3, (x2,0))
    
    if value.play_number<2:
        value.screen.blit(frame2, (frame2x,frame2y-x2))

    #フレーム
    frame_rect=[]
    for i in range(tab):
        x ,y= framex + i * frame_distance / 2.8 + frame_move[i]*frame_move_s+moveto1*move_distance*(framemove_distance)/move_time, framey + i * frame_distance
        value.screen.blit(frame, (x,y))
        value.screen.blit(menu_text[i], (x+90,y+15))
        frame_rect.append(frame.get_rect(topleft=(x, y)))
        if frame_rect[i].collidepoint(pygame.mouse.get_pos()):
            if frame_move[i]<frame_move_max:
                frame_move[i]+=1
            value.screen.blit(setumei[i], (600,200))
        else:
            if frame_move[i]>0:
                frame_move[i]-=1

    #もどる
    x,y=backx+frame_move[tab]*frame_move_s,backy
    value.screen.blit(frame, (x,y))
    value.screen.blit(back_text, (backx+200,backy+15))
    frame_rect.append(frame.get_rect(topleft=(x,y)))
    if frame_rect[tab].collidepoint(pygame.mouse.get_pos()):
        if frame_move[tab]<frame_move_max:
            frame_move[tab]+=1
    else:
        if frame_move[tab]>0:
            frame_move[tab]-=1

    #せってい
    
    if value.play_number<2:

        for i in range(len(menu2_text)):
            value.screen.blit(menu2_text[i], (menu2x,menu2y+menu2y_distance*i-x2))
        draw_arrow(arrowx1,arrowx2,arrowy-x2,arrow_push1[0],arrow_rect1[0],arrow_push2[0],arrow_rect2[0])
        draw_arrow(arrowx1,arrowx2,arrowy-x2+arrowy_distance,arrow_push1[1],arrow_rect1[1],arrow_push2[1],arrow_rect2[1])
        
        value.screen.blit(maisu[value.Startinghandsize], (maisux,maisuy-x2))
        value.screen.blit(sente[value.firstplayer], (sentex,sentey-x2))
        
        value.screen.blit(sente[1], (deckx-100,decky-x2))
        value.screen.blit(sente[2], (deckx2-100,decky-x2))

        value.screen.blit(ivent_switch[value.event_switch], (ivent_x,ivent_y-x2))

        value.screen.blit(deck[value.decks], (deckx,decky-x2))
        value.screen.blit(deck[value.decks], (deckx2,decky-x2))
        if games_rect.collidepoint(pygame.mouse.get_pos()):
            value.screen.blit(games2, (gamesx,gamesy-x2))
        else:
            value.screen.blit(games, (gamesx,gamesy-x2))
    #説明
    elif value.play_number==2:
        help.help(0,0,-x2)
        draw_arrow(arrowx1,arrowx2,arrowy_help-x2,arrow_push1[0],arrow_rect1[2],arrow_push2[0],arrow_rect2[2])
        page_text = font.render(f"{value.help_page+1}/{maxpage+1}", True, (255, 255, 255))
        text_width = page_text.get_width()
        value.screen.blit(page_text,(page_textx-text_width,arrowy_help-x2))
    #デッキ作成

    elif value.play_number==3:
        value.screen.blit(deckselect_text, (deckselect_textx,deckselect_texty-x2))
        draw_sq(value.make_deck_ka,-x2,90+40*math.sin(value.t/20))
        for i in range(1,4):
            if make_deck_rect[i].collidepoint(pygame.mouse.get_pos()):
                if mouse_check_change_deck[i]==0:
                    mouse_check_change_deck_time[i]=10
                mouse_check_change_deck[i]=1
            else:
                mouse_check_change_deck[i]=0
            value.screen.blit(deck[value.deckcolor[i]], (make_deckx[i]+math.sin(mouse_check_change_deck_time[i]*math.pi/2.5)*mouse_check_change_deck_time[i]/5,make_decky-x2))
        if frame4_rect.collidepoint(pygame.mouse.get_pos()):
            value.screen.blit(frame5,(frame4x,frame4y-x2))
        else:
            value.screen.blit(frame4,(frame4x,frame4y-x2))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i in range(tab+1):
                if frame_rect[i].collidepoint(pygame.mouse.get_pos()):
                    match(i):
                        case 4:
                            value.fade_out = True
                            value.fade_in = False
                            value.nextstep=-1
                        case (0 | 1 | 2 | 3):
                            value.menustep=1
                            moveto2=move_time+moveto1
                            value.play_number=i


                            
                    
    if value.fade_out:
        value.fade_alpha += 20  # フェード速度（調整可）
        if value.fade_alpha >= 255:
            value.fade_alpha = 255
            if value.nextstep==-1:
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

    if moveto1>0:moveto1-=1
    for i in range (2):
        if arrow_push1[i]>0:arrow_push1[i]-=1
        if arrow_push2[i]>0:arrow_push2[i]-=1

    value.t=pygame.time.get_ticks()
    pygame.display.update()

    pygame.time.delay(30)






def menu2():
    global moveto1
    global moveto2
    global arrow_push1
    global arrow_push2
    global deck_push
    global mouse_check_deck
    global mouse_check_deck_time
    global deck_change
    global deck_push2
    global mouse_check_deck2
    global mouse_check_deck_time2
    global deck_change2
    global mouse_check_change_deck_time
    global mouse_check_change_deck
    #壁紙
    value.screen.blit(pekin2, (widhe_skew2,0))
    
    if moveto1>0:
        x1=moveto1*move_distance*(framemove_distance)/move_time
    else:
        if move_time-moveto2>0:
            x1=(move_time-moveto2)*move_distance*(framemove_distance)/move_time
        else:
            x1=0
    value.screen.blit(pekin, (x1,0))

    if moveto1>0:
        x2=(move_time-moveto1)*move_distance/move_time
    else:
        x2=moveto2*move_distance/move_time
    
    value.screen.blit(pekin3, (x2,0))
    
    if value.play_number<2:
        value.screen.blit(frame2, (frame2x,frame2y-x2))

    #フレーム
    frame_rect=[]
    for i in range(tab):
        if moveto1>0:
            x ,y= framex + i * frame_distance / 2.8 + frame_move[i]*frame_move_s+moveto1*move_distance*(framemove_distance)/move_time, framey + i * frame_distance
        else:
            x ,y= framex + i * frame_distance / 2.8 + frame_move[i]*frame_move_s+(move_time-moveto2)*move_distance*(framemove_distance)/move_time, framey + i * frame_distance
        
        value.screen.blit(frame, (x,y))
        value.screen.blit(menu_text[i], (x+90,y+15))
        frame_rect.append(frame.get_rect(topleft=(x, y)))
        if value.play_number==i:
            if frame_move[i]<frame_move_max:
                frame_move[i]+=1
        else:
            if frame_move[i]>0:
                frame_move[i]-=1

    
    x,y=backx+frame_move[tab]*frame_move_s,backy

    #戻る
    value.screen.blit(frame, (x,y))
    value.screen.blit(back_text, (backx+200,backy+15))
    frame_rect.append(frame.get_rect(topleft=(x,y)))
    if frame_rect[tab].collidepoint(pygame.mouse.get_pos()):
        if frame_move[tab]<frame_move_max:
            frame_move[tab]+=1
    else:
        if frame_move[tab]>0:
            frame_move[tab]-=1



    #せってい
    if value.play_number<2:
    
        for i in range(len(menu2_text)):
            value.screen.blit(menu2_text[i], (menu2x,menu2y+menu2y_distance*i-x2))
        draw_arrow(arrowx1,arrowx2,arrowy-x2,arrow_push1[0],arrow_rect1[0],arrow_push2[0],arrow_rect2[0])
        draw_arrow(arrowx1,arrowx2,arrowy-x2+arrowy_distance,arrow_push1[1],arrow_rect1[1],arrow_push2[1],arrow_rect2[1])
        
        value.screen.blit(maisu[value.Startinghandsize], (maisux,maisuy-x2))
        value.screen.blit(sente[value.firstplayer], (sentex,sentey-x2))

        if ivent_rect.collidepoint(pygame.mouse.get_pos()):
            value.screen.blit(ivent_switch[value.event_switch+2], (ivent_x,ivent_y-x2))
        else:
            value.screen.blit(ivent_switch[value.event_switch], (ivent_x,ivent_y-x2))



        value.screen.blit(sente[1], (deckx-100,decky-x2))
        value.screen.blit(sente[2], (deckx2-100,decky-x2))


        if deck_rect.collidepoint(pygame.mouse.get_pos()):
            if mouse_check_deck==0:
                mouse_check_deck_time=10
            mouse_check_deck=1
            value.screen.blit(change, (changex,changey))
        else:
            mouse_check_deck=0
        
        if deck_rect2.collidepoint(pygame.mouse.get_pos()):
            if mouse_check_deck2==0:
                mouse_check_deck_time2=10
            mouse_check_deck2=1
            value.screen.blit(change, (changex2,changey))
        else:
            mouse_check_deck2=0
        
        value.screen.blit(deck[value.deckcolor[value.decks]], (deckx+math.sin(mouse_check_deck_time*math.pi/2.5)*mouse_check_deck_time/5,decky-x2+(4-abs(2-deck_push)*2)))
        value.screen.blit(deck[value.deckcolor[value.decks2]], (deckx2+math.sin(mouse_check_deck_time2*math.pi/2.5)*mouse_check_deck_time2/5,decky-x2+(4-abs(2-deck_push2)*2)))
        
        if deck_change:
            value.screen.blit(frame3, (frame3x,frame3y))
            for i in range(4):
                if change_deck_rect[i].collidepoint(pygame.mouse.get_pos()) and len(value.deck[i])==20:
                    if mouse_check_change_deck[i]==0:
                        mouse_check_change_deck_time[i]=10
                    mouse_check_change_deck[i]=1
                else:
                    mouse_check_change_deck[i]=0
                if len(value.deck[i])==20:
                    value.screen.blit(deck[value.deckcolor[i]], (change_deckx[i]+math.sin(mouse_check_change_deck_time[i]*math.pi/2.5)*mouse_check_change_deck_time[i]/5,change_decky))
                else:
                    value.screen.blit(deck[value.deckcolor[i]+5], (change_deckx[i]+math.sin(mouse_check_change_deck_time[i]*math.pi/2.5)*mouse_check_change_deck_time[i]/5,change_decky))
        if deck_change2:
            value.screen.blit(frame3, (frame3x+150,frame3y))
            for i in range(4):
                if change_deck_rect[i+4].collidepoint(pygame.mouse.get_pos()) and len(value.deck[i])==20:
                    if mouse_check_change_deck[i]==0:
                        mouse_check_change_deck_time[i]=10
                    mouse_check_change_deck[i]=1
                else:
                    mouse_check_change_deck[i]=0
                if len(value.deck[i])==20:
                    value.screen.blit(deck[value.deckcolor[i]], (change_deckx2[i]+math.sin(mouse_check_change_deck_time[i]*math.pi/2.5)*mouse_check_change_deck_time[i]/5,change_decky))
                else:
                    value.screen.blit(deck[value.deckcolor[i]+5], (change_deckx2[i]+math.sin(mouse_check_change_deck_time[i]*math.pi/2.5)*mouse_check_change_deck_time[i]/5,change_decky))

        if games_rect.collidepoint(pygame.mouse.get_pos()):
            value.screen.blit(games2, (gamesx,gamesy-x2))
        else:
            value.screen.blit(games, (gamesx,gamesy-x2))

    #説明
    elif value.play_number==2:
        help.help(value.help_page,0,-x2)
        draw_arrow(arrowx1,arrowx2,arrowy_help-x2,arrow_push1[0],arrow_rect1[2],arrow_push2[0],arrow_rect2[2])
        
        page_text = font.render(f"{value.help_page+1}/{maxpage+1}", True, (255, 255, 255))
        text_width = page_text.get_width()
        value.screen.blit(page_text,(page_textx-text_width,arrowy_help-x2))
    
    #デッキ作成
    elif value.play_number==3:
        
        value.screen.blit(deckselect_text, (deckselect_textx,deckselect_texty-x2))
        draw_sq(value.make_deck_ka,-x2,90+40*math.sin(value.t/40))
        for i in range(1,4):
            if make_deck_rect[i].collidepoint(pygame.mouse.get_pos()):
                if mouse_check_change_deck[i]==0:
                    mouse_check_change_deck_time[i]=10
                mouse_check_change_deck[i]=1
            else:
                mouse_check_change_deck[i]=0
            value.screen.blit(deck[value.deckcolor[i]], (make_deckx[i]+math.sin(mouse_check_change_deck_time[i]*math.pi/2.5)*mouse_check_change_deck_time[i]/5,make_decky-x2))
        if frame4_rect.collidepoint(pygame.mouse.get_pos()):
            value.screen.blit(frame5,(frame4x,frame4y-x2))
        else:
            value.screen.blit(frame4,(frame4x,frame4y-x2))



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if value.play_number<2:
                if deck_change:
                    for i in range(4):
                        if change_deck_rect[i].collidepoint(pygame.mouse.get_pos()) and len(value.deck[i])==20:
                            value.decks=i
                            deck_change=False
                    if not frame3_rect.collidepoint(pygame.mouse.get_pos()):
                        deck_change=False
                        deck_change2=False
                elif deck_change2:
                    for i in range(4):
                        if change_deck_rect[i+4].collidepoint(pygame.mouse.get_pos()) and len(value.deck[i])==20:
                            value.decks2=i
                            deck_change2=False
                    if not frame3_rect.collidepoint(pygame.mouse.get_pos()):
                        deck_change=False
                        deck_change2=False
                else:
                    for i in range(tab+1):
                        if frame_rect[i].collidepoint(pygame.mouse.get_pos()):
                            match(i):
                                case 4:
                                    value.menustep=0
                                    moveto1=move_time-moveto2
                                case _:
                                    pass
                    if arrow_rect1[0].collidepoint(pygame.mouse.get_pos()):
                        arrow_push1[0]=5
                        if value.Startinghandsize>0:value.Startinghandsize-=1
                    if arrow_rect2[0].collidepoint(pygame.mouse.get_pos()):
                        arrow_push2[0]=5
                        if value.Startinghandsize<Startinghandsize_size-1:value.Startinghandsize+=1
                    if arrow_rect1[1].collidepoint(pygame.mouse.get_pos()):
                        arrow_push1[1]=5
                        if value.firstplayer>0:value.firstplayer-=1
                    if arrow_rect2[1].collidepoint(pygame.mouse.get_pos()):
                        arrow_push2[1]=5
                        if value.firstplayer<firstplayer_size-1:value.firstplayer+=1
                    if sonota_rect.collidepoint(pygame.mouse.get_pos()):
                        pass
                    if games_rect.collidepoint(pygame.mouse.get_pos()):
                        value.fade_out = True
                        value.fade_in = False
                        value.nextstep=3
                    
                    if deck_rect.collidepoint(pygame.mouse.get_pos()):
                        deck_push=4
                        mouse_check_deck_time=0
                        deck_change=True
                    elif deck_rect2.collidepoint(pygame.mouse.get_pos()):
                        deck_push2=4
                        mouse_check_deck_time2=0
                        deck_change2=True
                    if ivent_rect.collidepoint(pygame.mouse.get_pos()):
                        value.event_switch=1-value.event_switch
            elif value.play_number==2:
                for i in range(tab+1):
                    if frame_rect[i].collidepoint(pygame.mouse.get_pos()):
                        match(i):
                            case 4:
                                value.menustep=0
                                moveto1=move_time-moveto2
                            case _:
                                pass
                if arrow_rect1[2].collidepoint(pygame.mouse.get_pos()):
                    arrow_push1[0]=5
                    if value.help_page>0:value.help_page-=1
                if arrow_rect2[2].collidepoint(pygame.mouse.get_pos()):
                    arrow_push2[0]=5
                    if value.help_page<maxpage:value.help_page+=1


            elif value.play_number==3:
                for i in range(tab+1):
                    if frame_rect[i].collidepoint(pygame.mouse.get_pos()):
                        match(i):
                            case 4:
                                value.menustep=0
                                moveto1=move_time-moveto2
                            case _:
                                pass
                for i in range(4):
                        if make_deck_rect[i].collidepoint(pygame.mouse.get_pos()):
                            value.make_deck_ka=i
                if frame4_rect.collidepoint(pygame.mouse.get_pos()):
                    value.fade_out=True
                    value.fade_in=False
                    value.nextstep=2

                            
                    
    if value.fade_out:
        value.fade_alpha += 20  # フェード速度（調整可）
        if value.fade_alpha >= 255:
            value.fade_alpha = 255
            if value.nextstep==3:
                value.step=4
                value.fade_out = False
                value.fade_in = True
            if value.nextstep==2:
                value.step=2
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

    if moveto1>0:moveto1-=1
    if moveto2>0:moveto2-=1
    for i in range (2):
        if arrow_push1[i]>0:arrow_push1[i]-=1
        if arrow_push2[i]>0:arrow_push2[i]-=1
    if deck_push>0:deck_push-=1
    if mouse_check_deck_time>0:mouse_check_deck_time-=1
    if mouse_check_deck_time2>0:mouse_check_deck_time2-=1
    for i in range(4):
        if mouse_check_change_deck_time[i]>0:mouse_check_change_deck_time[i]-=1
    

    value.t=pygame.time.get_ticks()
    pygame.display.update()

    pygame.time.delay(30)