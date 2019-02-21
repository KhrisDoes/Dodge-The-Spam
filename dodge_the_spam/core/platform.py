import pygame
import os

class Platform(pygame.Rect):

    ySpeed = 200
    SPAM_IMAGE = None
    SPAM_IMAGE_RECT = None


    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

        
       #  self.SPAM_IMAGE = pygame.image.load(os.path.join("../resources/spam.png")).convert()
       #  self.SPAM_IMAGE = pygame.transform.scale(self.SPAM_IMAGE, (width, height))




    def gravity(self, timedelta):
        self.y += self.ySpeed * timedelta

