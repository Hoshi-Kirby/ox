import pygame
import sys
import math

import value

pygame.init()

t=-1
collide=0

#壁紙
pekin = pygame.image.load("image/restrant.png").convert()
original_width, original_height = pekin.get_size()
pekin = pygame.transform.scale_by(pekin,value.WINDOW_HEIGHT/original_height)
width_skew=(value.WINDOW_WIDTH-original_width*value.WINDOW_HEIGHT/original_height)/2

black = pygame.image.load("image/leftwhite.png").convert()
black = pygame.transform.scale_by(black,2)
black.set_colorkey((255, 255, 255))
black.set_alpha(100)
blackx,blacky=0,0

#フレーム
frame3size=1
frame3 = pygame.image.load("image/frame3.png").convert()
frame3 = pygame.transform.scale_by(frame3,frame3size)
frame3.set_colorkey((255, 255, 255))
frame3.set_alpha(220)
frame3x,frame3y=1100,80
frame3= pygame.transform.rotate(frame3, 90)
frame3_rect=frame3.get_rect(topleft=(frame3x, frame3y))

frame1size=0.6
frame1 = pygame.image.load("image/frame1.png").convert()
frame1 = pygame.transform.scale_by(frame1,frame1size)
frame1.set_colorkey((255, 255, 255))
frame1.set_alpha(220)
frame1x,frame1y=-150,700
frame1x2=1080

back_frame=0
flont_frame=0

#結果
black_sq_size=2
black_sq = pygame.image.load("image/black_sq.png").convert()
black_sq.set_colorkey((255, 255, 255))
black_sq.set_alpha(140)
black_sq= pygame.transform.scale_by(black_sq,black_sq_size)
black_sqx,black_sqy=770,0
white_sq = pygame.image.load("image/white_sq.png").convert()
white_sq.set_colorkey((0,0,0))
white_sq= pygame.transform.scale_by(white_sq,black_sq_size)


 #もう一度
moresize=1.5
morename = pygame.image.load("image/more.png").convert()
morename = pygame.transform.scale_by(morename,moresize)
original_width_more, original_height_more = morename.get_size()
morename.set_colorkey((255, 255, 255))
more2name = pygame.image.load("image/more2.png").convert()
more2name = pygame.transform.scale_by(more2name,moresize)
more2name.set_colorkey((255, 255, 255))

morex=150
morey=700
more_rect = morename.get_rect(topleft=(morex,morey))

 #戻る
backsize=1.5
backname = pygame.image.load("image/backtomenu.png").convert()
backname = pygame.transform.scale_by(backname,backsize)
original_width_back, original_height_back = backname.get_size()
backname.set_colorkey((255, 255, 255))
back2name = pygame.image.load("image/backtomenu2.png").convert()
back2name = pygame.transform.scale_by(back2name,backsize)
back2name.set_colorkey((255, 255, 255))

backx=10
backy=700

#ox
tokensize=1.5
token=[]
token2=[]
token.append(pygame.image.load("image/maru.png").convert())
token.append(pygame.image.load("image/batu.png").convert())
token2.append(pygame.image.load("image/maru.png").convert())
token2.append(pygame.image.load("image/batu.png").convert())
for i in range(2):
    token[i] = pygame.transform.scale_by(token[i],tokensize)
    token[i].set_colorkey((255, 255, 255))

#detail
detail_image={}
for i in (11,12,13,21,22,23,24,25,31,32,33,41,42,43,44,45):
    detail_image[i]=pygame.image.load(f"image/detail{i}.png").convert_alpha()
    detail_image[i].set_colorkey((255, 255, 255))
detailx=990
detaily=200

#デッキ
deck_size=2
deck=[]
for i in range(5):
    deck.append(pygame.image.load(f"image/deck{i}.png").convert())
    deck[i] = pygame.transform.scale_by(deck[i],deck_size)
    deck[i].set_colorkey((255, 255, 255))
decks_size=5
deckx=1110
decky=70
deck_rect=deck[0].get_rect(topleft=(deckx,decky))
deck_change=False
deck_push=0

#変更デッキ
make_deckx=deckx
make_decky=[100,170,240,310,380]
make_deck_rect=[]
for i in range(5):
    make_deck_rect.append(deck[0].get_rect(topleft=(make_deckx,make_decky[i])))

mouse_check_deck=0
mouse_check_deck_time=0
mouse_check_make_deck=[0,0,0,0,0]
mouse_check_make_deck_time=[0,0,0,0,0]

#カード
all_cards_image={}
card_size=2
for i in (11,12,13,21,22,23,24,25,31,32,33,41,42,43,44,45):
    all_cards_image[i]=pygame.image.load(f"image/card{i // 10}-{i % 10}.png").convert()
    all_cards_image[i]=pygame.transform.scale_by(all_cards_image[i],card_size)

cards_select=-1

all_cards_bar={}
card_size=2
for i in (11,12,13,21,22,23,24,25,31,32,33,41,42,43,44,45):
    all_cards_bar[i]=pygame.image.load(f"image/card_{i // 10}-{i % 10}.png").convert_alpha()
    all_cards_bar[i]=pygame.transform.scale_by(all_cards_bar[i],card_size)
    for x in range(14):  # 左から7ピクセル
        for y in range(all_cards_bar[i].get_height()):
            color = all_cards_bar[i].get_at((x, y))
            if color.r == 255 and color.g == 255 and color.b == 255:
                all_cards_bar[i].set_at((x, y), (255, 255, 255, 0))  # 白を透明に



card_bar_x,card_bar_y=820,10
card_bar_distance=37


#コスト
cost_image=[]
for i in range(11):
    cost_image.append(pygame.image.load(f"image/cost{i}.png").convert())
    cost_image[i].set_colorkey((255, 255, 255))
    cost_image[i]=pygame.transform.scale_by(cost_image[i],card_size)
card_dcost_mode=False

#文字
font =pygame.font.SysFont("Meiryo UI", 36)

back_text = font.render("戻る", True, (255, 255, 255))
flont_text = font.render("保存", True, (255, 255, 255))

def detail(x,xx,yy):
    value.detail_check=True
    value.screen.blit(detail_image[x], (xx,yy))


def make():
    global t
    global deck_change
    global deck_push
    global mouse_check_deck
    global mouse_check_deck_time
    global mouse_check_make_deck
    global mouse_check_make_deck_time
    global cards_select
    global back_frame
    global flont_frame
    value.screen.blit(pekin, (width_skew,0))
    value.screen.blit(black, (blackx,blacky))
    value.screen.blit(black_sq, (black_sqx,black_sqy))

    collide=-1
    for i in range(len(value.deck[value.make_deck_ka])):
        card_bar_rect=all_cards_bar[11].get_rect(topleft=(card_bar_x,card_bar_y+card_bar_distance*i))
        if card_bar_rect.collidepoint(pygame.mouse.get_pos()) and collide==-1:
            collide=i
            detail(value.deck[value.make_deck_ka][i],detailx,detaily)
            value.screen.blit(all_cards_bar[value.deck[value.make_deck_ka][i]], (card_bar_x-10,card_bar_y+card_bar_distance*i))
            value.screen.blit(cost_image[value.cost[value.deck[value.make_deck_ka][i]]], (card_bar_x+2,card_bar_y+card_bar_distance*i))
        else:
            value.screen.blit(all_cards_bar[value.deck[value.make_deck_ka][i]], (card_bar_x,card_bar_y+card_bar_distance*i))
            value.screen.blit(cost_image[value.cost[value.deck[value.make_deck_ka][i]]], (card_bar_x+12,card_bar_y+card_bar_distance*i))

    value.screen.blit(white_sq, (black_sqx,black_sqy))

    #戻る　保存
    frame1_rect=frame1.get_rect(topleft=(frame1x+back_frame, frame1y))
    frame2_rect=frame1.get_rect(topleft=(frame1x2+flont_frame, frame1y))
    move=8
    if frame1_rect.collidepoint(pygame.mouse.get_pos()):
        back_frame+=move
        if back_frame>30:back_frame=30
    else:
        back_frame-=move
        if back_frame<0:back_frame=0
    if frame2_rect.collidepoint(pygame.mouse.get_pos()):
        flont_frame-=move
        if flont_frame<-30:flont_frame=-30
    else:
        flont_frame+=move
        if flont_frame>0:flont_frame=0
    value.screen.blit(frame1, (frame1x+back_frame,frame1y))
    value.screen.blit(frame1, (frame1x2+flont_frame,frame1y))
    
    value.screen.blit(back_text, (frame1x+200,frame1y+15))
    value.screen.blit(flont_text, (frame1x2+80,frame1y+15))

    #デッキカラー
    
    if deck_rect.collidepoint(pygame.mouse.get_pos()):
        if mouse_check_deck==0:
            mouse_check_deck_time=10
        mouse_check_deck=1
    else:
        mouse_check_deck=0

    value.screen.blit(deck[value.deckcolor[value.make_deck_ka]], (deckx+math.sin(mouse_check_deck_time*math.pi/2.5)*mouse_check_deck_time/5,decky+(4-abs(2-deck_push)*2)))

    if deck_change:
            value.screen.blit(frame3, (frame3x,frame3y))
            for i in range(5):
                if make_deck_rect[i].collidepoint(pygame.mouse.get_pos()):
                    if mouse_check_make_deck[i]==0:
                        mouse_check_make_deck_time[i]=10
                    mouse_check_make_deck[i]=1
                else:
                    mouse_check_make_deck[i]=0
                value.screen.blit(deck[i], (make_deckx+math.sin(mouse_check_make_deck_time[i]*math.pi/2.5)*mouse_check_make_deck_time[i]/5,make_decky[i]))

    #カード
    j=160
    cards_select=-1
    for i in range(3):
        value.screen.blit(all_cards_image[11+i],(50+140*i,50))
        value.screen.blit(cost_image[value.cost[11+i]],(50+140*i,50))
        cards_rect=all_cards_image[11].get_rect(topleft=(50+140*i,50))
        if cards_rect.collidepoint(pygame.mouse.get_pos()):
            cards_select=11+i
            detail(11+i,detailx,detaily)
    for i in range(5):
        value.screen.blit(all_cards_image[21+i],(50+140*i,50+j))
        value.screen.blit(cost_image[value.cost[21+i]],(50+140*i,50+j))
        cards_rect=all_cards_image[11].get_rect(topleft=(50+140*i,50+j))
        if cards_rect.collidepoint(pygame.mouse.get_pos()):
            cards_select=21+i
            detail(21+i,detailx,detaily)
    for i in range(3):
        value.screen.blit(all_cards_image[31+i],(50+140*i,50+j*2))
        value.screen.blit(cost_image[value.cost[31+i]],(50+140*i,50+j*2))
        cards_rect=all_cards_image[11].get_rect(topleft=(50+140*i,50+j*2))
        if cards_rect.collidepoint(pygame.mouse.get_pos()):
            cards_select=31+i
            detail(31+i,detailx,detaily)
    for i in range(5):
        value.screen.blit(all_cards_image[41+i],(50+140*i,50+j*3))
        value.screen.blit(cost_image[value.cost[41+i]],(50+140*i,50+j*3))
        cards_rect=all_cards_image[11].get_rect(topleft=(50+140*i,50+j*3))
        if cards_rect.collidepoint(pygame.mouse.get_pos()):
            cards_select=41+i
            detail(41+i,detailx,detaily)

    #event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if deck_change:
                    for i in range(5):
                        if make_deck_rect[i].collidepoint(pygame.mouse.get_pos()):
                            value.deckcolor[value.make_deck_ka]=i
                            deck_change=False
                    if not frame3_rect.collidepoint(pygame.mouse.get_pos()):
                        deck_change=False
            else:
                if deck_rect.collidepoint(pygame.mouse.get_pos()):
                    deck_push=4
                    mouse_check_deck_time=0
                    deck_change=True
                if frame1_rect.collidepoint(pygame.mouse.get_pos()):
                    value.nextstep=-1
                    value.fade_out=True
                    value.fade_in=False
                if frame2_rect.collidepoint(pygame.mouse.get_pos()):
                    value.nextstep=-1
                    value.fade_out=True
                    value.fade_in=False
                if collide>=0:
                    del value.deck[value.make_deck_ka][collide]
                if cards_select>=0 and len(value.deck[value.make_deck_ka])<20:
                    value.deck[value.make_deck_ka].append(cards_select)
                    value.deck[value.make_deck_ka].sort()



    



    if value.fade_out:
        value.fade_alpha += 20  # フェード速度（調整可）
        if value.fade_alpha >= 255:
            value.fade_alpha = 255
            if value.nextstep==-1:
                value.step=1
                value.fade_out=False
                value.fade_in=True

        value.fade_surface.set_alpha(value.fade_alpha)
        value.screen.blit(value.fade_surface, (0, 0))
    
    if value.fade_in:
        value.fade_alpha -= 20  # フェード速度（調整可）
        if value.fade_alpha <= 0:
            value.fade_alpha = 0
            value.fade_in = False
            t=0

        value.fade_surface.set_alpha(value.fade_alpha)
        value.screen.blit(value.fade_surface, (0, 0))

    if t>=0:t+=1
    if mouse_check_deck_time>0:mouse_check_deck_time-=1
    for i in range(5):
        if mouse_check_make_deck_time[i]>0:mouse_check_make_deck_time[i]-=1
    
    value.t=pygame.time.get_ticks()
    pygame.display.update()

    pygame.time.delay(30)