import pygame
import pygame.draw as dr
import numpy as np

pygame.init()

# colors
TOP_SKY_COLOR = (254, 213, 162)
BOTTOM_SKY_COLOR = (254, 213, 196)
SUN_COLOR = (252, 238, 33)
BACK_MOUNTAIN_COLOR = (252, 152, 49)
MIDDLE_MOUNTAIN_COLOR = (172, 67, 52)
TOP_MOUNTAIN_COLOR = (48, 16, 38)
TOP_GROUND_COLOR = (254, 213, 148)
BOTTOM_GROUND_COLOR = (179, 134, 148)
BIRD_COLOR = (66, 33, 11)

FPS = 30

DISPLAY_SIZE = (1000, 667)
screen = pygame.display.set_mode(DISPLAY_SIZE)


def draw_bird(x, y, bird_size):
    """
    Draw one bird

    :param x: bird center coordinate
    :param y: bird top coordinate
    :param bird_size: height of bird
    """
    bird_shape = [(x, y), (x + 2 * bird_size, y - bird_size)]
    x = x + 2 * bird_size
    y = y - bird_size
    for i in range(10):
        new_top = x - i / 10 * 2 * bird_size, y + bird_size * i ** 2 / 100
        bird_shape.append(new_top)
    bird_shape.append((x - 2 * bird_size, y + bird_size))
    bird_corner = (x - 9 / 10 * 2 * bird_size, y + bird_size * 9 ** 2 / 100)
    x -= 4 * bird_size
    bird_shape.append((x, y))
    for i in range(10):
        new_top = x + i / 9 * 2 * bird_size, y + bird_size * i ** 2 / 100
        bird_shape.append(new_top)
    bird_shape.append(bird_corner)
    dr.polygon(screen, BIRD_COLOR, bird_shape)


def draw_birds():
    """
    Draw all birds
    """
    draw_bird(600, 120, 15)
    draw_bird(450, 90, 20)
    draw_bird(400, 180, 15)
    draw_bird(500, 132, 10)
    draw_bird(550, 450, 35)
    draw_bird(500, 350, 40)
    draw_bird(480, 500, 35)
    draw_bird(700, 500, 30)


def background_mountains_shape():
    """
    Count coordinates of background mountain tops

    :return: list of background mountain coordinates
    """
    parameter = np.arange(0, 230, 1)
    coordinates = [(5, 280)]
    for variable in parameter:
        if variable <= 200:
            coordinates.append((variable + 10, 220 - (variable ** 2 // 340)))
    coordinates += [(250, 115), (265, 140), (380, 230), (437, 223), (470, 240), (510, 190), (560, 200), (590, 175)]
    for variable in parameter:
        coordinates.append((variable / 1.5 + 590, 2 * np.cos(variable / 180 * np.pi) * variable / 5 + 175))
    coordinates += [(800, 155), (835, 145)]
    for variable in parameter:
        if variable <= 60:
            coordinates.append((variable + 835, 145 + variable ** 2 / 100))
    coordinates += [(930, 165), (1000, 208)]
    return coordinates


def mid_mountains_shape():
    """
    Count coordinates of middle mountain tops

    :return: list of middle mountain coordinates
    """
    parameter = np.arange(0, 201, 1)
    coordinates = [(0, 300), (5, 300), (180, 380), (220, 330), (270, 360), (300, 285), (380, 300), (450, 350),
                   (540, 335)]
    for variable in parameter:
        if variable < 140:
            top = variable + 540, 335 - 80 * np.sin(variable / 220 * np.pi)
        else:
            top = (variable - 140) ** 1.7 / 10 + 680, 335 - 80 * np.sin(variable / 220 * np.pi) + (variable / 2 - 70)
        coordinates.append(top)
    coordinates += [(845, 290), (885, 325), (915, 290), (955, 300), (1000, 240), (1000, 500), (0, 500)]
    return coordinates


def top_mountains_shape():
    """
    Count coordinates of top mountain tops

    :return: list of top mountain coordinates
    """
    parameter = np.arange(200, 0, -1)
    coordinates = [(0, 320), (120, 340), (230, 520)]
    for variable in parameter:
        coordinates.append((430 - variable, (-variable ** 2 / 400) + 620))
    coordinates += [(500, 640), (650, 540), (710, 570)]
    for variable in parameter:
        coordinates.append((910 - variable, (-(variable - 160) ** 2 / 200) + 578))
    for variable in parameter:
        if variable >= 110:
            coordinates.append((1110 - variable, 450 - (np.sin(variable / 200 * np.pi) * 82)))
    coordinates += [(1000, 667), (0, 667)]
    return coordinates


def draw_far_landscape():
    """
    Draw sky and far ground
    """
    first_border = 133
    second_border = 266
    third_border = 399
    left_border = 0
    right_border = DISPLAY_SIZE[0]
    dr.polygon(screen, TOP_SKY_COLOR,
               [(left_border, 0), (right_border, 0), (right_border, first_border), (left_border, first_border)])
    dr.polygon(screen, BOTTOM_SKY_COLOR,
               [(left_border, first_border), (right_border, first_border), (right_border, second_border),
                (left_border, second_border)])
    dr.polygon(screen, TOP_GROUND_COLOR,
               [(left_border, second_border), (right_border, second_border), (right_border, third_border),
                (left_border, third_border)])


def draw_near_landscape():
    """
    Draw mountains, front ground and sun
    """
    dr.polygon(screen, BACK_MOUNTAIN_COLOR, background_mountains_shape())
    dr.ellipse(screen, MIDDLE_MOUNTAIN_COLOR, (10, 225, 175, 480))
    dr.polygon(screen, MIDDLE_MOUNTAIN_COLOR, mid_mountains_shape())
    dr.polygon(screen, BOTTOM_GROUND_COLOR, [(0, 409), (1000, 409), DISPLAY_SIZE, (0, 667)])
    dr.polygon(screen, TOP_MOUNTAIN_COLOR, top_mountains_shape())
    dr.circle(screen, SUN_COLOR, (450, 125), 45)


def draw_landscape():
    """
    Draw sun, sky, mountains, ground
    """
    draw_far_landscape()
    draw_near_landscape()


draw_landscape()
draw_birds()

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
