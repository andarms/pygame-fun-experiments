import pygame as pg

import util

class Option(pg.sprite.Sprite):
    """simple menu option"""
    def __init__(self, text, activate, arg, x, y, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.selected = False
        self.normal_image = util.font.render(text, 1, (255, 255, 255))
        self.highlight_image = util.big_font.render(text, 1, (255, 255, 0))
        self.image = self.normal_image
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.curr_x = -100 # to initial movement
        self.dest_x = x

        self.activate = activate
        self.arg = arg

    def update(self, dt):
        if self.curr_x < self.dest_x:
            self.curr_x += (self.dest_x - self.curr_x) / 5.0
            self.rect.x  = self.curr_x


    def toogle_select(self):
        if not self.selected:
            self.selected = True
            topleft = self.rect.topleft
            self.image = self.highlight_image
            self.rect = self.image.get_rect()
            self.rect.topleft = topleft
            self.curr_x = -100
        else:
            self.selected = False
            topleft = self.rect.topleft
            self.image = self.normal_image
            self.rect = self.image.get_rect()           
            self.rect.topleft = topleft

    def trigger(self):
        if self.arg:
            self.activate(self.arg)
        else:
            self.activate()


class NestedOption(pg.sprite.Sprite):
    def __init__(self, text, activate, options, x , y, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.text = text
        self.options = []
        for option in options:
            txt = self.text + ': < ' + option + ' >'
            # text value is passed as activate function arg
            Opt = Option(txt, activate, option, x, y)
            self.options.append(Opt)

        self.curr_inx = 0
        self.selected = False
        self.image = self.options[self.curr_inx].image
        self.rect = self.options[self.curr_inx].rect
        self.activate = activate
        self.rect.y = y
        self.curr_x = -100 # to initial movement
        self.dest_x = x

    def update(self, dt):
        if self.curr_x < self.dest_x:
            self.curr_x += (self.dest_x - self.curr_x) / 5.0
            self.rect.x  = self.curr_x

    def toogle_select(self):
        if not self.selected:
            self.selected = True
            topleft = self.options[self.curr_inx].rect.topleft
            self.image = self.options[self.curr_inx].highlight_image
            self.rect = self.image.get_rect()
            self.rect.topleft = topleft
            self.curr_x = -100
        else:
            self.selected = False
            topleft = self.rect.topleft
            self.image = self.options[self.curr_inx].normal_image
            self.rect = self.image.get_rect()           
            self.rect.topleft = topleft

    def trigger(self):
        self.options[self.curr_inx].trigger()

    def change_index(self, change):
        self.curr_inx += change

        if self.curr_inx == len(self.options):
            self.curr_inx = 0
        elif self.curr_inx < 0:
            self.curr_inx = len(self.options) - 1

        topleft = self.options[self.curr_inx].rect.topleft
        self.image = self.options[self.curr_inx].highlight_image
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
        # self.curr_x = -100


class Menu(object):
    """docstring for Menu"""
    def __init__(self, options, x, y):
        self.options = []
        self.options_sprites = pg.sprite.Group()
        self.x = x
        self.y = y
        
        self.generate_options(options)

        self.curr_inx = 0
        self.options[self.curr_inx].toogle_select()


    def generate_options(self, options):
        y = self.y
        line_height = 50
        for option in options:
            text = option['text']
            activate = option['activate']
            nested = option['nested']
            if nested:
                opts = option['options'] 
                Op = NestedOption(text, activate, opts, self.x, y, self.options_sprites)
            else:
                Op = Option(text, activate, None, self.x, y, self.options_sprites)
            
            self.options.append(Op)
            y += line_height

    def handle_events(self, key):
        if key == pg.K_DOWN:
            self.options[self.curr_inx].toogle_select()
            if self.curr_inx < len(self.options) - 1:
                self.curr_inx += 1
            else:
                self.curr_inx = 0
            self.options[self.curr_inx].toogle_select()

        if key == pg.K_UP:
            self.options[self.curr_inx].toogle_select()
            if self.curr_inx > 0:
                self.curr_inx -= 1
            else:
                self.curr_inx = len(self.options) - 1
            self.options[self.curr_inx].toogle_select()

        if key == pg.K_LEFT:
            if isinstance(self.options[self.curr_inx], NestedOption):
                self.options[self.curr_inx].change_index(-1)                

        if key == pg.K_RIGHT:
            if isinstance(self.options[self.curr_inx], NestedOption):
                self.options[self.curr_inx].change_index(1)


        if key == pg.K_RETURN:
            self.options[self.curr_inx].trigger()


    def update(self, dt):
        self.options_sprites.update(dt)

    def render(self, surface):
        self.options_sprites.draw(surface)