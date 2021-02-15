import constants
import pygame


def displayEnemy(screen, x, y):
    screen.blit(constants.enemyImg, (x, y))


class Enemy:

    def __init__(self):
        self.ChangeX = 0
        self.ChangeY = 0
        self.X = 1920 / 2
        self.Y = 1080 / 2 - 300
