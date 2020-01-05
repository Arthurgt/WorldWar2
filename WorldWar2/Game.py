import pygame
pygame.init()

windowWidth = 1280
windowHeight = 720

win = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("World War 2")

walkRight = [pygame.image.load('images/AgoingR1.png'),pygame.image.load('images/AgoingR2.png'),pygame.image.load('images/AgoingR3.png')]
walkLeft = [pygame.image.load('images/AgoingL1.png'),pygame.image.load('images/AgoingL2.png'),pygame.image.load('images/AgoingL3.png')]
charL = pygame.image.load('images/AstandingL.png')
charR = pygame.image.load('images/AstandingR.png')
crouchRight = [pygame.image.load('images/AcrouchR1.png'),pygame.image.load('images/AcrouchR2.png')]
crouchLeft = [pygame.image.load('images/AcrouchL1.png'),pygame.image.load('images/AcrouchL2.png')]
bg = pygame.image.load('images/omaha.jpg')

clock = pygame.time.Clock()

x = 50
y = 50
width = 40
height = 40
vel = 2
left = False
right = False
movingVer = False
sLeft = False
sRight = True
walkCount = 0

def redrawGameWindow():
    global walkCount
    win.blit(bg, (0,0))

    if walkCount + 1 >= 9:
        walkCount = 0
    if left:
        win.blit(walkLeft[walkCount//3], (x,y))
        walkCount += 1
    elif right:
        win.blit(walkRight[walkCount//3], (x,y))
        walkCount += 1
    elif movingVer and sRight:
        win.blit(walkRight[walkCount//3], (x,y))
        walkCount += 1
    elif movingVer and sLeft:
        win.blit(walkLeft[walkCount//3], (x,y))
        walkCount += 1
    else:
        if sRight:
            win.blit(charR, (x,y))
        else:
            win.blit(charL, (x,y))

    pygame.display.update()

#mainloop
run = True
while run:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and x > 0:
            x -= vel
            left = True
            right = False
            sRight = False
            sLeft = True
        elif keys[pygame.K_RIGHT] and x < windowWidth - width:
            x += vel
            left = False
            right = True
            sRight = True
            sLeft = False
        else :
            right = False
            left = False
        if keys[pygame.K_UP] and y > 0:
            y -= vel
            movingVer = True
        elif keys[pygame.K_DOWN] and y < windowHeight - height:
            y += vel
            movingVer = True
        else:
            movingVer = False
        redrawGameWindow()

pygame.quit()
