import pygame

class Platform(pygame.Rect):

    def __init__(self, x, y, width, height):
        super.__init__(x, y, width, height)


    def gravity(self):
        pass