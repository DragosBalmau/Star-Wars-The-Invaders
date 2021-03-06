import pygame

# Local Imports
import constants
import Singleplayer

pygame.init()

screen = pygame.display.set_mode((0, 0),  pygame.HWACCEL | pygame.SWSURFACE | pygame.DOUBLEBUF, vsync=0)
width = screen.get_width()
height = screen.get_height()

small_font = pygame.font.SysFont('Corbel', 35)

text_quit = small_font.render('Quit', True, constants.color)
text_singleplayer = small_font.render('Singleplayer', True, constants.color)
text_multiplayer = small_font.render('Multiplayer', True, constants.color)

logo_menu = pygame.image.load(constants.logo_star_wars_img).convert_alpha()
logo_menu = pygame.transform.scale(logo_menu, (900, 900))

logo_python = pygame.image.load(constants.logo_python).convert_alpha()
logo_python = pygame.transform.scale(logo_python, (750, 750))

logo_pygame = pygame.image.load(constants.logo_pygame).convert_alpha()
logo_pygame = pygame.transform.scale(logo_pygame, (1014, 300))

background_menu = pygame.image.load(constants.background_menu).convert()
background_menu = pygame.transform.scale(background_menu,
                                         (background_menu.get_rect().width, height)).convert_alpha()
background_x = 0


def main():

    clock = pygame.time.Clock()
    global logo_menu
    display_pregame_cinematic()
    logo_menu = pygame.image.load(constants.logo_star_wars_img).convert_alpha()
    logo_menu = pygame.transform.scale(logo_menu, (750, 750))

    while True:
        clock.tick(constants.FPS)
        menu_controls(clock)
        background()
        mouse = pygame.mouse.get_pos()
        button_singleplayer(screen, mouse, width, height)
        button_multiplayer(screen, mouse, width, height)
        button_quit(screen, mouse, width, height)

        screen.blit(logo_menu, ((width - logo_menu.get_rect().width) / 2, -100))

        # TODO de refacut cu date care nu sunt hardcodate
        screen.blit(text_singleplayer, ((width / 2 - 200) + (400 - text_singleplayer.get_rect().width) / 2,
                                        height / 2 + ((60 - text_singleplayer.get_rect().height) / 2)))
        screen.blit(text_multiplayer, ((width / 2 - 200) + (400 - text_multiplayer.get_rect().width) / 2,
                                       height / 2 + 80 + ((60 - text_multiplayer.get_rect().height) / 2)))
        screen.blit(text_quit, ((width / 2 - 200) + (400 - text_quit.get_rect().width) / 2,
                                height / 2 + 160 + + ((60 - text_quit.get_rect().height) / 2)))
        pygame.display.flip()


def menu_controls(clock):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if is_on_button_singleplayer(mouse, width, height):
                Singleplayer.init_singleplayer(screen, width, height, clock)

            elif is_on_button_multiplayer(mouse, width, height):
                pass

            elif is_on_button_quit(mouse, width, height):
                pygame.quit()
                exit()


def display_pregame_cinematic():
    pregame_cinematic = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return
        screen.fill((0, 0, 0))
        pregame_cinematic += 1

        if pregame_cinematic < 1500:
            if 0 <= pregame_cinematic < 505:
                logo_python.set_alpha(pregame_cinematic)
            if 994 <= pregame_cinematic < 1500:
                logo_python.set_alpha(255 - (pregame_cinematic - 994))
            screen.blit(logo_python, (width / 2 - logo_python.get_rect().width / 2, height / 2 - logo_python.get_rect().height / 2))
        elif 1500 <= pregame_cinematic < 3000:
            if 1500 <= pregame_cinematic < 2005:
                logo_pygame.set_alpha(pregame_cinematic - 1500)
            if 2494 <= pregame_cinematic < 3000:
                logo_pygame.set_alpha(255 - (pregame_cinematic - 2494))
            screen.blit(logo_pygame, (width / 2 - logo_pygame.get_rect().width / 2, height / 2 - logo_pygame.get_rect().height / 2))
        elif 3000 <= pregame_cinematic < 4500:
            if 3000 <= pregame_cinematic < 3505:
                logo_menu.set_alpha(pregame_cinematic - 3000)
            if 3994 <= pregame_cinematic < 4500:
                logo_menu.set_alpha(255 - (pregame_cinematic - 3994))
            screen.blit(logo_menu, (width / 2 - logo_menu.get_rect().width / 2, height / 2 - logo_menu.get_rect().height / 2))
        else:
            break
        pygame.display.flip()


def background():

    global background_menu
    global background_x
    relative_x = background_x % background_menu.get_rect().width
    screen.blit(background_menu, (relative_x - background_menu.get_rect().width, 0))
    if relative_x < width:
        screen.blit(background_menu, (relative_x, 0))
    background_x -= 0.5


# TODO
#  asociez un id pentru fiecare buton si fac o functie generala, astfel scapam de date harcodate si probabil din
#  6 functii facem una

def is_on_button_singleplayer(mouse, width, height):
    if width / 2 - 200 <= mouse[0] <= width / 2 + 200 and height / 2 <= mouse[1] <= height / 2 + 60:
        return True
    return False


def is_on_button_multiplayer(mouse, width, height):
    if width / 2 - 200 <= mouse[0] <= width / 2 + 200 and height / 2 + 80 <= mouse[1] <= height / 2 + 140:
        return True
    return False


def is_on_button_quit(mouse, width, height):
    if width / 2 - 200 <= mouse[0] <= width / 2 + 200 and height / 2 + 160 <= mouse[1] <= height / 2 + 220:
        return True
    return False


def button_singleplayer(screen, mouse, width, height):
    if is_on_button_singleplayer(mouse, width, height):
        pygame.draw.rect(screen, constants.color_light, [width / 2 - 200, height / 2, 400, 60])
    else:
        pygame.draw.rect(screen, constants.color_dark, [width / 2 - 200, height / 2, 400, 60])


def button_multiplayer(screen, mouse, width, height):
    if is_on_button_multiplayer(mouse, width, height):
        pygame.draw.rect(screen, constants.color_light, [width / 2 - 200, height / 2 + 80, 400, 60])
    else:
        pygame.draw.rect(screen, constants.color_light, [width / 2 - 200, height / 2 + 80, 400, 60])


def button_quit(screen, mouse, width, height):
    if is_on_button_quit(mouse, width, height):
        pygame.draw.rect(screen, constants.color_light, [width / 2 - 200, height / 2 + 160, 400, 60])
    else:
        pygame.draw.rect(screen, constants.color_dark, [width / 2 - 200, height / 2 + 160, 400, 60])


if __name__ == "__main__":
    main()
