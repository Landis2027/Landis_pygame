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

#Color Palette
night = pygame.Color('#0F0F0F')
rose_quartz = pygame.Color('#e9bec6')
jet = pygame.Color('#2D2E2E')
dim_gray = pygame.Color('#716969')
white = pygame.Color('#FBFBFB')
burgundy = pygame.Color('#800020')

#Define width and height of game screen
WIDTH = 1280
HEIGHT = 700

#Run the timer
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

#Create a player and an enemy (INIT)
player1 = Tank(screen, 100, 100, WIDTH, HEIGHT, bullet_group, color='dark')
player_group.add(player1)
enemy1 = EnemyTank(player1, screen, WIDTH-50, HEIGHT-50, WIDTH, HEIGHT, bullet_group, color='red')

#Enemy tank spawn
def spawn_tanks(WIDTH, HEIGHT, num_tanks, enemy_group):
    # spawn more tanks if needed, with a limit
    current_tanks = len(enemy_group)
    max_tanks = 20  # Limit the maximum number of enemy tanks
    for i in range(current_tanks, min(num_tanks[0], max_tanks)):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        enemy = EnemyTank(player1, screen, x, y, WIDTH, HEIGHT, bullet_group, color='red')
        enemy_group.add(enemy)

# add our sprite to the sprite group
num_tanks = [1]
spawn_tanks(WIDTH, HEIGHT, num_tanks, enemy_group)


# scoreboard
score = [0]
score_font = pygame.font.Font('assets/BebasNeue-Regular.ttf',size=50)

#INSTRUCTION_______________________________________________________________________________________

def make_instructions(screen):
    # black screen
    screen.fill(jet)
    title = ['BULLET HELL']
    instructions = [
        '',
        'Use W to move tank forward',
        'S to move backward',
        'A to rotate left',
        'D to rotate right'
        'Press Spacebar to shoot a bullet',
        'Press P to take a screenshot',
        '',
        '**PRESS ANY KEY TO START**'
    ]

    # make an instruction font
    i_font = pygame.font.Font('assets/BebasNeue-Regular.ttf',size=40)
    spacing = 80
    # render (make surface) for each instruction
    for ii in range(len(instructions)):
        # render the font
        font_surf = i_font.render(instructions[ii], True, rose_quartz)
        # get a rect
        font_rect = font_surf.get_rect()
        font_rect.center = (WIDTH//2, spacing + ii * spacing)
        # blit it to the screen
        screen.blit(font_surf, font_rect)
    t_font = pygame.font.Font('assets/BebasNeue-Regular.ttf',size=80)
    spacing = 80
    # render title above instructions
    for ii in range(len(title)):
        # grab font
        font_surf = t_font.render(title[ii], True, burgundy)
        # find rect
        font_rect = font_surf.get_rect()
        font_rect.center = (WIDTH//2, spacing + ii * spacing)
        # blit it
        screen.blit(font_surf, font_rect)

waiting = 1
# if we see the spacebar, exit the loop (break)
while waiting:
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            waiting = 0
        if event.type == pygame.KEYDOWN:
            # if any key pressed, break
            waiting = 0

    make_instructions(screen)

    pygame.display.flip()



#GAME LOOP_____________________________________________________________________________________________

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