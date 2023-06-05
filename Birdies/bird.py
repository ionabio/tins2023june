import pygame
import colorsys
import random
import math

def transformBird(image, scale):
    return pygame.transform.scale(image, (int(image.get_width()*scale), int(image.get_height()*scale)))
def shiftHue(image, hueShift):
    blue_rgb = (13,121,242)
    #convert to hsv
    hsv = colorsys.rgb_to_hsv(blue_rgb[0]/255, blue_rgb[1]/255, blue_rgb[2]/255)
    #change hue
    hsv = (hsv[0] + hueShift/255, hsv[1], hsv[2])
    #convert back to rgb and multply by 255
    rgb = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])
    rgb = (rgb[0]*255, rgb[1]*255, rgb[2]*255)
    
    #replace blue with new colour
    var = pygame.PixelArray(image)
    var.replace(blue_rgb, rgb)
    del var

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super(Bird, self).__init__()
        self.scale = 0.3
        self.images = []
        self.images.append(pygame.image.load('assets/bird0.png'))
        self.images.append(pygame.image.load('assets/bird1.png'))
        self.images.append(pygame.image.load('assets/bird2.png'))
        self.index = 0
        self.image = transformBird(self.images[self.index], self.scale)
        self.rect = pygame.Rect(5, 5, self.images[0].get_width()*self.scale, self.images[0].get_height()*self.scale)
        #scale the image to 50% of its original size
        self.rect.center = (250, 250)
        self.angle = 0
        self.speedX = 0
        self.speedY = 0
        self.accelerationY = 0
        self.speedA = 10
        self.minY = 0
        self.maxY = 0
        self.minX = 0
        self.hueShift = 0

    def flap(self, keyDown):
        if(keyDown):
            self.accelerationY -= .01
        else:
            self.accelerationY = 0
        self.speedA = 10
    
    def isFlying(self):
        return (self.rect.y <= self.minY*1.1)

    def stopFlap(self, percentageOfFlying = 0):
        #percentageOfFlying = 1 Cheat code for test
        self.accelerationY = .001*(1 - percentageOfFlying)

    def moveToTrap(self, x, y, screenHeight):
        self.rect.x = x
        self.rect.y = y 
        self.minY = y - screenHeight*.4
        self.maxY = y    
    
    def flyAway(self):
        self.minX = -100
        self.speedX = -1
    
    # animate the bird
    def update(self):
        self.index += 1
        #change the images slower
        if self.index >= len(self.images)*self.speedA:
            self.index = 0
        if (self.speedA == 0):
            self.image = transformBird(self.images[0], self.scale)
        else:
            self.image = transformBird(self.images[self.index//self.speedA], self.scale)
        # move the bird
        if (self.speedX != 0):
          self.rect.x += self.speedX
          if (self.rect.x < self.minX):
            self.rect.x = self.minX
            self.speedX = 0

        self.speedY += self.accelerationY
        if (self.speedY != 0):
            
            self.rect.y += self.speedY
            if (self.rect.y < self.minY):
                self.rect.y = self.minY
                self.accelerationY = 0
                self.speedY = 0 

            if (self.rect.y > self.maxY):
                self.rect.y = self.maxY
                self.accelerationY = 0
                self.speedA = 0
                self.speedY = 0


        if self.speedY > 0 and self.accelerationY != 0:
            self.hueShift += self.speedY
            if (self.hueShift > 255):
                    self.hueShift = 0
        else:
            self.hueShift = 0
        shiftHue(self.image, self.hueShift)
            


