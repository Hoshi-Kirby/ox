import pygame
import sys
import value
import random
pygame.init()

#壁紙
pekin = pygame.image.load("image/neon_city.png").convert()
original_width, original_height = pekin.get_size()
pekin = pygame.transform.scale_by(pekin,value.WINDOW_HEIGHT/original_height)
widhe_skew=(value.WINDOW_WIDTH-original_width*value.WINDOW_HEIGHT/original_height)/2-2

#駒
tokensize=1
token=[]
token.append(pygame.image.load("image/maru.png").convert())
token.append(pygame.image.load("image/batu.png").convert())
for i in range(2):
    token[i] = pygame.transform.scale_by(token[i],tokensize)
    token[i].set_colorkey((255, 255, 255))

font =pygame.font.SysFont("Meiryo UI", 36)

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
            line.set_at((x, y), (255,b,255))
        else:
            line.set_at((x, y), (255, 0, 255, alpha))
line = pygame.transform.scale_by(line,linesize)
line_x=-100
line_y=-110

#文字
ready_text=font.render("Ready?", True, (255, 255, 255))
font_size_max=60
font_size=60
ready_time=240
ready_time2=100
start_text=font.render("Start!", True, (255, 255, 255))
start_time=180
start_time2=100

#text.get_rect(center=(295, 300))

#カード
all_cards_image={}
for i in (11,12,13,21,22,23,24,25,31,32,33,41,42,43,44,45):
    all_cards_image[i]=pygame.image.load(f"image/card{i // 10}-{i % 10}.png").convert()
    all_cards_image[i]=pygame.transform.scale_by(all_cards_image[i],2)

spacing = 120  # カード間のスペース
width=all_cards_image[11].get_width()




def draw_lines():
    for i in range(1, value.BOARD_ROWS):
        value.screen.blit(line, (value.OFFSET_X+line_x, value.OFFSET_Y + i * value.SQUARE_SIZE+line_y))
    for i in range(1, value.BOARD_COLS):
        value.screen.blit(pygame.transform.rotate(line, -90), (value.OFFSET_X + i * value.SQUARE_SIZE+line_y, value.OFFSET_Y+line_x))

def draw_token(row, col,ox):
    x = value.OFFSET_X + col * value.SQUARE_SIZE
    y = value.OFFSET_Y + row * value.SQUARE_SIZE
    margin = value.SQUARE_SIZE // 2  # 余白を調整

    value.screen.blit(token[ox], (x-margin,y))

def check_win(player):
    for row in value.board:
        if all(cell == player for cell in row):
            return True
    for col in range(value.BOARD_COLS):
        if all(value.board[row][col] == player for row in range(value.BOARD_ROWS)):
            return True
    if all(value.board[i][i] == player for i in range(value.BOARD_ROWS)):
        return True
    if all(value.board[i][value.BOARD_ROWS - 1 - i] == player for i in range(value.BOARD_ROWS)):
        return True
    return False

def handsadd(n,m):
    check=[0]*20
    for i in range(len(value.hands)):
        check[value.hands[i]]=1
    for i in range(m):
        a=random.randint(0,19-len(value.hands))
        addnum=0
        while check[addnum]==1:
            addnum+=1
        for j in range(a):
            addnum+=1
            while check[addnum]==1:
                addnum+=1
        value.hands.append(value.deck[n][addnum])
        


def gameb():
    global font_size
    value.screen.blit(pekin, (widhe_skew,0))
    draw_lines()
    for i in range(value.BOARD_COLS):
        for j in range(value.BOARD_ROWS):
            match value.board[i][j]:
                case (1|2):
                    draw_token(i,j,value.board[i][j]-1)
                case _:
                    pass
    
    if ready_time<value.t<ready_time+ready_time2:
        font_size=int((ready_time+ready_time2-value.t)*font_size_max/ready_time2)  # 毎フレーム1ずつ小さく
    if start_time+ready_time+ready_time2<value.t<start_time+start_time2+ready_time+ready_time2:
        font_size=int((start_time+start_time2-value.t+ready_time+ready_time2)*font_size_max/start_time2)
    font = pygame.font.SysFont("Meiryo UI", font_size)
    if value.t<ready_time+ready_time2:
        ready_text = font.render("Ready?", True, (255, 160, 160))
        value.screen.blit(ready_text, ready_text.get_rect(center=(639.5, 400)))
    elif value.t<start_time+start_time2+ready_time+ready_time2:
        start_text = font.render("Start!", True, (255, 160, 160))
        value.screen.blit(start_text, start_text.get_rect(center=(639.5, 400)))

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

    value.t+=1
    pygame.display.update()




def game():
    global card_rect
    value.screen.blit(pekin, (widhe_skew,0))
    draw_lines()
    for i in range(value.BOARD_COLS):
        for j in range(value.BOARD_ROWS):
            match value.board[i][j]:
                case (1|2):
                    draw_token(i,j,value.board[i][j]-1)
                case _:
                    pass
    
    j=0
    
    cardx,cardy = 639.5 - ((spacing * (len(value.hands) - 1)+width) / 2),630
    for i in value.hands:
        card_rect = all_cards_image[11].get_rect(topleft=(cardx + j * spacing, cardy))
        y = cardy - 10 if card_rect.collidepoint(pygame.mouse.get_pos()) else cardy
        value.screen.blit(all_cards_image[i], (cardx + j * spacing, y))
        j+=1



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not value.game_over:
            mouseX, mouseY = event.pos
            if value.OFFSET_X <= mouseX < value.OFFSET_X + value.BOARD_SIZE and value.OFFSET_Y <= mouseY < value.OFFSET_Y + value.BOARD_SIZE:
                clicked_row = (mouseY - value.OFFSET_Y) // value.SQUARE_SIZE
                clicked_col = (mouseX - value.OFFSET_X) // value.SQUARE_SIZE

                if value.board[clicked_row][clicked_col] == 0:
                    value.board[clicked_row][clicked_col] = value.player

                    if check_win(value.player):
                        draw_token(i,j,value.player-1)
                        print(f"value.player {value.player} wins!")
                        value.game_over = True

                    value.player = 2 if value.player == 1 else 1
                    

                    
    if value.fade_out:
        value.fade_alpha += 20  # フェード速度（調整可）
        if value.fade_alpha >= 255:
            value.fade_alpha = 255
            if value.nextstep==3:
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

        value.fade_surface.set_alpha(value.fade_alpha)
        value.screen.blit(value.fade_surface, (0, 0))

    value.t+=1
    pygame.display.update()