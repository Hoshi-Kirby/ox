import pygame
import sys
import value
pygame.init()

pekin = pygame.image.load("image/neon_city.png").convert()
original_width, original_height = pekin.get_size()
pekin = pygame.transform.scale_by(pekin,value.WINDOW_HEIGHT/original_height)
widhe_skew=(value.WINDOW_WIDTH-original_width*value.WINDOW_HEIGHT/original_height)/2-2

def draw_lines():
    for i in range(1, value.BOARD_ROWS):
        pygame.draw.line(value.screen, value.WHITE,
                         (value.OFFSET_X, value.OFFSET_Y + i * value.SQUARE_SIZE),
                         (value.OFFSET_X + value.BOARD_SIZE, value.OFFSET_Y + i * value.SQUARE_SIZE),
                         value.LINE_WIDTH)
    for i in range(1, value.BOARD_COLS):
        pygame.draw.line(value.screen, value.WHITE,
                         (value.OFFSET_X + i * value.SQUARE_SIZE, value.OFFSET_Y),
                         (value.OFFSET_X + i * value.SQUARE_SIZE, value.OFFSET_Y + value.BOARD_SIZE),
                         value.LINE_WIDTH)

def draw_circle(row, col):
    center = (value.OFFSET_X + col * value.SQUARE_SIZE + value.SQUARE_SIZE // 2,
              value.OFFSET_Y + row * value.SQUARE_SIZE + value.SQUARE_SIZE // 2)
    pygame.draw.circle(value.screen, value.WHITE, center, value.CIRCLE_RADIUS, value.CIRCLE_WIDTH)

def draw_cross(row, col):
    x = value.OFFSET_X + col * value.SQUARE_SIZE
    y = value.OFFSET_Y + row * value.SQUARE_SIZE
    margin = value.SQUARE_SIZE // 5  # 余白を調整

    # 左上 → 右下
    pygame.draw.line(value.screen, value.WHITE,
                     (x + margin, y + margin),
                     (x + value.SQUARE_SIZE - margin, y + value.SQUARE_SIZE - margin),
                     value.CROSS_WIDTH)

    # 左下 → 右上
    pygame.draw.line(value.screen, value.WHITE,
                     (x + margin, y + value.SQUARE_SIZE - margin),
                     (x + value.SQUARE_SIZE - margin, y + margin),
                     value.CROSS_WIDTH)

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

def game():
    value.screen.blit(pekin, (widhe_skew,0))
    draw_lines()
    for i in range(value.BOARD_COLS):
        for j in range(value.BOARD_ROWS):
            match value.board[i][j]:
                case 1:
                    draw_circle(i,j)
                case 2:
                    draw_cross(i,j)
                case _:
                    pass
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
                        if value.player == 1:
                            draw_circle(clicked_row, clicked_col)
                        else:
                            draw_cross(clicked_row, clicked_col)
                        print(f"value.player {value.player} wins!")
                        value.game_over = True

                    value.player = 2 if value.player == 1 else 1

    pygame.display.update()