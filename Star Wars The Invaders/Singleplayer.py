import pygame
import random
import threading

# Local imports
import constants
import Enemy
import Player
import Bullet

background_y = 0
background_loop = True


def initSingleplayer(screen, width, height, clock):
    player = Player.Player()
    enemies = create_all_enemies()
    bullet = Bullet.Bullet(player.x, player.y)

    level = 1
    global background_loop
    background_loop = True

    thread_background = threading.Thread(target=background, args=(screen, height))
    thread_background.start()

    render_index = []
    render_index = generate_enemies(level, render_index)

    while True:

        clock.tick(constants.FPS)

        # screen.fill((255, 255, 255))
        # TODO de cautat problema la lag-ul miscarii celorlate entitati

        # print(player.X, player.Y)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.change_x = -7
                if event.key == pygame.K_RIGHT:
                    player.change_x = 7
                if event.key == pygame.K_UP:
                    player.change_y = -7
                if event.key == pygame.K_DOWN:
                    player.change_y = 7
                if event.key == pygame.K_SPACE:
                    if bullet.state == "Ready":
                        bullet.y = player.y
                        bullet.x = player.x + (player.image.get_rect().width / 2) - (bullet.image.get_rect().width / 2)
                        bullet.state = bullet.fire(screen)
                if event.key == pygame.K_ESCAPE:
                    background_loop = False
                    thread_background.join()
                    return

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.change_x = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player.change_y = 0

        player.x += player.change_x
        player.y += player.change_y

        player.stay_in_screen(width, height)
        bullet.verif_bullet(screen)

        if len(render_index) == 0:
            level += 1
            render_index = generate_enemies(level, render_index)

        for enemy in enemies:
            if enemies.index(enemy) in render_index:
                collision = is_collision(enemy, bullet)
                if collision:
                    bullet.state = "Ready"
                    bullet.y = player.y
                    player.score += 1
                    render_index.remove(enemies.index(enemy))

        display_level(screen, level, width, height)
        display_score(screen, player.score, width, height)
        display_health(screen, player.health, width, height)

        player.display_player(screen)

        for enemy in enemies:
            if enemies.index(enemy) in render_index:
                enemy.display_enemy(screen)

        pygame.display.update()


def generate_enemies(level, render_index):
    for i in range(set_nr_enemies(level)):
        position = random.randint(0, 29)
        while position in render_index:
            position = random.randint(0, 29)
        render_index.append(position)

    return render_index


def create_all_enemies():
    enemies = []
    start_x = 60
    start_y = 60

    for enemy in range(33):
        if start_x < 1800:
            enemies.append(Enemy.Enemy(start_x, start_y))
            start_x += 186.66
        else:
            start_y += 160
            start_x = 60

    return enemies


def set_nr_enemies(level):
    # if level == 3:
    #     # meteorites
    #     number = 25
    if level == 10:
        # boss level
        number = 1
    else:
        number = level * 2

    print(level, number)
    return number


def background(screen, height):
    global background_loop
    while background_loop:
        global background_y
        background_game = pygame.image.load(constants.background_game).convert_alpha()
        background_game = pygame.transform.scale(background_game, (background_game.get_rect().width, height))

        relative_y = background_y % background_game.get_rect().height
        screen.blit(background_game, (0, relative_y - background_game.get_rect().height))
        if relative_y < height:
            screen.blit(background_game, (0, relative_y))
        background_y += 3


def is_collision(entity, bullet):
    if entity.x <= bullet.x + bullet.image.get_rect().width and bullet.x <= entity.x + entity.image.get_rect().width \
            and bullet.y <= entity.y + entity.image.get_rect().height:
        return True
    return False


# TODO putin design la score si health bar
def display_score(screen, score, width, height):
    small_font = pygame.font.SysFont('Corbel', 35)
    text_score = small_font.render('Score: ' + str(score), True, constants.color)
    screen.blit(text_score, (30, height - 100))


def display_health(screen, health, width, height):
    small_font = pygame.font.SysFont('Corbel', 35)
    text_health = small_font.render('Health: ' + str(health), True, constants.color)
    screen.blit(text_health, (30, height - 50))


def display_level(screen, level, width, height):
    small_font = pygame.font.SysFont('Corbel', 35)
    text_health = small_font.render('Level: ' + str(level), True, constants.color)
    screen.blit(text_health, (30, height - 150))
