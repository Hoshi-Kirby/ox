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
cost[11]=1#delete
cost[12]=3#超新星爆発
cost[13]=1#カード割り
cost[21]=6#外れ値
cost[22]=6#囲碁
cost[23]=6#ダブルダウン
cost[24]=1#１ドロー
cost[25]=5#cout<<
cost[31]=1#NOT FOUND
cost[32]=3#ファイアウォール
cost[33]=0#ハイパーインフレ
cost[41]=4#キャスリング
cost[42]=3#突き歩
cost[43]=3#立体交差
cost[44]=7#中割り
cost[45]=1#デフレスパイラル



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
make_deck_ka=1
event_switch=0
help_page=0

#deck
deck=[[11]*20,[],[],[]]
deck[0]=[11,11,13,13,23,24,24,25,25,25,25,31,31,32,33,42,42,44,44,45]#11~45
hands=[]#0~19
hands2=[]
deckname=[]
deckcard=[]
deckcolor=[0,0,0,0]

#game
gamestep=0
gamereset=False
firstfirst=True
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

event_turn=0
event_turn_min=5
event_turn_max=8
nextevent=0
eventnum=-1
event_t=0

winner=0

#make
hold_deck=[]