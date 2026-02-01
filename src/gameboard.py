import pygame
from src.snake import Snake

class Gameboard():
    def __init__(self, colour, blocksize):
        self.bordercolour = colour
        self.blocksize = blocksize

    def draw(self, screen):
        pygame.draw.rect(screen, self.bordercolour, [150,100,25*self.blocksize,20*self.blocksize], 1)
        
    def checkDeath(self, playersnake):
        for i in range(len(playersnake.fullsnake)):
            if playersnake.xposition == playersnake.fullsnake[i][0] and playersnake.yposition == playersnake.fullsnake[i][1]:
                return True
        if not playersnake.CanSnakeMove():
            return True
        return False
