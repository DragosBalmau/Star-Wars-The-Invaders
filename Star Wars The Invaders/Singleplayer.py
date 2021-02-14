import pygame
import random
import constants
import math
import Enemy

playerChangeX = 0
playerChangeY = 0

playerX = 1920 / 2
playerY = 1080 - 100

bulletY = playerY
bulletX = playerX

bulletChangeY = -50
bulletState = "Ready"

score = 0
health = 100


# TODO de rezolvat sa atinga oricare parte a texturii (modif distance / dimensiunea texturii pe post de interval!!!)
def isCollision(firstObjectX, firstObjectY, secondObjectX, secondObjectY):

    distance = math.sqrt(((firstObjectX - secondObjectX) ** 2) + ((firstObjectY - secondObjectY) ** 2))
    if distance < 27:
        return True
    return False


def initSingleplayer(screen, width, height, clock):

    backgroundY = 0

    while True:

        backgroundY = backgroundWallpaper(screen, height, backgroundY)
        # screen.fill((255, 255, 255))
        # TODO De cautat o metoda prin care sa paralelizez render-ul de la fundal si cel de la entitati (sau GIFImage)
        global playerX, playerY
        global playerChangeX, playerChangeY
        global bulletX, bulletY, bulletChangeY, bulletState
        global score

        print(playerX, playerY)

        # TODO de facut functie singleplayerControls
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerChangeX = -20
                if event.key == pygame.K_RIGHT:
                    playerChangeX = 20
                if event.key == pygame.K_UP:
                    playerChangeY = -20
                if event.key == pygame.K_DOWN:
                    playerChangeY = 20
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

        collision = isCollision(Enemy.enemyX, Enemy.enemyY, bulletX, bulletY)
        if collision:
            bulletState = "Ready"
            bulletY = playerY
            score += 1
            Enemy.enemyX = random.randint(0, 1900)
            Enemy.enemyY = random.randint(0, 1000)

        displayScore(screen, score, width, height)
        displayHealth(screen, health, width, height)
        player(screen, playerX, playerY)
        Enemy.enemy(screen, Enemy.enemyX, Enemy.enemyY)

        pygame.display.update()
        clock.tick(constants.FPS)



def backgroundWallpaper(screen, height, y):

    backgroundSingleplayer = pygame.image.load("Resources/backgroundSingleplayer.png").convert()
    backgroundSingleplayer = pygame.transform.scale(backgroundSingleplayer, (backgroundSingleplayer.get_rect().width, height))

    relativeY = y % backgroundSingleplayer.get_rect().height
    screen.blit(backgroundSingleplayer, (0, relativeY - backgroundSingleplayer.get_rect().height))
    if relativeY < height:
        screen.blit(backgroundSingleplayer, (0, relativeY))
    y += 3
    return y


def player(screen, x, y):
    screen.blit(constants.playerImg, (x, y))

# TODO putin design la score si health bar
def displayScore(screen, score, width, height):

    smallfont = pygame.font.SysFont('Corbel', 35)
    textScore = smallfont.render('Score: ' + str(score), True, constants.color)
    screen.blit(textScore, (30 , height - 100))

def displayHealth(screen, health, width, height):

    smallfont = pygame.font.SysFont('Corbel', 35)
    textHealth = smallfont.render('Health: ' + str(health), True, constants.color)
    screen.blit(textHealth, (30 , height - 50))


# TODO
#  - de centrat glontul
#  - de gandit o modalitate sa trag mai multe gloante (sa creez un obiect pentru fiecare)
def fire(screen, x, y):
    global bulletState
    bulletState = "Fire"
    screen.blit(constants.bulletImg, (x, y))
