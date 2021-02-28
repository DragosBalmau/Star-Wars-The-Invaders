import pygame
import constants


class Boss:

    def __init__(self, bullet):
        self.hp = 100
        self.bullet = bullet
        self.changeX = 9
        self.x = 100
        self.y = 200
        self.image = pygame.image.load(constants.boss).convert_alpha()
        self.image = pygame.transform.scale(self.image, (200, 120)).convert_alpha()
        self.bullet.image = pygame.image.load(constants.laser_img_green)
        self.bullet.image = pygame.transform.scale(self.bullet.image, (80, 80)).convert_alpha()

    def constant_move(self, screen):
        self.x += self.changeX
        if self.x + self.image.get_rect().width + self.changeX > 1920 or self.x + self.changeX < 0:
            self.changeX *= -1
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
        return True

