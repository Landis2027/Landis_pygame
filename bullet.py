import pygame
from math import sin, cos, radians

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, theta, speed=3, WIDTH = 1280, HEIGHT = 700):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.speed = speed
        self.theta = theta  # degrees
        self.image = pygame.image.load('assets/bulletDark1.png')
        self.original_image = self.image  # Keep a reference to the original image for rotating
        self.rect = self.image.get_rect()
        # place the bullet
        self.rect.center = (self.x, self.y)
        
        # Screen boundaries
        self.screen_width = WIDTH
        self.screen_height = HEIGHT
        
        # Ricochet counter
        self.bounce_count = 0

    def update(self):
        # Calculate the change in x and y based on the current angle (theta)
        dx = self.speed * cos(radians(self.theta))
        dy = self.speed * sin(radians(self.theta))
        
        self.x += dx
        self.y -= dy  # negative y in math is + y in pygame

        # Rotate the bullet image to match the current direction
        self.image = pygame.transform.rotate(self.original_image, self.theta-90)  # Rotate image counterclockwise
        self.rect = self.image.get_rect()  # Recreate the rect after rotation
        self.rect.center = (self.x, self.y)  # Keep the center of the rect consistent with the bullet position

        # Check if the bullet is out of bounds and reverse direction
        bounced = False
        
        if self.x <= 0 or self.x >= self.screen_width:
            self.theta = 180 - self.theta  # Reverse the horizontal direction
            self.bounce_count += 1
            bounced = True
            
        if self.y <= 0 or self.y >= self.screen_height:
            self.theta = -self.theta  # Reverse the vertical direction
            self.bounce_count += 1
            bounced = True
        
        # If the bullet has ricocheted twice, remove it
        if self.bounce_count > 2:
            self.kill()  # This removes the bullet from all sprite groups