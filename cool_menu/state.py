import random

import pygame as pg

import util
import menu


class StateManager(object):
    """ This class control all the states of the game """
    def __init__(self):
        self.screen_size = util.screen_size
        self.caption = util.CAPTION        
        self._screen = pg.display.get_surface()
        self.screen = self._screen.convert().subsurface(0,0, self.screen_size[0], self.screen_size[1])
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.show_fps = True
        self.done = False        
        self.state_dict = {}
        self.state = None
        self.state_name = None
        self.bg_color = (0,0,0)

    def setup_states(self, state_dict, start_state):
        """ state_dict in a dict with a instance of each state of the game"""
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True

            if event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                self.toggle_show_fps(event.key)
                if event.key == pg.K_ESCAPE:
                    self.done = True

            if event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()

            self.state.handle_events(event)

    def toggle_show_fps(self, key):
        """Press f5 to turn on/off displaying the framerate in the caption."""
        if key == pg.K_F5:
            self.show_fps = not self.show_fps
            if not self.show_fps:
                pg.display.set_caption(self.caption)

    def update(self, dt):
        self.current_time = pg.time.get_ticks()
        self.state.update(dt, self.current_time)
        if self.show_fps:
            fps = self.clock.get_fps()
            with_fps = "{} - {:.2f} FPS".format(self.caption, fps)
            pg.display.set_caption(with_fps)

        if self.state.quit:
            self.done = True            
        if self.state.done:
            self.change_state()            

    def change_state(self):
        previous, self.state_name = self.state_name, self.state.next
        data = self.state.clear()
        self.state = self.state_dict[self.state_name]
        self.state.start(data, self.current_time)
        self.state.previous = previous

    def render(self):
        self.screen.fill(self.bg_color)
        self.state.render(self.screen)
        tmp = pg.transform.scale(self.screen, util.screen_size)
        self._screen.blit(tmp, (0,0))
        pg.display.update()

    def main_loop(self):
        while not self.done:
            dt = self.clock.tick(self.fps)/1000.0
            self.event_loop()
            self.update(dt)
            self.render()
            

class _State(object):
    """ Parent class for the game states. All states should inherint from it."""
    def __init__(self):
        self.quit = False
        self.done = False
        self.previous = None
        self.next = None
        self.data = {}
        self.star_time = 0.0
        self.current_time = 0.0

    def handle_events(self):
        pass

    def update(self, dt , current_time):
        pass

    def render(self, screen):
        pass

    def clear(self):
        """ Retunr the persintant data cleanup all changes. 
            For complex states this method should be overloaded"""
        self.done = False
        return self.data

    def start(self, data, star_time):
        self.star_time = star_time
        self.data = data


class RamdomBgState(_State):
    def __init__(self):
        super(RamdomBgState, self).__init__()

    def generate_triangle(self, surface):
        color = [random.randint(0, 255) for _ in range(3)]

        x1 = random.randint(0, util.screen_witdh)
        y1 = random.randint(0, util.screen_height)
        x2 = random.randint(0, util.screen_witdh)
        y2 = random.randint(0, util.screen_height)
        x3 = random.randint(0, util.screen_witdh)
        y3 = random.randint(0, util.screen_height)
        pg.draw.line(surface, color, (x1, y1), (x2, y2))
        pg.draw.line(surface, color, (x2, y2), (x3, y3))
        pg.draw.line(surface, color, (x3, y3), (x1, y1))

    def render(self, surface):
        self.generate_triangle(surface)
        self.generate_triangle(surface)
        self.generate_triangle(surface)
        
      
class MenuState(RamdomBgState):
    def __init__(self):
        super(MenuState, self).__init__()

    def set_options(self, options):     
        self.menu = menu.Menu(options, 50, 50)

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            self.menu.handle_events(event.key)
            if event.key == pg.K_ESCAPE:
                self.quit = True

    def update(self, dt, current_time):
        self.menu.update(dt)

    def render(self, surface):
        super(MenuState, self).render(surface)
        self.menu.render(surface)
    



class MainMenuState(MenuState):    

    def __init__(self):
        super(MainMenuState, self).__init__()
        self.options = [
            {"text":"Play", "nested": False, "activate": self.play},
            {"text":"Settings", "nested": False, "activate": self.settings},
            {"text":"Credits", "nested": False, "activate": self.credits},
            {"text":"Quit", "nested": False, "activate": self.exit}
        ]
        self.set_options(self.options)

    def start(self, data, start_time):
        self.set_options(self.options)

    def play(self):        
        print("play func have to be implemented")

    def settings(self):
        self.done = True
        self.next = "Settings"

    def credits(self):
        self.done = True
        self.next = "Credits"

    def exit(self):
        self.quit = True

class SettingsState(MenuState):
    def __init__(self):
        super(SettingsState, self).__init__()
        self.options = [
            {
                "text":"Window size",
                "nested": True,
                "options": ["480x400", "800x600", "1024x768"],    
                "activate": self.change_window_size
            },
            {
                "text":"Fullscreen", 
                "nested": True,
                "options": ["Yes", "No"],    
                "activate": self.toggle_fullscreen
            },
            {"text":"Back", "nested": False, "activate": self.back}
        ]
        self.set_options(self.options)

    def start(self, data, start_time):
        self.set_options(self.options)

    def back(self):
        self.done = True
        self.next = "MainMenu"

    def change_window_size(self, size):
        # type of size is srt '800x600'
        size = size.split('x')
        size = int(size[0]), int(size[1])
        util.chage_window_size(size)



    def toggle_fullscreen(self, yesno):
        if yesno == 'Yes':
            util.toogle_fullscreen(True)
        else:
            util.toogle_fullscreen(False)


class CreditsState(RamdomBgState):
    def __init__(self):
        super(CreditsState, self).__init__()       
        self.msn = pg.sprite.Group()
        self.credits_msn = util.credits_msn
        self.generate_text()

    def generate_text(self):
        lines = self.credits_msn.split('\n')
        size = width, height = util.screen_witdh, util.screen_height

        y = 50
        line_height = 40
        for line in lines:
            if line is not '':
                line_rendered = pg.sprite.Sprite(self.msn)
                l = util.font.render(line, 1, (255,255,255))
                rect = l.get_rect(centerx=width/2, centery=y+line_height)
                line_rendered.image = l
                line_rendered.rect = rect
            y += line_height

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.quit = True
            self.back()

    def back(self):
        self.done = True
        self.next = "MainMenu"

    def render(self, surface):
        super(CreditsState, self).render(surface)
        self.msn.draw(surface)