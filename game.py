# Example file showing a basic pygame "game loop"
import pygame
from helpers import build_background
from tank import Tank

# pygame setup
pygame.init()

WIDTH = 1280
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
running = True

# BUILD THE BACKGROUND WITH TILES
background = build_background(WIDTH, HEIGHT)
        
# make a sprite group
tank_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

player1 = Tank(screen, WIDTH/2, HEIGHT/2, WIDTH, HEIGHT, bullet_group, color='dark')
enemy1 = Tank(screen, 400,400, WIDTH, HEIGHT, bullet_group, color='red')

# add our sprite to the sprite group
tank_group.add(player1)
tank_group.add(enemy1)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    tank_group.update()
    bullet_group.update()
    # check for collision
    has_collided = pygame.sprite.collide_rect(player1,enemy1)
    
    if has_collided:
        player1.kill()

    # Blit the background to the screen
    screen.blit(background,(0,0))

    tank_group.draw(screen)
    bullet_group.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()


    clock.tick(60)  # limits FPS to 60

pygame.quit()