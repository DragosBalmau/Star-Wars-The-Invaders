import pygame
import random
import threading

# Local imports
import constants
import Bullet
import Enemy
import Player

background_y = 0
background_loop = True


def init_singleplayer(screen, width, height, clock):
    small_font = pygame.font.SysFont('Corbel', 35)
    big_font = pygame.font.SysFont('Corbel', 100)

    team = choose_team(screen, width, height, clock)
    print(team)
    if team == "Republic":
        pass
    elif team == "Empire":
        pass
    else:
        return

    pygame.display.flip()
    # display_star_wars_cinematic(screen, width, height, clock)

    player = Player.Player(team=team)
    enemies = create_all_enemies(team)

    level = 1
    global background_loop
    background_loop = True

    level_display_time = 0

    # TODO respawn cooldown
    respawn_cooldown_player = 0

    thread_background = threading.Thread(target=background, args=(screen, height, clock))
    thread_background.start()

    render_index = []
    render_index = generate_enemies(level, render_index)

    enemy_picked = random_enemy_fire(enemies, render_index)
    xwing_sound = pygame.mixer.Sound(constants.xwing_sound)
    fighter_sound = pygame.mixer.Sound(constants.fighter_sound)

    while True:

        clock.tick(constants.FPS)

        # screen.fill((255, 255, 255))
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
                        xwing_sound.play()
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

        if enemy_picked.fire(screen):
            pass
            # fighter_sound.play()

        if is_collision(player, enemy_picked.bullet):
            enemy_picked.bullet.player_contact = True
            player.health -= 20
            player.x = width / 2 - player.image.get_rect().width / 2
            player.y = height - 150

        if enemy_picked.verif_bullet() == 0:
            enemy_picked = random_enemy_fire(enemies, render_index)

        if len(render_index) == 0:
            level += 1
            if level > 10:
                background_loop = False
                thread_background.join()
                lose_win(screen, width, height, clock, "Win")
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

                if is_collision(player, enemy):
                    player.health -= 20
                    player.x = width / 2 - player.image.get_rect().width / 2
                    player.y = height - 150

        level_display_time += 1
        if level_display_time < 100:
            display_level(screen, level, width, height, big_font)
        display_score(screen, player.score, height, small_font)
        display_health(screen, player.health, height, small_font)

        if player.health == 0:
            background_loop = False
            thread_background.join()
            lose_win(screen, width, height, clock, "Lose")
            return

        player.display_player(screen)

        for enemy in enemies:
            if enemies.index(enemy) in render_index:
                enemy.display_enemy(screen)

        pygame.display.flip()


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


def lose_win(screen, width, height, clock, state):

    lose_win_image = pygame.image.load(constants.win)
    if state == "Lose":
        lose_win_image = pygame.image.load(constants.lose)
    lose_win_image = pygame.transform.scale(lose_win_image, (700, 700)).convert_alpha()

    background_lose_win = pygame.image.load(constants.background_menu).convert_alpha()
    background_lose_win = pygame.transform.scale(background_lose_win,
                                                 (background_lose_win.get_rect().width, height))
    alpha_factor = 0
    background_lose_win.set_alpha(alpha_factor)
    lose_win_image.set_alpha(alpha_factor)

    x_text = width / 2 - lose_win_image.get_rect().width / 2
    y_text = height / 2 - lose_win_image.get_rect().height / 2

    while True:
        clock.tick(constants.FPS)
        while alpha_factor <= 255:

            clock.tick(constants.FPS)
            background_lose_win.set_alpha(alpha_factor)
            lose_win_image.set_alpha(alpha_factor)

            screen.blit(background_lose_win, (0, 0))
            screen.blit(lose_win_image, (x_text, y_text))

            alpha_factor += 1
            # mouse = pygame.mouse.get_pos()
            # if width / 2 - 450 <= mouse[0] <= width / 2 - 50 and height / 2 + 100 <= mouse[1] <= height / 2 + 160:
            #     pygame.draw.rect(screen, constants.color_light, [width / 2 - 450, height / 2 + 100, 400, 60])
            # else:
            #     pygame.draw.rect(screen, constants.color_dark, [width / 2 - 450, height / 2 + 100, 400, 60])
            #
            # if width / 2 + 50 <= mouse[0] <= width / 2 + 450 and height / 2 + 100 <= mouse[1] <= height / 2 + 160:
            #     pygame.draw.rect(screen, constants.color_light, [width / 2 + 50, height / 2 + 100, 400, 60])
            # else:
            #     pygame.draw.rect(screen, constants.color_dark, [width / 2 + 50, height / 2 + 100, 400, 60])
            pygame.display.flip()
        return


def background(screen, height, clock):
    global background_loop
    global background_y

    background_game = pygame.image.load(constants.background_game).convert_alpha()
    background_game = pygame.transform.scale(background_game, (background_game.get_rect().width, height))

    while background_loop:
        clock.tick(constants.FPS)
        relative_y = background_y % background_game.get_rect().height
        screen.blit(background_game, (0, relative_y - background_game.get_rect().height))
        if relative_y < height:
            screen.blit(background_game, (0, relative_y))
        background_y += 0.5


def is_collision(entity, bullet):
    if isinstance(entity, Enemy.Enemy) and isinstance(bullet, Bullet.Bullet):
        if entity.x <= bullet.x + bullet.image.get_rect().width and \
                bullet.x <= entity.x + entity.image.get_rect().width \
                and bullet.y <= entity.y + entity.image.get_rect().height:
            return True
    elif isinstance(entity, Enemy.Enemy) and isinstance(bullet, Bullet.Bullet):
        if entity.x <= bullet.x + bullet.image.get_rect().width - 30 and \
                bullet.x + 30 <= entity.x + entity.image.get_rect().width \
                and bullet.y + bullet.image.get_rect().height >= entity.y and \
                bullet.y <= entity.y + entity.image.get_rect().height:
            return True
    else:
        player = entity
        enemy = bullet
        if player.x <= enemy.x + enemy.image.get_rect().width - 10 and \
                enemy.x + 10 <= player.x + player.image.get_rect().width \
                and enemy.y + enemy.image.get_rect().height >= player.y and \
                enemy.y <= player.y + player.image.get_rect().height:
            return True

    return False


def display_star_wars_cinematic(screen, width, height, clock):
    big_font = pygame.font.SysFont('Arial', 100)

    cinematic_text_part1 = big_font.render('A long time ago in a galaxy far,', True, constants.color_blue)
    cinematic_text_part2 = big_font.render('far away....', True, constants.color_blue)

    background_cinematic = pygame.image.load(constants.background_menu).convert_alpha()
    background_cinematic = pygame.transform.scale(background_cinematic, (background_cinematic.get_rect().width, height))

    logo_star_wars = pygame.image.load(constants.logo_star_wars_img).convert_alpha()
    logo_star_wars = pygame.transform.scale(logo_star_wars, (1800, 1800))

    song_star_wars = pygame.mixer.Sound(constants.theme_star_wars)

    cinematic_counter = 0

    x_text = width / 2 - cinematic_text_part1.get_rect().width / 2
    y_text = height / 2 - cinematic_text_part1.get_rect().height / 2 - 50

    dim_x = logo_star_wars.get_rect().width
    dim_y = logo_star_wars.get_rect().height

    song_ok = True

    while True:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return

        clock.tick(constants.FPS)
        screen.blit(background_cinematic, (0, 0))
        cinematic_counter += 1

        if cinematic_counter < 1500:

            if 0 <= cinematic_counter < 505:
                cinematic_text_part1.set_alpha(cinematic_counter)
                cinematic_text_part2.set_alpha(cinematic_counter)
            elif 994 <= cinematic_counter < 1500:
                cinematic_text_part1.set_alpha(255 - (cinematic_counter - 994))
                cinematic_text_part2.set_alpha(255 - (cinematic_counter - 994))
            else:
                cinematic_counter += 6

            screen.blit(cinematic_text_part1, (x_text, y_text))
            screen.blit(cinematic_text_part2, (x_text, y_text + cinematic_text_part1.get_rect().height + 5))

        elif 1500 <= cinematic_counter < 6000:

            if song_ok:
                song_ok = False
                song_star_wars.play()

            logo_star_wars = pygame.image.load(constants.logo_star_wars_img).convert_alpha()
            logo_star_wars = pygame.transform.scale(logo_star_wars, (dim_x, dim_y))
            x_logo = width / 2 - dim_x / 2
            y_logo = height / 2 - dim_y / 2
            screen.blit(logo_star_wars, (x_logo, y_logo))

            if dim_x - 4 and dim_y - 4:
                dim_x -= 4
                dim_y -= 4

            else:
                song_star_wars.stop()
                return
        pygame.display.flip()


def choose_team(screen, width, height, clock):
    republican_team = pygame.image.load(constants.republican).convert_alpha()
    empire_team = pygame.image.load(constants.empire).convert_alpha()
    background_choose_team = pygame.image.load(constants.background_menu).convert_alpha()
    background_choose_team = pygame.transform.scale(background_choose_team,
                                                    (background_choose_team.get_rect().width, height))

    small_font = pygame.font.SysFont('Corbel', 100)
    choose_team_text = small_font.render('Choose your team', True, constants.color)

    while True:
        clock.tick(constants.FPS)
        screen.blit(background_choose_team, (0, 0))
        screen.blit(choose_team_text, (
            width / 2 - choose_team_text.get_rect().width / 2, height / 4 - choose_team_text.get_rect().height / 2))
        screen.blit(republican_team, (width / 2 - 2 * republican_team.get_rect().width, height / 2.5))
        screen.blit(empire_team, (width / 2 + empire_team.get_rect().width, height / 2.5))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if width / 2 - 2 * republican_team.get_rect().width <= mouse[
                    0] <= width / 2 - republican_team.get_rect().width and height / 2.5 <= mouse[
                    1] <= height / 2.5 + republican_team.get_rect().height:
                    return "Republic"
                elif width / 2 + empire_team.get_rect().width <= mouse[
                    0] <= width / 2 + 2 * empire_team.get_rect().width and height / 2.5 <= mouse[
                    1] <= height / 2.5 + republican_team.get_rect().height:
                    return "Empire"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
        pygame.display.flip()


# TODO putin design la score si health bar
# TODO schimbat fontul
def display_score(screen, score, height, small_font):
    text_score = small_font.render('Score: ' + str(score), True, constants.color)
    screen.blit(text_score, (30, height - 100))


def display_health(screen, health, height, small_font):
    text_health = small_font.render('Health: ' + str(health), True, constants.color)
    screen.blit(text_health, (30, height - 50))


def display_level(screen, level, width, height, big_font):
    text_level = big_font.render('Level ' + str(level), True, constants.color)
    screen.blit(text_level,
                (width / 2 - text_level.get_rect().width / 2, height / 2 - text_level.get_rect().height / 2))
