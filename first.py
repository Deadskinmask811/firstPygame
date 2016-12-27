# simple test to draw a rectangle to the screen that can be moved within but not out of the
# bounds of the screen
import pygame, sys, random
from pygame.locals import *

WINDOWHEIGHT = 500
WINDOWWIDTH = 500
PLAYERSIZE = 30
PLAYERMOVERATE = 10
POOPSIZE = 30
ADDNEWPOOPRATE = 30

FPS = 40
BACKGROUNDCOLOR = (0,0,0)
WHITE = (255, 255, 255)


def terminate():
    pygame.quit()
    sys.exit

def drawText(text, color, x, y, surface):
    text = font.render(text, 1, color)
    textRect = text.get_rect()
    textRect.topleft = (x, y)
    surface.blit(text, textRect)
    
def waitForInput():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return


# setting up pygame and window
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWHEIGHT, WINDOWWIDTH))
pygame.display.set_caption('My First Pygame')
font = pygame.font.SysFont(None, 22)

# set up player
playerImage = pygame.image.load('player.png')
playerRect = playerImage.get_rect() 
moveLeft = moveUp = moveRight = moveDown = False

# set up enemy
poopImage = pygame.image.load('poop.png')
poopImage = pygame.transform.scale(poopImage, (30, 30))
poopRect = pygame.Rect(random.randint(0, WINDOWWIDTH - POOPSIZE), random.randint(0, WINDOWHEIGHT - POOPSIZE), POOPSIZE, POOPSIZE)

while True: # main menu loop
 
    addNewPoop = 0
    poopList = []
    score = 0

    windowSurface.fill(BACKGROUNDCOLOR)
    drawText("POOPER SCOOPER", WHITE, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3), windowSurface)
    drawText("PRESS ANY KEY TO START...", WHITE, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 30, windowSurface)
    pygame.display.update()

    waitForInput()
    playerRect.topleft = ((WINDOWWIDTH / 2) - (playerRect.width / 2), (WINDOWHEIGHT / 2) - (playerRect.height / 2)) 

    # game loop
    while True:

        addNewPoop += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate() 
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


        # MUST CHANGE THIS CODE TO REFLECT CHANGES WITH ADDING NEW POOPS
        for poop in poopList[:]:
            if playerRect.colliderect(poop['rect']):
                score += 1
                poopList.remove(poop)

           
        if addNewPoop == ADDNEWPOOPRATE:
            addNewPoop = 0
            newPoop = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - POOPSIZE), random.randint(0, WINDOWHEIGHT - POOPSIZE), POOPSIZE, POOPSIZE),
                    'surface': poopImage}
            poopList.append(newPoop)

        windowSurface.fill(BACKGROUNDCOLOR)
        windowSurface.blit(playerImage, playerRect)

        for p in poopList:
            windowSurface.blit(p['surface'], p['rect'])

        drawText("SCORE: %s" %(score), WHITE, 10, 10, windowSurface)
        
        pygame.display.update()
        mainClock.tick(FPS)
