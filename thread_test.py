from threading import Thread
import time
import sys

import pygame


class Counter (Thread):   
    done = False     

    def run(self):
        counter = 0
        for i in xrange(6):
            counter += 2
            time.sleep(.5)
        print counter
        self.done = True



def main():
    pygame.init()

    size = width, height = 320, 240

    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    c = Counter()
    c.start()
    bg_color = (255,255,255)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        screen.fill(bg_color)

        if c.done:
            bg_color = (123, 234, 231)

        caption = "{} - FPS: {:.2f}".format('CAPTION',clock.get_fps())
        pygame.display.set_caption(caption)
        pygame.display.flip()
        clock.tick(60)



if __name__ == '__main__':
    main()