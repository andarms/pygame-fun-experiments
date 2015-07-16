import random
import sys

import pygame as pg


pg.init()

SCREEN_WIDTH = pg.display.Info().current_w
SCREEN_HEIGHT = pg.display.Info().current_h

max_size = 100
min_size = 20

image = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

width = SCREEN_HEIGHT

x, y = 0, 0
while x < SCREEN_WIDTH:
	w = random.randint(min_size, max_size)
	while y < SCREEN_HEIGHT:
		h = random.randint(min_size, max_size)
		color = [random.randint(0,255) for _ in range(3)]
		rect = (x, y, w, h)
		image.fill(color, rect)
		y += h
	x += w
	y = 0



pg.image.save(image, 'wallpaper.png')
pg.quit()
sys.exit()