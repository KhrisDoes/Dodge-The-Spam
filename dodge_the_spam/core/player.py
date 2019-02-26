import pygame
import os

class Player(pygame.Rect):


    def __init__(self, x, y, width, height):

        super().__init__(x, y, width, height)
        # self.PLAYER_IMAGE = pygame.image.load(os.path.join("resources/player_icon.png")).convert()
        # self.PLAYER_IMAGE = pygame.transform.scale(self.PLAYER_IMAGE, (width, height))

        self.PLAYER_IMAGE = None
        self.PLAYER_IMAGE_RECT = None


        self.xSpeed = 320
        self.ySpeed = 200

        self.moving_left = False
        self.moving_right = False

	# Experimental
        self.moving_down = False

        self.jumping = False







