import constants
import pygame


class Enemy:

    def __init__(self, x, y, bullet):
        self.change_x = 0
        self.change_y = 0
        self.x = x
        self.y = y
        self.bullet = bullet

        self.image = pygame.image.load(constants.enemy_img)
        self.image = pygame.transform.scale(self.image, (120, 120)).convert_alpha()

        self.bullet.image = pygame.image.load(constants.laser_img_red)
        self.bullet.image = pygame.transform.scale(self.bullet.image, (80, 80)).convert_alpha()

    def display_enemy(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def verif_bullet(self):
        if self.bullet.y >= 1080 or self.bullet.player_contact:
            self.bullet.player_contact = False
            self.bullet.x = self.x + (self.image.get_rect().width / 2) - (self.bullet.image.get_rect().width / 2)
            self.bullet.y = self.y + self.image.get_rect().height
            return 0
        return 1

    def fire(self, screen):
        self.bullet.y += self.bullet.change_y_enemy
        screen.blit(self.bullet.image.convert_alpha(), (self.bullet.x, self.bullet.y))
