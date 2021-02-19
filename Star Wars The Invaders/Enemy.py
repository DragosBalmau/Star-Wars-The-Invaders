import constants
import pygame


class Enemy:

    def __init__(self, x, y):
        self.change_x = 0
        self.change_y = 0
        self.x = x
        self.y = y

        self.image = pygame.image.load(constants.enemy_img)
        self.image = pygame.transform.scale(self.image, (120, 120)).convert_alpha()

    def display_enemy(self, screen):
        screen.blit(self.image, (self.x, self.y))
