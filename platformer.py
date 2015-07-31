import sys

import pygame as pg

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

GRAVITY = 15 #px/s

LEVEL_MAP = [
	'##############################',
	'#                            #',
	'#                            #',
	'#                            #',
	'#                            #',
	'#                            #',
	'#                            #',
	'#                            #',
	'#                            #',
	'#                            #',
	'#                            #',
	'#                            #',
	'#                            #',
	'#                #############',
	'#                            #', 
	'#                            #',
	'#      ##########            #',
	'#                            #',
	'#                            #',
	'##############################'
]

class Wall(pg.sprite.Sprite):
	def __init__(self, x, y):
		pg.sprite.Sprite.__init__(self)

		self.image = pg.Surface([20,20])
		self.image.fill(WHITE)

		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Level(pg.sprite.Group):
	def __init__(self, level_map):
		pg.sprite.Group.__init__(self)
		x, y = 0, 0
		for row in level_map:
			for col in row:
				if col == '#':
					w = Wall(x, y)
					self.add(w)
				x += 20
			y += 20
			x = 0

	def render(self, screen):
		self.draw(screen)


class Player(pg.sprite.Sprite):
	def __init__(self, x, y):
		pg.sprite.Sprite.__init__(self)

		self.image = pg.Surface([15, 20])
		self.image.fill(RED)

		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.speed = 100 # px/s
		self.accel =  0.046875
		self.max_speed =  250 # px/s
		self.vx = 0
		self.vy = 0
		self.jump_power = -1
		self.jump_speed = 0.05
		self.max_jump_length = -100

		self.runing = False
		self.falling = True
		self.jumping = False
		

	def handle_input(self, keys):
		self.runing = False
		self.vx = 0
		if keys[pg.K_LEFT]:
			self.vx = -self.speed
			self.runing = True
		if keys[pg.K_RIGHT]:
			self.vx = self.speed
			self.runing = True
		if keys[pg.K_UP]:
			self.jumping = True

	@property
	def accelerate(self):
		if self.speed > self.max_speed:
			return self.max_speed
		self.speed += self.accel
		return self.speed

	def cut_jump(self):
		self.jumping = False
		self.max_jump_length = -100
		self.vy = 0

	def update(self, level, dt):
		print self.rect.x
		if self.runing:
			self.rect.x += self.vx * dt

		collitions = pg.sprite.spritecollide(self, level, False)
		if collitions:
			if self.vx > 0:
				self.rect.right = collitions[0].rect.left
			else:
				self.rect.left = collitions[0].rect.right


		if self.jumping:
			self.vy +=  self.max_jump_length
			self.max_jump_length += GRAVITY
			if self.vy >= 0:
				self.cut_jump()
		
		if self.falling and not self.jumping:
			self.vy += GRAVITY
			
		self.rect.y += self.vy * dt
		
		collitions = pg.sprite.spritecollide(self, level, False)
		if collitions:
			if self.falling and self.vy >= 0:
				self.rect.bottom = collitions[0].rect.top
				self.falling = False
				self.vy = 0
			else:
				self.rect.top = collitions[0].rect.bottom
				if self.jumping: self.cut_jump()
		else: self.falling = True


	def render(self, screen):
		screen.blit(self.image, self.rect)

class Game:

	def __init__(self):
		pg.init()

		self.screen_size = (600, 400)
		self.bg_color = BLACK

		self.fps = 60

		self.screen = pg.display.set_mode(self.screen_size)
		self.clock = pg.time.Clock()
		self.keys = pg.key.get_pressed()

		self.player = Player(50, 50)
		self.level = Level(LEVEL_MAP)

	def handle_input(self):
		for event in pg.event.get():
			self.keys = pg.key.get_pressed()
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()
		
		self.player.handle_input(self.keys)


	def update(self, dt):
		capition = "Platformer - FPS: {:.2f}".format(self.clock.get_fps())
		pg.display.set_caption(capition)
		self.player.update(self.level, dt)

	def render(self):
		self.screen.fill(self.bg_color)
		self.player.render(self.screen)
		self.level.render(self.screen)

	def main_loop(self):
		while True:
			time_delta = self.clock.tick(self.fps)/1000.0
			self.handle_input()
			self.update(time_delta)
			self.render()

			pg.display.flip()




if __name__ == '__main__':
	g = Game()
	g.main_loop()