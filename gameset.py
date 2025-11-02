import pygame
import sys
import math

import value

pygame.init()

t=-1

#壁紙
pekin = pygame.image.load("image/neon_scene.png").convert()
original_width, original_height = pekin.get_size()
pekin = pygame.transform.scale_by(pekin,value.WINDOW_WIDTH/original_width)
height_skew=value.WINDOW_HEIGHT-original_height*value.WINDOW_WIDTH/original_width+30

black = pygame.image.load("image/leftblack.png").convert()
black.set_colorkey((255, 255, 255))
black.set_alpha(120)
blackx,blacky=-100,-450
#結果
result_size=1.5
result = pygame.image.load("image/result.png").convert()
result.set_colorkey((255, 255, 255))
result= pygame.transform.scale_by(result,result_size)
resultx,resulty=80,5


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

backx=860
backy=700
back_rect = backname.get_rect(topleft=(backx,backy))

 #勝者
winnersize=0.75
winnername = pygame.image.load("image/winner.png").convert()
winnername = pygame.transform.scale_by(winnername,winnersize)
original_width_winner, original_height_winner = winnername.get_size()
winnername.set_colorkey((255, 255, 255))
winnerx=500
winnery=170

winner_time=5
winner_time2=10
winner_time3=5

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
tokenx=755
tokeny=winnery+10






def gameset():
    global t
    value.screen.blit(pekin, (0,height_skew))
    value.screen.blit(black, (blackx,blacky))
    value.screen.blit(result, (resultx,resulty))


    if 0<t<winner_time:
        font_size=(1+0.2*(winner_time-t)/winner_time)
    elif t<winner_time2+winner_time:
        font_size=1
    elif t<winner_time3+winner_time2+winner_time:
        font_size=(1+0.2*(winner_time+winner_time2+winner_time3-t)/(winner_time+winner_time2+winner_time3))
    elif 0<t:
        font_size=1
    if 0<t:
        if t<winner_time+winner_time2:
            winnername2= pygame.transform.scale_by(winnername,font_size)
            rect =winnername2.get_rect(center=(winnerx, winnery))
            value.screen.blit(winnername2, rect)
        else:
            rect =winnername.get_rect(center=(winnerx, winnery))
            value.screen.blit(winnername, rect)
            token2[value.winner-1]= pygame.transform.scale_by(token[value.winner-1],font_size)
            rect =token2[value.winner-1].get_rect(center=(tokenx,tokeny))
            value.screen.blit(token2[value.winner-1], rect)


            if more_rect.collidepoint(pygame.mouse.get_pos()):
                value.screen.blit(more2name, (morex,morey))
            else:
                value.screen.blit(morename, (morex,morey))
            if back_rect.collidepoint(pygame.mouse.get_pos()):
                value.screen.blit(back2name, (backx,backy))
            else:
                value.screen.blit(backname, (backx,backy))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if winner_time2<=t:
                    if back_rect.collidepoint(pygame.mouse.get_pos()):
                        value.fade_out = True
                        value.fade_in = False
                        value.nextstep=-1
                    if more_rect.collidepoint(pygame.mouse.get_pos()):
                        value.fade_out = True
                        value.fade_in = False
                        value.nextstep=1

    



    if value.fade_out:
        value.fade_alpha += 20  # フェード速度（調整可）
        if value.fade_alpha >= 255:
            value.fade_alpha = 255
            t=-1
            if value.nextstep==-1:
                value.step=1
                value.fade_out = False
                value.fade_in = True
            if value.nextstep==1:
                value.step=4
                value.fade_out = False
                value.fade_in = True

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
    value.t=pygame.time.get_ticks()
    pygame.display.update()

    pygame.time.delay(30)