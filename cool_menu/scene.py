import random
import sys

import pygame

from util import *

bg_color = (0,0,0)

class SceneManager:

    def __init__(self):
        self.screen_size = (800,600)
        flags = pygame.DOUBLEBUF|pygame.HWSURFACE
        self._screen = pygame.display.set_mode(self.screen_size, flags)
        self.screen = self._screen.convert().subsurface(0,0,800,600)

        self.scene = None
        self.clock = pygame.time.Clock()
        self.fps = 60

    def loop(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quit()

            self.scene.handle_events()
            self.scene.update()
            self.scene.render(self.screen)

            caption = "{} - FPS: {:.2f}".format('scene manager', self.clock.get_fps())
            pygame.display.set_caption(caption)

            tmp = pygame.transform.scale(self.screen, self.screen_size)
            self._screen.blit(tmp, (0,0))

            pygame.display.update()
            self.clock.tick(self.fps)


    def change_scene(self, scene):
        self.scene = scene

    def quit(self):
        pygame.quit()
        sys.exit()


class Scene(object):
    def __init__(self, manager):
        self.manager = manager
        self.back_scene = None
        self.hold = False

    def handle_events(self):
        raise NotImplemented("handle_events func have to be implemented")

    def update(self):
        raise NotImplemented("update func have to be implemented")

    def render(self, screen):
        raise NotImplemented("render func have to be implemented")

    def back(self):
        self.manager.change_scene(self.back_scene)





class MenuScene(Scene):
    def __init__(self, manager):
        super(MenuScene, self).__init__(manager)

        self.options = {}
        self.rendered_options = []
        self.curr_index = 0
        self.hold = False
        self.first = True

    def prepare_options(self):
        x = y = 20
        line_height = 50
        for text, func in self.options:
            if type(func) == list:
                op = NestedOption(text, func, x, y)
            else:
                op = Option(text, func, x, y)

            self.rendered_options.append(op)
            y += line_height

    def generate_background(self, screen):
        c1 = [random.randint(0, 255) for _ in range(3)]
        c2 = [random.randint(0, 255) for _ in range(3)]
        c3 = [random.randint(0, 255) for _ in range(3)]

        x1, y1 = random.randint(0, SCREEN_WITDH), random.randint(0, SCREEN_HEIGHT)
        x2, y2 = random.randint(0, SCREEN_WITDH), random.randint(0, SCREEN_HEIGHT)
        x3, y3 = random.randint(0, SCREEN_WITDH), random.randint(0, SCREEN_HEIGHT)
        pygame.draw.line(screen, c1, (x1, y1), (x2, y2))
        pygame.draw.line(screen, c2, (x2, y2), (x3, y3))
        pygame.draw.line(screen, c3, (x3, y3), (x1, y1))



    def handle_events(self):
        key = pygame.key.get_pressed()
        o = self.rendered_options[self.curr_index]

        if not self.hold and not self.first:
            if key[pygame.K_RETURN]:
                o.func()

            if key[pygame.K_DOWN]:
                self.curr_index += 1
                if self.curr_index >= len(self.rendered_options):
                    self.curr_index = 0

            if key[pygame.K_UP]:
                self.curr_index -= 1
                if self.curr_index < 0:
                    self.curr_index = len(self.rendered_options) - 1

            if key[pygame.K_LEFT]:
                if isinstance(o, NestedOption):
                    o.handle_events(-1)

            if key[pygame.K_RIGHT]:                
                if isinstance(o, NestedOption):
                    o.handle_events(1)


        keys = (key[pygame.K_UP], key[pygame.K_DOWN], key[pygame.K_RETURN],
               key[pygame.K_LEFT], key[pygame.K_RIGHT])
        self.hold =  any(keys)
        self.first = False # wait to pass here more that once

    def update(self):
        self.rendered_options[self.curr_index].highlighted = True
        for option in self.rendered_options:
            option.update()
        self.rendered_options[self.curr_index].highlighted = False

    def render(self, screen):
        screen.fill(bg_color)
        self.generate_background(screen)      
        self.generate_background(screen)      
        self.generate_background(screen)      
        for option in self.rendered_options:
            option.render(screen)



class MainMenuScene(MenuScene):    

    def __init__(self, manager):
        super(MainMenuScene, self).__init__(manager)

        self.options = [
            ('Play', self.play),
            ('Settings', self.settings),
            ('Credits', self.credits),
            ('Quit', self.manager.quit)
        ]

        self.prepare_options()

    def play(self):        
        raise NotImplemented("play func have to be implemented")

    def settings(self):
        scene = SettingsScene(self.manager)
        scene.back_scene = self
        self.manager.change_scene(scene)

    def credits(self):
        scene = CreditsScene(self.manager)
        scene.back_scene = self
        self.manager.change_scene(scene)

class SettingsScene(MenuScene):
    def __init__(self, manager):
        super(SettingsScene, self).__init__(manager)

        self.options = [
            ('Window size:', [
                    ('480x400', self.change_window_size),
                    ('800x600', self.change_window_size),
                    ('1024x768', self.change_window_size)
                ]),
            ('Fullscreen:', [
                    ('yes', self.toggle_fullscreen),
                    ('no', self.toggle_fullscreen)
                ]),
            ('Back', self.back)
        ]
        self.prepare_options()

    def change_window_size(self, size):
        # type of size is srt '800x600'
        size = size.split('x')
        size = w, h = int(size[0]), int(size[1])
        flags = self.manager._screen.get_flags()
        self.manager._screen = pygame.display.set_mode(size, flags)
        self.manager.screen_size = size



    def toggle_fullscreen(self, yesno):
        if yesno == 'yes':
            flags = pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF 
            self._screen = pygame.display.set_mode(self.manager.screen_size, flags)
        else:
            flags = pygame.DOUBLEBUF|pygame.HWSURFACE
            self._screen = pygame.display.set_mode(self.screen_size, flags)


class CreditsScene(Scene):
    def __init__(self, manager):
        super(CreditsScene, self).__init__(manager)

        self.credits = """Created by Adrian Manjarrez
@andarms


A simple sample to test a multi level menu.
with a scene manager feature.


Press Spacebar to back"""

        self.lines = self.credits.split('\n')
        size = width, height = self.manager.screen.get_size()
        self.image = pygame.Surface(size)
        self.image.fill(bg_color)
        self.rect = self.image.get_rect()
        self.rect.x = 0

        self.dest_y = -height
        self.y = height

        y = 150
        line_height = 40
        for line in self.lines:
            if line is not '':
                l = font.render(line, 1, (255,255,255))
                rect = l.get_rect(centerx=width/2, centery=y+line_height)
                self.image.blit(l, rect)
            y += line_height

    def handle_events(self):
        key = pygame.key.get_pressed()

        if not self.hold:
            if key[pygame.K_SPACE]:
                self.back()


        self.hold =  key[pygame.K_SPACE]

    def update(self):
        self.y -= (self.y - self.dest_y)/500
        self.rect.y = int(self.y)

    def render(self, screen):
        screen.fill(bg_color)
        screen.blit(self.image, self.rect)