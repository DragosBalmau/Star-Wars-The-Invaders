import constants
import pygame


class Enemy:

    def __init__(self):

        self.ChangeX = 0
        self.ChangeY = 0
        self.X = 1920 / 2
        self.Y = 1080 / 2 - 300

        self.image = pygame.image.load(constants.enemy_img)
        self.image = pygame.transform.scale(self.image, (120, 120))

    def display_enemy(self, screen):
        screen.blit(self.image, (self.X, self.Y))