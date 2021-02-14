import pygame
import constants
import math

playerChangeX = 0
playerChangeY = 0

playerX = 1920 / 2
playerY = 1080 - 100

enemyChangeX = 0
enemyChangeY = 0

enemyX = 1920 / 2
enemyY = 1080 / 2 - 300

bulletY = playerY
bulletX = playerX

bulletChangeY = -5
bulletState = "Ready"

score = 0

# TODO de rezolvat sa atinga oricare parte a texturii (modif distance / dimensiunea texturii pe post de interval!!!)
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(((enemyX - bulletX) ** 2) + ((enemyY - bulletY) ** 2))
    if distance < 27:
        return True
    return False


def initSingleplayer(screen, width, height):
    while True:
        screen.fill((255, 255, 255))

        global playerX, playerY
        global playerChangeX, playerChangeY
        global bulletX, bulletY, bulletChangeY, bulletState
        global enemyX, enemyY
        global score

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerChangeX = -1
                if event.key == pygame.K_RIGHT:
                    playerChangeX = 1
                if event.key == pygame.K_UP:
                    playerChangeY = -1
                if event.key == pygame.K_DOWN:
                    playerChangeY = 1
                if event.key == pygame.K_SPACE:
                    if bulletState == "Ready":
                        bulletY = playerY
                        bulletX = playerX
                        fire(screen, bulletX, bulletY)
                if event.key == pygame.K_ESCAPE:
                    return

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerChangeX = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    playerChangeY = 0

        playerX += playerChangeX
        playerY += playerChangeY

        if playerX <= 0:
            playerX = 0
        if playerX >= width - constants.playerImg.get_width():
            playerX = width - constants.playerImg.get_width()

        if playerY <= 0:
            playerY = 0
        if playerY >= height - constants.playerImg.get_height():
            playerY = height - constants.playerImg.get_height()


        if bulletY <= 0:
            bulletState = "Ready"

        if bulletState == "Fire":
            fire(screen, bulletX, bulletY)
            bulletY += bulletChangeY

        collision = isCollision(enemyX, enemyY, bulletX, bulletY)
        if collision:
            bulletState = "Ready"
            bulletY = playerY
            score += 1
            print(score)

        player(screen, playerX, playerY)
        enemy(screen, enemyX, enemyY)


        pygame.display.update()


def player(screen, x, y):
    screen.blit(constants.playerImg, (x, y))


def enemy(screen, x, y):
    screen.blit(constants.enemyImg, (x, y))


def fire(screen, x, y):
    global bulletState
    bulletState = "Fire"
    screen.blit(constants.bulletImg, (x, y))
