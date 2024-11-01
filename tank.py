from math import cos, sin, pi
import pygame

class Tank():
    def __init__(self, x, y, theta=0, color='black'):
        self.x = x
        self.y = y
        self.speed = 0
        self.theta = theta
        try:
            self.image = pygame.image.load('assets/tank_dark.png')
        except pygame.error as e:
            print(f"Unable to load image: {e}")

    def deg_to_rad(self, deg):
        # Converts degrees to radians
        return (deg / 180) * pi

    def update(self):
        # Moves the tank at each frame
        theta_rad = self.deg_to_rad(self.theta)
        x_dot = cos(theta_rad) * self.speed
        y_dot = sin(theta_rad) * self.speed

        self.x += x_dot
        self.y -= y_dot  # y is inverted in pygame

    def draw(self, screen):
        # Rotate the image
        new_image = pygame.transform.rotozoom(self.image, self.theta+90, 0.7)  # Negative for correct rotation
        rect = new_image.get_rect(center=(self.x, self.y))
        screen.blit(new_image, rect.topleft)


    def turn(self, angle):
        self.theta = (self.theta - angle) % 360  # Subtract angle to rotate left

    def stop(self):
        self.speed = 0

    def boundaries(self, WIDTH, HEIGHT):
        # Check boundaries and keep the tank within the screen
        if self.x < 0:
            self.x = 0
        elif self.x > WIDTH-128:
            self.x = WIDTH-128

        if self.y < 0:
            self.y = 0
        elif self.y > HEIGHT:
            self.y = HEIGHT

    def rotate_left(self):
        self.theta = (self.theta + 90) % 360  # Rotate left by 90 degrees
