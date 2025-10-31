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
#cost
cost={}
cost[11]=3
cost[12]=5
cost[13]=2
cost[21]=5
cost[22]=6
cost[23]=6#ダブルダウン
cost[24]=1
cost[25]=4#インベート
cost[31]=2#NOT FOUND
cost[32]=4
cost[33]=1#ハイパーインフレ
cost[41]=7
cost[42]=4#突き歩
cost[43]=3#立体交差
cost[44]=8#中割り
cost[45]=0#デフレスパイラル



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
decks=0#0~3
decks2=0
handsize_change=[0,3,5]


#deck
deck=[[11]*20,[11]*20,[11]*20,[11]*20]
deck[0]=[11,11,13,13,23,24,24,25,25,25,25,31,31,32,33,42,42,44,44,45]#11~45
deck[3]=[12,12,12,21,21,21,22,22,22,41,41,41,43,43,25,25,25,25,45,45]
hands=[]#0~19
hands2=[]
deckname=[]
deckcard=[]
deckcolor=[0,1,3,2]

#game
gamestep=0
OFFSET_X = (WINDOW_WIDTH - BOARD_SIZE) // 2
OFFSET_Y = (WINDOW_HEIGHT - BOARD_SIZE) // 2
board = [[0 for _ in range(5)] for _ in range(5)]
board2 = [[0 for _ in range(5)] for _ in range(5)]
turn404 = [[-1 for _ in range(5)] for _ in range(5)]
block=[-1]*4
bridge_direct=[[0 for _ in range(5)] for _ in range(5)]  #0=横
bridge_direct_n=0

player = 1
game_over = False
click=0
skillstep=0
card_dx=[[0]*10,[0]*10]
card_dy=[[0]*10,[0]*10]
card_dy_mode=False
card_dcost=[0]*2

card_select_base=[-1]*2
spacing=120
spacing2=120
spacing_after=120
spacing2_after=120
detail_check=False