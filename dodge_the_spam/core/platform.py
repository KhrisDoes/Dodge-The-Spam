import pygame

class Platform(pygame.Rect):

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.ySpeed = 200




    def gravity(self, timedelta):
        self.y += self.ySpeed * timedelta

