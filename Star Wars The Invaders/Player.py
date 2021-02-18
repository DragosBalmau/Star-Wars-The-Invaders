import constants
import pygame


class Player:

    def __init__(self, health=100, score=0):
        self.ChangeX = 0
        self.ChangeY = 0

        self.X = 1920 / 2
        self.Y = 1080 - 100

        self.health = health
        self.score = score

        self.image = pygame.image.load(constants.player_img)
        self.image = pygame.transform.scale(self.image, (120, 120))

    def display_player(self, screen):
        screen.blit(self.image, (self.X, self.Y))

    def stay_in_screen(self, width, height):
        if self.X <= 0:
            self.X = 0
        if self.X >= width - self.image.get_width():
            self.X = width - self.image.get_width()

        if self.Y <= 0:
            self.Y = 0
        if self.Y >= height - self.image.get_height():
            self.Y = height - self.image.get_height()
