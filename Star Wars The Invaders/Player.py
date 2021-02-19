import constants
import pygame


class Player:

    def __init__(self, health=100, score=0):
        self.change_x = 0
        self.change_y = 0

        self.x = 1920 / 2
        self.y = 1080 - 100

        self.health = health
        self.score = score

        self.image = pygame.image.load(constants.player_img)
        self.image = pygame.transform.scale(self.image, (120, 120)).convert_alpha()

    def display_player(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def stay_in_screen(self, width, height):
        if self.x <= 0:
            self.x = 0
        if self.x >= width - self.image.get_width():
            self.x = width - self.image.get_width()

        if self.y <= 0:
            self.y = 0
        if self.y >= height - self.image.get_height():
            self.y = height - self.image.get_height()
