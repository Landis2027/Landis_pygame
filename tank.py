from math import cos, sin, pi
import pygame
from bullet import Bullet

class Tank(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, WIDTH, HEIGHT, bullet_group, theta=0, color='red'):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.speed = 0
        self.screen = screen
        self.fixed_speed = 3
        self.theta = theta
        self.color = color
        if color == 'dark':
            self.orig_image = pygame.image.load('assets/tank_dark.png')
        else:
            self.orig_image = pygame.image.load('assets/tank_red.png')
            color == 'red'
        self.image = self.orig_image # keep orig image to never be rotated
        self.rect = self.image.get_rect()
        self.screen_w = WIDTH
        self.screen_h = HEIGHT
        self.bullet_group = bullet_group
        self.reverse_time = pygame.time.get_ticks()  # Initialize reverse timer in __init__
        self.shoot_time = 0 # stop rapid fire
        self.shoot_cooldown = 1000 # wait ms before next shot
        self.shoot_sound = pygame.mixer.Sound('assets/pop.mp3')
        # load up explosion images
        self.explosion_image = pygame.image.load('assets/explosionSmoke3.png')
        self.explosion_image = pygame.transform.scale_by(self.explosion_image, 6)
        self.explosion_timer = 0
        self.explosion_length = 500

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
            self.theta += 3
        if keys[pygame.K_d]:
            self.theta -= 3
        
        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        # Only shoot after cooldown
        if pygame.time.get_ticks() - self.shoot_time > self.shoot_cooldown:
            self.shoot_sound.set_volume(0.1)  # Adjust the volume
            self.shoot_sound.play()
            self.shoot_time = pygame.time.get_ticks()
            # if we have waited long enough, then make bullet
            b = Bullet(self.screen, self, self.x, self.y, self.theta)
            # put the bullet in a group
            self.bullet_group.add(b)

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
    
    def explode(self):
        # if the timer is already set, do nothing
        self.speed = 0
        if self.explosion_timer ==0:
            # start a timer so that it gets killed later
            self.explosion_timer = pygame.time.get_ticks()
            self.speed = 0

    def track_player(self):
        pass

    def update(self):
        if self.color =='dark':   
            self.check_keys()  
        else:
            pass
        # get x and y components of speed
        theta_rad = self.deg_to_rad(self.theta)
        x_dot = cos(theta_rad) * self.speed
        y_dot = sin(theta_rad) * self.speed

        self.x += x_dot
        self.y -= y_dot # y-axis is inverted



    
    # now rotate the image and drew new rect
        self.image = pygame.transform.rotozoom(self.orig_image, self.theta - 270, 0.4)
        self.rect = self.image.get_rect(center = (self.x, self.y))

        self.check_border()

          # check explosion
        if self.explosion_timer != 0:
            delta_time = pygame.time.get_ticks() - self.explosion_timer
            # if time kill, kill kill tank
            if delta_time >= self.explosion_length:
                self.kill()
            # execute explosion
            if delta_time < (self.explosion_length/2):
                # grow the explosion
                self.orig_image = pygame.transform.scale_by(self.explosion_image, delta_time/1000)
            else:
                # shrink the explosion
                self.orig_image = pygame.transform.scale_by(self.explosion_image, self.explosion_length/1000 - (delta_time - self.explosion_length/2)/1000)