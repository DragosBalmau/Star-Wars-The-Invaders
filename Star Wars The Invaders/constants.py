import pygame

# TODO fara importuri in constante, doar variabile de tipuri primitive

FPS = 120

# Colors
color = (255, 255, 255)
color_light = (170, 170, 170)
color_dark = (100, 100, 100)

# Images
background = pygame.image.load("Resources\_backgroung.jpg")



playerImg = pygame.image.load("Resources\\x-wing.png")
playerImg = pygame.transform.scale(playerImg, (120, 120))

enemyImg = pygame.image.load("Resources\\fighter.png")
enemyImg = pygame.transform.scale(enemyImg, (120, 120))

bulletImg = pygame.image.load("Resources\Bullet.png")
bulletImg = pygame.transform.scale(bulletImg, (60, 60))