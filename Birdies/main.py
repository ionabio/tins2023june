import pygame
import random
import math
from bird import Bird
from intro import Intro
from game import Game
from outtro import Outtro

#initialize pygame
pygame.init()

screenSize = (827/2, 932/2)

screen = pygame.display.set_mode(screenSize[0:2])
pygame.display.set_caption('Birdies')
background = pygame.transform.scale(pygame.image.load('assets/sky.png'), screenSize[0:2])
field = pygame.transform.scale(pygame.image.load('assets/field.png'), screenSize[0:2])
tree = pygame.transform.scale(pygame.image.load('assets/tree.png'), (int(827/2*0.5), int(932/2*0.5)))

gameStage = 0
# 0 = intro
# 1 = game
# 2 = outro

seed = pygame.transform.scale(pygame.image.load('assets/seed.png'), (int(827*0.01), int(932*0.005)))
seeds = pygame.sprite.Group()
for i in range(20):
    seedSprite = pygame.sprite.Sprite()
    seedSprite.image = seed
    seedSprite.rect = seedSprite.image.get_rect()
    seedSprite.rect.x = random.randint(int(screenSize[0]*.1), int(screenSize[0]*.5))
    seedSprite.rect.y = random.randint(int(screenSize[1]*.5), int(screenSize[1]*.7))
    seeds.add(seedSprite)

def setupBG():
    screen.fill((255, 255, 255))
    #load background image
    screen.blit(background, (0, 0))
    screen.blit(field, (0, 0))
    screen.blit(tree, (screenSize[0]-200, screenSize[1]/2-100))
    if (gameStage == 0):
        seeds.draw(screen)


def resetGame():
    birds = pygame.sprite.Group()
    grid = pygame.sprite.Group()
    intro = Intro(screenSize, birds, screen)
    game = Game(screenSize, birds, screen)
    outtro = Outtro(screenSize, birds, screen, field, tree)
    return (birds, grid, intro, game, outtro)

(birds, grid, intro, game, outtro) = resetGame()

def runOutro():
    return

#run until the user asks to quit
running = True
resetGame()
while running:
    #did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    setupBG()
    #switch gameStage
    if gameStage == 0:
        if (intro.runIntro()) : gameStage = 1
    elif gameStage == 1:
        if (game.runGame()) : gameStage = 2
    elif gameStage == 2:
        if (outtro.runOuttro()) : 
            gameStage = 0
            (birds, grid, intro, game, outtro) = resetGame()

    pygame.display.flip()

pygame.quit()



