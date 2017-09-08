import sys
import math
from random import randint, choice

import pygame

SCREEN_SIZE = (800, 600)


class Ball():
    """Simple Ball Class"""

    def __init__(self, x, y):
        self.pos = [x, y]
        self.radius = randint(5, 30)
        self.color = [randint(0, 255) for _ in range(3)]
        self.speed = math.ceil(50/self.radius)
        self.dx = randint(-1, 1)
        self.dy = randint(-1, 1)
        if self.dx == 0:
            self.dx = 1
        if self.dy == 0:
            self.dy = 1

    def update(self):
        self.pos[0] += self.speed * self.dx
        self.pos[1] += self.speed * self.dy

        if self.pos[0] < 0 or self.pos[0] > SCREEN_SIZE[0]:
            self.dx *= -1
        if self.pos[1] < 0 or self.pos[1] > SCREEN_SIZE[1]:
            self.dy *= -1

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.pos, self.radius)


class Game:

    def __init__(self):
        pygame.init()

        self.screen_size = SCREEN_SIZE
        self.bg_color = (255, 255, 255)

        self.fps = 60

        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()

        self.balls = []
        nums = randint(5, 500)
        for i in range(nums):
            x = randint(0, SCREEN_SIZE[0])
            y = randint(0, SCREEN_SIZE[1])
            self.balls.append(Ball(x, y))

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        capition = "Balls {} - FPS: {:.2f}".format(
            len(self.balls), self.clock.get_fps())
        pygame.display.set_caption(capition)

        for b in self.balls:
            b.update()

    def render(self):
        self.screen.fill(self.bg_color)
        for b in self.balls:
            b.draw(self.screen)

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
