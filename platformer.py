import sys

import pygame as pg

WHITE = (255, 255, 255)
BLACK = (255, 255, 255)
RED = (255, 0, 0)

class Player(pg.sprite.Sprite):
	def __init__(self, x, y):
		pg.sprite.Sprite.__init__(self)

		self.image = pg.Surface([15, 20])
		self.image.fill(RED)

		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.speed = 5
		self.vx = x
		self.vy = y

		self.runing = False

	def handle_input(self, keys):
		self.runing = False
		if keys[pg.K_LEFT]:
			self.vx -= self.speed
			self.runing = True
		elif keys[pg.K_RIGHT]:
			self.vx += self.speed
			self.runing = True
		elif keys[pg.K_UP]:
			self.vy -= self.speed
			self.runing = True
		elif keys[pg.K_DOWN]:
			self.vy += self.speed
			self.runing = True

	def update(self):
		if self.runing:
			self.rect.x = self.vx
			self.rect.y = self.vy

	def render(self, screen):
		screen.blit(self.image, self.rect)

class Game:

	def __init__(self):
		pg.init()

		self.screen_size = (300, 240)
		self.bg_color = (255, 255, 255)
		self.rect_color = (0, 0, 255)

		self.fps = 60

		self.screen = pg.display.set_mode(self.screen_size)
		self.clock = pg.time.Clock()
		self.keys = pg.key.get_pressed()

		self.player = Player(20, 20)

	def handle_input(self):
		for event in pg.event.get():
			self.keys = pg.key.get_pressed()
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()
		
		self.player.handle_input(self.keys)


	def update(self):
		capition = "Platformer - FPS: {:.2f}".format(self.clock.get_fps())
		pg.display.set_caption(capition)
		self.player.update()

	def render(self):
		self.screen.fill(self.bg_color)
		self.player.render(self.screen)

	def main_loop(self):
		while True:
			self.handle_input()
			self.update()
			self.render()

			pg.display.flip()
			self.clock.tick(self.fps)




if __name__ == '__main__':
	g = Game()
	g.main_loop()