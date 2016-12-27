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
ADDNEWSOAPRATE = 300
SOAPWIDTH = 46
SOAPHEIGHT = 24

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

# set up poops 
poopImage = pygame.image.load('poop.png')
poopImage = pygame.transform.scale(poopImage, (30, 30))
poopRect = pygame.Rect(random.randint(0, WINDOWWIDTH - POOPSIZE), random.randint(0, WINDOWHEIGHT - POOPSIZE), POOPSIZE, POOPSIZE)

# set up soaps
soapImage = pygame.image.load('soap.png')
soapRect = soapImage.get_rect()

while True: # main menu loop
 
    addNewPoop = 0
    poopList = []
    addNewSoap = 0
    soapList = []
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
        addNewSoap += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate() 
            if event.type == KEYDOWN:
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False
                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_UP or event.key == ord('w'):
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


        # check collission for player and all poop in list
        for poop in poopList[:]:
            if playerRect.colliderect(poop['rect']):
                score += 5
                poopList.remove(poop)

        for soap in soapList[:]:
            if playerRect.colliderect(soap['rect']):
                score -= 10
                soapList.remove(soap)

        # spawns new poop   
        if addNewPoop == ADDNEWPOOPRATE:
            addNewPoop = 0
            newPoop = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - POOPSIZE), random.randint(0, WINDOWHEIGHT - POOPSIZE), POOPSIZE, POOPSIZE),
                    'surface': poopImage}
            poopList.append(newPoop)

        # spawns new soap
        if addNewSoap == ADDNEWSOAPRATE:
            addNewSoap = 0
            newSoap = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - SOAPWIDTH), random.randint(0, WINDOWHEIGHT - SOAPHEIGHT), SOAPWIDTH, SOAPHEIGHT),
                    'surface': soapImage}
            soapList.append(newSoap)

        # draw info to screen
        windowSurface.fill(BACKGROUNDCOLOR)
        windowSurface.blit(playerImage, playerRect)

        for p in poopList:
            windowSurface.blit(p['surface'], p['rect'])

        for s in soapList:
            windowSurface.blit(s['surface'], s['rect'])

        drawText("SCORE: %s" %(score), WHITE, 10, 10, windowSurface)
        
        pygame.display.update()
        mainClock.tick(FPS)
