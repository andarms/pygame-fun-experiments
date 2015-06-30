import sys

import pygame

class Game:

	def __init__(self):
		pygame.init()

		self.screen_size = (300, 240)
		self.bg_color = (255, 255, 255)
		self.text_color = (0, 0, 255)
		self.font = pygame.font.Font('cool_menu/visitor2.ttf', 40)
		self.message = ""

		self.fps = 60

		self.screen = pygame.display.set_mode(self.screen_size)
		self.clock = pygame.time.Clock()
		

	def handle_input(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if event.key == 8: # delete keycode
					self.message = self.message[:-1]
				else:
					self.message += event.unicode

	def update(self):
		capition = "Text input test - FPS: {:.2f}".format(self.clock.get_fps())
		pygame.display.set_caption(capition)

	def render(self):
		self.screen.fill(self.bg_color)
		if self.message:
			text_surface = self.font.render(self.message, 1, self.text_color)
			rect = text_surface.get_rect(x=50, y=50)
			self.screen.blit(text_surface, rect)

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