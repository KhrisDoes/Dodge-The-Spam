import pygame

class Player(pygame.Rect):


    def __init__(self, x, y, width, height):

        super().__init__(x, y, width, height)

        self.xSpeed = 360
        self.ySpeed = 200

        self.moving_left = False
        self.moving_right = False




    def move_left(self, timedelta):
        self.x -= self.xSpeed * timedelta

    def move_right(self, timedelta):
        self.x += self.xSpeed * timedelta

    def jump(self):
        self.y -= self.ySpeed


    def gravity(self):
        pass


