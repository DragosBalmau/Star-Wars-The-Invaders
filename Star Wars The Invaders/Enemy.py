import constants

enemyChangeX = 0
enemyChangeY = 0

enemyX = 1920 / 2
enemyY = 1080 / 2 - 300

def enemy(screen, x, y):
    screen.blit(constants.enemyImg, (x, y))
