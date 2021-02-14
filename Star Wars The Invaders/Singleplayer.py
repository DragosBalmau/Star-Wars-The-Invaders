import pygame
import random
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

bulletChangeY = -10
bulletState = "Ready"

score = 0


# TODO de rezolvat sa atinga oricare parte a texturii (modif distance / dimensiunea texturii pe post de interval!!!)
def isCollision(firstObjectX, firstObjectY, secondObjectX, secondObjectY):

    distance = math.sqrt(((firstObjectX - secondObjectX) ** 2) + ((firstObjectY - secondObjectY) ** 2))
    if distance < 27:
        return True
    return False


def initSingleplayer(screen, width, height, clock):


    backgroundY = 0

    while True:

        # screen.fill((255, 255, 255))
        # TODO BUG: the ship is moving slow !!!!!!!!!!!!!
        backgroundY = backgroundWallpaper(screen, height, backgroundY)
        global playerX, playerY
        global playerChangeX, playerChangeY
        global bulletX, bulletY, bulletChangeY, bulletState
        global enemyX, enemyY
        global score

        print(playerX, playerY)

        # TODO de facut functie singleplayerControls
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
            enemyX = random.randint(0, 1900)
            enemyY = random.randint(0, 1000)

        player(screen, playerX, playerY)
        enemy(screen, enemyX, enemyY)

        pygame.display.update()
        clock.tick(constants.FPS)


def backgroundWallpaper(screen, height, y):

    backgroundSingleplayer = pygame.image.load("Resources/backgroundSingleplayer.png").convert()
    backgroundSingleplayer = pygame.transform.scale(backgroundSingleplayer, (backgroundSingleplayer.get_rect().width, height))
    relativeY = y % backgroundSingleplayer.get_rect().height
    screen.blit(backgroundSingleplayer, (0, relativeY - backgroundSingleplayer.get_rect().height))
    if relativeY < height:
        screen.blit(backgroundSingleplayer, (0, relativeY))
    y += 5
    return y


def player(screen, x, y):
    screen.blit(constants.playerImg, (x, y))


def enemy(screen, x, y):
    screen.blit(constants.enemyImg, (x, y))


# TODO de centrat glontul
def fire(screen, x, y):
    global bulletState
    bulletState = "Fire"
    screen.blit(constants.bulletImg, (x, y))
