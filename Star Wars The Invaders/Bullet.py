import constants
import pygame


class Bullet:

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.change_y_player = -10
        self.change_y_enemy = 7
        self.state = "Ready"
        self.image = pygame.image.load(constants.laser_img_blue)
        self.player_contact = False
