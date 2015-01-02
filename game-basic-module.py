import sys

import pygame

class Game:

	def __init__(self):
		pygame.init()

		self.screen_size = (300, 240)
		self.bg_color = (255, 255, 255)
		self.rect_color = (0, 0, 255)

		self.fps = 60

		self.screen = pygame.display.set_mode(self.screen_size)
		self.clock = pygame.time.Clock()

		self.rect = pygame.Rect(20, 20, 50, 50)

	def handle_input(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

	def update(self):
		capition = "Hola mundo - FPS: {:.2f}".format(self.clock.get_fps())
		pygame.display.set_caption(capition)

	def render(self):
		self.screen.fill(self.bg_color)
		pygame.draw.rect(self.screen, self.rect_color, self.rect)

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