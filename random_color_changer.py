"""
change the background color, choosing between random colors
using the arrow keys and the enter key.

Using some math tricks to make things work

Author: Adrian Manjarres - @andarms
"""
import sys
import random
from math import ceil

import pygame

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT =(820, 600)
HOVER_COLOR = (21, 88, 177)
SEL_COLOR = (215, 218, 34)

class Option(pygame.Rect):
    """
    Extending the pygame.Rect to add some helpful features.
    """
    def __init__(self, x, y, w, h, i):
        super(Option, self).__init__(x, y, w, h)
        self.is_hover = False
        self.is_selected = False
        self.index = i
        self.color = (0,0,0)
        

class Menu():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.keys = pygame.key.get_pressed()

        self.bg_color = (123, 153, 232)

        self.options = []
        self.max_options = 48
        self.rect_width = 80
        self.rect_height = 80
        self.space = 20
        self.options_x_row = int(ceil(SCREEN_WIDTH / (self.rect_width + self.space)))

        self.current_index = 0 # the current rect
        self.current_selected = None # the last rect selected

        # A little magic of math to center rects on the screen
        aux = (self.rect_width + self.space) * self.options_x_row
        initial_x = (((SCREEN_WIDTH - aux) / 2) + (self.space / 2))
        x = initial_x
        y = 10
        for i in range(self.max_options):
            option = Option(x, y, self.rect_width, self.rect_height, i)
            option.color = [random.randint(0, 255) for _ in range(3)]
            self.options.append(option)
            x = x + self.rect_width + self.space
            if x > SCREEN_WIDTH - self.rect_width:
                x = initial_x
                y = y + self.rect_height + self.space

        self.options[0].is_hover = True




    def update(self):

        for option in self.options:
            pygame.draw.rect(self.screen, option.color, option)

            if option.is_hover:
                pygame.draw.rect(self.screen, HOVER_COLOR, option, 5)
                
            if option.is_selected:
                pygame.draw.rect(self.screen, SEL_COLOR, option, 5)

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    if self.current_selected is not None:
                        self.options[self.current_selected].is_selected = False

                    option = self.options[self.current_index]
                    option.is_selected = True
                    self.bg_color = option.color
                    self.current_selected = self.current_index

                if event.key == pygame.K_RIGHT:
                    self.options[self.current_index].is_hover = False
                    self.current_index += 1
                    if self.current_index == self.max_options:
                        self.current_index = 0
                    self.options[self.current_index].is_hover = True

                if event.key == pygame.K_LEFT:
                    self.options[self.current_index].is_hover = False
                    self.current_index -= 1
                    if self.current_index < 0:
                        self.current_index = self.max_options - 1
                    self.options[self.current_index].is_hover = True

                if event.key == pygame.K_UP:
                    self.options[self.current_index].is_hover = False
                    old_index = self.current_index
                    self.current_index -= self.options_x_row
                    if self.current_index < 0:                       
                        aux = self.options_x_row * ((self.max_options / self.options_x_row) + 1)
                        self.current_index += aux 
                        if self.current_index >= self.max_options:
                            self.current_index -= self.options_x_row
                    
                    self.options[self.current_index].is_hover = True


                if event.key == pygame.K_DOWN:
                    self.options[self.current_index].is_hover = False
                    old_index = self.current_index
                    self.current_index += self.options_x_row
                    if self.current_index > self.max_options:
                        self.current_index =  old_index % self.options_x_row
                    self.options[self.current_index].is_hover = True




    def main_loop(self):
        while True:
            self.screen.fill(self.bg_color)
            self.event_loop()
            self.update()

            caption = "{} - FPS: {:.2f}".format('press enter to change color', self.clock.get_fps())
            pygame.display.set_caption(caption)

            pygame.display.update()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    g = Menu()
    g.main_loop()