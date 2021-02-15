import constants


class Player:

    def __init__(self, health=100, score=0):
        self.ChangeX = 0
        self.ChangeY = 0

        self.X = 1920 / 2
        self.Y = 1080 - 100

        self.health = health
        self.score = score


def display_player(screen, x, y):
    screen.blit(constants.playerImg, (x, y))
