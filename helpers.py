import pygame

def build_background(WIDTH, HEIGHT):

    # BUILD THE BACKGROUND WITH TILES
    background = pygame.Surface((WIDTH,HEIGHT))
    background.fill((255,0,0))

    # load tile images to variables
    grass = pygame.image.load('assets/tileGrass1.png')     
    n_road = pygame.image.load('assets/tileGrass_roadNorth.png') 
    sand = pygame.image.load('assets/tileSand1.png')
    sand_n_road = pygame.image.load('assets/tileSand_roadNorth.png')
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
            if x>((WIDTH//2)-64):
                background.blit(sand, (x,y))
  
    return background