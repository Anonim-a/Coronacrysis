#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import random

MIN_SPEED = 3
MAX_SPEED = 6
DENSITY = 60

pygame.init()
win = pygame.display.set_mode((900, 600))

pygame.display.set_caption("Coronacrysis")

speed = 10
x = 50
y = 450
width = 200
height = 149
catched = 0
missed = 0
isJump = False
jumpCount = 10

run = True
state = "start"

# "start", "go",  "win",  "lose"


left = True
right = False

scr_st = pygame.image.load("startscreen.png")

# Подгрузка фона игры
bg = pygame.image.load("bg.png")

# Подгрузка поделей героя, врагов и прочих текстур
hero_left = pygame.image.load("hero_left.png")
hero_right = pygame.image.load("hero_right.png")
if_win = pygame.image.load("win.png")
if_lose = pygame.image.load("lose.png")
covid = pygame.image.load("covid.png")

win.blit(bg, (0, 0))

class Covid:
    x = 0
    y = 0
    speed = 0

    def update(self):
        self.y += self.speed


viruses = []

# Процесс игры
while run:
    pygame.time.delay(20)
    # Условие остановки игры
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        state = "go"

    # Обработка состояний игры
    if state == "start":
        # Игра еще не началась
        win.blit(scr_st, (0, 0))
    elif state == "win":
        win.blit(if_win, (0, 0))
        catched = 0
        missed = 0

    elif state == "lose":
        win.blit(if_lose, (0, 0))
        catched = 0
        missed = 0

    elif state == "go":
        # Обработка нажатий на клавиши передвижения
        if keys[pygame.K_LEFT] and x > 5:
            left = True
            right = False
            x -= speed

        if keys[pygame.K_RIGHT] and x < 700:
            left = False
            right = True
            x += speed

        # Обработка прыжка
        if not (isJump):
            if keys[pygame.K_SPACE]:
                isJump = True

        else:
            if jumpCount >= -10:
                if jumpCount < 0:
                    y += (jumpCount ** 2) / 2
                else:
                    y -= (jumpCount ** 2) / 2
                jumpCount -= 1

            else:
                isJump = False
                jumpCount = 10

        # Вывод на экран
        win.blit(bg, (0, 0))
        # Поворот персонажа и его помещение на экран
        if left and not (right):
            win.blit(hero_left, (x, y))
        else:
            win.blit(hero_right, (x, y))

        if random.randint(0, DENSITY) == 0:
            new_virus = Covid()
            new_virus.y = 10
            new_virus.x = random.randint(40, 860)
            new_virus.speed = random.randint(MIN_SPEED, MAX_SPEED)
            viruses.append(new_virus)

        # Covid
        sur_viruses = []
        for virus in viruses:
            # Если доктор поймал вирус
            if virus.x - x >= -5 and virus.x - x <= 205 and virus.y - y >= -5:
                # Если поймали, то пока ничего не делаем
                catched += 1

            elif virus.y >= 600:
                missed += 1

            else:
                sur_viruses.append(virus)
                win.blit(covid, (virus.x, virus.y))
                virus.update()

        viruses = sur_viruses.copy()

        if catched == 20:
            state = "win"

        if missed == 3:
            state = "lose"

    pygame.display.flip()

pygame.quit()
