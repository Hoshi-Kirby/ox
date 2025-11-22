import pygame
import sys
import math

import value

def bgmplay(x):
    if value.bgm_track != x:
        if x==1:
            pygame.mixer.music.load(f"sound/op.mp3")
            pygame.mixer.music.set_volume(0.3)  # 30%くらいに下げる
        if x==2:
            pygame.mixer.music.load(f"sound/mm.mp3")
            pygame.mixer.music.set_volume(0.1)  # 30%くらいに下げる
        if x==3:
            pygame.mixer.music.load(f"sound/vs.mp3")
            pygame.mixer.music.set_volume(0.1)  # 30%くらいに下げる
        pygame.mixer.music.play(-1)
        value.bgm_track=x