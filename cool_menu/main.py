import pygame

from scene import SceneManager, MainMenuScene


def main():
    manager = SceneManager()
    scene = MainMenuScene(manager)
    manager.change_scene(scene)
    manager.loop()



if __name__ == '__main__':
    pygame.init()
    main()