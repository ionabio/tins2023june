import pygame
import random
import math
from bird import Bird
from grid import Grid

def transform(image, scale):
    return pygame.transform.scale(image, (int(image.get_width()*scale), int(image.get_height()*scale)))

class Outtro:
    def __init__(self, screenSize, birds, screen, field, tree):
        self.screenSize = screenSize
        self.screen = screen
        self.introStage = 0
        self.birds = birds
        self.grid = Grid(birds, screen)
        self.gameInitiated = False
        self.timer = 0
        self.speechBubbleInterval = 100
        self.outtroStage = 0
        # stage 0 : birds talk and tell moral of the story
        # stage 1 : birds fly away
        # stage 2 : a rainbow appears with a winning message with a button to play again

        self.rainbow = transform(pygame.image.load('assets/rainbow.png'), 0.6)
        self.field = field
        self.tree = tree


    def birdsTalk(self):
        self.grid.draw()
        RBBird = self.birds.sprites()[-1]#last element of array
        speechBubble = transform(pygame.image.load('assets/bubble0.png'), 0.3)
        speechBubble = pygame.transform.flip(speechBubble, True, False)
        font = pygame.font.SysFont('Comic Sans MS', 10)
        if (self.timer < 1 * self.speechBubbleInterval):
            text = font.render('Oh, Thank you human', False, (0, 0, 0))
        elif (self.timer < 2 * self.speechBubbleInterval):
            text = font.render('With team power,', False, (0, 0, 0))
        elif (self.timer < 3 * self.speechBubbleInterval):
            text = font.render('we are finally free!', False, (0, 0, 0))
        elif (self.timer < 4 * self.speechBubbleInterval):
            text = font.render('I know the wise mouse', False, (0, 0, 0))
        elif (self.timer < 5 * self.speechBubbleInterval):
            text = font.render('can cut us free', False, (0, 0, 0))
        elif (self.timer < 6 * self.speechBubbleInterval):
            text = font.render('Lets go!', False, (0, 0, 0))
        else:
            return True
        speechBubble.blit(text, (speechBubble.get_width()/2 - text.get_width()/2, speechBubble.get_height()/2 - text.get_height()/2 - 5))
        
        self.birds.update()
        self.birds.draw(self.screen)

        self.screen.blit(speechBubble, (RBBird.rect.topright[0]- speechBubble.get_width()*.9,
        RBBird.rect.topright[1]- speechBubble.get_height()))
        self.timer += 1
        return False

    def birdsFlyAway(self):
        for bird in self.birds:
            bird.flyAway()
 
        self.birds.update()
        self.birds.draw(self.screen)
        # if all birds are off screen return true
        for bird in self.birds:
            if (bird.rect.bottomright[0] > -10):
                return False
        return True

    def showRainbow(self):
        # load and draw rainbow
        # fade in rainbow
        if (self.timer < 400):
            self.rainbow.set_alpha(self.timer)
        self.screen.blit(self.rainbow, (-10, 80))

        # copies of rainbow scal up and fade out

        biggerRainbow = transform(self.rainbow, 1 + self.timer % 400/400)
        biggerRainbow.set_alpha(400 - (self.timer % 400))
        self.screen.blit(biggerRainbow, (-10 - (biggerRainbow.get_width() - self.rainbow.get_width())/2,
                                         80 - (biggerRainbow.get_height() - self.rainbow.get_height())/2))

        self.screen.blit(self.field, (0, 0))
        self.screen.blit(self.tree, (self.screenSize[0]-200, self.screenSize[1]/2-100))
        # show a restart button
        font = pygame.font.SysFont('Comic Sans MS', 30)
        text = font.render('Play Again', False, (0, 0, 0))
        self.screen.blit(text, (self.screenSize[0]/2 - text.get_width()/2, self.screenSize[1]/2 - text.get_height()/2))
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if (self.screenSize[0]/2 - text.get_width()/2 < mouse[0] < self.screenSize[0]/2 + text.get_width()/2 and
            self.screenSize[1]/2 - text.get_height()/2 < mouse[1] < self.screenSize[1]/2 + text.get_height()/2):
            if click[0] == 1:
                return True


        #show a text message bottom of screen
        font = pygame.font.SysFont('Comic Sans MS', 10)
        text = font.render('Story from Kelila and Demnah, Nabio 2023', False, (0, 0, 0))
        self.screen.blit(text, (self.screenSize[0]/2 - text.get_width()/2, self.screenSize[1] - text.get_height() - 10))
        self.timer += 1

     


        return False

    def runOuttro(self):
        if (self.outtroStage == 0):
            if(self.birdsTalk()):
                self.outtroStage = 1
        elif (self.outtroStage == 1):
            if(self.birdsFlyAway()):
                self.outtroStage = 2
                self.timer = 0
        elif (self.outtroStage == 2):
            if(self.showRainbow()):
                return True
        return False