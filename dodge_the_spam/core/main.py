import pygame, os
from pygame.locals import *
from pygame.compat import geterror
import player
import platform
import random


base_dir = "/home/chris/dev-projects/DodgeTheSpam/dodge_the_spam"

# core_dir = os.path.split(os.path.abspath(__file__))[0]

resources_dir = os.path.join(base_dir, 'resources')

class Game:

    WIDTH, HEIGHT = 0, 0

    def __init__(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height
        self.timedelta = 0
        self.counting_seconds = 0
        self.start_time = 0
        self.counting_time = 0

        self.HIGH_SCORE = 0



        # TODO: do something other than printing when collision occurs
        #       change background image


        pygame.init()
        self.running = True



        self.basic_font = pygame.font.SysFont(None, 32)

        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Dodge the spam!")
        self.background = pygame.Surface(self.screen.get_size()).convert()

        self.background.fill((255,255,255))

        self.player = player.Player(self.WIDTH / 2, self.HEIGHT - 150, 30, 30)

        (player_image, player_image_rect) = self.load_image("player_icon.png")
        (platform_image, platform_image_rect) = self.load_image("spam.png")
        
        self.player.PLAYER_IMAGE = player_image
        self.player.PLAYER_IMAGE = pygame.transform.scale(self.player.PLAYER_IMAGE, (self.player.width, self.player.height))
        self.player.PLAYER_IMAGE_RECT = player_image_rect
 
        platform.Platform.SPAM_IMAGE = platform_image
        platform.Platform.SPAM_IMAGE = pygame.transform.scale(platform.Platform.SPAM_IMAGE, (50, 50))
        platform.Platform.SPAM_IMAGE_RECT = platform_image_rect        

        self.screen.blit(self.background, (0,0))

        self.platforms = []
        self.init_platforms()


    def init_platforms(self):
        for i in range(10):
            self.platforms.append(platform.Platform(random.randint(0, self.WIDTH), random.randint(-350, 0), 50, 50))

    def reset_platforms(self):
        for i in range(10):
            self.platforms[i] = platform.Platform(random.randint(0, self.WIDTH), random.randint(-350, 0), 50, 50)

    def move_left(self):
        self.player.x -= self.player.xSpeed * self.timedelta

    def move_right(self):
        self.player.x += self.player.xSpeed * self.timedelta

    def jump(self):
        self.player.y -= self.player.ySpeed * 2 * self.timedelta


    def gravity(self, rect):
        rect.y += rect.ySpeed * self.timedelta


    def update_player_position(self):
        if self.player.moving_left:
            self.move_left()
        elif self.player.moving_right:
            self.move_right()

        if self.player.jumping:
            self.jump()

        self.gravity(self.player)

        if self.player.y > self.HEIGHT or self.player.y < 0 or self.player.x < 0 or self.player.x > self.WIDTH:
            self.restart()




    def restart(self):


        if self.HIGH_SCORE < float(self.counting_seconds):
            self.HIGH_SCORE = float(self.counting_seconds)

        self.start_time = pygame.time.get_ticks()
        self.counting_time = pygame.time.get_ticks() - self.start_time
        self.timedelta = self.clock.tick(60)
        self.timedelta /= 1000
        self.player.x = self.WIDTH / 2
        self.player.y = self.HEIGHT - 150
        self.reset_platforms()




    def on_collision(self, platform):
        if self.player.colliderect(platform):
            self.restart()


    def on_render(self):

        self.background.fill((255, 255, 255))

        counting_string = "%s" % (self.counting_seconds)

        score = self.basic_font.render("Score: " + counting_string, True, (255, 0, 0), (255,255,255))


        self.update_player_position()

        self.screen.blit(self.background, (0,0)) # Order matters

        # Speed up player
        # self.player.xSpeed += float(counting_string)






        for obstacle in self.platforms:

            # Speed up obstacle
            obstacle.ySpeed += float(counting_string) / 10

            obstacle.gravity(self.timedelta)

            self.reset(obstacle)
            # pygame.draw.rect(self.background, (30, 40, 50), obstacle)
            self.screen.blit(obstacle.SPAM_IMAGE, (obstacle.x, obstacle.y))


        # Draw player image
        self.screen.blit(self.player.PLAYER_IMAGE, (self.player.x, self.player.y))

        # Draw score
        self.screen.blit(score, (0,0))


        pygame.display.update()

    def on_event(self, event):

        if event.type == QUIT:
            self.running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.running = False
            if event.key == K_LEFT:
                self.player.moving_left = True
            elif event.key == K_RIGHT:
                self.player.moving_right = True
            if event.key == K_UP or event.key == K_SPACE:
                self.player.jumping = True
        elif event.type == KEYUP:
            if event.key == K_LEFT:
                self.player.moving_left = False
            elif event.key == K_RIGHT:
                self.player.moving_right = False
            if event.key == K_UP or event.key == K_SPACE:
                self.player.jumping = False




    def on_loop(self):
        pass


    def reset(self, platform):
        if platform.y > self.HEIGHT:
            platform.y = -15
            platform.x = random.randint(0, self.WIDTH)

    # functions to create our resources
    def load_image(self, name, colorkey=None):
        fullname = resources_dir + "/" + name
        print(fullname)
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

        self.start_time = pygame.time.get_ticks()

        while self.running:
            self.counting_time = pygame.time.get_ticks() - self.start_time
            self.timedelta = self.clock.tick(60)
            self.timedelta /= 1000

            # Check for collisions
            for platform in self.platforms:
                self.on_collision(platform)

            # Handle events
            for event in pygame.event.get():
                self.on_event(event)

            self.counting_seconds = str((self.counting_time % 60000) / 1000).zfill(2)
            self.on_render()


        print("Highest score:", self.HIGH_SCORE, sep=' ')
        pygame.quit()


if __name__ == "__main__":
    game = Game(800, 600)
    game.main()

