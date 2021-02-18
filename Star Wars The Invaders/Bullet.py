import constants
import pygame

    # TODO
    #  - de gandit o modalitate sa trag mai multe gloante (sa creez un obiect pentru fiecare -> Class bullet)

class Bullet:

    def __init__(self, bulletX, bulletY):
        self.Y = bulletY
        self.X = bulletX

        self.ChangeY = -10
        self.state = "Ready"
        self.image = pygame.image.load(constants.bullet_img)

    def verif_bullet(self, screen):
        if self.Y <= 0:
            self.state = "Ready"

        if self.state == "Fire":
            self.state = self.fire(screen)
            self.Y += self.ChangeY

    def fire(self, screen):

        self.state = "Fire"
        screen.blit(self.image, (self.X, self.Y))
        return self.state



