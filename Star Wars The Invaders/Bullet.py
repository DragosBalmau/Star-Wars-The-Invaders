import constants


class Bullet:

    def __init__(self, bulletX, bulletY):
        self.Y = bulletY
        self.X = bulletX

        self.ChangeY = -50
        self.state = "Ready"

    def verif_bullet(self, screen):
        if self.Y <= 0:
            self.state = "Ready"

        if self.state == "Fire":
            self.state = fire(screen, self.X, self.Y, self.state)
            self.Y += self.ChangeY


# TODO
#  - de centrat glontul
#  - de gandit o modalitate sa trag mai multe gloante (sa creez un obiect pentru fiecare -> Class bullet)
def fire(screen, x, y, state):
    state = "Fire"
    screen.blit(constants.bulletImg, (x, y))
    return state
