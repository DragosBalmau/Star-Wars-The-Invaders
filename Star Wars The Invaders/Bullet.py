import constants
import pygame


# TODO
#  - de gandit o modalitate sa trag mai multe gloante

class Bullet:

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.change_y = -10
        self.state = "Ready"
        self.image = pygame.image.load(constants.laser_img).convert_alpha()

    def verif_bullet(self, screen):
        if self.y <= 0:
            self.state = "Ready"

        if self.state == "Fire":
            self.state = self.fire(screen)
            self.y += self.change_y

    def fire(self, screen):

        self.state = "Fire"
        screen.blit(self.image, (self.x, self.y))
        return self.state
