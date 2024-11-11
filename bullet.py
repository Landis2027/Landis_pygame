import pygame
from math import sin, cos, radians
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x,y,theta,speed = 3):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.speed = speed
        self.theta = theta # degrees
        self.image = pygame.image.load('assets/bulletDark1.png')
        self.rect = self.image.get_rect()
        # place the bullet
        self.rect.center = (self.x,self.y)
    
    def update(self):
        dx = self.speed * cos(radians(self.theta))
        dy = self.speed * sin(radians(self.theta))
        
        self.x += dx
        self.y -= dy
        self.rect.center = (self.x,self.y)