# simple test to draw a rectangle to the screen that can be moved within but not out of the
# bounds of the screen
import pygame, sys
from pygame.locals import *

WINDOWHEIGHT = 500
WINDOWWIDTH = 500
PLAYERSIZE = 30
PLAYERMOVERATE = 10
FPS = 40
BACKGROUNDCOLOR = (0,0,0)

pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWHEIGHT, WINDOWWIDTH))
pygame.display.set_caption('My First Pygame')

# set up player
playerImage = pygame.image.load('player.png')
playerRect = pygame.Rect(0, 0, PLAYERSIZE, PLAYERSIZE)
moveLeft = moveUp = moveRight = moveDown = False
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit
        
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moveLeft = False
                moveRight = True
            if event.key == K_DOWN:
                moveUp = False
                moveDown = True
            if event.key == K_LEFT:
                moveRight = False
                moveLeft = True
            if event.key == K_UP:
                moveDown = False
                moveUp = True

        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit
            if event.key == K_RIGHT:
                moveRight = False
            if event.key == K_DOWN:
                moveDown = False
            if event.key == K_LEFT:
                moveLeft = False
            if event.key == K_UP:
                moveUp = False
    
    # move character 
    if moveRight and playerRect.right < WINDOWWIDTH:
        playerRect.move_ip(PLAYERMOVERATE, 0)
    if moveDown and playerRect.bottom < WINDOWHEIGHT:
        playerRect.move_ip(0, PLAYERMOVERATE)
    if moveLeft and playerRect.left > 0:
        playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
    if moveUp and playerRect.top > 0:
        playerRect.move_ip(0, -1 * PLAYERMOVERATE)
    
    
    windowSurface.fill(BACKGROUNDCOLOR)

    windowSurface.blit(playerImage, playerRect)
    pygame.display.update()
    mainClock.tick(FPS)
