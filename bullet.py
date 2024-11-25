import pygame
from math import sin, cos, radians

class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen, tank, x, y, theta, speed=5, WIDTH=1280, HEIGHT=700):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen  # Store screen reference 
        self.tank = tank  # Store tank reference 
        self.x = x
        self.y = y
        self.speed = speed
        self.theta = theta  # Angle in degrees
        self.image = pygame.image.load('assets/bulletDark1.png')
        self.original_image = self.image  # Keep a reference to the original image for rotating
        
        # Create rect from the image and set its center position
        self.rect = self.image.get_rect()  
        self.rect.center = (self.x, self.y)  # Place the bullet at the initial position
        
        self.screen_width = WIDTH  # Boundaries
        self.screen_height = HEIGHT
        self.bounce_count = 0  # Ricochet counter
        self.screen_rect = screen.get_rect()
        self.tank = tank

    def update(self):
        # Calculate the change in x and y based on the current angle (theta)
        dx = self.speed * cos(radians(self.theta))
        dy = self.speed * sin(radians(self.theta))
        
        # Update the position
        self.x += dx
        self.y -= dy  # In pygame, increasing y goes down, so we subtract to move up

        # Rotate the bullet image to match the current direction
        self.image = pygame.transform.rotate(self.original_image, self.theta - 90)  # Rotate the image counterclockwise
        self.rect = self.image.get_rect()  # Recreate the rect after rotation
        self.rect.center = (self.x, self.y)  # Keep the center of the rect consistent with the bullet position

        # Check if the bullet is out of bounds and reverse direction
        if self.x <= 0 or self.x >= self.screen_width:
            self.theta = 180 - self.theta  # Reverse the horizontal direction
            self.bounce_count += 1
            
        if self.y <= 0 or self.y >= self.screen_height:
            self.theta = -self.theta  # Reverse the vertical direction
            self.bounce_count += 1
        
        # If the bullet has ricocheted twice, remove it
        if self.bounce_count > 1:
            self.kill()  # This removes the bullet from all sprite groups