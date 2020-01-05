import pygame
pygame.init()

windowWidth = 1200
windowHeight = 850

win = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("World War 2")

x = 50
y = 50
width = 40
height = 60
vel = 10

run = True
while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and x > 0:
            x -= vel
        if keys[pygame.K_RIGHT] and x < windowWidth - width:
            x += vel
        if keys[pygame.K_UP] and y > 0:
            y -= vel
        if keys[pygame.K_DOWN] and y < windowHeight - height:
            y += vel

        win.fill((0,0,0))
        pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
        pygame.display.update()

pygame.quit()
