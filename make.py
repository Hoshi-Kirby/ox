import pygame
import sys
import math
import sqlite3
import pyperclip

import value
import save_load
import soundplay
pygame.init()

t=-1
collide=0
collide_first=[0]*100

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
frame1y3=600

frame7size=5
frame7 = pygame.image.load("image/frame7.png").convert()
frame7 = pygame.transform.scale_by(frame7,frame7size)
frame7.set_colorkey((255, 255, 255))
frame7.set_alpha(220)
frame7x,frame7y=325,250
f7w, f7h = frame7.get_size()
f7on=0
f7off=0

back_frame=0
flont_frame=0
code_frame=0

#コピーアイコン
copysize=2
copy = pygame.image.load("image/copy.png").convert()
copy = pygame.transform.scale_by(copy,copysize)
copyx,copyy=frame7x+400,frame7y+20
copy_rect=copy.get_rect(topleft=(copyx, copyy))
copydonesize=2
copydone = pygame.image.load("image/copydone.png").convert()
copydone = pygame.transform.scale_by(copydone,copydonesize)
copydone.set_colorkey((255, 255, 255))
copydonex,copydoney=frame7x+350,frame7y+60
#作成ボタン
makebuttonsize=5
makebutton = pygame.image.load("image/make.png").convert()
makebutton = pygame.transform.scale_by(makebutton,makebuttonsize)
makebutton.set_colorkey((255, 255, 255))
makebutton2 = pygame.image.load("image/make2.png").convert()
makebutton2 = pygame.transform.scale_by(makebutton2,makebuttonsize)
makebutton2.set_colorkey((255, 255, 255))
makex,makey=frame7x+100,frame7y+140
makebutton_rect=makebutton.get_rect(topleft=(makex, makey))

#×
closesize=5
close = pygame.image.load("image/close.png").convert()
close = pygame.transform.scale_by(close,closesize)
closex,closey=frame7x+600,frame7y+10
close_rect=close.get_rect(topleft=(closex,closey))
#作成
makedsize=4
maked = pygame.image.load("image/make_make.png").convert()
maked = pygame.transform.scale_by(maked,makedsize)
maked2 = pygame.image.load("image/make_make2.png").convert()
maked2 = pygame.transform.scale_by(maked2,makedsize)
makedx,makedy=frame7x+550,frame7y+220
maked_rect=maked.get_rect(topleft=(makedx,makedy))

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
    img = pygame.image.load(f"image/card{i // 10}-{i % 10}.png").convert()
    img = pygame.transform.scale_by(img, card_size)
    all_cards_image[i] = img

    gray_img = img.copy()
    for x in range(img.get_width()):
        for y in range(img.get_height()):
            r, g, b, a = img.get_at((x, y))
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)  # NTSC係数でグレースケール
            gray_img.set_at((x, y), (gray, gray, gray, a))
    

    # 白黒画像を +50 したキーで保存
    all_cards_image[i + 50] = gray_img


    


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

#デッキコード
deckcode_step=0
code_table=[
    ["s","x","a","m","i","v","t","f","z","l","q","o","c","d","g","u"],
    ["d","e","u","j","b","c","q","i","l","m","t","h","y","x","f","n"],
    ["f","g","y","k","q","u","c","h","v","e","p","d","j","z","i","m"],
    ["a","q","e","c","w","x","v","z","p","m","t","k","l","j","i","d"],
    ["i","a","e","x","r","t","n","l","h","b","k","v","z","o","m","j"],
    ["v","k","h","c","p","q","s","w","g","a","d","m","r","u","l","y"],
    ["f","k","x","a","t","q","h","i","o","v","j","y","p","l","u","b"],
    ["k","z","s","u","d","n","r","f","i","a","x","j","o","v","g","b"],
    ["f","q","d","p","b","o","u","l","t","c","n","z","w","a","v","s"],
    ["i","l","f","r","t","x","u","v","g","s","y","h","q","n","b","k"]
    ]
skill_list = [11,12,13,21,22,23,24,25,31,32,33,41,42,43,44,45]
pairs=[[11,12],[13,21],[22,23],[24,25],[31,32],[33,41],[42,43],[44,45]]
copydone_time=0
can_not_make_time=0
code_paste=""

#文字
font =pygame.font.SysFont("Meiryo UI", 36)
font2 =pygame.font.SysFont("Meiryo UI", 25)

back_text = font.render("戻る", True, (255, 255, 255))
flont_text = font.render("保存", True, (255, 255, 255))
code_text = font2.render("デッキコード", True, (255, 255, 255))
can_not_make_text = font2.render("クリップボードに正しいコードを入れてください", True, (255, 255, 255))

def detail(x,xx,yy):
    value.detail_check=True
    value.screen.blit(detail_image[x], (xx,yy))

def make_code(deck):
    if len(deck)!=20:
        return ""
    card={}
    for s in skill_list:
        card[s] = 0
    for i in range(20):
        card[deck[i]]+=1
    s2=[0]*8
    i=0
    for p in pairs:
        s10=card[p[0]]*5+card[p[1]]
        s2[i]=format(s10, '05b')
        i+=1
    code=""
    for i in range(5):
        s10_2=int(s2[0][i])+int(s2[1][i])*2+int(s2[2][i])*4+int(s2[3][i])*8+int(s2[4][i])*16+int(s2[5][i])*32+int(s2[6][i])*64+int(s2[7][i])*128
        s16=format(s10_2, '02x')
        s10_3=int(s16[0], 16)
        code+=code_table[i*2][s10_3]
        s10_3=int(s16[1], 16)
        code+=code_table[i*2+1][s10_3]
    return code
        

def make_deck(code):
    if len(code)!=10:
        return []
    s2=[0]*5
    for i in range(5):
        try:
            hi = code_table[2*i].index(code[2*i])
            lo = code_table[2*i+1].index(code[2*i+1])
            s10 = hi*16 + lo
            if s10 > 255:
                return []
            s2[i]=format(s10, '08b')
        except ValueError:
            return []
    s5=[0]*16
    sum=0
    for i in range(8):
        s10_2=int(s2[4][7-i])+int(s2[3][7-i])*2+int(s2[2][7-i])*4+int(s2[1][7-i])*8+int(s2[0][7-i])*16
        s5[2*i]=s10_2//5
        s5[2*i+1]=s10_2%5
        sum+=s10_2//5+s10_2%5
        if s5[2*i] > 4:
            return []

    if sum!=20:
        return[]
    deck={}
    for i in range(16):
        deck[skill_list[i]]=s5[i]
    return deck

def se_collide(i,n):
    global collide_first
    if collide_first[n]==1:
        soundplay.se_play(i)
        collide_first[n]=0


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
    global code_frame
    global collide_first
    global deckcode_step
    global code_code
    global code_code_text
    global copydone_time
    global code_paste
    global maked_deck
    global can_not_make_time
    global code_paste_text
    global f7on
    global f7off

    if value.t<8:
        x2=100*(8-value.t)
    else:
        x2=0

    value.screen.blit(pekin, (width_skew,0))
    value.screen.blit(black, (blackx-x2,blacky))
    value.screen.blit(black_sq, (black_sqx,black_sqy-x2))

    collide=-1
    for i in range(len(value.deck[value.make_deck_ka])):
        card_bar_rect=all_cards_bar[11].get_rect(topleft=(card_bar_x,card_bar_y+card_bar_distance*i))
        if card_bar_rect.collidepoint(pygame.mouse.get_pos()) and collide==-1 and deckcode_step==0:
            collide=i
            detail(value.deck[value.make_deck_ka][i],detailx,detaily)
            value.screen.blit(all_cards_bar[value.deck[value.make_deck_ka][i]], (card_bar_x-10,card_bar_y+card_bar_distance*i-x2))
            value.screen.blit(cost_image[value.cost[value.deck[value.make_deck_ka][i]]], (card_bar_x+2,card_bar_y+card_bar_distance*i-x2))
            se_collide(2,i)
        else:
            value.screen.blit(all_cards_bar[value.deck[value.make_deck_ka][i]], (card_bar_x,card_bar_y+card_bar_distance*i-x2))
            value.screen.blit(cost_image[value.cost[value.deck[value.make_deck_ka][i]]], (card_bar_x+12,card_bar_y+card_bar_distance*i-x2))
            collide_first[i]=1

    value.screen.blit(white_sq, (black_sqx,black_sqy-x2))

    #戻る　保存
    frame1_rect=frame1.get_rect(topleft=(frame1x+back_frame, frame1y))
    frame2_rect=frame1.get_rect(topleft=(frame1x2+flont_frame, frame1y))
    frame3_rect=frame1.get_rect(topleft=(frame1x2+code_frame, frame1y3))
    move=8
    if frame1_rect.collidepoint(pygame.mouse.get_pos()) and deckcode_step==0:
        back_frame+=move
        if back_frame>30:back_frame=30
        se_collide(2,50)
    else:
        back_frame-=move
        if back_frame<0:back_frame=0
        collide_first[50]=1
    if frame2_rect.collidepoint(pygame.mouse.get_pos()) and deckcode_step==0:
        flont_frame-=move
        if flont_frame<-30:flont_frame=-30
        se_collide(2,51)
    else:
        flont_frame+=move
        if flont_frame>0:flont_frame=0
        collide_first[51]=1
    if frame3_rect.collidepoint(pygame.mouse.get_pos()) and deckcode_step==0:
        code_frame-=move
        if code_frame<-30:code_frame=-30
        se_collide(2,52)
    else:
        code_frame+=move
        if code_frame>0:code_frame=0
        collide_first[52]=1
    value.screen.blit(frame1, (frame1x+back_frame,frame1y))
    value.screen.blit(frame1, (frame1x2+flont_frame,frame1y))
    value.screen.blit(frame1, (frame1x2+code_frame,frame1y3))
    
    value.screen.blit(back_text, (frame1x+200,frame1y+15))
    value.screen.blit(flont_text, (frame1x2+80,frame1y+15))
    value.screen.blit(code_text, (frame1x2+40,frame1y3+25))

    #デッキカラー
    
    if deck_rect.collidepoint(pygame.mouse.get_pos()) and deckcode_step==0:
        if mouse_check_deck==0:
            mouse_check_deck_time=10
        mouse_check_deck=1
        se_collide(2,21)
    else:
        mouse_check_deck=0
        collide_first[21]=1

    value.screen.blit(deck[value.deckcolor[value.make_deck_ka]], (deckx+math.sin(mouse_check_deck_time*math.pi/2.5)*mouse_check_deck_time/5,decky+(4-abs(2-deck_push)*2-x2)))

    if deck_change:
        value.screen.blit(frame3, (frame3x,frame3y))
        for i in range(5):
            if make_deck_rect[i].collidepoint(pygame.mouse.get_pos()):
                if mouse_check_make_deck[i]==0:
                    mouse_check_make_deck_time[i]=10
                mouse_check_make_deck[i]=1
                se_collide(2,22+i)
            else:
                mouse_check_make_deck[i]=0
                collide_first[22+i]=1
            value.screen.blit(deck[i], (make_deckx+math.sin(mouse_check_make_deck_time[i]*math.pi/2.5)*mouse_check_make_deck_time[i]/5,make_decky[i]))

    #カード
    j=160
    cards_select=-1
    for i in range(3):
        if 4>value.deck[value.make_deck_ka].count(11+i):
            value.screen.blit(all_cards_image[11+i],(50+140*i,50))
        else:
            value.screen.blit(all_cards_image[11+i+50],(50+140*i,50))
        value.screen.blit(cost_image[value.cost[11+i]],(50+140*i,50))
        cards_rect=all_cards_image[11].get_rect(topleft=(50+140*i,50))
        if cards_rect.collidepoint(pygame.mouse.get_pos()) and deckcode_step==0:
            cards_select=11+i
            detail(11+i,detailx,detaily)
            se_collide(2,30+i)
        else:
            collide_first[30+i]=1
    for i in range(5):
        if 4>value.deck[value.make_deck_ka].count(21+i):
            value.screen.blit(all_cards_image[21+i],(50+140*i,50+j))
        else:
            value.screen.blit(all_cards_image[21+i+50],(50+140*i,50+j))
        value.screen.blit(cost_image[value.cost[21+i]],(50+140*i,50+j))
        cards_rect=all_cards_image[11].get_rect(topleft=(50+140*i,50+j))
        if cards_rect.collidepoint(pygame.mouse.get_pos()) and deckcode_step==0:
            cards_select=21+i
            detail(21+i,detailx,detaily)
            se_collide(2,33+i)
        else:
            collide_first[33+i]=1
    for i in range(3):
        if 4>value.deck[value.make_deck_ka].count(31+i):
            value.screen.blit(all_cards_image[31+i],(50+140*i,50+j*2))
        else:
            value.screen.blit(all_cards_image[31+i+50],(50+140*i,50+j*2))
        value.screen.blit(cost_image[value.cost[31+i]],(50+140*i,50+j*2))
        cards_rect=all_cards_image[11].get_rect(topleft=(50+140*i,50+j*2))
        if cards_rect.collidepoint(pygame.mouse.get_pos()) and deckcode_step==0:
            cards_select=31+i
            detail(31+i,detailx,detaily)
            se_collide(2,38+i)
        else:
            collide_first[38+i]=1
    for i in range(5):
        if 4>value.deck[value.make_deck_ka].count(41+i):
            value.screen.blit(all_cards_image[41+i],(50+140*i,50+j*3))
        else:
            value.screen.blit(all_cards_image[41+i+50],(50+140*i,50+j*3))
        value.screen.blit(cost_image[value.cost[41+i]],(50+140*i,50+j*3))
        cards_rect=all_cards_image[11].get_rect(topleft=(50+140*i,50+j*3))
        if cards_rect.collidepoint(pygame.mouse.get_pos()) and deckcode_step==0:
            cards_select=41+i
            detail(41+i,detailx,detaily)
            se_collide(2,41+i)
        else:
            collide_first[41+i]=1


    if deckcode_step==1:
        if f7on>0:
            scale=5-f7on
        elif f7off>0:
            scale=f7off
        frame7_2 = pygame.transform.scale_by(frame7,(1,scale/5))
        value.screen.blit(frame7_2, (frame7x,frame7y+f7h/2*(5-scale)/5))
        if f7on==1:
            deckcode_step=2
        if f7off==1:
            deckcode_step=0
            
    if deckcode_step==2:
        value.screen.blit(frame7, (frame7x,frame7y))
        value.screen.blit(code_code_text, (frame7x+230,frame7y+25))
        value.screen.blit(copy, (copyx,copyy))
        if copydone_time>0:
            value.screen.blit(copydone, (copydonex,copydoney))
        if makebutton_rect.collidepoint(pygame.mouse.get_pos()):
            value.screen.blit(makebutton2, (makex,makey))
            se_collide(2,53)
        else:
            value.screen.blit(makebutton, (makex,makey))
            collide_first[53]=1
        
        value.screen.blit(close, (closex,closey))
        value.screen.blit(maked, (makedx,makedy))

        if code_paste!="":
            value.screen.blit(code_paste_text,(makex+130,makey+50))
            value.screen.blit(maked2, (makedx,makedy))
        else:
            value.screen.blit(maked, (makedx,makedy))

        if can_not_make_time>0:
            value.screen.blit(can_not_make_text,(makex-60,makey+50))

    #event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if deckcode_step==0:
                if deck_change:
                        for i in range(5):
                            if make_deck_rect[i].collidepoint(pygame.mouse.get_pos()):
                                value.deckcolor[value.make_deck_ka]=i
                                deck_change=False
                                soundplay.se_play(4)
                        if not frame3_rect.collidepoint(pygame.mouse.get_pos()):
                            deck_change=False
                else:
                    if deck_rect.collidepoint(pygame.mouse.get_pos()):
                        deck_push=4
                        mouse_check_deck_time=0
                        deck_change=True
                        soundplay.se_play(4)
                    if frame1_rect.collidepoint(pygame.mouse.get_pos()):
                        value.nextstep=-2
                        value.fade_out=True
                        value.fade_in=False
                        soundplay.se_play(3)
                    if frame2_rect.collidepoint(pygame.mouse.get_pos()):
                        value.nextstep=-1
                        value.fade_out=True
                        value.fade_in=False
                        save_load.save(value.make_deck_ka)
                        soundplay.se_play(5)
                    if frame3_rect.collidepoint(pygame.mouse.get_pos()):
                        deckcode_step=1
                        f7on=5
                        code_code=make_code(value.deck[value.make_deck_ka])
                        code_code_text = font2.render(code_code, True, (255, 255, 255))
                        soundplay.se_play(4)
                    if collide>=0:
                        del value.deck[value.make_deck_ka][collide]
                        soundplay.se_play(7)
                    if cards_select>=0 and len(value.deck[value.make_deck_ka])<20 and 4>value.deck[value.make_deck_ka].count(cards_select):
                        value.deck[value.make_deck_ka].append(cards_select)
                        value.deck[value.make_deck_ka].sort()
                        soundplay.se_play(7)
            elif deckcode_step==2:
                if copy_rect.collidepoint(pygame.mouse.get_pos()):
                    if code_code!="":
                        pyperclip.copy(code_code)
                        copydone_time=30
                elif makebutton_rect.collidepoint(pygame.mouse.get_pos()):
                    maked_deck={}
                    code_paste = pyperclip.paste()
                    maked_deck=make_deck(code_paste)
                    if len(maked_deck)!=0:
                        code_paste_text = font2.render(code_paste, True, (255, 255, 255))
                        soundplay.se_play(4)
                    else:
                        code_paste=""
                        can_not_make_time=30
                        soundplay.se_play(25)
                elif maked_rect.collidepoint(pygame.mouse.get_pos()) and code_paste!="":
                    value.deck[value.make_deck_ka]=[]
                    for skill in skill_list:
                        for i in range(maked_deck[skill]):
                            value.deck[value.make_deck_ka].append(skill)
                    code_paste=""
                    f7off=5
                    deckcode_step=1
                    soundplay.se_play(24)
                elif close_rect.collidepoint(pygame.mouse.get_pos()):
                    code_paste=""
                    f7off=5
                    deckcode_step=1
                    soundplay.se_play(4)



    



    if value.fade_out:
        value.fade_alpha += 20  # フェード速度（調整可）
        if value.fade_alpha >= 255:
            value.fade_alpha = 255
            if value.nextstep==-2:
                value.step=1
                value.fade_out=False
                value.fade_in=True
                value.deck[value.make_deck_ka]=value.hold_deck[:]
                value.deckcolor[value.make_deck_ka]=value.hold_color
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
    
    value.t+=1
    if copydone_time>0:copydone_time-=1
    if can_not_make_time>0:can_not_make_time-=1
    if f7on>0:f7on-=1
    if f7off>0:f7off-=1
    pygame.display.update()

    pygame.time.delay(30)