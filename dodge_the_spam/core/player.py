import pygame

class Player(pygame.Rect):


    def __init__(self, x, y, width, height):

        super().__init__(x, y, width, height)

        self.xSpeed = 1
        self.ySpeed = 1


    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def jump(self):
        self.y -= 1


    def gravity(self):
        pass


