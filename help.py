import pygame
import sys
import math

import value

pygame.init()

white=(255,255,255)

helppicture={}
helppicsize=[1,0.46,0.6,0.4]
for i in (1,2,3):
    helppicture[i] = pygame.image.load(f"image/helppic{i}.png").convert()
    helppicture[i]= pygame.transform.scale_by(helppicture[i],helppicsize[i])
    helppicture[i].set_colorkey((0,0,0))


helptext=[]
helptext.append("このゲームはカードゲームと○×ゲームを組み合わせたゲームです。カードを駆使して自分のマークを縦、横、斜めのいずれかに揃えたら勝ちとなります。")
helptext.append("「ひとりで」と「ふたりで」はどちらも二人で遊ぶモードです。「デッキ編成」は自分で好きなデッキを編成して、ゲームで使うことができます。")
helptext.append("上の図がゲーム画面と名称です。")
helptext.append("上の図はこのゲームで使用するカードの図です。カードにはコストと属性がありますが、タイプ相性はないので属性は関係ないです。カードの効果は、ゲーム中のウィンドウに表示されます。")
helptext.append("自分のターンでは、まずカードを２枚引きます。（先攻１ターン目は引かない、後攻１ターン目は１枚のみ）使用するカードを選択し、使用するカードとは別にコストの数分のカードを山札に戻します。使用したカードも山札に戻ります。")
helptext.append("カードは１ターンに何枚も使用することができ、使用しないこともできます。")
helptext.append("ゲーム前の設定で「イベント」を「あり」にすると、ゲーム中に３～４ターンに一度共通で何かが起こります。何が起こるかは実際にやってみてください。")
helptext.append("イベントの効果は、ゲーム中に「イベントあり」や「次のイベントまであと◯ターン」の文字にカーソルを合わせると確認することができます。")


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
    y = rect.top

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
        case 1:
            x,y,wx,wy=500,200,700,500
            draw_text_wrapped(value.screen, helptext[1], font, white,pygame.Rect(x+xx,y+yy,wx,wy))
        case 2:
            x,y,wx,wy=500,500,700,500
            draw_text_wrapped(value.screen, helptext[2], font, white,pygame.Rect(x+xx,y+yy,wx,wy))
            value.screen.blit(helppicture[1], (380,-20))
        case 3:
            x,y,wx,wy=500,300,700,500
            draw_text_wrapped(value.screen, helptext[3], font, white,pygame.Rect(x+xx,y+yy,wx,wy))
            value.screen.blit(helppicture[2], (690,20))
        case 4:
            x,y,wx,wy=500,200,700,700
            draw_text_wrapped(value.screen, helptext[4], font, white,pygame.Rect(x+xx,y+yy,wx,wy))
        case 5:
            x,y,wx,wy=500,200,700,700
            draw_text_wrapped(value.screen, helptext[5], font, white,pygame.Rect(x+xx,y+yy,wx,wy))
        case 6:
            x,y,wx,wy=500,200,700,700
            draw_text_wrapped(value.screen, helptext[6], font, white,pygame.Rect(x+xx,y+yy,wx,wy))
        case 7:
            x,y,wx,wy=500,300,700,700
            draw_text_wrapped(value.screen, helptext[7], font, white,pygame.Rect(x+xx,y+yy,wx,wy))
            value.screen.blit(helppicture[3], (600,20))