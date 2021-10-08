import pygame
import pygame.draw as dr
from random import randint

pygame.init()

FPS = 30
screen = pygame.display.set_mode((1200, 800))

count = 0
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [BLACK, YELLOW, MAGENTA, CYAN, WHITE, RED, GREEN, BLUE]
TEXT_COLORS = [WHITE, BLUE, GREEN, RED, BLACK, CYAN, MAGENTA, YELLOW]
level_color = BLACK
active_colors = [COLORS[i] for i in range(8)]
active_colors.pop(COLORS.index(level_color))
number_of_balls = 10
ball_list = []


def update_screen():
    """
    updates screen keeping all drawn balls
    """
    screen.fill(level_color)
    for ball in ball_list:
        col = ball[3]
        if ball[3] == level_color:
            col = TEXT_COLORS[COLORS.index(level_color)]
        dr.circle(screen, col, (ball[0], ball[1]), ball[2])


def new_ball():
    """
    draws new ball
    """
    x = randint(100, 1100)
    y = randint(200, 800)
    r = randint(20, 100)
    vx = randint(-5, 5)
    vy = randint(-5, 5)
    color = active_colors[randint(0, 6)]
    dr.circle(screen, color, (x, y), r)
    ball_list.append([x, y, r, color, vx, vy])


def click(event_name):
    """
    :param event_name: holds parameters of our mouseclick

    checks whether mouse was clicked in or outside of the ball, adds point if former, subtracts otherwise
    """
    global count
    ch = 1
    for ball in ball_list:
        if (event_name.pos[0] - ball[0]) ** 2 + (event_name.pos[1] - ball[1]) ** 2 <= ball[2] ** 2:
            count += 6 - ball[2] // 20
            ball_list.pop(ball_list.index(ball))
            update_screen()
            ch = 0
    if count != 0:
        count -= ch * count // 10
    score()


def score():
    """
    writes players score, changes level (background color)
    """
    global level_color, active_colors
    level_number = (count % 800) // 100
    level_color = COLORS[level_number]
    text_color = TEXT_COLORS[level_number]
    active_colors = [COLORS[i] for i in range(8)]
    active_colors.pop(COLORS.index(level_color))
    update_screen()
    font = pygame.font.Font(None, 120)
    text = font.render(str(count), True, text_color)
    screen.blit(text, (20, 20))


def move_balls():
    """
    moves balls according to their velocity
    """
    for ball_number in range(len(ball_list)):
        ball_list[ball_number][0] += ball_list[ball_number][4]
        ball_list[ball_number][1] += ball_list[ball_number][5]
        if ball_list[ball_number][0] - ball_list[ball_number][2] <= 0:
            ball_list[ball_number][4] *= -1
            ball_list[ball_number][0] -= ball_list[ball_number][0] - ball_list[ball_number][2]
        elif ball_list[ball_number][0] + ball_list[ball_number][2] >= 1200:
            ball_list[ball_number][4] *= -1
            ball_list[ball_number][0] -= ball_list[ball_number][0] + ball_list[ball_number][2] - 1200
        if ball_list[ball_number][1] - ball_list[ball_number][2] <= 0:
            ball_list[ball_number][5] *= -1
            ball_list[ball_number][1] -= ball_list[ball_number][1] - ball_list[ball_number][2]
        elif ball_list[ball_number][1] + ball_list[ball_number][2] >= 800:
            ball_list[ball_number][5] *= -1
            ball_list[ball_number][1] -= ball_list[ball_number][1] + ball_list[ball_number][2] - 800
        update_screen()
        score()


pygame.display.update()
clock = pygame.time.Clock()
finished = False

score()
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click(event)
    if len(ball_list) < number_of_balls:  # draws balls before reaching maximum
        new_ball()
    move_balls()
    pygame.display.update()

pygame.quit()
