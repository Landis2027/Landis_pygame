from math import atan2, degrees, cos, sin
import pygame
from tank import Tank
from bullet import Bullet

class EnemyTank(Tank):
    def __init__(self, player, screen, x, y, WIDTH, HEIGHT, bullet_group, theta=270, color='red'):
        # Initialize with the player tank, as the enemy needs to track it
        super().__init__(screen, x, y, WIDTH, HEIGHT, bullet_group, theta, color)
        self.player = player  # The enemy needs to track the player
        self.speed = 0.4  # Set the enemy speed
        self.shoot_time = 0  # Timer for shooting (to prevent rapid firing)
        self.shoot_cooldown = 2000  # 2-second cooldown for shooting

    def track_player(self):
        # Track the player tank's position
        player_x, player_y = self.player.x, self.player.y
        delta_x = player_x - self.x
        delta_y = player_y - self.y

        # Calculate the angle to face the player using atan2 (in radians)
        angle_to_player = degrees(atan2(-delta_y, delta_x))

        # Ensure the angle is within a sensible range
        if angle_to_player < 0:
            angle_to_player += 360

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
        super().update()  # Update image, position, and collision checks

        # Check if the enemy is facing the player and the cooldown has passed
        angle_to_player = degrees(atan2(-(self.player.y - self.y), (self.player.x - self.x)))
        if abs(self.theta - angle_to_player) < 5:  # If it's pointed at the player
            # Shoot if enough time has passed (2 seconds cooldown)
            if pygame.time.get_ticks() - self.shoot_time > self.shoot_cooldown:
                self.shoot()

    def shoot(self):
        """Shoot a bullet at the player if facing it, with a 2-second cooldown"""
        self.shoot_sound.set_volume(0.1)  # Adjust the volume
        self.shoot_sound.play()  # Play the shooting sound
        self.shoot_time = pygame.time.get_ticks()  # Reset the shoot timer
        b = Bullet(self.screen, self, self.x, self.y, self.theta)
        self.bullet_group.add(b)  # Add the bullet to the group
