import pygame
from src.food import Food

GREEN = (0, 255, 0)


class Snake():
    def __init__(self):
        self.blocksize = 20
        self.xposition = 12
        self.yposition = 10
        self.xspeed = 1
        self.yspeed = 0
        self.xgridposition = 150 + self.xposition*self.blocksize
        self.ygridposition = 100 + self.yposition*self.blocksize
        self.total = 0
        self.tail = []
        self.fullsnake = []
        
    def draw(self,screen):
        for i in range (len(self.fullsnake)):
            pygame.draw.rect(screen, GREEN,[150+self.fullsnake[i][0]*self.blocksize, 100+ self.fullsnake[i][1]*self.blocksize, self.blocksize, self.blocksize], 1)
        pygame.draw.rect(screen, GREEN,[150+self.xposition*self.blocksize, 100+ self.yposition*self.blocksize, self.blocksize, self.blocksize], 1)

    def updatePosition(self):
        self.tail.append([self.xposition, self.yposition])
        self.tail = self.tail[len(self.tail)-self.total-1:]
        self.xgridposition = 150 + self.xposition*self.blocksize
        self.ygridposition = 100 + self.yposition*self.blocksize
                
        
    def movesnake(self):
        if (self.total == 1):
            self.fullsnake[0] = [self.xposition,self.yposition]
        elif (self.total > 1):
            for i in range(self.total-1):
                self.fullsnake[self.total-i-1] = self.fullsnake[self.total-i-2]
            self.fullsnake[0] = [self.xposition,self.yposition]
        self.yposition += self.yspeed
        self.xposition += self.xspeed
            

    def CanSnakeMove(self):
        if self.xgridposition <= 140 or self.xgridposition >= (660 - self.blocksize):
            return False
        elif self.ygridposition <= 90 or self.ygridposition >= (510-self.blocksize):
            return False
        else:
            return True

    def eatfood(self, food):
        if self.xposition == food.spawnx and self.yposition == food.spawny:
            return True
        return False


        
        
