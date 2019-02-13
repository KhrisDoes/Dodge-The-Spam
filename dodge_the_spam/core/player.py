import pygame
import os

class Player(pygame.Rect):


    def __init__(self, x, y, width, height):

        super().__init__(x, y, width, height)
        self.PLAYER_IMAGE = pygame.image.load(os.path.join("resources/player_icon.png")).convert()
        self.PLAYER_IMAGE = pygame.transform.scale(self.PLAYER_IMAGE, (width, height))



        self.xSpeed = 360
        self.ySpeed = 200

        self.moving_left = False
        self.moving_right = False
        self.jumping = False







