import pygame
import random
import constants
import math
import Enemy
import Player
import Bullet


def initSingleplayer(screen, width, height, clock):
    enemy = Enemy.Enemy()
    player = Player.Player()
    bullet = Bullet.Bullet(player.X, player.Y)

    backgroundY = 0
    level = 1

    while True:

        # screen.fill((255, 255, 255))
        # TODO De cautat o metoda prin care sa paralelizez render-ul de la fundal si cel de la entitati (sau GIFImage)
        backgroundY = backgroundWallpaper(screen, height, backgroundY)
        print(player.X, player.Y)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.ChangeX = -20
                if event.key == pygame.K_RIGHT:
                    player.ChangeX = 20
                if event.key == pygame.K_UP:
                    player.ChangeY = -20
                if event.key == pygame.K_DOWN:
                    player.ChangeY = 20
                if event.key == pygame.K_SPACE:
                    if bullet.state == "Ready":
                        bullet.Y = player.Y
                        bullet.X = player.X
                        bullet.state = Bullet.fire(screen, bullet.X, bullet.Y, bullet.state)
                if event.key == pygame.K_ESCAPE:
                    return

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.ChangeX = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player.ChangeY = 0

        player.X += player.ChangeX
        player.Y += player.ChangeY

        player.X, player.Y = stayInTheScreen(player.X, player.Y, width, height)

        enemies = generateEnemies(setNumberEnemies(level))

        # for enemy in enemies:
        #     EnemyClass.displayEnemy(screen, enemy.X, enemy.Y)

        bullet.verif_bullet(screen)

        # TODO de mutat isCollision in Bullet
        collision = isCollision(enemy.X, enemy.Y, bullet.X, bullet.Y)
        if collision:
            bullet.state = "Ready"
            bullet.Y = player.Y
            player.score += 1
            enemy.X = random.randint(0, 1900)
            enemy.Y = random.randint(0, 1000)

        displayScore(screen, player.score, width, height)
        displayHealth(screen, player.health, width, height)

        Player.display_player(screen, player.X, player.Y)

        Enemy.displayEnemy(screen, enemy.X, enemy.Y)
        pygame.display.update()
        clock.tick(constants.FPS)


def generateEnemies(number):
    enemies = []
    #
    # for enemy in range(number):
    #     enemies.append(enemy())

    return enemies


def setNumberEnemies(level):
    if level == 3:
        # meteorites
        number = 25
    elif level == 10:
        # boss level
        number = 1
    else:
        number = level * 2
    return number


def stayInTheScreen(playerX, playerY, width, height):
    if playerX <= 0:
        playerX = 0
    if playerX >= width - constants.playerImg.get_width():
        playerX = width - constants.playerImg.get_width()

    if playerY <= 0:
        playerY = 0
    if playerY >= height - constants.playerImg.get_height():
        playerY = height - constants.playerImg.get_height()

    return playerX, playerY


def backgroundWallpaper(screen, height, y):
    backgroundSingleplayer = pygame.image.load("Resources/backgroundSingleplayer.png").convert_alpha()
    backgroundSingleplayer = pygame.transform.scale(backgroundSingleplayer,
                                                    (backgroundSingleplayer.get_rect().width, height))

    relativeY = y % backgroundSingleplayer.get_rect().height
    screen.blit(backgroundSingleplayer, (0, relativeY - backgroundSingleplayer.get_rect().height))
    if relativeY < height:
        screen.blit(backgroundSingleplayer, (0, relativeY))
    y += 3
    return y


# TODO de rezolvat sa atinga oricare parte a texturii (modif distance / dimensiunea texturii pe post de interval!!!)
def isCollision(object_x, object_y, bullet_x, bullet_y):
    distance = math.sqrt((((object_x + constants.enemyImg.get_rect().width / 2) - bullet_x) ** 2) + (((object_y + constants.enemyImg.get_rect().height / 2) - bullet_y) ** 2))
    if distance <= constants.enemyImg.get_rect().height / 2:
        return True
    return False


# TODO putin design la score si health bar
def displayScore(screen, score, width, height):
    smallfont = pygame.font.SysFont('Corbel', 35)
    textScore = smallfont.render('Score: ' + str(score), True, constants.color)
    screen.blit(textScore, (30, height - 100))


def displayHealth(screen, health, width, height):
    smallfont = pygame.font.SysFont('Corbel', 35)
    textHealth = smallfont.render('Health: ' + str(health), True, constants.color)
    screen.blit(textHealth, (30, height - 50))
