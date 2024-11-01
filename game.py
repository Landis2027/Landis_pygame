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
        
player1 = Tank(WIDTH//2,HEIGHT//2)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player1.speed = 1.5  # Move forward at constant speed
    elif keys[pygame.K_s]:
        player1.speed = -1.5  # Move backward at constant speed
    else:
        player1.speed = 0  # Stop when no key is pressed

    if keys[pygame.K_a]:
        player1.turn(-2)  # Rotate left
    if keys[pygame.K_d]:
        player1.turn(2)   # Rotate right

    # Blit the background to the screen
    screen.blit(background,(0,0))

    # RENDER YOUR GAME HERE
    player1.update()
    player1.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()


    clock.tick(60)  # limits FPS to 60

pygame.quit()