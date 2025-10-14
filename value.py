import pygame
import sys

WINDOW_WIDTH, WINDOW_HEIGHT = 1279, 800
BOARD_SIZE = 200
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = BOARD_SIZE // BOARD_COLS
LINE_WIDTH = 5
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 5
CROSS_WIDTH = 7
SPACE = SQUARE_SIZE // 4
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
step=0
nextstep=0

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("○×ゲーム")


#title
t=0

#フェードアウト
fade_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
fade_surface.fill((0, 0, 0))
fade_out=False
fade_in=False
fade_alpha=0

#menu
menustep=0
play_number=0
Startinghandsize=1
firstplayer=0
decks=0

deckname=[]
deckcard=[]
deckcolor=[0,1,3,2]

#game
OFFSET_X = (WINDOW_WIDTH - BOARD_SIZE) // 2
OFFSET_Y = (WINDOW_HEIGHT - BOARD_SIZE) // 2
board = [[0 for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
player = 1
game_over = False