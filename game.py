import pygame
from helpers import build_background
from tank import Tank
from enemytank import EnemyTank
import random

# pygame setup
pygame.init()
pygame.mixer.init()

# load background music
bg_music = pygame.mixer.Sound('assets/WiiPlayTanksMusic.mp3')
bg_music.play(-1)

WIDTH = 1280
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
running = True

# BUILD THE BACKGROUND WITH TILES
background = build_background(WIDTH, HEIGHT)
        
# make a sprite group
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
all_tanks_group = pygame.sprite.Group()

player1 = Tank(screen, 100, 100, WIDTH, HEIGHT, bullet_group, color='dark')
player_group.add(player1)
enemy1 = EnemyTank(player1, screen, WIDTH-50, HEIGHT-50, WIDTH, HEIGHT, bullet_group, color='red')


def spawn_tanks(WIDTH, HEIGHT, num_tanks, enemy_group):
    # spawn more tanks if needed, with a limit
    current_tanks = len(enemy_group)
    max_tanks = 10  # Limit the maximum number of enemy tanks
    for i in range(current_tanks, min(num_tanks[0], max_tanks)):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        enemy = EnemyTank(player1, screen, x, y, WIDTH, HEIGHT, bullet_group, color='red')
        enemy_group.add(enemy)

# add our sprite to the sprite group
num_tanks = [1]
spawn_tanks(WIDTH, HEIGHT, num_tanks, enemy_group)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player_group.update()
    enemy_group.update()
    bullet_group.update()

    # Blit the background to the screen
    screen.blit(background,(0,0))

    spawn_tanks(WIDTH, HEIGHT, num_tanks, enemy_group)

    player_group.draw(screen)
    enemy_group.draw(screen)
    bullet_group.draw(screen)


# Check for bullets fired by the player hitting enemy tanks
    coll_dict = pygame.sprite.groupcollide(enemy_group, bullet_group, False, False)
    for tank, bullets in coll_dict.items():
        for bullet in bullets:
            if bullet.tank == player1:  # Bullet fired by the player
                tank.explode()
                bullet.kill()
                num_tanks[0] += 1  # Increment enemy tank count

    # Check for bullets hitting the player (any bullet from enemy tanks)
    coll_dict = pygame.sprite.groupcollide(player_group, bullet_group, False, False)
    for tank, bullets in coll_dict.items():
        for bullet in bullets:
            if bullet.tank != player1:  # Bullet not fired by the player (i.e., fired by an enemy)
                tank.explode()
                bullet.kill()

    # flip() the display to put your work on screen

    pygame.display.flip()


    clock.tick(60)  # limits FPS to 60

pygame.quit()