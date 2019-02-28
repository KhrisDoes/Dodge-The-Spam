#!/usr/bin/env python3
import pygame, os
from pygame.locals import *
from pygame.compat import geterror
import player
import platform
import random
import sys

import neat
import pickle

# core_path = os.path.dirname(os.path.realpath(__file__))

if getattr(sys, 'frozen', False):
    # frozen
    core_path = os.path.dirname(sys.executable)
else:
    # unfrozen
    core_path = os.path.dirname(os.path.realpath(__file__))


folders_path = os.path.normpath(core_path + os.sep + os.pardir )
resources_dir = os.path.join(folders_path, "resources")
core_dir = os.path.join(folders_path, "core")


GENERATION = 0
MAX_FITNESS = 0
BEST_GENOME = 0
FPS = 60



class Game:

    WIDTH, HEIGHT = 0, 0

    def __init__(self, width, height):
       pass


    def init(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height
        self.timedelta = 0
        self.counting_seconds = 0
        self.start_time = 0
        self.counting_time = 0

        self.HIGH_SCORE = 0
        self.GENOME_SCORE = 0



        # TODO: change background image
        #       GENOME_SCORE is not working properly          

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
        self.player.x -= self.player.xSpeed * self.timedelta * 2

    def move_right(self):
        self.player.x += self.player.xSpeed * self.timedelta * 2

    def jump(self):
        self.player.y -= self.player.ySpeed * 2 * self.timedelta * 2

    def move_down(self):
        self.player.y += self.player.ySpeed * 2 * self.timedelta * 2

    def gravity(self, rect):
        rect.y += rect.ySpeed * self.timedelta * 2


    def update_player_position(self):
        if self.player.moving_left:
            self.move_left()
        elif self.player.moving_right:
            self.move_right()

        if self.player.jumping:
            self.jump()
        elif self.player.moving_down:
            self.move_down()

        self.gravity(self.player)

        x = 0
        if self.player.y > self.HEIGHT or self.player.y < 0 or self.player.x < 0 or self.player.x > self.WIDTH:
            x = float(self.counting_seconds)
            self.GENOME_SCORE -= 1000

        return x 



    def restart(self):


        if self.HIGH_SCORE < float(self.counting_seconds):
            self.HIGH_SCORE = float(self.counting_seconds)

        self.start_time = pygame.time.get_ticks()
        self.counting_time = pygame.time.get_ticks() - self.start_time
        self.timedelta = self.clock.tick(FPS)
        self.timedelta /= 1000
        self.player.x = self.WIDTH / 2
        self.player.y = self.HEIGHT - 150
        self.reset_platforms()
        self.GENOME_SCORE = 0



    def on_collision(self, platform):
        x = 0
        if self.player.colliderect(platform):
            x = float(self.counting_seconds)
            # self.restart()
        return x


    def on_render(self):

        self.background.fill((255, 255, 255))

        counting_string = "%s" % (self.counting_seconds)

        score = self.basic_font.render("Score: " + counting_string, True, (255, 0, 0), (255,255,255))


        self.screen.blit(self.background, (0,0)) # Order matters

        # Speed up player
        # self.player.xSpeed += float(counting_string)


        for obstacle in self.platforms:

            # Speed up obstacle
            # obstacle.ySpeed += float(counting_string) / 10 Too hard for the AI currently, tryng to train it in simpler environments

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
            elif event.key == K_DOWN:
                self.player.moving_down = True

        elif event.type == KEYUP:
            if event.key == K_LEFT:
                self.player.moving_left = False
            elif event.key == K_RIGHT:
                self.player.moving_right = False
            if event.key == K_UP or event.key == K_SPACE:
                self.player.jumping = False
            elif event.key == K_DOWN:
                self.player.moving_down = False




    def on_loop(self):
        pass


    def has_platform_passed_player(self, platform):
        if platform.y > self.player.y:
#            print("PASSED")
            if platform.passed_player == False:
                platform.passed_player = True
                self.GENOME_SCORE += 10


    def reset(self, platform):
        if platform.y > self.HEIGHT:
            platform.y = -15
            platform.x = random.randint(0, self.WIDTH)
            platform.passed_player = False
            # GENOME_SCORE += 1

    # functions to create our resources
    def load_image(self, name, colorkey=None):
        # fullname = resources_dir + "/" + name
        fullname = resources_dir + os.sep + name
#        print(fullname)
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

    def eval_genomes(self, genomes, config):
        i = 0
        global GENERATION, MAX_FITNESS, BEST_GENOME
        GENERATION = GENERATION + 1
        for genome_id, genome in genomes:
            genome.fitness = self.main(genome, config)

            print("Gen : %d Genome # : %d  Fitness : %f Max Fitness : %f"%(GENERATION,i,genome.fitness, MAX_FITNESS))
            if genome.fitness >= MAX_FITNESS:
                MAX_FITNESS = genome.fitness
                BEST_GENOME = genome
            self.GENOME_SCORE = 0
            i+=1

    def main(self, genome, config):

        self.init(800, 600)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        self.start_time = pygame.time.get_ticks()
        #distances = []
        while self.running:
            self.counting_time = pygame.time.get_ticks() - self.start_time
            self.timedelta = self.clock.tick(FPS)
            self.timedelta /= 1000
            inputs = []
            for platform in self.platforms:
                inputs.append(platform.x)
                inputs.append(platform.y)
                self.has_platform_passed_player(platform)
                #plat_x = (platform.x + platform.width ) / 2
                #plat_y = (platform.y + platform.height) / 2
                # distances.append()
            inputs.append(self.player.x)
            inputs.append(self.player.y)
            print(inputs)
            x = 0
            # Check for collisions
            for platform in self.platforms:
                x = self.on_collision(platform)
                if x != 0:
                    print("x = ", x, ", genome_score = " , self.GENOME_SCORE)
                    return x / 10 + self.GENOME_SCORE 

            x = self.update_player_position()

            if x != 0:
                print("x = ", x, ", genome_score = " , self.GENOME_SCORE)
                return x / 10 + self.GENOME_SCORE

            output = net.activate(inputs)
#            print("Output: ", output)

            if output[0] >= 0.5:
                self.jump()
            elif output[1] >= 0.5:
                self.move_left()
            if output[2] >= 0.5:
                self.move_right()
            if output[3] >= 0.5:
                self.move_down() 

            self.counting_seconds = str((self.counting_time % 60000) / 1000).zfill(2)
            self.on_render()
#            self.clock.tick(FPS)


        print("Highest score:", self.HIGH_SCORE, sep=' ')
        pygame.quit()

    def run(self):
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         'config')
        pop = neat.Population(config)
        stats = neat.StatisticsReporter()
        pop.add_reporter(stats)
        winner = pop.run(self.eval_genomes, 2)
        outputFile = "bestGenome/winner.p"
        with open(outputFile, 'wb') as pickle_file:
            pickle.dump(all, pickle_file)


if __name__ == "__main__":
    game = Game(800, 600)
    game.run()





