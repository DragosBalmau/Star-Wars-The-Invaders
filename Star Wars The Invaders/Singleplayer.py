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
    enemy = Enemy.Enemy()
    player = Player.Player()
    bullet = Bullet.Bullet(player.X, player.Y)

    level = 1
    global background_loop
    background_loop = True

    thread_background = threading.Thread(target=background, args=(screen, height))
    thread_background.start()

    while True:

        # screen.fill((255, 255, 255))
        # TODO de cautat problema la lag-ul miscarii celorlate entitati

        print(player.X, player.Y)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.ChangeX = -7
                if event.key == pygame.K_RIGHT:
                    player.ChangeX = 7
                if event.key == pygame.K_UP:
                    player.ChangeY = -7
                if event.key == pygame.K_DOWN:
                    player.ChangeY = 7
                if event.key == pygame.K_SPACE:
                    if bullet.state == "Ready":
                        bullet.Y = player.Y
                        bullet.X = player.X + (player.image.get_rect().width / 2) - (bullet.image.get_rect().width / 2)
                        bullet.state = bullet.fire(screen)
                if event.key == pygame.K_ESCAPE:
                    background_loop = False
                    thread_background.join()
                    return

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.ChangeX = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player.ChangeY = 0

        player.X += player.ChangeX
        player.Y += player.ChangeY

        player.stay_in_screen(width, height)

        enemies = generate_enemies(set_nr_enemies(level))

        # for enemy in enemies:
        #     EnemyClass.displayEnemy(screen, enemy.X, enemy.Y)

        bullet.verif_bullet(screen)

        # TODO de mutat isCollision in Bullet ???
        collision = is_collision(enemy, bullet)
        if collision:
            bullet.state = "Ready"
            bullet.Y = player.Y
            player.score += 1
            enemy.X = random.randint(100, 1800)
            enemy.Y = random.randint(100, 900)

        display_score(screen, player.score, width, height)
        display_health(screen, player.health, width, height)

        player.display_player(screen)
        enemy.display_enemy(screen)
        pygame.display.update()
        clock.tick(constants.FPS)


def generate_enemies(number):
    enemies = []
    #
    # for enemy in range(number):
    #     enemies.append(enemy())

    return enemies


def set_nr_enemies(level):
    if level == 3:
        # meteorites
        number = 25
    elif level == 10:
        # boss level
        number = 1
    else:
        number = level * 2
    return number


def background(screen, height):
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
    if entity.X <= bullet.X + bullet.image.get_rect().width and bullet.X <= entity.X + entity.image.get_rect().width \
            and bullet.Y <= entity.Y + entity.image.get_rect().height:
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
