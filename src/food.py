import random
import pygame

RED = (255,0,0)

class Food():
    def __init__(self):
        self.spawnx = random.randint(0,24)
        self.spawny = random.randint(0,19)
        self.colour = RED
        self.blocksize = 20

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, [150 + self.spawnx*self.blocksize, 100 + self.spawny*self.blocksize, self.blocksize, self.blocksize], 0)
