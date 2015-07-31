import pygame as pg

# GAME CONTS
screen_witdh, screen_height = screen_size = (800, 600)
CAPTION = "Cool Menu"
credits_msn= """
Created by Adrian Manjarrez
@andarms


A simple multi-level menu test
with a state manager feature.


Press any key to back"""

# Initialization
pg.init()
FLAGS = pg.DOUBLEBUF|pg.HWSURFACE
SCREEN = pg.display.set_mode(screen_size, FLAGS)
SCREEN_RECT = SCREEN.get_rect()


font = pg.font.Font('visitor2.ttf', 40)
big_font = pg.font.Font('visitor2.ttf', 70)
## Help functions
def toogle_fullscreen(turn_on):
    global FLAGS
    if turn_on:
        FLAGS = pg.FULLSCREEN|pg.HWSURFACE|pg.DOUBLEBUF
    else:
        FLAGS = pg.HWSURFACE|pg.DOUBLEBUF       
    SCREEN = pg.display.set_mode(screen_size, FLAGS)
    SCREEN_RECT = SCREEN.get_rect()

def chage_window_size(size):
    global screen_size
    screen_size = size
    SCREEN = pg.display.set_mode(screen_size, FLAGS)
    SCREEN_RECT = SCREEN.get_rect()