import sys

import pygame

class TextCursor():
	"""docstring for TextCursor"""
	def __init__(self, x, y, spacing, height):
		self.init_x = x
		self.init_y = y
		self.x = x
		self.y = y
		self.height = height
		self.spacing = spacing
		self.ticks = 0

	def update(self):
		self.ticks += 1
		if self.ticks > 60:
			self.ticks = 0

	def render(self, screen):		
		if self.ticks < 30:
			p1 = (self.x, self.y)
			p2 = (self.x, self.y + self.height)
			pygame.draw.line(screen, (0,0,150), p1, p2, 3)

	def move_left(self):
		self.x -= self.spacing

	def move_right(self):
		self.x += self.spacing
		

class TextInput:
	"""docstring for TextInput"""
	def __init__(self, x, y):
		self.fg_color = (225, 225, 225)
		self.text_color = (0, 0, 255)
		self.font_size = 40
		self.font = pygame.font.Font('cool_menu/visitor2.ttf', self.font_size)

		self.message = ""
		self.max_chars = 10

		letter_w, letter_h = self.font.size('a')
		w = letter_w * self.max_chars + 40
		h = letter_h + 10
		self.rect = pygame.Rect(0, 0, w, h)
		self.rect.topleft = x, y

		self.cursor = TextCursor(self.rect.x + 20, self.rect.y + 5, letter_w, letter_h)

	def update(self):
		self.cursor.update()

	def handle_input(self, event):
		if event.key == 8: # delete keycode
			self.message = self.message[:-1]
			self.cursor.move_left()
		else:
			if event.unicode != "\r" and len(self.message) < self.max_chars:
				self.message += event.unicode
				self.cursor.move_right()

	def render(self, screen):
		pygame.draw.rect(screen, self.fg_color, self.rect)
		if self.message:
			text_surface = self.font.render(self.message, 1, self.text_color)
			rect = text_surface.get_rect(x=self.rect.x + 20, y=self.rect.y + 5)
			screen.blit(text_surface, rect)
		self.cursor.render(screen)


class Game:

	def __init__(self):
		pygame.init()

		self.screen_size = (300, 240)
		self.bg_color = (255, 255, 255)
		self.TextInput = TextInput(35,50)

		self.fps = 60

		self.screen = pygame.display.set_mode(self.screen_size)
		self.clock = pygame.time.Clock()
		

	def handle_input(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.KEYDOWN:
				self.TextInput.handle_input(event)

	def update(self):
		capition = "Text input test - FPS: {:.2f}".format(self.clock.get_fps())
		pygame.display.set_caption(capition)
		self.TextInput.update()

	def render(self):
		self.screen.fill(self.bg_color)
		self.TextInput.render(self.screen)

	def main_loop(self):
		while True:
			self.handle_input()
			self.update()
			self.render()

			pygame.display.flip()
			self.clock.tick(self.fps)




if __name__ == '__main__':
	g = Game()
	g.main_loop()