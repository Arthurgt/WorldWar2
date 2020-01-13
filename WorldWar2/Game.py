import pygame

pygame.init()

windowWidth = 1280
windowHeight = 720

win = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("World War 2")

walkRight = [pygame.image.load('images/AgoingR1.png'), pygame.image.load('images/AgoingR2.png'),
             pygame.image.load('images/AgoingR3.png')]
walkLeft = [pygame.image.load('images/AgoingL1.png'), pygame.image.load('images/AgoingL2.png'),
            pygame.image.load('images/AgoingL3.png')]
charL = pygame.image.load('images/AstandingL.png')
charR = pygame.image.load('images/AstandingR.png')
bg = pygame.image.load('images/omaha.jpg')

clock = pygame.time.Clock()


class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 2
        self.left = False
        self.right = False
        self.movingVer = False
        self.sLeft = False
        self.sRight = True
        self.walkCount = 0

    def draw(self, win):
        if self.walkCount + 0 >= 9:
            self.walkCount = 0
        if self.left:
            win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        elif self.right:
            win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        elif self.movingVer and self.sRight:
            win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        elif self.movingVer and self.sLeft:
            win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        else:
            if self.sRight:
                win.blit(charR, (self.x, self.y))
            else:
                win.blit(charL, (self.x, self.y))

class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 3 * facing

    def draw (self, win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

def redrawGameWindow():
    win.blit(bg, (0, 0))
    player.draw(win)
    pygame.display.update()


# mainloop
player = player(10, 10, 40, 40)
run = True
while run:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x:
        player.x -= player.vel
        player.left = True
        player.right = False
        player.sRight = False
        player.sLeft = True
    elif keys[pygame.K_RIGHT] and player.x < windowWidth - player.width:
        player.x += player.vel
        player.left = False
        player.right = True
        player.sRight = True
        player.sLeft = False
    else:
        player.right = False
        player.left = False
    if keys[pygame.K_UP] and player.y > 0:
        player.y -= player.vel
        player.movingVer = True
    elif keys[pygame.K_DOWN] and player.y < windowHeight - player.height:
        player.y += player.vel
        player.movingVer = True
    else:
        player.movingVer = False
    redrawGameWindow()

pygame.quit()
