import pygame
import random
import math
from bird import Bird
from grid import Grid
    
class Game:
    def __init__(self, screenSize, birds, screen):
        self.screenSize = screenSize
        self.screen = screen
        self.introStage = 0
        self.birds = birds
        self.grid = Grid(birds, screen)
        self.gameInitiated = False
        self.timer = 0
    
    def initiateGame(self):
        # put birds in a grid of 4 x 4
        birdSpacing = 50
        trapTLX = 20
        trapTLY = self.screenSize[1] / 2
        for bird in self.birds:
            index = self.birds.sprites().index(bird)
            col = (index % 4) 
            row = (index // 4)
            bird.moveToTrap(col * birdSpacing + trapTLX + (3- row) * 10, row * birdSpacing + trapTLY, self.screenSize[1])
            bird.stopFlap()
        return True
    def checkInput(self):
        #if mouse over a bird, make it flap
        numberOfFlyingBirds = 0
        for bird in self.birds:
             if (bird.isFlying()):
                 numberOfFlyingBirds += 1
        for bird in self.birds:
            if bird.rect.collidepoint(pygame.mouse.get_pos()):
                bird.flap(pygame.mouse.get_pressed()[0])
            else:
                bird.stopFlap(numberOfFlyingBirds/len(self.birds.sprites()))
        return numberOfFlyingBirds == len(self.birds.sprites())
    
    def drawChart(self):
        radius = 50
        numberOfFlyingBirds = 0
        for bird in self.birds:
             if (bird.isFlying()):
                 numberOfFlyingBirds += 1
        percentage = numberOfFlyingBirds/len(self.birds.sprites())
        pygame.draw.circle(self.screen, (0,0,0), (self.screenSize[0]-radius-12, self.screenSize[1]-radius-12), radius+4)
        pygame.draw.arc(self.screen, (13,121,242), (self.screenSize[0]-radius*2-11, self.screenSize[1]-radius*2-11, radius*2, radius*2)
        , 0, 3.14*2*percentage, radius)


    def runGame(self):
        if (self.gameInitiated == False):
            self.gameInitiated = self.initiateGame()
        self.drawChart()
        self.birds.update()
        self.grid.draw()
        self.birds.draw(self.screen)
        return self.checkInput()
