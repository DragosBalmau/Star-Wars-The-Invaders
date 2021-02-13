import constants

# stanga sus e originea
playerX = 370
playerY = 480
playerChangeX = 0
playerChangeY = 0

bulletY = 480
bulletChangeY = 10


def initSingleplayer(screen):
    pass
    # playerX += playerChangeX
    # playerY += playerChangeY
    #
    # if playerX <= 0:
    #     playerX = 0
    # if playerX >= 765:
    #     playerX = 765
    #
    # if playerY <= 0:
    #     playerY = 0
    # if playerY >= 565:
    #     playerY = 565


def player(screen, x, y):
    # Draw the image
    screen.blit(constants.playerImg, (x, y))


def fire(screen, x, y):
    pass

    # for event in pygame.event.get():
    #     if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_LEFT:
    #             playerChangeX = -0.1
    #         if event.key == pygame.K_RIGHT:
    #             playerChangeX = 0.1
    #         if event.key == pygame.K_UP:
    #             playerChangeY = -0.1
    #         if event.key == pygame.K_DOWN:
    #             playerChangeY = 0.1
    #         if event.key == pygame.K_SPACE:
    #             # fire(playerX, bulletY)
    #             pass
    #
    #     if event.type == pygame.KEYUP:
    #         if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
    #             playerChangeX = 0
    #         if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
    #             playerChangeY = 0

    # player(playerX, playerY)

