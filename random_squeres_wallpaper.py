import random
import sys

import pygame as pg


pg.init()

SCREEN_WIDTH = pg.display.Info().current_w
SCREEN_HEIGHT = pg.display.Info().current_h

max_width = SCREEN_WIDTH/6
max_height = SCREEN_HEIGHT/6

image = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

width = SCREEN_HEIGHT
height = SCREEN_HEIGHT
x = 0
y = 0
while x < SCREEN_WIDTH:
	size = random.randint(0, max_width)
	if size + x > SCREEN_WIDTH: size = SCREEN_WIDTH - x
	for y in xrange(0, SCREEN_HEIGHT, size):
		color = [random.randint(0,255) for _ in range(3)]
		rect = (x, y, size, size)
		image.fill(color, rect)
	x += size



pg.image.save(image, 'wallpaper.png')
pg.quit()
sys.exit()