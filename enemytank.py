from math import atan2, degrees, cos, sin
import pygame
from tank import Tank
from bullet import Bullet

def normalize_angle(angle):
    """Normalize angle to be between 0 and 360 degrees."""
    while angle < 0:
        angle += 360
    while angle >= 360:
        angle -= 360
    return angle


class EnemyTank(Tank):
    def __init__(self, player, screen, x, y, WIDTH, HEIGHT, bullet_group, theta=270, color='red'):
        super().__init__(screen, x, y, WIDTH, HEIGHT, bullet_group, theta, color)
        self.player = player
        self.speed = 0.25  # Set the enemy speed
        self.shoot_time = 0  # Timer for shooting
        self.shoot_cooldown = 4000  # 4-second cooldown for shooting

    def track_player(self):
        # Calculate the angle to the player
        player_x, player_y = self.player.x, self.player.y
        delta_x = player_x - self.x
        delta_y = player_y - self.y

        # Calculate the angle to the player using atan2 (in degrees)
        angle_to_player = degrees(atan2(-delta_y, delta_x))
        angle_to_player = normalize_angle(angle_to_player)

        # Smoothly rotate the tank towards the player
        angle_diff = (angle_to_player - self.theta) % 360
        if angle_diff > 180:
            angle_diff -= 360

        # Rotate smoothly (clockwise or counter-clockwise)
        if abs(angle_diff) < 5:  # Small threshold for rotation to avoid jitter
            self.theta = angle_to_player
        elif angle_diff > 0:
            self.theta += 2  # Rotate clockwise
        else:
            self.theta -= 2  # Rotate counter-clockwise

        # Move towards the player
        theta_rad = self.deg_to_rad(self.theta)
        self.x += cos(theta_rad) * self.speed
        self.y -= sin(theta_rad) * self.speed

    def update(self):
        # Track the player and update movement
        self.track_player()
        super().update()  # Update the image, position, and collision checks

        # Normalize angle for comparison
        angle_to_player = degrees(atan2(-(self.player.y - self.y), (self.player.x - self.x)))
        angle_to_player = normalize_angle(angle_to_player)

        # Shoot if the enemy is facing the player (allow small angle range for shooting)
        if abs(self.theta - angle_to_player) < 5:  # If the tank is pointed at the player
            if pygame.time.get_ticks() - self.shoot_time > self.shoot_cooldown:  # Check cooldown
                self.shoot()

    def shoot(self):
        """Shoot a bullet at the player if facing it, with a 2-second cooldown"""
        self.shoot_sound.set_volume(0.1)  # Adjust the volume
        self.shoot_sound.play()  # Play the shooting sound
        self.shoot_time = pygame.time.get_ticks()  # Reset the shoot timer
        b = Bullet(self.screen, self, self.x, self.y, self.theta)
        self.bullet_group.add(b)  # Add the bullet to the group
