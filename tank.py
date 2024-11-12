from math import cos, sin, pi
import pygame

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, WIDTH, HEIGHT, theta=0, color='red'):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.speed = 0
        self.fixed_speed = 1.5
        self.theta = theta
        self.color = color
        if color == 'dark':
            self.orig_image = pygame.image.load('assets/tank_dark.png')
        else:
            self.orig_image = pygame.image.load('assets/tank_red.png')
        self.image = self.orig_image # keep orig image to never be rotated
        self.rect = self.image.get_rect()
        self.screen_w = WIDTH
        self.screen_h = HEIGHT
        self.reverse_time = pygame.time.get_ticks()  # Initialize reverse timer in __init__

    def deg_to_rad(self, deg):
        # converts deg to rad
        rad = (deg/180) * pi
        return rad
    
    def check_keys(self):
        # check keys to move ship around
        keys = pygame.key.get_pressed()
        #(forward/backward)
        if keys[pygame.K_w]:
            self.speed = self.fixed_speed  # Move forward at fixed speed
        elif keys[pygame.K_s]:
            self.speed = -self.fixed_speed  # Move backward at fixed speed
        else:
            self.speed = 0  # Stop if no movement key is pressed
        # check a, d theta left/right
        if keys[pygame.K_a]:
            self.theta += 2
        if keys[pygame.K_d]:
            self.theta -= 2
    
    def check_border(self):
        c_x, c_y = self.rect.center

        if c_x > self.screen_w:  # Right wall
            self.x = self.screen_w
            self.speed = 0  # Stop movement
        elif c_x < 0:  # Left wall
            self.x = 0
            self.speed = 0  # Stop movement
        
        if c_y > self.screen_h:  # Floor
            self.y = self.screen_h
            self.speed = 0  # Stop movement
        elif c_y < 0:  # Ceiling
            self.y = 0
            self.speed = 0  # Stop movement
        
        # If the tank leaves the border, reverse after 500ms
        if not pygame.Rect(0, 0, self.screen_w, self.screen_h).contains(self.rect):
            if pygame.time.get_ticks() - self.reverse_time > 500:  # Only reverse after 500ms
                self.speed = -0.2 * self.speed  # Reverse speed
                self.reverse_time = pygame.time.get_ticks()  # Reset reverse time

    def update(self):
        if self.color =='dark':   
            self.check_keys()  
        # get x and y components of speed
        theta_rad = self.deg_to_rad(self.theta)
        x_dot = cos(theta_rad) * self.speed
        y_dot = sin(theta_rad) * self.speed

        self.x += x_dot
        self.y -= y_dot # y-axis is inverted



    
    # now rotate the image and drew new rect
        self.image = pygame.transform.rotozoom(self.orig_image, self.theta - 270, 0.5)
        self.rect = self.image.get_rect(center = (self.x, self.y))

        self.check_border()