import pygame
import sys
import value
import random
import skillcard
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

#説明
detail_image={}
for i in (11,12,13,21,22,23,24,25,31,32,33,41,42,43,44,45):
    detail_image[i]=pygame.image.load(f"image/detail{i}.png").convert_alpha()

#文字
ready_text=font.render("Ready?", True, (255, 255, 255))
font_size_max=200
font_size=60
ready_time=240
ready_time2=100
start_text=font.render("Start!", True, (255, 255, 255))
start_time=200
start_time2=100

#text.get_rect(center=(295, 300))

#カード
all_cards_image={}
for i in (11,12,13,21,22,23,24,25,31,32,33,41,42,43,44,45):
    all_cards_image[i]=pygame.image.load(f"image/card{i // 10}-{i % 10}.png").convert()
    all_cards_image[i]=pygame.transform.scale_by(all_cards_image[i],2)

spacing = 120  # カード間のスペース
width=all_cards_image[11].get_width()
cardx_move=0
cardx_move2=0
card_select=-1
skillcard=0


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

def handsadd(h,n,m):
    check=[0]*20
    if h==1:
        for i in range(len(value.hands)):
            check[value.hands[i]]=1
    elif h==2:
        for i in range(len(value.hands2)):
            check[value.hands2[i]]=1   
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
        
def detail(x):
    if x==11:
        pass

        

def gameb():
    global font_size
    global cardx_move
    global cardx_move2
    value.screen.blit(pekin, (widhe_skew,0))
    draw_lines()
    for i in range(value.BOARD_COLS):
        for j in range(value.BOARD_ROWS):
            match value.board[i][j]:
                case (1|2):
                    draw_token(i,j,value.board[i][j]-1)
                case _:
                    pass
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

    cardx,cardy,cardy2 = 639.5 - ((spacing * (len(value.hands) - 1)+width) / 2),630,10
    j=0
    x = cardx+cardx_move/10 * spacing
    x2 = cardx+cardx_move2/10 * spacing*20
    for i in value.hands:
        card_rect = all_cards_image[11].get_rect(topleft=(x + j * spacing, cardy))
        y = cardy - 10 if card_rect.collidepoint(pygame.mouse.get_pos()) else cardy
        if j==len(value.hands):
            value.screen.blit(all_cards_image[value.deck[value.decks][i]], (x2 + j * spacing, y))
        else:
            value.screen.blit(all_cards_image[value.deck[value.decks][i]], (x + j * spacing, y))
        j+=1
    j=0
    for i in value.hands2:
        card_rect = all_cards_image[11].get_rect(topleft=(x + j * spacing, cardy2))
        y = cardy2 + 10 if card_rect.collidepoint(pygame.mouse.get_pos()) else cardy2
        if j==len(value.hands2):
            value.screen.blit(all_cards_image[value.deck[value.decks2][i]], (x2 + j * spacing, y))
        else:
            value.screen.blit(all_cards_image[value.deck[value.decks2][i]], (x + j * spacing, y))
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
        if value.t>0 and value.handsize_change[value.Startinghandsize]>0 and (ready_time+ready_time2)*j/(value.handsize_change[value.Startinghandsize])<=value.t<(ready_time+ready_time2)*j/(value.handsize_change[value.Startinghandsize])+1:
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
    value.screen.blit(pekin, (widhe_skew,0))
    draw_lines()
    for i in range(value.BOARD_COLS):
        for j in range(value.BOARD_ROWS):
            match value.board[i][j]:
                case (1|2):
                    draw_token(i,j,value.board[i][j]-1)
                case _:
                    pass
    
    
    cardx,cardx2,cardy,cardy2 = 639.5 - ((spacing * (len(value.hands) - 1)+width) / 2), 639.5 - ((spacing * (len(value.hands2) - 1)+width) / 2),630,10
    j=0
    card_select=-1
    for i in value.hands:
        card_rect = all_cards_image[11].get_rect(topleft=(cardx + j * spacing, cardy))
        y = cardy - 10 if card_rect.collidepoint(pygame.mouse.get_pos()) else cardy
        value.screen.blit(all_cards_image[value.deck[value.decks][i]], (cardx + j * spacing, y))
        if card_rect.collidepoint(pygame.mouse.get_pos()):
            if value.player==1:
                card_select=i
            detail(all_cards_image[value.deck[value.decks][i]])
        j+=1
    j=0
    for i in value.hands2:
        card_rect = all_cards_image[11].get_rect(topleft=(cardx + j * spacing, cardy2))
        y = cardy2 + 10 if card_rect.collidepoint(pygame.mouse.get_pos()) else cardy2
        value.screen.blit(all_cards_image[value.deck[value.decks2][i]], (cardx2 + j * spacing, y))
        if value.player==1 and card_rect.collidepoint(pygame.mouse.get_pos()):
            card_select=i
        j+=1

    if turnend_rect.collidepoint(pygame.mouse.get_pos()):
        value.screen.blit(turnend2,(turnendx,turnendy))
    else:
        value.screen.blit(turnend,(turnendx,turnendy))


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
                if value.player==1:
                    skillcard=value.deck[value.decks][card_select]
                else:
                    skillcard=value.deck[value.decks2][card_select]

            # mouseX, mouseY = event.pos
            # if value.OFFSET_X <= mouseX < value.OFFSET_X + value.BOARD_SIZE and value.OFFSET_Y <= mouseY < value.OFFSET_Y + value.BOARD_SIZE:
            #     clicked_row = (mouseY - value.OFFSET_Y) // value.SQUARE_SIZE
            #     clicked_col = (mouseX - value.OFFSET_X) // value.SQUARE_SIZE
            #     if 0<=clicked_row<3 and 0<=clicked_col<3:
            #         if value.board[clicked_row][clicked_col] == 0:
            #             value.board[clicked_row][clicked_col] = value.player

            #             if check_win(value.player):
            #                 draw_token(i,j,value.player-1)
            #                 print(f"value.player {value.player} wins!")
            #                 value.game_over = True

            #             value.player = 2 if value.player == 1 else 1
                        
    if skillcard>0:
        pass
                    
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

def change():
    global font_size
    global cardx_move
    global cardx_move2
    value.screen.blit(pekin, (widhe_skew,0))
    draw_lines()
    for i in range(value.BOARD_COLS):
        for j in range(value.BOARD_ROWS):
            match value.board[i][j]:
                case (1|2):
                    draw_token(i,j,value.board[i][j]-1)
                case _:
                    pass
    
    #カード
    cardx,cardx2,cardy,cardy2 = 639.5 - ((spacing * (len(value.hands) - 1)+width) / 2),639.5 - ((spacing * (len(value.hands2) - 1)+width) / 2),630,10

    j=0
    x = cardx+cardx_move/10 * spacing
    x2 = cardx+cardx_move2/10 * spacing*20
    x3 = cardx2+cardx_move/10 * spacing
    x4 = cardx2+cardx_move2/10 * spacing*20
    
    for i in value.hands:
        card_rect = all_cards_image[11].get_rect(topleft=(x + j * spacing, cardy))
        y = cardy - 10 if card_rect.collidepoint(pygame.mouse.get_pos()) else cardy
        if value.player==1:
            if j==len(value.hands):
                value.screen.blit(all_cards_image[value.deck[value.decks][i]], (x2 + j * spacing, y))
            else:
                value.screen.blit(all_cards_image[value.deck[value.decks][i]], (x + j * spacing, y))
        else:
            value.screen.blit(all_cards_image[value.deck[value.decks][i]], (cardx+j * spacing, y))
        j+=1
    j=0
    for i in value.hands2:
        card_rect = all_cards_image[11].get_rect(topleft=(x + j * spacing, cardy2))
        y = cardy2 + 10 if card_rect.collidepoint(pygame.mouse.get_pos()) else cardy2
        if value.player==2:
            if j==len(value.hands2):
                value.screen.blit(all_cards_image[value.deck[value.decks2][i]], (x4 + j * spacing, y))
            else:
                value.screen.blit(all_cards_image[value.deck[value.decks2][i]], (x3 + j * spacing, y))
        else:
            value.screen.blit(all_cards_image[value.deck[value.decks2][i]], (cardx2 + j * spacing, y))
        j+=1
    
    #ターンエンド
    value.screen.blit(turnend,(turnendx,turnendy))

    #pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    
    if value.t>60:
        value.gamestep=1

    if value.t==1:
        if value.player==1:
            handsadd(1,value.decks,1)
        else:
            handsadd(2,value.decks2,1)
        cardx_move=10
        cardx_move2=30

    if cardx_move>0:cardx_move-=1
    if cardx_move2>0:cardx_move2-=1
    value.t+=1
    pygame.display.update()