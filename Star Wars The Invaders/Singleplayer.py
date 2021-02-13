import pygame
import constants
import time

bulletY = 480
bulletChangeY = 10

playerChangeX = 0
playerChangeY = 0

playerX = 1920 / 2
playerY = 1080 - 100


def initSingleplayer(screen, width, height):
    while True:
        screen.fill((255, 255, 255))

        global playerX, playerY
        global playerChangeX, playerChangeY

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
                    fire(screen, playerX, bulletY)
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

        player(screen, playerX, playerY)
        pygame.display.update()


def player(screen, x, y):
    # Draw the image
    screen.blit(constants.playerImg, (x, y))


def fire(screen, x, y):
    pass
