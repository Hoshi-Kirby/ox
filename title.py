import pygame
import sys
import math

import value

pygame.init()

#壁紙
pekin = pygame.image.load("image/city_scene.png").convert()
original_width, original_height = pekin.get_size()
pekin = pygame.transform.scale_by(pekin,value.WINDOW_HEIGHT/original_height)
width_skew=(value.WINDOW_WIDTH-original_width*value.WINDOW_HEIGHT/original_height)/2

 #はじめる
startsize=1
startname = pygame.image.load("image/start.png").convert()
startname = pygame.transform.scale_by(startname,startsize)
original_width_start, original_height_start = startname.get_size()
width_skew_start=value.WINDOW_WIDTH/2-original_width_start/2
startname.set_colorkey((255, 255, 255))
start2name = pygame.image.load("image/start2.png").convert()
start2name = pygame.transform.scale_by(start2name,startsize)
width_skew_start=value.WINDOW_WIDTH/2-original_width_start/2
start2name.set_colorkey((255, 255, 255))

starty=500
start_rect = startname.get_rect(topleft=(width_skew_start,starty))

 #おわる
endsize=1
endname = pygame.image.load("image/end.png").convert()
endname = pygame.transform.scale_by(endname,endsize)
original_width_end, original_height_end = endname.get_size()
width_skew_end=value.WINDOW_WIDTH/2-original_width_end/2
endname.set_colorkey((255, 255, 255))
end2name = pygame.image.load("image/end2.png").convert()
end2name = pygame.transform.scale_by(end2name,endsize)
width_skew_end=value.WINDOW_WIDTH/2-original_width_end/2
end2name.set_colorkey((255, 255, 255))

endy=650
end_rect = endname.get_rect(topleft=(width_skew_end,endy))

 #タイトル
titlesize=1.5
titlename = pygame.image.load("image/title.png").convert()
titlename = pygame.transform.scale_by(titlename,titlesize)
original_width_title, original_height_title = titlename.get_size()
width_skew_title=value.WINDOW_WIDTH/2-original_width_title/2
titlename.set_colorkey((255, 255, 255))
titley=50

  # グラデーション用Surfaceを作成
gradient = pygame.Surface((original_width_title, original_height_title), pygame.SRCALPHA)

for y in range(original_height_title):
    # 上が白、下が赤紫（例：RGB(255, 200, 255)）
    ratio = y / original_height_title
    r = int(255 * (1 - ratio) + 180 * ratio)
    g = int(230 * (1 - ratio) + 220 * ratio)
    b = int(180 * (1 - ratio) + 255 * ratio)
    pygame.draw.line(gradient, (r, g, b, 255), (0, y), (original_width_title, y))

  # マスクとして画像のアルファを使う
maskedtitle = titlename.copy()
maskedtitle = pygame.Surface((original_width_title, original_height_title), pygame.SRCALPHA)
for x in range(original_width_title):
    for y in range(original_height_title):
        pixel = titlename.get_at((x, y))
        if pixel[:3] != (255, 255, 255):  # 白以外
            grad_color = gradient.get_at((x, y))
            maskedtitle.set_at((x, y), grad_color)
        else:
            maskedtitle.set_at((x, y), (255, 255, 255, 0))  # 白は透明に








def title():
    value.screen.blit(pekin, (width_skew,0))
    value.screen.blit(maskedtitle, (width_skew_title,titley+math.sin(value.t/300)*10))
    if start_rect.collidepoint(pygame.mouse.get_pos()):
        value.screen.blit(start2name, (width_skew_start,starty))
    else:
        value.screen.blit(startname, (width_skew_start,starty))
    if end_rect.collidepoint(pygame.mouse.get_pos()):
        value.screen.blit(end2name, (width_skew_end,endy))
    else:
        value.screen.blit(endname, (width_skew_end,endy))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if end_rect.collidepoint(pygame.mouse.get_pos()):
                    value.fade_out = True
                    value.fade_in = False
                    value.nextstep=-1
                if start_rect.collidepoint(pygame.mouse.get_pos()):
                    value.fade_out = True
                    value.fade_in = False
                    value.nextstep=1

    



    if value.fade_out:
        value.fade_alpha += 20  # フェード速度（調整可）
        if value.fade_alpha >= 255:
            value.fade_alpha = 255
            if value.nextstep==-1:
                pygame.quit()
                sys.exit()
            if value.nextstep==1:
                value.step=1
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

    value.t=pygame.time.get_ticks()
    pygame.display.update()

    pygame.time.delay(30)