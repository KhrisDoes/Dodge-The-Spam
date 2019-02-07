import pygame, os
from pygame.locals import *
from pygame.compat import geterror
import player


main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

class Game:

    WIDTH, HEIGHT = 0, 0

    def __init__(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height

        pygame.init()
        self.running = True

        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Dodge the spam!")
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((255,255,255))

        self.player = player.Player(self.WIDTH / 2, self.HEIGHT - 50, 30, 30)

        self.screen.blit(self.background, (0,0))



    # TODO: smooth movement


    def on_render(self):

        pygame.draw.rect(self.background, (30, 40, 50), self.player)
        self.screen.blit(self.background, (0,0))

        pygame.display.update()

    def on_event(self, event):
        if event.type == QUIT:
            self.running = False
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                self.player.move_left()
            elif event.key == K_RIGHT:
                self.player.move_right()
            elif event.key == K_SPACE:
                self.player.jump()

        pass

    def on_loop(self):
        pass

    def on_collision(self):
        print("Collision detected!!")

    # functions to create our resources
    def load_image(self, name, colorkey=None):
        fullname = os.path.join(data_dir, name)
        try:
            image = pygame.image.load(fullname)
        except pygame.error:
            print('Cannot load image:', fullname)
            raise SystemExit(str(geterror()))
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image, image.get_rect()


    def main(self):


        while self.running:
            self.clock.tick(360)
            for event in pygame.event.get():
                self.on_event(event)
            self.on_render()

        pygame.quit()


if __name__ == "__main__":
    game = Game(800, 600)
    game.main()

