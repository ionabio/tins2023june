import pygame
import random
import math
from bird import Bird
from grid import Grid

def transform(image, scale):
    return pygame.transform.scale(image, (int(image.get_width()*scale), int(image.get_height()*scale)))

class Intro():
    def __init__(self, screenSize, birds, screen):
        self.screenSize = screenSize
        self.screen = screen
        self.introStage = 0
        self.birds = birds
        self.grid = Grid(birds, screen)
        self.introStage = 0
        # 0 = birds fly in
        # 1 = birds talk
        # 2 = birds land to eat seeds
        # 3 = birds tell game instructions
        self.timer = 0
        self.speechBubbleInterval = 100
        

    def initBirds(self):
        self.birds.empty()
        numberOfBirds = 16
        xPos = [random.randint(int(self.screenSize[0]*0.6), int(self.screenSize[0]*.9)) for i in range(numberOfBirds)]
        yPos = [random.randint(50+ int(self.screenSize[1]*0.1), int(self.screenSize[1]*0.3)) for i in range(numberOfBirds)]

        for i in range(numberOfBirds):
            self.birds.add(Bird())
        for bird in self.birds:
            # index of the bird
            i = self.birds.sprites().index(bird)
            bird.rect.x = 100 +  xPos[i//2]
            bird.rect.y = yPos[i//2]

        return True

    def flyInBirds(self):
        # move birds until all of them reach middle of screen
        for bird in self.birds:
            bird.speedX = -2
        # check if all birds reached middle of screen
        for bird in self.birds:
            if bird.rect.x > self.screenSize[0]/2+100:
                return False
        for bird in self.birds:  
            bird.speedX = 0
        return True

    def birdsTalk(self):
        leftBird = self.birds.sprites()[0]
        for bird in self.birds:
            if bird.rect.x < leftBird.rect.x:
                leftBird = bird
        speechBubble = transform(pygame.image.load('assets/bubble0.png'), 0.2)
        font = pygame.font.SysFont('Comic Sans MS', 10)
        if (self.timer < 1 * self.speechBubbleInterval):
            text = font.render('Hello, I am a bird!', False, (0, 0, 0))
        elif (self.timer < 2 * self.speechBubbleInterval):
            text = font.render('Oh look!, Food...', False, (0, 0, 0))
        elif (self.timer < 3 * self.speechBubbleInterval):
            text = font.render('Lets eat!...', False, (0, 0, 0))
        else:
            return True
        speechBubble.blit(text, (speechBubble.get_width()/2 - text.get_width()/2, speechBubble.get_height()/2 - text.get_height()/2 - 5))
        self.screen.blit(speechBubble, (leftBird.rect.x - speechBubble.get_width()*.9,
         leftBird.rect.y - speechBubble.get_height()))
        self.timer += 1
        return False
    def flyBirdsDown(self):
        # put birds in a grid of 4 x 4
        birdSpacing = 50
        trapTLX = 20
        trapTLY = self.screenSize[1] / 2
        for bird in self.birds:
            index = self.birds.sprites().index(bird)
            col = (index % 4) 
            row = (index // 4)
            bird.minX = col * birdSpacing + trapTLX + (3- row) * 10
            bird.maxY = row * birdSpacing + trapTLY
            bird.speedX = -1
            bird.speedY = 1
        # check if all birds are in minX and minY
        for bird in self.birds:
            if bird.rect.x > bird.minX or bird.rect.y < bird.maxY:
                return False
        self.grid.draw()
        self.timer = 0
        return True

    def talkGameInstructions(self):
        self.grid.draw()
        RBBird = self.birds.sprites()[-1]#last element of array
        speechBubble = transform(pygame.image.load('assets/bubble0.png'), 0.3)
        speechBubble = pygame.transform.flip(speechBubble, True, False)
        font = pygame.font.SysFont('Comic Sans MS', 10)
        if (self.timer < 1 * self.speechBubbleInterval):
            text = font.render('Oh, No!, we''re trapped', False, (0, 0, 0))
        elif (self.timer < 2 * self.speechBubbleInterval):
            text = font.render('Lets get out of here!', False, (0, 0, 0))
        elif (self.timer < 3 * self.speechBubbleInterval):
            text = font.render('We need to work together', False, (0, 0, 0))
        elif (self.timer < 4 * self.speechBubbleInterval):
            text = font.render('to get out of here', False, (0, 0, 0))
        elif (self.timer < 5 * self.speechBubbleInterval):
            text = font.render('Click on each of use', False, (0, 0, 0))
        elif (self.timer < 6 * self.speechBubbleInterval):
            text = font.render('to make us fly!', False, (0, 0, 0))
        elif (self.timer < 7 * self.speechBubbleInterval):
            text = font.render('Lets go!', False, (0, 0, 0))
        else:
            return True
        speechBubble.blit(text, (speechBubble.get_width()/2 - text.get_width()/2, speechBubble.get_height()/2 - text.get_height()/2 - 5))
        
        self.birds.draw(self.screen)
        self.birds.update()
        self.screen.blit(speechBubble, (RBBird.rect.topright[0]- speechBubble.get_width()*.9,
        RBBird.rect.topright[1]- speechBubble.get_height()))
        self.timer += 1
        return False

    def runIntro(self):
        # run initBirds only once
        if (self.introStage == 0):
            self.initBirds()
            self.introStage = 1

        if (self.introStage == 1):
            if (self.flyInBirds()):
                self.introStage =  2
        if (self.introStage == 2):
            if (self.birdsTalk()):
                self.introStage =  3
        if (self.introStage == 3):
            if (self.flyBirdsDown()):
                self.introStage =  4
        if (self.introStage == 4):
            if (self.talkGameInstructions()):
                return True # Start game
        #move birds to random screen positions
        else:
            self.birds.draw(self.screen)
            self.birds.update()
        return False