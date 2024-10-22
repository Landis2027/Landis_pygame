# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()

WIDTH = 1080
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
running = True

# BUILD THE BACKGROUND WITH TILES
background = pygame.Surface((WIDTH,HEIGHT))
background.fill((255,0,0))

# load tile images to variables
grass = pygame.image.load('assets/tileGrass1.png')     
n_road = pygame.image.load('assets/tileGrass_roadNorth.png') 
# get to the tile_size
TILE_SIZE = grass.get_width()

# loop over x direction
for x in range(0,WIDTH,TILE_SIZE):
    # loop over y direction
    for y in range(0,HEIGHT, TILE_SIZE):
        # blit the tile to our BG
        background.blit(grass, (x,y))
        if x<TILE_SIZE:
            background.blit(n_road, (x,y))
        


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Blit the background to the screen
    screen.blit(background,(0,0))

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()