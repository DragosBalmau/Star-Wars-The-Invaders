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

    team = choose_team(screen, width, height, clock)
    print(team)
    if team == "Republic":
        pass
    elif team == "Empire":
        pass
    else:
        return

    player = Player.Player(team=team)
    enemies = create_all_enemies(team)

    level = 1
    global background_loop
    background_loop = True

    level_display_time = 0

    # TODO respawn cooldown
    respawn_cooldown_player = 0

    thread_background = threading.Thread(target=background, args=(screen, height))
    thread_background.start()

    render_index = []
    render_index = generate_enemies(level, render_index)

    enemy_picked = random_enemy_fire(enemies, render_index)

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
                    if player.bullet.state == "Ready":
                        player.bullet.y = player.y
                        player.bullet.x = player.x + (player.image.get_rect().width / 2) - (
                                    player.bullet.image.get_rect().width / 2)
                        player.bullet.state = player.fire(screen)
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
        player.verif_bullet(screen)

        enemy_picked.fire(screen)

        if is_collision(player, enemy_picked.bullet):
            enemy_picked.bullet.player_contact = True
            player.health -= 20
            player.x = width / 2
            player.y = height / 2

        if enemy_picked.verif_bullet() == 0:
            enemy_picked = random_enemy_fire(enemies, render_index)

        if len(render_index) == 0:
            level += 1
            if level > 10:
                background_loop = False
                thread_background.join()
                return
            render_index = generate_enemies(level, render_index)
            level_display_time = 0

        for enemy in enemies:
            if enemies.index(enemy) in render_index:
                if is_collision(enemy, player.bullet):
                    player.bullet.state = "Ready"
                    player.bullet.y = player.y
                    player.score += 1
                    render_index.remove(enemies.index(enemy))

        level_display_time += 1
        if level_display_time < 100:
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


def random_enemy_fire(enemies, render_index):
    picked_id = random.randint(0, 29)
    while picked_id not in render_index:
        picked_id = random.randint(0, 29)
    print(picked_id)

    return enemies[picked_id]


def create_all_enemies(team):
    enemies = []
    start_x = 60
    start_y = 60

    for enemy in range(33):
        if start_x < 1800:
            enemies.append(Enemy.Enemy(start_x, start_y, Bullet.Bullet(start_x + 20, start_y + 120), team))
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
    global background_y
    while background_loop:
        # TODO imaginea nu trebuie incarcata la fiecare apelarea a functiei
        background_game = pygame.image.load(constants.background_game).convert_alpha()
        background_game = pygame.transform.scale(background_game, (background_game.get_rect().width, height))

        relative_y = background_y % background_game.get_rect().height
        screen.blit(background_game, (0, relative_y - background_game.get_rect().height))
        if relative_y < height:
            screen.blit(background_game, (0, relative_y))
        background_y += 3


def is_collision(entity, bullet):
    if isinstance(entity, Enemy.Enemy):
        if entity.x <= bullet.x + bullet.image.get_rect().width and bullet.x <= entity.x + entity.image.get_rect().width \
                and bullet.y <= entity.y + entity.image.get_rect().height:
            return True
    else:
        if entity.x <= bullet.x + bullet.image.get_rect().width and bullet.x <= entity.x + entity.image.get_rect().width \
                and bullet.y + bullet.image.get_rect().height >= entity.y and bullet.y <= entity.y + entity.image.get_rect().height:
            return True
    return False


def choose_team(screen, width, height, clock):

    republican_team = pygame.image.load(constants.republican).convert_alpha()
    # republican_team = pygame.transform.scale(republican_team, (background_game.get_rect().width, height))
    empire_team = pygame.image.load(constants.empire).convert_alpha()
    # republican_team = pygame.transform.scale(republican_team, (background_game.get_rect().width, height))
    background_choose_team = pygame.image.load(constants.background_menu).convert_alpha()
    background_choose_team = pygame.transform.scale(background_choose_team, (background_choose_team.get_rect().width, height))

    small_font = pygame.font.SysFont('Corbel', 100)
    choose_team_text = small_font.render('Choose your team', True, constants.color)

    while True:
        clock.tick(constants.FPS)
        screen.blit(background_choose_team, (0, 0))
        screen.blit(choose_team_text, (width / 2 - choose_team_text.get_rect().width / 2, height / 4 - choose_team_text.get_rect().height / 2))
        screen.blit(republican_team, (width / 2 - 2 * republican_team.get_rect().width, height / 2.5))
        screen.blit(empire_team, (width / 2 + empire_team.get_rect().width, height / 2.5))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if width / 2 - 2 * republican_team.get_rect().width <= mouse[0] <= width / 2 - republican_team.get_rect().width and height / 2.5 <= mouse[1] <= height / 2.5 + republican_team.get_rect().height:
                    return "Republic"
                elif width / 2 + empire_team.get_rect().width <= mouse[0] <= width / 2 + 2 * empire_team.get_rect().width and height / 2.5 <= mouse[1] <= height / 2.5 + republican_team.get_rect().height:
                    return "Empire"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
        pygame.display.update()


# TODO putin design la score si health bar
# TODO schimbat fontul
# TODO de incarcat textul doar o singura data
def display_score(screen, score, width, height):
    small_font = pygame.font.SysFont('Corbel', 35)
    text_score = small_font.render('Score: ' + str(score), True, constants.color)
    screen.blit(text_score, (30, height - 100))


def display_health(screen, health, width, height):
    small_font = pygame.font.SysFont('Corbel', 35)
    text_health = small_font.render('Health: ' + str(health), True, constants.color)
    screen.blit(text_health, (30, height - 50))


def display_level(screen, level, width, height):
    small_font = pygame.font.SysFont('Corbel', 100)
    text_level = small_font.render('Level ' + str(level), True, constants.color)
    screen.blit(text_level,
                (width / 2 - text_level.get_rect().width / 2, height / 2 - text_level.get_rect().height / 2))
