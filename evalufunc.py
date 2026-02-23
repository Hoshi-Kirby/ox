import pygame
import sys
import math
import copy
import itertools

import value
import skillcardfunccpu
import skillcardfunccpu3
import random
pygame.init()

def blockch(x,y,dx,dy,p):
    if 0<=x*2-2+dx<5 and 0<=y*2-2+dy<5:
        if value.board2[x*2-2+dx][y*2-2+dy]==0 or value.board2[x*2-2+dx][y*2-2+dy]==9-p:
            return True
    else:
        return True
    return False

def blockch2(x,y,dx,dy,p):
    if 0<=x*2-2+dx<5 and 0<=y*2-2+dy<5:
        if value.board2[x*2-2+dx][y*2-2+dy]==p:
            return True
    return False

def tokench(x,y,dx,dy,p):
    ch=0
    for i in range(3):
        if 0<=x+dx*i<5 and 0<=y+dy*i<5:
            if value.board[x+dx*i][y+dy*i]==p or value.board[x+dx*i][y+dy*i]==3 or 5<=value.board[x+dx*i][y+dy*i]<=6:
                ch+=1
    
    for i in range(2):
        if 0<=x+dx*i<5 and 0<=y+dy*i<5:
            if blockch(x+dx*i,y+dy*i,dx,dy,p):
                ch+=1
    if ch==5:
        return True
    return False

def tokench2(x,y,dx,dy,p):
    ch=0
    ch2=0
    for i in range(2):
        if 0<=x+dx*i<5 and 0<=y+dy*i<5:
            if value.board[x+dx*i][y+dy*i]==p or value.board[x+dx*i][y+dy*i]==3 or 5<=value.board[x+dx*i][y+dy*i]<=6:
                ch+=1
                if i==0:
                    ch2+=1
    
    if blockch2(x,y,dx,dy,p):
        ch+=1
        ch2+=1
    if blockch2(x,y,-dx,-dy,p):
        ch2+=1
    if ch==3 or ch2==3:
        return True
    return False

def check_win(p):
    for row in range(5):
        for col in range(5):
            for i in range(4):
                dx=0
                dy=0
                match i:
                    case 0:
                        dx=1
                    case 1:
                        dx=1
                        dy=1
                    case 2:
                        dy=1
                    case 3:
                        dx=-1
                        dy=1
                if tokench(row,col,dx,dy,p) or tokench2(row,col,dx,dy,p):
                    return True
    return False

#リーチ
def check_reach(p,x,y):
    hold = value.board[x][y]
    value.board[x][y] = p 

    result = check_win(p)

    value.board[x][y] = hold
    return result

def check_reach2(p,x,y):
    hold = value.board2[x][y]
    value.board2[x][y] = p 

    result = check_win(p)

    value.board2[x][y] = hold
    return result

reach_cache = {}
reach2_cache = {}

def reach(p):
    key = (p, tuple(map(tuple, value.board)))
    if key in reach_cache:
        return reach_cache[key]
    spots = []
    for i in range(5):
        for j in range(5):
            if check_reach(p, i, j):
                spots.append((i, j))
    reach_cache[key] = spots
    return spots

def reach2(p):
    key = (p, tuple(map(tuple, value.board2)))
    if key in reach2_cache:
        return reach2_cache[key]
    spots = []
    for i in range(2):
        for j in range(2):
            if check_reach2(p, i*2+1, j*2+1):
                spots.append((i*2+1, j*2+1))
    reach2_cache[key] = spots
    return spots

def reach_contribution(x, y, p):
    if value.board[x][y] != p:
        return 0
    original = len(reach(p))
    hold = value.board[x][y]
    value.board[x][y] = 0
    after = len(reach(p))
    value.board[x][y] = hold

    return original - after

def reach_contribution2(x, y, p):
    if value.board2[x][y] != p:
        return 0
    original = len(reach(p))
    hold = value.board2[x][y]
    value.board2[x][y] = 0
    after = len(reach(p))
    value.board2[x][y] = hold

    return original - after


def number(p):
    n=0
    for i in range(5):
        for j in range(5):
            if value.board[i][j]==p:
                n+=1
            if value.board[i][j]==3-p:
                n-=0.9
            if value.board2[i][j]==p:
                n+=1.5
            if value.board2[i][j]==3-p:
                n-=1.35
    return n
def number25(p):
    n=0
    for i in range(5):
        for j in range(5):
            if value.board[i][j]==p:
                n+=1
    return n
def numberp(p):
    n=0
    for i in range(5):
        for j in range(5):
            if value.board[i][j]==p or value.board2[i][j]==p:
                n+=1
    return n

def fullhands(p):
    if p==1:
        if len(value.hands)==9:
            return 1
        if len(value.hands)==10:
            return 2
    if p==2:
        if len(value.hands2)==9:
            return 1
        if len(value.hands2)==10:
            return 2
    return 0

#カードの価値
CACHEABLE = {11,12,21,22,23,25,31,32,41,42,43,44}
cardvalue_cache = {}
C={
    11: 2,
    12: 2,
    13: 1,
    21: 2,
    22: 2,
    23: 2,
    24: 1,
    25: 2,
    31: 1,
    32: 1,
    33: 1,
    41: 1,
    42: 2,
    43: 2,
    44: 1,
    45: 0.5
}
def cardvalue(s, p):
    # 盤面依存カードだけキャッシュする
    if s in CACHEABLE:
        key = (
            s,
            p,
            tuple(map(tuple, value.board)),
            tuple(map(tuple, value.board2)),
        )
        if key in cardvalue_cache:
            return cardvalue_cache[key]
    if s==11:
        best = 0
        for x in range(1,4):
            for y in range(1,4):
                if value.board[x][y] == 3-p or value.board[x][y] == 3:
                    k = reach_contribution(x, y, 3-p)
                    best = max(best, k)
        r=best
    elif s==12:
        best = 0
        for x in range(1,4):
            for y in range(1,4):
                destroyed = [(x,y),(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
                k=0
                for (cx,cy) in destroyed:
                    if value.board[cx][cy] == 3-p or value.board[cx][cy] == 3:
                        k += reach_contribution(cx, cy, 3-p)
                best = max(best, k)
        r=best
    elif s==13:#相手の手札価値の最大値
        op = 3-p
        if op == 1:
            deck_id = value.decks
            hand = [ value.deck[deck_id][ value.hands[i] ] for i in range(len(value.hands)) ]
        else:
            deck_id = value.decks2
            hand = [ value.deck[deck_id][ value.hands2[i] ] for i in range(len(value.hands2)) ]
        destroyable = [t for t in hand if t not in (13, 45)]
        if len(destroyable) == 0:
            r=0
        else:
            best = max(destroyable, key=lambda s: cardvalue(s, op))
            r=cardvalue(best, op)

    elif s==21:
        sum=0
        for x in range(5):
            for y in range(5):
                if 1 <= x <= 3 and 1 <= y <= 3:
                    continue
                if (x, y) in reach(p) and value.board[x][y]==0:
                    sum+=1
        r=sum
    elif s==22:
        r=len(reach2(p))
    elif s==23:
        sum=0
        for x in range(1,4):
            for y in range(1,4):
                if (x, y) in reach(p) and value.board[x][y]==3-p:
                    sum+=1
        r=sum
    elif s==24:
        r=1#評価関数そのまま
    elif s==25:
        sum=0
        for x in range(1,4):
            for y in range(1,4):
                if (x, y) in reach(p) and value.board[x][y]==0:
                    sum+=1
        r=sum
    elif s==31:
        sum=0
        for x in range(1,4):
            for y in range(1,4):
                if (x, y) in reach(3-p) and value.board[x][y]==0:
                    sum=1
        r=sum
    elif s==32:
        r=0
        if len(reach(3-p))==1:r=1
    elif s==33:
        r=1#やらないかも。相手手札枚数+2のコストのカードの価値
    elif s==41:
        best = 0
        for x in range(1,4):
            for y in range(1,4):
                if value.board[x][y] == 3-p or value.board[x][y] == 3:
                    k = reach_contribution(x, y, 3-p)
                    if (x, y) in reach(p) and value.board[x][y]==0 and numberp(p)>=3:
                        k+=2
                    best = max(best, k)
        r=best
    elif s==42:
        sum=0
        for x in range(1,4):
            for y in range(1,4):
                if (x, y) in reach(p) and value.board[x][y]==0 and numberp(p)>=3:
                    sum+=1
        r=sum
    elif s==43:
        sum=0
        for x in range(1,4):
            for y in range(1,4):
                if (x, y) in reach(p) and value.board[x][y]==3-p:
                    sum+=1
        r=sum
    elif s==44:
        best=0
        for x in range(0,5):
            for y in range(0,5):
                if value.board[x][y] == 3-p or value.board[x][y] == 3:
                    k = reach_contribution(x, y, 3-p)
                    if (x, y) in reach(p) and value.board[x][y]==3-p:
                        k+=2
                    best = max(best, k)
        r=best
    elif s==45:
        before ,after= combo_value_greedy(p)
        r=after - before

    r = r * C[s]
    if p==1:
        if value.cost[s]+value.card_dcost[0]+1<len(value.hands):
            r=r*1.5
    else:
        if value.cost[s]+value.card_dcost[1]+1<len(value.hands2):
            r=r*1.5

    if s in CACHEABLE:
        cardvalue_cache[key] = r

    if not isinstance(r, (int, float)):
        print("BAD RETURN:", s, type(r), r)
    
    return r

#連続使用のカード価値の最大値
def combo_value_greedy(p):
    # p = 1 or 2
    # 手札の skillnum を列挙
    if p == 1:
        deck_id = value.decks
        hand = [ value.deck[deck_id][ value.hands[i] ] for i in range(len(value.hands)) ]
    else:
        deck_id = value.decks2
        hand = [ value.deck[deck_id][ value.hands2[i] ] for i in range(len(value.hands2)) ]

    # デフレ（skillnum=25）は未来行動に含めない
    usable = [s for s in hand if s not in (13, 45)]

    # 行動価値の高い順に並べる
    usable.sort(key=lambda s: cardvalue(s, p), reverse=True)

    # コストは手札枚数
    remaining = len(hand)
    total = 0
    for s in usable:
        c = value.cost[s]+value.card_dcost[p-1]+1 # skillnum→コスト
        if c <= remaining:
            total += cardvalue(s, p)
            remaining -= c

    # コストは手札枚数
    remaining = len(hand)
    total2 = 0
    for s in usable:
        c = value.cost[s]+value.card_dcost[p-1] # skillnum→コスト
        if c <= remaining:
            total2 += cardvalue(s, p)
            remaining -= c

    return [total,total2]

def combo_value_greedy_next(p):
    if p == 1:
        deck_id = value.decks
        hand = [ value.deck[deck_id][ value.hands[i] ] for i in range(len(value.hands)) ]
    else:
        deck_id = value.decks2
        hand = [ value.deck[deck_id][ value.hands2[i] ] for i in range(len(value.hands2)) ]
    usable = [s for s in hand if s not in (13, 45)]
    usable.sort(key=lambda s: cardvalue(s, p), reverse=True)
    remaining = len(hand)+2
    total = 0
    for s in usable:
        c = value.cost[s]+value.card_dcost[p-1]+1 # skillnum→コスト
        if c <= remaining:
            total += cardvalue(s, p)
            remaining -= c
    return total

#手札価値
def handvalue():
    deck1 = value.decks
    hand1 = [ value.deck[deck1][ value.hands[i] ] for i in range(len(value.hands)) ]

    deck2 = value.decks2
    hand2 = [ value.deck[deck2][ value.hands2[i] ] for i in range(len(value.hands2)) ]

    hv1 = sum(cardvalue(s, 1) for s in hand1)
    hv2 = sum(cardvalue(s, 2) for s in hand2)

    return [hv1, hv2]

# 評価関数
k=0.2
def evalufunc(p):
    c1, c2, c3, c4, c5, c6 = value.c[value.decks]
    rate = math.exp(k* value.card_dcost_cor[p-1])  # d<0 → rate<1, d>0 → rate>1, 常に正
    c4 *= rate
    c6 *= rate


    hv = handvalue()
    my_hand = hv[p-1]
    op_hand = hv[2-p]
    combo= combo_value_greedy(p)[0]
    if p==1:
        lenhands=len(value.hands)
    else:
        lenhands=len(value.hands2)

    r=(number(p)*c1+(len(reach(p))+len(reach2(p)))*c2+(my_hand-op_hand)*c3+combo*c4-fullhands(p)*c5+lenhands*c6)
    return r

def evalufuncnext(p):
    c1, c2, c3, c4, c5, c6 = value.c[value.decks]
    rate = math.exp(k* value.card_dcost_cor[p-1])  # d<0 → rate<1, d>0 → rate>1, 常に正
    c4 *= rate
    c6 *= rate

    hv = handvalue()
    my_hand = hv[p-1]
    op_hand = hv[2-p]
    combo= combo_value_greedy_next(p)
    if p==1:
        lenhands=len(value.hands)
    else:
        lenhands=len(value.hands2)

    r=(number(p)*c1+(len(reach(p))+len(reach2(p)))*c2+(my_hand-op_hand)*c3+combo*c4-fullhands(p)*c5+(lenhands+2-fullhands(p))*c6)
    return r

#評価関数＝(盤面の駒数ー相手の駒数)×c1+(自分のリーチ数-相手のリーチ数)×c2
# +(自分の手札価値-相手の手札価値+このターンに使用したカードの価値)×c3
# +(自分が現在連続で使用できるカードの価値の総和の最大値)×c4
# -(手札が9枚なら1,手札が10枚なら2)×c5+自分の手札枚数×c6
#[1 , 2 , 0.5 , 0.2 , 2 , 0.1]











def bestmove(p):
    max=evalufuncnext(p)
    copyboard=copy.deepcopy(value.board)
    copyboard2=copy.deepcopy(value.board2)
    copyhands=copy.deepcopy(value.hands)
    copyhands2=copy.deepcopy(value.hands2)
    copyblock=copy.deepcopy(value.block)
    copy404=copy.deepcopy(value.turn404)
    copydcost=copy.deepcopy(value.card_dcost)
    copyskillstep=copy.deepcopy(value.skillstep)
    copygamestep=copy.deepcopy(value.gamestep)
    x=0
    maxi=[-1]
    if p==2:
        for i in range (len(value.hands2)):
            skillnum=value.deck[value.decks2][value.hands2[i]]
            if len(value.hands2)>value.cost[skillnum]+value.card_dcost[p-1]:
                skillcardfunccpu.riset(i)
                value.skillstep=0
                value.gamestep=3
                cardvalueb=cardvalue(skillnum, p)*value.c[value.decks][3]
                while value.gamestep!=1:
                    skillcardfunccpu.portal(skillnum)
                    value.t+=1
                x=evalufunc(p)+cardvalueb
                if x > max:
                    max = x
                    maxi = [i]
                elif x == max:
                    maxi.append(i)
                value.board=copy.deepcopy(copyboard)
                value.board2=copy.deepcopy(copyboard2)
                value.hands=copy.deepcopy(copyhands)
                value.hands2=copy.deepcopy(copyhands2)
                value.block=copy.deepcopy(copyblock)
                value.turn404=copy.deepcopy(copy404)
                value.card_dcost=copy.deepcopy(copydcost)
    value.skillstep=copy.deepcopy(copyskillstep)
    value.gamestep=copy.deepcopy(copygamestep)
                
    return random.choice(maxi)



#op,ch
def opset(p, skillnum):
    SKILL_OP = {
        11: [1,4,1,4],
        12: [1,4,1,4],
        13: lambda p: [0, len(value.hands2)] if p == 1 else [0, len(value.hands)],
        21: [0,5,0,5],
        22: [1,4,1,4],#1or3
        23: [1,4,1,4],
        25: [1,4,1,4],
        31: [1,4,1,4],
        32: [0,4],
        41: [0,5,0,5,0,5,0,5],
        42: [0,5,0,5,0,5,0,5],
        43: [1,4,1,4,0,2],
        44: [0,5,0,5]
    }
    op = SKILL_OP[skillnum]
    return op(p) if callable(op) else op

def can_use(skillnum, p, i):
    SKILL_COND = {
        11: lambda p, i: value.board[i[0]][i[1]]==3-p or value.board[i[0]][i[1]]==3,
        12: lambda p, i: 1<=value.board[i[0]][i[1]] or 1<=value.board[i[0]-1][i[1]] or 1<=value.board[i[0]][i[1]-1] or 1<=value.board[i[0]+1][i[1]] or 1<=value.board[i[0]][i[1]+1],
        13: lambda p, i: True,
        21: lambda p, i: value.board[i[0]][i[1]]==0 and (i[0]==0 or i[0]==4 or i[1]==0 or i[1]==4),
        22: lambda p, i: i[0]!=2 and i[1]!=2 and(value.board2[i[0]][i[1]]==0 or value.board2[i[0]][i[1]]==3-p),
        23: lambda p, i: value.board[i[0]][i[1]]==3-p,
        25: lambda p, i: value.board[i[0]][i[1]]==0,
        31: lambda p, i: value.board[i[0]][i[1]]==0,
        32: lambda p, i: value.board2[1][1]==0 and value.board2[3][1]==0 and i[0]==0
                      or value.board2[1][3]==0 and value.board2[3][3]==0 and i[0]==1
                      or value.board2[1][1]==0 and value.board2[1][3]==0 and i[0]==2
                      or value.board2[3][1]==0 and value.board2[3][3]==0 and i[0]==3,
        41: lambda p, i: value.board[i[0]][i[1]]==p and value.board[i[2]][i[3]]==3-p,
        42: lambda p, i: value.board[i[0]][i[1]]==p and value.board[i[2]][i[3]]==0,
        43: lambda p, i: value.board[i[0]][i[1]]==3-p,
        44: lambda p, i: value.board[i[0]][i[1]]==3-p
    }
    return SKILL_COND[skillnum](p, i)



def bestmove3(p,sknum):
    max = -10**18
    maxi = []
    copyboard=copy.deepcopy(value.board)
    copyboard2=copy.deepcopy(value.board2)
    copyhands=copy.deepcopy(value.hands)
    copyhands2=copy.deepcopy(value.hands2)
    copyblock=copy.deepcopy(value.block)
    copy404=copy.deepcopy(value.turn404)
    copydcost=copy.deepcopy(value.card_dcost)
    copyskillstep=copy.deepcopy(value.skillstep)
    copygamestep=copy.deepcopy(value.gamestep)
    x=0
    op=opset(p,sknum)
    if p==2:#opは選択できる[最小値,最大値]配列
        for cpui in itertools.product(*(range(op[i], op[i+1])for i in range(0, len(op), 2))):
            if can_use(sknum, p, cpui):
                value.changes = []  # 変更ログ初期化
                value.skillstep=1
                skillcardfunccpu3.riset(0)
                value.gamestep=3
                while value.gamestep!=1:
                    skillcardfunccpu3.portal(sknum,cpui)
                    value.t+=1
                x=evalufunc(p)
                if x > max:
                    max = x
                    maxi = [cpui]
                elif x == max:
                    maxi.append(cpui)

                
                for change in reversed(value.changes):
                    restore(change)

                value.changes.clear()

    value.board=copy.deepcopy(copyboard)
    value.board2=copy.deepcopy(copyboard2)
    value.hands=copy.deepcopy(copyhands)
    value.hands2=copy.deepcopy(copyhands2)
    value.block=copy.deepcopy(copyblock)
    value.turn404=copy.deepcopy(copy404)
    value.card_dcost=copy.deepcopy(copydcost)
    value.skillstep=copy.deepcopy(copyskillstep)
    value.gamestep=copy.deepcopy(copygamestep)
    if maxi==[]:
        value.gamestep=1
        return cpui
                
    return random.choice(maxi)

def restore(change):
    kind = change[0]
    if kind == "board":
        _, x, y, old = change
        value.board[x][y] = old
    elif kind == "board2":
        _, x, y, old = change
        value.board2[x][y] = old
    elif kind == "block":
        _, x, old = change
        value.block[x] = old
    elif kind == "turn404":
        _, x, y, old = change
        value.turn404[x][y] = old
    elif kind == "cost":
        _, idx, old = change
        value.card_dcost[idx] = old
    elif kind == "hands":
        _, old_list = change
        value.hands = old_list
    elif kind == "hands2":
        _, old_list = change
        value.hands2 = old_list
    elif kind == "bridge_direct":
        _, x, y, old = change
        value.bridge_direct[x][y] = old
    elif kind == "skillstep":
        _, old = change
        value.skillstep = old

def learn_from_loss():
    p=2
    deck = value.decks2 if p==2 else value.decks
    c = value.c[deck]
    c_default = value.c_default  # [1,2,0.5,0.2,2,0.1]

    base_alpha = 0.01

    hv = handvalue()
    my_hand = hv[p-1]
    op_hand = hv[2-p]

    v = [
        number(p),
        len(reach(p)) + len(reach2(p)),
        my_hand - op_hand,
        combo_value_greedy(p)[0],
        fullhands(p),
        len(value.hands2) if p==2 else len(value.hands)
    ]

    for i in range(6):
        # α を係数に応じて変動させる
        alpha_i = base_alpha * (c_default[i] / (abs(c[i]) + 0.001))

        # 学習
        c[i] -= alpha_i * v[i]

    print("更新後の係数:", c)