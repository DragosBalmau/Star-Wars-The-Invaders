import constants
import pygame


# TODO
#  - de gandit o modalitate sa trag mai multe gloante

class Bullet:

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.change_y_player = -10
        self.change_y_enemy = 7
        self.state = "Ready"
        self.image = pygame.image.load(constants.laser_img_blue)
        self.player_contact = False
