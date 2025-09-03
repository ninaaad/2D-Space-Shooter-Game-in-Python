import pygame
import random
import math
from pygame import mixer
from playmenu import Menu

pygame.init()
clock = pygame.time.Clock()

# Screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Shooter ")
icon = pygame.image.load("assets/spIcon.png")
pygame.display.set_icon(icon)

# Fonts
font = pygame.font.Font("freesansbold.ttf", 28)
title_font = pygame.font.Font("freesansbold.ttf", 60)

# Sounds
mixer.music.load("assets/bgmsc.wav")
mixer.music.play(-1)

# Menu
menu = Menu(screen, font, title_font, mixer)

# Player
playerImg = pygame.image.load("assets/spMain.png")
playerX = 370
playerY = 500
playerX_change = 0

def player(x, y):
    screen.blit(playerImg, (x, y))

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_en = 7

for i in range(num_en):
    enemyImg.append(pygame.image.load("assets/monster.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(0, 100))
    enemyX_change.append(2.2)
    enemyY_change.append(0.8)

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# Bullet
bulletImg = pygame.image.load("assets/bullet32.png")
bulletX = 0
bulletY = 480
bulletY_change = 3
bullet_state = "ready"

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def iscollision(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist < 27

def run_game():
    global playerX, bulletX, bulletY, bullet_state

    # Reset game state
    playerX = 370
    bulletY = 480
    bullet_state = "ready"
    score_val = 0
    for i in range(num_en):
        enemyX[i] = random.randint(0, 735)
        enemyY[i] = random.randint(0, 100)

    running = True
    game_over_flag = False
    playerX_change = 0

    while running:
        screen.fill((0, 0, 0))
        bckgnd = pygame.image.load("assets/bgscrn.png")
        screen.blit(bckgnd, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -5
                elif event.key == pygame.K_RIGHT:
                    playerX_change = 5
                elif event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)
                        mixer.Sound("assets/laser.wav").play()
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    playerX_change = 0

        playerX += playerX_change
        playerX = max(0, min(playerX, 736))

        for i in range(num_en):
            if enemyY[i] > 440:
                game_over_flag = True
                break

            enemyX[i] += enemyX_change[i]
            enemyY[i] += enemyY_change[i]

            if enemyX[i] <= 0:
                enemyX_change[i] = 3
                enemyY_change[i] = 0.5
            elif enemyX[i] >= 736:
                enemyX_change[i] = -3
                enemyY_change[i] = 0.5

            if bulletY <= 0:
                bulletY = 480
                bullet_state = "ready"

            if bullet_state == "fire":
                fire_bullet(bulletX, bulletY)
                bulletY -= bulletY_change

            if iscollision(enemyX[i], enemyY[i], bulletX, bulletY):
                mixer.Sound("assets/explosion.wav").play()
                bulletY = 480
                bullet_state = "ready"
                score_val += 1
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(0, 100)

            enemy(enemyX[i], enemyY[i], i)

        player(playerX, playerY)

        # Score
        score = font.render("Score: " + str(score_val), True, (255, 255, 255))
        screen.blit(score, (10, 10))

        pygame.display.update()
        clock.tick(60)

        if game_over_flag:
            return menu.game_over_menu(score_val)

# --- Main Loop ---
running = True
while running:
    choice = menu.main_menu()
    if choice == "quit":
        running = False
    elif choice == "settings":
        back = menu.settings_menu()
        if back == "quit":
            running = False
    elif choice == "play":
        result = run_game()
        if result == "quit":
            running = False
        elif result == "main_menu":
            continue
        elif result == "restart_game":
            run_game()
