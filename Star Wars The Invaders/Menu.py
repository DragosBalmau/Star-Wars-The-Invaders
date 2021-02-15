import pygame
import random
import time

# Local Imports
import constants
import Singleplayer

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width = screen.get_width()
height = screen.get_height()

smallfont = pygame.font.SysFont('Corbel', 35)

textQuit = smallfont.render('Quit', True, constants.color)
textSingleplayer = smallfont.render('Singleplayer', True, constants.color)
textMultiplayer = smallfont.render('Multiplayer', True, constants.color)



def main():

    clock = pygame.time.Clock()
    backgroundX = 0

    while True:

        backgroundX = backgroundWallpaper(backgroundX)

        menuControls(clock)

        mouse = pygame.mouse.get_pos()
        buttonSingleplayer(screen, mouse, width, height)
        buttonMultiplayer(screen, mouse, width, height)
        buttonQuit(screen, mouse, width, height)

        # TODO de refacut cu date care nu sunt hardcodate
        screen.blit(textSingleplayer, ((width / 2 - 200) + (400 - textSingleplayer.get_rect().width) / 2,
                                       height / 2 + ((60 - textSingleplayer.get_rect().height) / 2)))
        screen.blit(textMultiplayer, ((width / 2 - 200) + (400 - textMultiplayer.get_rect().width) / 2,
                                      height / 2 + 80 + ((60 - textMultiplayer.get_rect().height) / 2)))
        screen.blit(textQuit, ((width / 2 - 200) + (400 - textQuit.get_rect().width) / 2,
                               height / 2 + 160 + + ((60 - textQuit.get_rect().height) / 2)))
        pygame.display.update()
        clock.tick(constants.FPS)


def menuControls(clock):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if isOnButtonSingleplayer(mouse, width, height):
                Singleplayer.initSingleplayer(screen, width, height, clock)

            elif isOnButtonMultiplayer(mouse, width, height):
                pass

            elif isOnButtonQuit(mouse, width, height):
                pygame.quit()
                exit()


def backgroundWallpaper(x):

    logoMenu = pygame.image.load("Resources/StarWarsLogo.png")
    logoMenu = pygame.transform.scale(logoMenu, (750, 750))

    backgroundMenu = pygame.image.load("Resources/backgroundMenu.png").convert()
    backgroundMenu = pygame.transform.scale(backgroundMenu, (backgroundMenu.get_rect().width, height))

    relativeX = x % backgroundMenu.get_rect().width
    screen.blit(backgroundMenu, (relativeX - backgroundMenu.get_rect().width, 0))
    if relativeX < width:
        screen.blit(backgroundMenu, (relativeX, 0))
    x -= 1
    screen.blit(logoMenu, ((width - logoMenu.get_rect().width) / 2, -100))
    return x


# TODO
#  asociez un id pentru fiecare buton si fac o functie generala, astfel scapam de date harcodate si probabil din
#  6 functii facem una

def isOnButtonSingleplayer(mouse, width, height):
    if width / 2 - 200 <= mouse[0] <= width / 2 + 200 and height / 2 <= mouse[1] <= height / 2 + 60:
        return True
    return False


def isOnButtonMultiplayer(mouse, width, height):
    if width / 2 - 200 <= mouse[0] <= width / 2 + 200 and height / 2 + 80 <= mouse[1] <= height / 2 + 140:
        return True
    return False


def isOnButtonQuit(mouse, width, height):
    if width / 2 - 200 <= mouse[0] <= width / 2 + 200 and height / 2 + 160 <= mouse[1] <= height / 2 + 220:
        return True
    return False


def buttonSingleplayer(screen, mouse, width, height):
    if isOnButtonSingleplayer(mouse, width, height):
        pygame.draw.rect(screen, constants.color_light, [width / 2 - 200, height / 2, 400, 60])
    else:
        pygame.draw.rect(screen, constants.color_dark, [width / 2 - 200, height / 2, 400, 60])


def buttonMultiplayer(screen, mouse, width, height):
    if isOnButtonMultiplayer(mouse, width, height):
        pygame.draw.rect(screen, constants.color_light, [width / 2 - 200, height / 2 + 80, 400, 60])
    else:
        pygame.draw.rect(screen, constants.color_light, [width / 2 - 200, height / 2 + 80, 400, 60])


def buttonQuit(screen, mouse, width, height):
    if isOnButtonQuit(mouse, width, height):
        pygame.draw.rect(screen, constants.color_light, [width / 2 - 200, height / 2 + 160, 400, 60])
    else:
        pygame.draw.rect(screen, constants.color_dark, [width / 2 - 200, height / 2 + 160, 400, 60])


if __name__ == "__main__":
    main()
