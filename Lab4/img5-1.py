import pygame
import pygame.draw as dr
import numpy as np

pygame.init()

FPS = 30
screen = pygame.display.set_mode((1000, 667))
TOPSKY = (254, 213, 162)
BOTSKY = (254, 213, 196)
SUN = (252, 238, 33)
BACKMNT = (252, 152, 49)
FOREMNT = (172, 67, 52)
TOPGR = (254, 213, 148)
BOTGR = (179, 134, 148)

# background mountains:
x1 = np.arange(0, 230, 1)
xy1 = [(5, 280)]

# 1st slide:
for el in x1:
    if el <= 200:
        T = el + 10, 220 - (el ** 2 // 340)
        xy1.append(T)

# mountains-1:
xy1.append((250, 115))
xy1.append((265, 140))
xy1.append((380, 230))
xy1.append((437, 223))
xy1.append((470, 240))
xy1.append((510, 190))
xy1.append((560, 200))
xy1.append((590, 175))

# 2nd slide:
for el in x1:
    T = el / 1.5 + 590, 2 * np.cos(el / 180 * np.pi) * el / 5 + 175
    xy1.append(T)

xy1.append((800, 155))
xy1.append((835, 145))

# 3rd slide:
for el in x1:
    if el <= 60:
        T = el + 835, 145 + el ** 2 / 100
        xy1.append(T)

xy1.append((930, 165))
xy1.append((1000, 208))

# foreground mountains:
x2 = np.arange(0, 201, 1)
xy2 = [(0, 300), (5, 300), (180, 380), (220, 330), (270, 360), (300, 285), (380, 300), (450, 350), (540, 335)]

# hill:
for el in x2:
    if el < 140:
        T = el + 540, 335 - 80 * np.sin(el / 220 * np.pi)
    else:
        T = (el - 140) ** 1.7 / 10 + 680, 335 - 80 * np.sin(el / 220 * np.pi) + (el / 2 - 70)
    xy2.append(T)

xy2.append((845, 290))
xy2.append((885, 325))
xy2.append((915, 290))
xy2.append((955, 300))
xy2.append((1000, 240))
xy2.append((1000, 500))
xy2.append((0, 500))

dr.polygon(screen, TOPSKY, [(0, 0), (1000, 0), (1000, 133), (0, 133)])
dr.polygon(screen, BOTSKY, [(0, 133), (1000, 133), (1000, 266), (0, 266)])
dr.polygon(screen, TOPGR, [(0, 266), (1000, 266), (1000, 399), (0, 399)])
dr.circle(screen, SUN, (450, 125), 45)
dr.polygon(screen, BACKMNT, xy1)
dr.ellipse(screen, FOREMNT, (10, 225, 175, 480))
dr.polygon(screen, FOREMNT, xy2)
dr.polygon(screen, BOTGR, [(0, 409), (1000, 409), (1000, 667), (0, 667)])

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
