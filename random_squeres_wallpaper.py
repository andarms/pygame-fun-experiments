"""
inspired by https://github.com/anshulc95/rangeela
Just a wallpaper generator to test pygame.image.save function 
"""
import random
import sys

import pygame as pg


pg.init()

SCREEN_WIDTH = pg.display.Info().current_w
SCREEN_HEIGHT = pg.display.Info().current_h

max_size = 200
min_size = 50
amount = 100
bg_color = (0,0,0)

image = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
image.fill(bg_color)

width = SCREEN_HEIGHT

print "Creating wallpaper wait please..."

canvas_w = SCREEN_WIDTH - max_size
canvas_h = SCREEN_HEIGHT - max_size
for x in xrange(amount):
	size = random.randint(min_size, max_size)
	x = random.randint(0, canvas_w)
	y = random.randint(0, canvas_h)
	color = [random.randint(0,255) for _ in range(3)]		
	rect = (x, y, size, size)	
	image.fill(color, rect)



pg.image.save(image, 'wallpaper.png')
print "Done."
pg.quit()
sys.exit()