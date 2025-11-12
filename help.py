import pygame
import sys
import math

import value

pygame.init()

white=(255,255,255)

helppicture={}
for i in (1,1):
    helppicsize=0.5
    helppicture[i] = pygame.image.load(f"image/helppic{i}.png").convert()
    helppicture[i]= pygame.transform.scale_by(helppicture[i],helppicsize)
    helppicture[i].set_colorkey((0,0,0))


helptext=[]
helptext.append("このゲームは○×ゲームです。カードを駆使して自分のマークを縦、横、斜めのいずれかに揃えたら勝ちとなります。")



font =pygame.font.SysFont("Meiryo UI", 36)



#文字

#文章
def draw_text_wrapped(surface, text, font, color, rect, line_spacing=5):
    lines = []
    current_line = ""
    x_max = rect.width

    for char in text:
        test_line = current_line + char
        test_surface = font.render(test_line, False, color)
        if test_surface.get_width() > x_max:
            lines.append(current_line)
            current_line = char
        else:
            current_line = test_line
    lines.append(current_line)
    line_height = font.get_height()
    total_height = len(lines) * line_height + (len(lines) - 1) * line_spacing

    # 最初の行のY座標を調整
    y = 280 - total_height // 2

    for line in lines:
        rendered = font.render(line, False, color)
        surface.blit(rendered, (rect.left, y))
        y += rendered.get_height() + line_spacing
        if y > rect.bottom:
            break

#value.screen.blit(helppicture[1], (500,0))

def help(page,xx,yy):
    match page:
        case 0:
            x,y,wx,wy=500,200,700,500
            draw_text_wrapped(value.screen, helptext[0], font, white,pygame.Rect(x+xx,y+yy,wx,wy))