import pygame
import random
import math

# a py class list of pygame lines
class Grid():
    def __init__(self, birds, screen):
        self.birds = birds
        self.screen = screen
    def draw(self):
        for i in range(4):
            for j in range(4):
                index = i * 4 + j
                bird = self.birds.sprites()[index]
                trapColor = (0,0,0)
                if (i != 0): # is not top row
                    topBird = self.birds.sprites()[index - 4]
                    pygame.draw.line(self.screen, trapColor, bird.rect.center, topBird.rect.center, 1)
                if (j != 0): # is not left column
                    leftBird = self.birds.sprites()[index - 1]
                    pygame.draw.line(self.screen,trapColor, bird.rect.center, leftBird.rect.center, 1)
        
