import sys
from random import randint

import pygame

GRID_SIZE = 20
COLS = ROWS = 20
SCREEN_SIZE = (COLS*GRID_SIZE, ROWS*GRID_SIZE)


class Snake():
    """Simple Skane Class"""

    def __init__(self, x, y):
        self.x = x * GRID_SIZE
        self.y = y * GRID_SIZE
        self.vx = 1 * GRID_SIZE
        self.vy = 0 * GRID_SIZE
        self.trail = []
        self.size = 5
        self.color = (0, 100, 255)
        self.reset()

    def reset(self):
        self.size = 5
        self.trail = []
        self.x = 10 * GRID_SIZE
        self.y = 10 * GRID_SIZE

    def handle_input(self, key):
        if key == pygame.K_RIGHT and self.vx == 0:
            self.vx = GRID_SIZE
            self.vy = 0

        if key == pygame.K_LEFT and self.vx == 0:
            self.vx = -GRID_SIZE
            self.vy = 0

        if key == pygame.K_DOWN and self.vy == 0:
            self.vx = 0
            self.vy = GRID_SIZE

        if key == pygame.K_UP and self.vy == 0:
            self.vx = 0
            self.vy = -GRID_SIZE

    def update(self, apple):
        self.x += self.vx
        self.y += self.vy
        if self.x > SCREEN_SIZE[0] - GRID_SIZE:
            self.x = 0
        if self.x < 0:
            self.x = SCREEN_SIZE[0] - GRID_SIZE
        if self.y > SCREEN_SIZE[1]:
            self.y = 0
        if self.y < 0:
            self.y = SCREEN_SIZE[1] - GRID_SIZE

        for t in self.trail:
            if t['x'] == self.x and t['y'] == self.y:
                self.reset()

        self.trail.append({'x': self.x, 'y': self.y})

        while len(self.trail) > self.size:
            self.trail.pop(0)

        if(apple.x == self.x and apple.y == self.y):
            self.size += 1
            apple.x = randint(0, COLS - 1) * GRID_SIZE
            apple.y = randint(0, ROWS - 1) * GRID_SIZE

    def draw(self, surface):
        for t in self.trail:
            pygame.draw.rect(surface, self.color,
                             (t['x'], t['y'], GRID_SIZE, GRID_SIZE), 1)
        pygame.draw.rect(surface, self.color,
                         (self.trail[-1]['x'],
                          self.trail[-1]['y'],
                             GRID_SIZE,
                             GRID_SIZE))


class Game:

    def __init__(self):
        pygame.init()

        self.screen_size = SCREEN_SIZE
        self.bg_color = (255, 255, 255)
        self.apple_color = (255, 0, 0)
        self.fps = 10

        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()

        self.snake = Snake(10, 10)
        self.apple = pygame.Rect(
            randint(0, COLS) * GRID_SIZE,
            randint(0, ROWS) * GRID_SIZE,
            GRID_SIZE,
            GRID_SIZE)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYUP:
                self.snake.handle_input(event.key)

    def update(self):
        capition = "Hola mundo - FPS: {:.2f}".format(self.clock.get_fps())
        pygame.display.set_caption(capition)
        self.snake.update(self.apple)

    def render(self):
        self.screen.fill(self.bg_color)
        self.snake.draw(self.screen)
        pygame.draw.rect(self.screen, self.apple_color, self.apple)

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
