import pygame
import pygame.draw as dr
from random import random, randint

pygame.init()

FPS = 30
screen = pygame.display.set_mode((1250, 750))

possible_shape_number_maximum = 0
shape_list = []
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

ball_speed = 10  # starting speed of shapes and
square_speed = 5  # hitting wall resets shape's speed to its given constant
square_fracture_acceleration = 5  # clicked big square will fracture, and new squares will gain extra speed
number_of_shapes = 8


def update_screen():
    """
    updates screen keeping all drawn balls and shapes
    """
    screen.fill(level_color)
    for shape in shape_list:
        col = shape[4]
        if shape[4] == level_color:
            col = TEXT_COLORS[COLORS.index(level_color)]
        if shape[0] == "ball":
            dr.circle(screen, col, (shape[1], shape[2]), shape[3])
        elif shape[0] == "square":
            dr.rect(screen, col, (shape[1], shape[2], shape[3], shape[3]))


def new_ball(speed):
    """
    :param speed: starting ball velocity

    draws new ball
    """
    x = randint(100, 1100)
    y = randint(200, 800)
    r = randint(20, 100)
    direction_x = random() - 0.5
    direction_y = random() - 0.5
    if direction_x != 0:
        direction_x *= 1 / abs(direction_x)
    if direction_y != 0:
        direction_y *= 1 / abs(direction_y)
    vx = speed * random() * direction_x
    vy = (speed ** 2 - vx ** 2) ** (1 / 2) * direction_y
    color = active_colors[randint(0, 6)]
    dr.circle(screen, color, (x, y), r)
    shape_list.append(["ball", x, y, r, color, vx, vy])
    return 1


def new_square(speed):
    """
    :param speed: starting square velocity

    draws new square
    """
    x = randint(100, 1100)
    y = randint(200, 800)
    a = randint(81, 320)
    direction_x = random() - 0.5
    direction_y = random() - 0.5
    if direction_x != 0:
        direction_x *= 1 / abs(direction_x)
    if direction_y != 0:
        direction_y *= 1 / abs(direction_y)
    vx = speed * random() * direction_x
    vy = (speed ** 2 - vx ** 2) ** (1 / 2) * direction_y
    color = active_colors[randint(0, 6)]
    dr.circle(screen, color, (x, y), a)
    shape_list.append(["square", x, y, a, color, vx, vy])
    if a <= 160:
        return 5
    elif a <= 320:
        return 21


def click(event_name):
    """
    :param event_name: holds parameters of our mouseclick

    checks whether mouse was clicked in or outside of the ball, adds point if former, subtracts otherwise
    """
    global count, possible_shape_number_maximum
    ch = 1
    for shape in shape_list:
        if shape[0] == "ball":
            if (event_name.pos[0] - shape[1]) ** 2 + (event_name.pos[1] - shape[2]) ** 2 <= shape[3] ** 2:
                possible_shape_number_maximum -= 1
                count += 5 - shape[3] // 20
                shape_list.pop(shape_list.index(shape))
                update_screen()
                ch = 0
        if shape[0] == "square":
            if event_name.pos[0] >= shape[1]:
                if event_name.pos[0] <= shape[1] + shape[3]:
                    if event_name.pos[1] >= shape[2]:
                        if event_name.pos[1] <= shape[2] + shape[3]:
                            ch = 0
                            possible_shape_number_maximum -= 1
                            if shape[3] > 80:
                                shape_list.append([shape[0], shape[1], shape[2], shape[3] / 2, shape[4],
                                                   -square_fracture_acceleration - abs(shape[5]),
                                                   -square_fracture_acceleration - abs(shape[6])])
                                shape_list.append([shape[0], shape[1] + shape[3] / 2, shape[2], shape[3] / 2, shape[4],
                                                   abs(shape[5]) + square_fracture_acceleration,
                                                   -square_fracture_acceleration - abs(shape[6])])
                                shape_list.append([shape[0], shape[1], shape[2] + shape[3] / 2, shape[3] / 2, shape[4],
                                                   -square_fracture_acceleration - abs(shape[5]),
                                                   abs(shape[6]) + square_fracture_acceleration])
                                shape_list.append(
                                    [shape[0], shape[1] + shape[3] / 2, shape[2] + shape[3] / 2, shape[3] / 2, shape[4],
                                     abs(shape[5]) + square_fracture_acceleration,
                                     abs(shape[6]) + square_fracture_acceleration])
                                shape_list.pop(shape_list.index(shape))
                            else:
                                shape_list.pop(shape_list.index(shape))
                                count += 2
    if count != 0:
        count -= ch * count // 10
    score()


def score():
    """
    writes players score, changes level (background color)
    """
    global level_color, active_colors
    level_number = (count % 400) // 50
    level_color = COLORS[level_number]
    text_color = TEXT_COLORS[level_number]
    active_colors = [COLORS[j] for j in range(8)]
    active_colors.pop(COLORS.index(level_color))
    update_screen()
    font = pygame.font.Font(None, 120)
    text = font.render(str(count), True, text_color)
    screen.blit(text, (20, 20))


def move_shapes():
    """
    moves shapes according to their velocity, hitting walls results in randomisation of it
    """
    for shape_number in range(len(shape_list)):
        shape_list[shape_number][1] += shape_list[shape_number][5]
        shape_list[shape_number][2] += shape_list[shape_number][6]

        if shape_list[shape_number][0] == "ball":
            shape_velocity = ball_speed
            hit_velocity = ball_speed * (2 * random() - 1)  # new velocity for the axis of hit wall
            sizes = [shape_list[shape_number][3]] * 4  # contains variables deciding figures borders
        elif shape_list[shape_number][0] == "square":  # (first 2 : x-axis (+ and -), second 2 : y-axis (+ and -)
            shape_velocity = square_speed
            hit_velocity = square_speed * (2 * random() - 1)
            sizes = [shape_list[shape_number][3], 0] * 2
        else:
            shape_velocity = 0
            hit_velocity = 0
            sizes = [0] * 4

        if shape_list[shape_number][1] - sizes[1] <= 0:
            shape_list[shape_number][5] = (shape_velocity ** 2 - hit_velocity ** 2) ** (1 / 2)
            shape_list[shape_number][6] = hit_velocity  # randomizes velocities after hitting a wall
            shape_list[shape_number][1] -= shape_list[shape_number][1] - sizes[1]
        elif shape_list[shape_number][1] + sizes[0] >= 1250:
            shape_list[shape_number][5] = -(shape_velocity ** 2 - hit_velocity ** 2) ** (1 / 2)
            shape_list[shape_number][6] = hit_velocity
            shape_list[shape_number][1] -= shape_list[shape_number][1] + sizes[0] - 1250
        if shape_list[shape_number][2] - sizes[3] <= 0:
            shape_list[shape_number][6] = (shape_velocity ** 2 - hit_velocity ** 2) ** (1 / 2)
            shape_list[shape_number][5] = hit_velocity
            shape_list[shape_number][2] -= shape_list[shape_number][2] - sizes[3]
        elif shape_list[shape_number][2] + sizes[2] >= 750:
            shape_list[shape_number][6] = -(shape_velocity ** 2 - hit_velocity ** 2) ** (1 / 2)
            shape_list[shape_number][5] = hit_velocity
            shape_list[shape_number][2] -= shape_list[shape_number][2] + sizes[2] - 750
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
    if len(shape_list) < number_of_shapes:  # draws balls and other shapes before reaching maximum
        if random() >= 0.2 or possible_shape_number_maximum >= 2 * number_of_shapes - 1:
            possible_shape_number_maximum += new_ball(ball_speed)
        else:
            possible_shape_number_maximum += new_square(square_speed)
    move_shapes()
    pygame.display.update()

pygame.quit()
