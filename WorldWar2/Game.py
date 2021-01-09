import pygame
import random
from random import seed
from random import randint

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
menu = pygame.image.load('images/menu.jpg')
history1 = pygame.image.load('images/history1.jpg')
history2 = pygame.image.load('images/history2.jpg')
history3 = pygame.image.load('images/history3.jpg')
landingCraftPhoto = pygame.image.load('images/landingcraft.png')
introPhoto = pygame.image.load('images/intro.jpg')
obstaclePhoto = pygame.image.load('images/metal.png')

backgroundSound = pygame.mixer.music.load('sounds/menuMusic.mp3')
garandShot = pygame.mixer.Sound('sounds/garand.wav')
karShot = pygame.mixer.Sound('sounds/kar98.wav')
friendShot = pygame.mixer.Sound('sounds/friendShot.wav')
landingCraftSound = pygame.mixer.Sound('sounds/landingCrafts.wav')
whistleSound = pygame.mixer.Sound('sounds/Whistle.wav')
startSound = pygame.mixer.Sound('sounds/Start.wav')
enemyDeadSound = pygame.mixer.Sound('sounds/edead.wav')
friendDeadSound = pygame.mixer.Sound('sounds/adead.wav')

clock = pygame.time.Clock()
random.seed(0)
reloading = 1
shootLoop = 0
killCount = 0
initialize = 0
choice = 0
run = True
game = 0
intro = 0
gameOver = 0
resetGame = 0
victory = 0
bullets = []
enemies = []
friends = []
obstacles = []
landingCrafts = []
enemiesCounter = 0

class player(object):
    deadImage = pygame.image.load('images/Fdead1.png')

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 1
        self.left = False
        self.right = False
        self.movingVer = False
        self.dead = False
        self.sLeft = False
        self.sRight = True
        self.walkCount = 0
        self.hitbox = (self.x + 5, self.y + 5, 32, 32)

    def draw(self, win):
        if not self.dead:
            if self.walkCount >= 9:
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
            self.hitbox = (self.x, self.y, 40, 40)
        else:
            win.blit(self.deadImage,(self.x, self.y))

    def hit(self):
        global gameOver
        self.dead = True
        gameOver = 1

class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = facing

    def draw (self, win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

class landingCraft(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.vel = 3

    def draw (self, win):
        win.blit(landingCraftPhoto,(self.x, self.y))

    def move(self):
        self.x = self.x + self.vel

class obstacleC(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.hitbox = (self.x, self.y, 57, 50)

    def draw (self, win):
        win.blit(obstaclePhoto,(self.x, self.y))

class enemyS (object):
    walkLeft = [pygame.image.load('images/EgoingL1.png'), pygame.image.load('images/EgoingL2.png'),
                pygame.image.load('images/EgoingL3.png'), pygame.image.load('images/EgoingL2.png'),pygame.image.load('images/EgoingL1.png'),]
    deadImage = pygame.image.load('images/Edead1.png')
    myBullets = []
    myShootLoop = 1


    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 1
        self.walkCount = 0
        self.hitbox = (self.x + 5, self.y + 5, 40, 40)
        self.dead = False
        self.deadAnimation = 0
        self.reachedX = True
        self.reachedY = True
        self.yVel = self.vel
        self.xVel = self.vel
        self.xpoint = 0
        self.ypoint = 0

    def draw(self, win):
        if( not self.dead):
            self.move()
            if self.walkCount > 4:
                self.walkCount = 0
            win.blit(self.walkLeft[self.walkCount],(self.x, self.y))
            self.walkCount += 1
            self.hitbox = (self.x, self.y, 40, 40)
        else:
            win.blit(self.deadImage,(self.x, self.y))
            self.hitbox = (self.x, self.y, 0, 0)

    def move(self):
        if self.y + self.yVel == self.ypoint:
            self.reachedY = True
        else:
            self.y += self.yVel
        if self.x + self.xVel == self.xpoint:
            self.reachedX = True
        else:
            self.x += self.xVel
        if(self.reachedX and self.reachedY):
            self.newPoint()

    def newPoint(self):
        self.xpoint = randint(640,1280)
        self.ypoint = randint(50,720)
        self.reachedX = False
        self.reachedY = False
        if(self.ypoint >= self.y):
            self.yVel = self.vel

        else:
            self.yVel = self.vel * -1
        if (self.xpoint > self.x):
            self.xVel = self.vel
        else:
            self.xVel = self.vel * -1

    def hit(self, killCount):
        global enemiesCounter
        if(not self.dead):
            killCount += 1
        self.dead = True
        enemyDeadSound.play()
        return killCount

class friendS (object):
    walkRight = [pygame.image.load('images/FgoingR1.png'), pygame.image.load('images/FgoingR2.png'),
                 pygame.image.load('images/FgoingR3.png'), pygame.image.load('images/FgoingR4.png'),pygame.image.load('images/FgoingR3.png'),pygame.image.load('images/FgoingR2.png'), pygame.image.load('images/FgoingR1.png')]
    deadImage = pygame.image.load('images/Fdead1.png')
    myBullets = []
    myShootLoop = 1

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 1
        self.xpoint = 0
        self.ypoint = 0
        self.walkCount = 0
        self.hitbox = (self.x + 5, self.y + 5, 40, 40)
        self.dead = False
        self.deadAnimation = 0
        self.reachedX = True
        self.reachedY = True
        self.yVel = self.vel
        self.xVel = self.vel

    def draw(self, win):
        if( not self.dead):
            self.move()
            if self.walkCount > 6:
                self.walkCount = 0
            win.blit(self.walkRight[self.walkCount],(self.x, self.y))
            self.walkCount += 1
            self.hitbox = (self.x, self.y, 40, 40)
        else:
            win.blit(self.deadImage,(self.x, self.y))
            self.hitbox = (self.x, self.y, 0, 0)

    def move(self):
        if self.y + self.yVel == self.ypoint:
            self.reachedY = True
        else:
            self.y += self.yVel
        if self.x + self.xVel == self.xpoint:
            self.reachedX = True
        else:
            self.x += self.xVel
        if(self.reachedX and self.reachedY):
            self.newPoint()

    def newPoint(self):
        self.xpoint = randint(0,640)
        self.ypoint = randint(50,720)
        self.reachedX = False
        self.reachedY = False
        if(self.ypoint >= self.y):
            self.yVel = self.vel
        else:
            self.yVel = self.vel * -1
        if (self.xpoint > self.x):
            self.xVel = self.vel
        else:
            self.xVel = self.vel * -1

    def hit(self):
        self.dead = True
        friendDeadSound.play()

def redrawGameWindow():
    global enemiesCounter
    win.blit(bg, (0, 0))
    text = font.render('Trafienia: ' + str(killCount), 1, (0,0,0))
    text2 = font.render('Przeładowywanie', 1, (0,0,0))
    text3 = font.render('Gotowa do strzału', 1, (0,0,0))
    text4 = font.render('Pozostalo przeciwnikow: ' + str(enemiesCounter), 1, (0,0,0))
    win.blit(text, (10, 10))
    win.blit(text4,(160,10))
    global intro
    global initialize
    global choice
    global gameOver
    global enemies
    global obstacles
    global friends
    global bullets
    global resetGame
    global game
    global victory
    if(reloading):
        win.blit(text3, (10, 30))
    else:
        win.blit(text2, (10, 30))
    for obstacle in obstacles:
        obstacle.draw(win)
    player1.draw(win)
    localEnemiesCounter = 0
    for enemy in enemies:
        if(not enemy.dead):
            localEnemiesCounter = localEnemiesCounter + 1
        enemy.draw(win)
        for enemyBullet in enemy.myBullets:
            enemyBullet.draw(win)
    enemiesCounter = localEnemiesCounter
    if(enemiesCounter == 0):
        victory = 1
    for friend in friends:
        friend.draw(win)
        for friendBullet in friend.myBullets:
            friendBullet.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    if (victory):
        while victory == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            menuFont = pygame.font.SysFont('comicsans', 60, True)
            optionFont = pygame.font.SysFont('comicsans', 50, True)
            text4 = optionFont.render('Menu', 1, (0, 0, 0))
            text5 = optionFont.render('Od Nowa', 1, (0, 0, 0))
            text6 = menuFont.render('Wygrales z trafieniami: ' + str(killCount), 1, (0, 0, 0))
            win.blit(text6, (536, 280))
            win.blit(text5, (420, 330))
            win.blit(text4, (680, 330))
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if ((mouse[0] > 420) and (mouse[0] < 575) and (mouse[1] > 330) and (mouse[1] < 365)):
                if (click[0] == 1):
                    choice = 1
                    intro = 0
                    initialize = 0
                    resetGame = 1
                    gameOver = 0
                    victory = 0
            if ((mouse[0] > 680) and (mouse[0] < 835) and (mouse[1] > 330) and (mouse[1] < 365)):
                if (click[0] == 1):
                    choice = 0
                    initialize = 0
                    intro = 0
                    resetGame = 1
                    gameOver = 0
                    game = 0
                    victory = 0
                    pygame.mixer.music.load('sounds/menuMusic.mp3')
                    pygame.mixer_music.play(-1)
            pygame.display.update()
            clock.tick(30)
    if(gameOver):
        while gameOver == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            menuFont = pygame.font.SysFont('comicsans', 60, True)
            optionFont = pygame.font.SysFont('comicsans', 50, True)
            text4 = optionFont.render('Menu', 1, (0, 0, 0))
            text5 = optionFont.render('Od Nowa', 1, (0, 0, 0))
            text6 = menuFont.render('Poległeś', 1, (0, 0, 0))
            win.blit(text6, (536, 280))
            win.blit(text5, (420, 330))
            win.blit(text4, (680, 330))
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if ((mouse[0] > 420) and (mouse[0] < 575) and (mouse[1] > 330) and (mouse[1] < 365)):
                if (click[0] == 1):
                    choice = 1
                    intro = 0
                    initialize = 0
                    resetGame = 1
                    gameOver = 0
            if ((mouse[0] > 680) and (mouse[0] < 835) and (mouse[1] > 330) and (mouse[1] < 365)):
                if (click[0] == 1):
                    choice = 0
                    initialize = 0
                    intro = 0
                    resetGame = 1
                    gameOver = 0
                    game = 0
                    pygame.mixer.music.load('sounds/menuMusic.mp3')
                    pygame.mixer_music.play(-1)
            pygame.display.update()
            clock.tick(30)

    pygame.display.update()

def drawHistory():
    global choice
    global initialize
    font = pygame.font.SysFont('comicsans', 20, True)
    while choice==2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        win.blit(menu, (0, 0))
        win.blit(history1, (140, 415))
        win.blit(history2, (490, 415))
        win.blit(history3, (840, 415))
        menuFont = pygame.font.SysFont('comicsans', 60, True)
        optionFont = pygame.font.SysFont('comicsans', 50, True)
        text = menuFont.render('Lądowanie na plaży Omaha', 1, (0, 0, 0))
        text2 = font.render('O godzinie 5:30 do plaż zbliżyły się pierwsze oddziały amerykańskie.', 1, (0, 0, 0))
        text3 = font.render('W pierwszej fali ataku brało bezpośrednio udział 3 tys. żołnierzy. Były to grupy bojowe z 1, 29, 4 dywizji oraz pododdziały wojsk lądowych i marynarki wojennej.', 1, (0, 0, 0))
        text5 = font.render('Ich zadaniem było zniszczenie przeszkód podwodnych. Każda z grup miała wyznaczoną strefę lądowania. ', 1, (0, 0, 0))
        text6 = font.render('Plaża była przydzielona po połowie 16 pułkowi 1 dywizji generała Clarence’a Huebnera i 116 pułkowi 29 dywizji generała majora Charlesa Gerharda.', 1, (0, 0, 0))
        text7 = font.render('Z 32 amerykańskich czołgów pływających typu Sherman DD, stanowiących wsparcie działań piechoty, jedynie 4 dotarło do brzegu.', 1, (0, 0, 0))
        text8 = font.render('Przygotowanie natarcia w postaci bombardowania z powietrza i ostrzału artyleryjskiego z morza nie zniszczyło niemieckiej obrony. ', 1, (0, 0, 0))
        text9 = font.render('Wiatr, wysokie fale i prąd morski uniemożliwił jednostkom desantowym precyzyjne lądowanie w wyznaczonych rejonach. ', 1, (0, 0, 0))
        text10 = font.render('Nacierająca piechota amerykańska znalazła się w krzyżowym ogniu niemieckich karabinów maszynowych i pod ostrzałem moździerzy oraz dział 88 mm. ', 1, (0, 0, 0))
        text11 = font.render('Dodatkowym utrudnieniem dla nacierających była ograniczona widoczność spowodowana dymem wybuchów wcześniejszego bombardowania i ostrzału. ', 1, (0, 0, 0))
        text12 = font.render('Żołnierze byli zmęczeni i cierpieli z powodu choroby morskiej. Ekwipunek, nasiąknięty wodą i wypełniony piaskiem, uniemożliwiał szybkie posuwanie się do przodu. ', 1, (0, 0, 0))
        text13 = font.render('W ciągu pierwszych godzin desantu wszyscy dowódcy zostali albo ciężko ranni, albo zabici. Natarcie załamało się. ', 1, (0, 0, 0))
        text14 = font.render('W toku ciężkich walk atakującym udało się jednak dotrzeć do umocnień brzegowych. ', 1, (0, 0, 0))
        text15 = font.render('Dzięki podłużnym minom bangalore zniszczyli zasieki z drutu kolczastego i unieszkodliwili pola minowe, co pozwoliło na ominięcie bunkrów, zajście ich od tyłu i zdobycie.', 1, (0, 0, 0))
        text16 = font.render('Alianckie niszczyciele, ryzykując wpadnięcie na mieliznę, z bliska ostrzelały niemieckie pozycje obronne. Po prawie 10 godzinach boju plaża została zdobyta. ', 1, (0, 0, 0))
        text17 = font.render('Powodzenie natarcia zostało okupione ok. 3 tysiącami zabitych, rannych i zaginionych alianckich żołnierzy.', 1, (0, 0, 0))
        text4 = optionFont.render('Powrót', 1, (0, 0, 0))
        win.blit(text, (300, 30))
        win.blit(text2,(10,100))
        win.blit(text3, (10, 120))
        win.blit(text5, (10, 140))
        win.blit(text6, (10, 160))
        win.blit(text7, (10, 180))
        win.blit(text8, (10, 200))
        win.blit(text9, (10, 220))
        win.blit(text10, (10, 240))
        win.blit(text11, (10, 260))
        win.blit(text12, (10, 280))
        win.blit(text13, (10, 300))
        win.blit(text14, (10, 320))
        win.blit(text15, (10, 340))
        win.blit(text16, (10, 360))
        win.blit(text17, (10, 380))
        win.blit(text4, (560, 680))
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if((mouse[0] > 560) and (mouse[0] < 715) and (mouse[1] > 680) and (mouse[1] < 715)):
            if(click[0] == 1):
                choice = 0
                initialize = 0
        pygame.display.update()
        clock.tick(30)

def drawMenu():
    global choice
    global initialize
    global intro
    while choice==0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        win.blit(menu, (0, 0))
        menuFont = pygame.font.SysFont('comicsans', 60, True)
        optionFont = pygame.font.SysFont('comicsans', 50, True)
        text = menuFont.render('World War 2: Omaha Beach', 1, (0, 0, 0))
        text2 = optionFont.render('Graj', 1, (0, 0, 0))
        text3 = optionFont.render('Historia', 1, (0, 0, 0))
        text4 = optionFont.render('Wyjscie', 1, (0, 0, 0))
        win.blit(text, (300, 30))
        win.blit(text2, (596, 280))
        win.blit(text3, (560, 330))
        win.blit(text4, (560, 380))
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if((mouse[0] > 596) and (mouse[0] < 675) and (mouse[1] > 280) and (mouse[1] < 315)):
            if(click[0] == 1):
                choice = 1
                intro = 1
        if((mouse[0] > 560) and (mouse[0] < 715) and (mouse[1] > 330) and (mouse[1] < 365)):
            if(click[0] == 1):
                choice = 2
                initialize = 0
        if((mouse[0] > 566) and (mouse[0] < 715) and (mouse[1] > 380) and (mouse[1] < 415)):
            if(click[0] == 1):
                pygame.quit()
        pygame.display.update()
        clock.tick(30)

def drawIntro(landingCrafts):
    global choice
    global initialize
    global game
    global intro
    landingCraftSound.set_volume(0.7)
    landingCraftSound.play()
    while game == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        win.blit(introPhoto, (0, 0))
        for landingCraft in landingCrafts:
            landingCraft.draw(win)
            landingCraft.move()
        if(landingCrafts[1].x > 1280):
            game = 1
            initialize = 0
            intro = 0
        pygame.display.update()
        clock.tick(30)

def fadeInIntro(width, height):
    pygame.mixer.music.load('sounds/warSound.mp3')
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)
    fade = pygame.Surface((width, height))
    fade.fill((0,0,0))
    for alpha in range(0, 1000):
        fade.set_alpha(alpha)
        win.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(5)

def fadeInLanding(width, height):
    fade = pygame.Surface((width, height))
    fade.fill((0,0,0))
    startSound.play()
    for alpha in range(0, 1500):
        fade.set_alpha(alpha)
        win.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(1)

# mainloop
font = pygame.font.SysFont('comicsans', 30, True)
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)
while run:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if (resetGame == 1):
        enemies.clear()
        friends.clear()
        bullets.clear()
        obstacles.clear()
        killCount = 0
        resetGame = 0
        enemiesCounter = 0
    if (choice == 0 and initialize == 0):
        initialize = 1
        drawMenu()
    if (choice == 1 and intro == 1):
        landingCraft1 = landingCraft(-300,20)
        landingCraft2 = landingCraft(-400, 80)
        landingCraft3 = landingCraft(-200,200)
        landingCraft4 = landingCraft(-100, 600)
        landingCraft5 = landingCraft(-320,350)
        landingCraft6 = landingCraft(-200, 450)
        landingCraft7 = landingCraft(-340,420)
        landingCraft8 = landingCraft(-200, 580)
        landingCraft9 = landingCraft(-300,124)
        landingCraft10 = landingCraft(-250, 150)
        landingCrafts.append(landingCraft1)
        landingCrafts.append(landingCraft2)
        landingCrafts.append(landingCraft3)
        landingCrafts.append(landingCraft4)
        landingCrafts.append(landingCraft5)
        landingCrafts.append(landingCraft6)
        landingCrafts.append(landingCraft7)
        landingCrafts.append(landingCraft8)
        landingCrafts.append(landingCraft9)
        landingCrafts.append(landingCraft10)
        fadeInIntro(1280,720)
        drawIntro(landingCrafts)
    if (choice == 1 and initialize == 0 and intro == 0):
        initialize = 1
        landingCrafts.clear()
        fadeInLanding(1280,720)
        whistleSound.play()
        obstacle1 = obstacleC(600, 100)
        obstacle2 = obstacleC(700, 300)
        obstacle3 = obstacleC(800, 400)
        obstacle4 = obstacleC(600, 500)
        obstacle5 = obstacleC(500, 360)
        player1 = player(10, 600, 40, 40)
        enemy1 = enemyS(1000, 200, 40, 40)
        enemy2 = enemyS(1000, 300, 40, 40)
        enemy3 = enemyS(1100, 110, 40, 40)
        enemy4 = enemyS(1000, 210, 40, 40)
        enemy5 = enemyS(1000, 310, 40, 40)
        enemy6 = enemyS(1100, 320, 40, 40)
        enemy7 = enemyS(1000, 120, 40, 40)
        enemy8 = enemyS(1000, 220, 40, 40)
        enemy9 = enemyS(1100, 130, 40, 40)
        enemy10 = enemyS(1000, 230, 40, 40)
        enemy11 = enemyS(1100, 330, 40, 40)
        enemy12 = enemyS(1000, 140, 40, 40)
        friend1 = friendS(10, 610, 40, 40)
        friend2 = friendS(40, 510, 40, 40)
        friend3 = friendS(100, 600, 40, 40)
        friend4 = friendS(40, 650, 40, 40)
        friend5 = friendS(100, 500, 40, 40)
        friend6 = friendS(40, 620, 40, 40)
        friend7 = friendS(100, 520, 40, 40)
        enemies.append(enemy1)
        enemies.append(enemy2)
        enemies.append(enemy3)
        enemies.append(enemy4)
        enemies.append(enemy5)
        enemies.append(enemy6)
        enemies.append(enemy7)
        enemies.append(enemy8)
        enemies.append(enemy9)
        enemies.append(enemy10)
        enemies.append(enemy11)
        enemies.append(enemy12)
        friends.append(friend1)
        friends.append(friend2)
        friends.append(friend3)
        friends.append(friend4)
        friends.append(friend5)
        friends.append(friend6)
        friends.append(friend7)
        obstacles.append(obstacle1)
        obstacles.append(obstacle2)
        obstacles.append(obstacle3)
        obstacles.append(obstacle4)
        obstacles.append(obstacle5)
        gameOver=0
        enemiesCounter=12
    if(choice == 2 and initialize ==0):
        initialize = 1
        drawHistory()
    if(game == 1):
        ################################################### petla po przeciwnikach wraz z ich strzalami ###################################################################
        for enemy in enemies:
            if len(enemy.myBullets) < len(enemies) and not enemy.dead and enemy.myShootLoop == 1:
                enemy.myBullets.append(
                    projectile(enemy.x + enemy.width // 2, round(enemy.y + enemy.height // 2), 3, (0, 0, 0), -1))
                karShot.play()
                enemy.myShootLoop = 2

            if enemy.myShootLoop > 1:
                enemy.myShootLoop += 1
            if enemy.myShootLoop > 30:
                enemy.myShootLoop = 1
            # kolizje strzalow przeciwnika z graczem
            for bullet in enemy.myBullets:
                if bullet.y - bullet.radius < player1.hitbox[1] + player1.hitbox[3] and bullet.y + bullet.radius > \
                        player1.hitbox[1]:
                    if bullet.x + bullet.radius > player1.hitbox[0] and bullet.x - bullet.radius < player1.hitbox[0] + \
                            player1.hitbox[2]:
                        enemy.myBullets.pop(enemy.myBullets.index(bullet))
                        player1.hit()
                        continue
                if bullet.x < 1280 and bullet.x > 0 and bullet.y > 0 and bullet.y < 720:
                    bullet.x += bullet.vel
                else:
                    enemy.myBullets.pop(enemy.myBullets.index(bullet))
                    continue
            # kolizje strzalow gracza z przeciwnikiem
            for bullet in bullets:
                if bullet.y - bullet.radius < enemy.hitbox[1] + enemy.hitbox[3] and bullet.y + bullet.radius > \
                        enemy.hitbox[
                            1]:
                    if bullet.x + bullet.radius > enemy.hitbox[0] and bullet.x - bullet.radius < enemy.hitbox[0] + \
                            enemy.hitbox[2]:
                        killCount = enemy.hit(killCount)
                        bullets.pop(bullets.index(bullet))
                        continue
                if bullet.x < 1280 and bullet.x > 0:
                    bullet.x += bullet.vel
                else:
                    bullets.pop(bullets.index(bullet))
                for obstacle in obstacles:
                    if bullet.y - bullet.radius < obstacle.hitbox[1] + obstacle.hitbox[3] and bullet.y + bullet.radius > \
                            obstacle.hitbox[1]:
                        if bullet.x + bullet.radius > obstacle.hitbox[0] and bullet.x - bullet.radius < obstacle.hitbox[
                            0] + \
                                obstacle.hitbox[2]:
                            bullets.pop(bullets.index(bullet))
                # kolizje strzalow przeciwnika z przyjaciolmi
            for friend in friends:
                for bullet in enemy.myBullets:
                    if bullet.y - bullet.radius < friend.hitbox[1] + friend.hitbox[3] and bullet.y + bullet.radius > \
                            friend.hitbox[
                                1]:
                        if bullet.x + bullet.radius > friend.hitbox[0] and bullet.x - bullet.radius < friend.hitbox[0] + \
                                friend.hitbox[2]:
                            friend.hit()
                            enemy.myBullets.pop(enemy.myBullets.index(bullet))
        for enemy in enemies:
            for obstacle in obstacles:
                for bullet in enemy.myBullets:
                    if bullet.y - bullet.radius < obstacle.hitbox[1] + obstacle.hitbox[3] and bullet.y + bullet.radius > \
                            obstacle.hitbox[1]:
                        if bullet.x + bullet.radius > obstacle.hitbox[0] and bullet.x - bullet.radius < obstacle.hitbox[
                            0] + \
                                obstacle.hitbox[2]:
                            enemy.myBullets.pop(enemy.myBullets.index(bullet))

        ################################################### petla po przyjaciolach wraz z ich strzalami ###################################################################
        for friend in friends:
            if len(friend.myBullets) < len(friends) and not friend.dead and friend.myShootLoop == 1:
                friend.myBullets.append(
                    projectile(friend.x + friend.width // 2, round(friend.y + friend.height // 2), 3, (0, 0, 0), 1))
                friendShot.set_volume(0.4)
                friendShot.play()
                friend.myShootLoop = 2

            if friend.myShootLoop > 1:
                friend.myShootLoop += 1
            if friend.myShootLoop > 30:
                friend.myShootLoop = 1

            for bullet in friend.myBullets:
                if bullet.x < 1280 and bullet.x > 0 and bullet.y > 0 and bullet.y < 720:
                    bullet.x += bullet.vel
                else:
                    friend.myBullets.pop(friend.myBullets.index(bullet))
                    continue
                for obstacle in obstacles:
                    if bullet.y - bullet.radius < obstacle.hitbox[1] + obstacle.hitbox[3] and bullet.y + bullet.radius > \
                            obstacle.hitbox[1]:
                        if bullet.x + bullet.radius > obstacle.hitbox[0] and bullet.x - bullet.radius < obstacle.hitbox[
                            0] + \
                                obstacle.hitbox[2]:
                            pass
                            #friend.myBullets.pop(friend.myBullets.index(bullet))
            # Kolizje strzalow przyjaciol z przeciwnikami
            for enemy in enemies:
                for bullet in friend.myBullets:
                    if bullet.y - bullet.radius < enemy.hitbox[1] + enemy.hitbox[3] and bullet.y + bullet.radius > \
                            enemy.hitbox[
                                1]:
                        if bullet.x + bullet.radius > enemy.hitbox[0] and bullet.x - bullet.radius < enemy.hitbox[0] + \
                                enemy.hitbox[2]:
                            noMatters = enemy.hit(0)
                            friend.myBullets.pop(friend.myBullets.index(bullet))
        for friend in friends:
            for obstacle in obstacles:
                for bullet in friend.myBullets:
                    if bullet.y - bullet.radius < obstacle.hitbox[1] + obstacle.hitbox[3] and bullet.y + bullet.radius > \
                            obstacle.hitbox[1]:
                        if bullet.x + bullet.radius > obstacle.hitbox[0] and bullet.x - bullet.radius < obstacle.hitbox[
                            0] + \
                                obstacle.hitbox[2]:
                            friend.myBullets.pop(friend.myBullets.index(bullet))
        ################################################### strzaly i przyciski gracza ###################################################################
        if shootLoop > 0:
            shootLoop += 1
            reloading = 0
        if shootLoop > 30:
            shootLoop = 0
            reloading = 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and shootLoop == 0 and not player1.dead:
            if player1.sLeft:
                facing = -1
            else:
                facing = 1
            garandShot.play()
            if len(bullets) < 3:
                bullets.append(
                    projectile(player1.x + player1.width // 2, round(player1.y + player1.height // 2), 3, (0, 0, 0),
                                facing))
            shootLoop = 1

        if keys[pygame.K_LEFT] and player1.x and not player1.dead:
            player1.x -= player1.vel
            player1.left = True
            player1.right = False
            player1.sRight = False
            player1.sLeft = True
        elif keys[pygame.K_RIGHT] and player1.x < windowWidth - player1.width and not player1.dead:
            player1.x += player1.vel
            player1.left = False
            player1.right = True
            player1.sRight = True
            player1.sLeft = False
        else:
            if (player1.right):
                player1.sRight = True
            elif (player1.left):
                player1.sLeft = True
            player1.right = False
            player1.left = False
        if keys[pygame.K_UP] and player1.y > 50 and not player1.dead:
            player1.y -= player1.vel
            player1.movingVer = True
        elif keys[pygame.K_DOWN] and player1.y < windowHeight - player1.height and not player1.dead:
            player1.y += player1.vel
            player1.movingVer = True
        else:
            player1.movingVer = False
        redrawGameWindow()

pygame.quit()
