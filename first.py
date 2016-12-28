import pygame, sys, random
from pygame.locals import *

WINDOWHEIGHT = 750 
WINDOWWIDTH = 750 
FPS = 30
BACKGROUNDCOLOR = (0,0,0)
WHITE = (255, 255, 255)


PLAYERSIZE = 30
PLAYERMOVERATE = 9

BULLETSIZE = 5
BULLETSPEED = 12
POOPSIZE = 30
ADDNEWPOOPRATE = 20

SOAPWIDTH = 46
SOAPHEIGHT = 24
ADDNEWSOAPRATE = 10 

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

def shoot(direction, surface):
    newBullet = {'rect': pygame.Rect(playerRect.centerx, playerRect.centery, BULLETSIZE, BULLETSIZE),
            'surface': bulletImage,
            'speed': BULLETSPEED,
            'direction': None}
    bulletList.append(newBullet)

    if direction == 'RIGHT':
        newBullet['direction'] = 'RIGHT'
    if direction == 'DOWN':
        newBullet['direction'] = 'DOWN'
    if direction == 'LEFT':
        newBullet['direction'] = 'LEFT'
    if direction == 'UP':
        newBullet['direction'] = 'UP'

    surface.blit(bulletImage, newBullet['rect']) 

# setting up pygame and window
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWHEIGHT, WINDOWWIDTH))
pygame.display.set_caption('My First Pygame')
font = pygame.font.SysFont(None, 22)

# set up player
playerImage = pygame.image.load('player.png')
playerRect = pygame.Rect(0, 0, 30, 30) 
moveLeft = moveUp = moveRight = moveDown = False

# set up bullets for player to shoot
bulletImage = pygame.image.load('bullet.png')
shootLeft = shootUp = shootRight = shootDown = False
# set up poops 
poopImage = pygame.image.load('poop.png')
poopImage = pygame.transform.scale(poopImage, (30, 30))

# set up soaps
soapImage = pygame.image.load('soap.png')
soapRect = soapImage.get_rect()

while True: # main menu loop
 
    bulletList = []
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
                # movement keys
                if event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == ord('s'):
                    moveUp = False
                    moveDown = True
                if event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == ord('w'):
                    moveDown = False
                    moveUp = True

                # shooting keys
                if event.key == K_RIGHT:
                    shootUp = False
                    shootDown = False
                    shootLeft = False
                    shootRight = True
                if event.key == K_DOWN:
                    shootUp = False
                    shootRight = False
                    shootLeft = False
                    shootDown = True
                if event.key == K_LEFT:
                    shootRight = False
                    shootDown = False
                    shootUp = False
                    shootLeft = True
                if event.key == K_UP:
                    shootRight = False
                    shootDown = False
                    shootLeft = False
                    shootUp = True

                
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit
                if event.key == ord('d'):
                    moveRight = False
                if event.key == ord('s'):
                    moveDown = False
                if event.key == ord('a'):
                    moveLeft = False
                if event.key == ord('w'):
                    moveUp = False
        
                if event.key == K_RIGHT:
                   shootRight = False
                if event.key == K_DOWN:
                    shootDown = False
                if event.key == K_LEFT:
                    shootLeft = False
                if event.key == K_UP:
                    shootUp = False


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

        # check collission for player and soaps
        for soap in soapList[:]:
            if playerRect.colliderect(soap['rect']):
                score -= 10
                soapList.remove(soap)

        # check collission for bullets and soaps
        for bullet in bulletList[:]:
            for soap in soapList[:]:
                if bullet['rect'].colliderect(soap['rect']):
                    bulletList.remove(bullet)
                    soapList.remove(soap)
                    score += 100
        # spawns new poop   
        if addNewPoop == ADDNEWPOOPRATE:
            addNewPoop = 0
            newPoop = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - POOPSIZE), random.randint(0, WINDOWHEIGHT - POOPSIZE) , POOPSIZE, POOPSIZE),
                    'surface': poopImage}
            poopList.append(newPoop)

        # spawns new soap
        if addNewSoap == ADDNEWSOAPRATE:
            addNewSoap = 0
            newSoap = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - SOAPWIDTH), 0 - SOAPHEIGHT, SOAPWIDTH, SOAPHEIGHT),
                    'surface': soapImage}
            soapList.append(newSoap)

        # spawn bullets
        if shootRight:
            shoot('RIGHT', windowSurface)
        if shootDown:
            shoot('DOWN', windowSurface)
        if shootLeft:
            shoot('LEFT', windowSurface)
        if shootUp:
            shoot('UP', windowSurface)

        # move bullets
        for b in bulletList:
            if b['direction'] == 'RIGHT':
                b['rect'].move_ip(b['speed'], 0)
            if b['direction'] == 'DOWN':
                b['rect'].move_ip(0, b['speed'])
            if b['direction'] == 'LEFT':
                b['rect'].move_ip((-1 * b['speed']), 0)
            if b['direction'] == 'UP':
                b['rect'].move_ip(0, (-1 * b['speed']))

        for b in bulletList:
            if b['rect'].right > WINDOWWIDTH:
                bulletList.remove(b)
            if b['rect'].bottom > WINDOWHEIGHT:
                bulletList.remove(b)
            if b['rect'].left < 0:
                bulletList.remove(b)
            if b['rect'].top < 0:
                bulletList.remove(b)
        # move soaps
        for soap in soapList:
            soap['rect'].move_ip(0, 5)

        # draw info to screen
        windowSurface.fill(BACKGROUNDCOLOR)
        windowSurface.blit(playerImage, playerRect)

        for b in bulletList:
            windowSurface.blit(b['surface'], b['rect'])

        for p in poopList:
            windowSurface.blit(p['surface'], p['rect'])

        for s in soapList:
            windowSurface.blit(s['surface'], s['rect'])

        drawText("SCORE: %s" %(score), WHITE, 10, 10, windowSurface)
        print(len(bulletList))
        pygame.display.update()
        mainClock.tick(FPS)
