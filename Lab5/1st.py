import pygame
import pygame.draw as dr
from random import random, randint

pygame.init()

FPS = 30
screen = pygame.display.set_mode((1250, 750))

time = 0
level = 0
wall_count = -1
possible_shape_number_maximum = 0
shape_list = []
count = 0

start_ball_speed = 6  # starting speed of shapes
start_square_speed = 3
start_wall_speed = 10
ball_speed = start_ball_speed
square_speed = start_square_speed
wall_speed = start_wall_speed

start_wall_width = 50
wall_width = start_wall_width
square_fracture_acceleration = 5  # clicked big square will fracture, new squares gain extra speed before hitting wall
number_of_shapes = 8  # don't set more then 20
level_goal = 50

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_RED = (100, 0, 0)
DARK_GREEN = (0, 100, 0)
DARK_BLUE = (0, 0, 100)
GREY = (100, 100, 100)
COLORS = [WHITE, YELLOW, MAGENTA, CYAN, RED, GREEN, BLUE, BLACK, GREY, GREY]
TEXT_COLORS = [BLACK, BLUE, GREEN, RED, CYAN, MAGENTA, YELLOW, WHITE, BLACK, BLACK]
WALL_COLORS = [DARK_RED, DARK_GREEN, DARK_BLUE, GREY]
MESSAGE_LIST2 = ["clicking on background subtracts points",
                 "for every " + str(level_goal) + " points gained, level changes",
                 "every square hit gives equal amount of points", "are present, no more squares will appear",
                 "will result in losing points", "faster and thinner, but subtract the same amount",
                 "from all sources is equal to level number",
                 "gives bonus points for every additional figure",
                 "gain " + str(10 * level_goal) + " points to loop"]
MESSAGE_LIST = ["Hit balls to get points", "Smaller balls give more points", "Squares fracture when hit",
                "If " + str((number_of_shapes + 3) // 4) + " medium or 1 big square", "Hitting moving wall spaces",
                "New walls will be",
                "Number of subtracted points", "Hitting 2+ figures with 1 click", "No more figures will appear"]
level_color = WHITE
active_colors = [COLORS[i] for i in range(8)]
active_colors.pop(active_colors.index(level_color))


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
        elif shape[0] == "wall":
            dr.rect(screen, col, (shape[1], shape[2], shape[3], 748))
            dr.rect(screen, WHITE, (shape[1] - 1, shape[2] - 1, shape[3], 750), 5)


def new_ball(speed):
    """
    :param speed: starting ball velocity

    draws new ball

    :return: number of created circles to control potential number of shapes on screen
    """
    x = randint(100, 1100)
    y = randint(200, 800)
    if level == 0:
        r = 80
    else:
        r = randint(20, 100)
    direction_x = random() - 0.5
    direction_y = random() - 0.5
    if direction_x != 0:
        direction_x *= 1 / abs(direction_x)
    if direction_y != 0:
        direction_y *= 1 / abs(direction_y)
    vx = speed * random() * direction_x
    vy = (speed ** 2 - vx ** 2) ** (1 / 2) * direction_y
    color = active_colors[randint(0, 5)]
    dr.circle(screen, color, (x, y), r)
    shape_list.append(["ball", x, y, r, color, vx, vy])
    return 1


def new_square(speed):
    """
    :param speed: starting square velocity

    draws new square

    :return: number of potential squares stacked inside of created one to control potential number of shapes on screen
    """
    x = randint(100, 800)
    y = randint(200, 800)
    if level == 2:
        a = 120
    else:
        a = randint(81, 320)
    direction_x = random() - 0.5
    direction_y = random() - 0.5
    if direction_x != 0:
        direction_x *= 1 / abs(direction_x)
    if direction_y != 0:
        direction_y *= 1 / abs(direction_y)
    vx = speed * random() * direction_x
    vy = (speed ** 2 - vx ** 2) ** (1 / 2) * direction_y
    color = active_colors[randint(0, 5)]
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

    :return: number of level after click
    """
    global count, possible_shape_number_maximum
    fee = level + 1  # how many points will be lost for clicking
    for shape in shape_list:
        if shape[0] == "wall":
            if event_name.pos[0] >= shape[1] - 1:
                if event_name.pos[0] <= shape[1] - 1 + shape[3]:
                    fee += level + 1

        elif shape[0] == "ball":
            if (event_name.pos[0] - shape[1]) ** 2 + (event_name.pos[1] - shape[2]) ** 2 <= shape[3] ** 2:
                possible_shape_number_maximum -= 1
                count += 6 - (shape[3] + 10) // 20
                shape_list.pop(shape_list.index(shape))
                update_screen()
                fee -= level + 1

        elif shape[0] == "square":
            if event_name.pos[0] >= shape[1]:
                if event_name.pos[0] <= shape[1] + shape[3]:
                    if event_name.pos[1] >= shape[2]:
                        if event_name.pos[1] <= shape[2] + shape[3]:
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
                                fee -= level + 1
                                count += 2
    count = max(count - fee, count - count % (10 * level_goal))
    return score()


def score():
    """
    writes players score and current level

    :return: number of current level (-1)
    """
    global level_color, active_colors
    level_number = (count % (10 * level_goal)) // level_goal
    MESSAGE_LIST2[8] = "gain " + str(
        10 * level_goal * ((count + 10 * level_goal) // (10 * level_goal))) + " points to loop"
    if level_number == 9:
        level_number = 8
    level_color = COLORS[level_number]
    text_color = TEXT_COLORS[level_number]
    if level_number != 8:
        active_colors = [COLORS[j] for j in range(8)]
        active_colors.pop(active_colors.index(level_color))
        active_colors.pop(active_colors.index(text_color))
    update_screen()
    font = pygame.font.Font(None, 120)
    font2 = pygame.font.Font(None, 60)
    score_counter = font.render(str(count), True, text_color)
    level_counter = font.render(str(level_number + 1), True, text_color)
    time_counter = font.render((2 - len(str((time // 30) // 60))) * "0" + str((time // 30) // 60) + ":" + (
                2 - len(str((time // 30) % 60))) * "0" + str((time // 30) % 60), True, text_color)
    message = font.render(MESSAGE_LIST[level], True, text_color)
    message2 = font2.render(MESSAGE_LIST2[level], True, text_color)
    place = message.get_rect(center=(625, 305))
    place2 = message2.get_rect(center=(625, 385))
    time_place = time_counter.get_rect(center=(625, 60))
    screen.blit(time_counter, time_place)
    screen.blit(score_counter, (20, 20))
    screen.blit(level_counter, (1190, 20))
    screen.blit(message, place)
    screen.blit(message2, place2)
    return level_number


def move_shapes():
    """
    moves shapes according to their velocity, hitting walls results in randomisation of it
    """
    for shape_number in range(len(shape_list)):
        shape_list[shape_number][1] += shape_list[shape_number][5]
        shape_list[shape_number][2] += shape_list[shape_number][6]

        if shape_list[shape_number][0] == "wall":
            shape_velocity = shape_list[shape_number][5]
            hit_velocity = 0
            sizes = [shape_list[shape_number][3], 0, 0, 0]
        elif shape_list[shape_number][0] == "ball":
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
            final_score = count
        elif event.type == pygame.MOUSEBUTTONDOWN:
            level = click(event)
    if level == 8:
        for i in range(wall_count + 1):
            shape_list.pop(0)
            wall_count -= 1
    elif 3 <= level < wall_count + 4:
        while level < wall_count + 4:
            shape_list.pop(wall_count)
            wall_count -= 1
    elif level >= 4 and len(shape_list) != 0 and wall_count + 4 < level:
        wall_count += 1
        wall = ["wall", 1, 1, wall_width * (4 - wall_count), WALL_COLORS[wall_count], wall_speed * (wall_count + 1), 0]
        shape_list.append(shape_list[wall_count])
        shape_list[wall_count] = wall
    elif len(shape_list) - wall_count - 1 < number_of_shapes:
        if random() >= 0.2 or level <= 1 or possible_shape_number_maximum >= 2 * number_of_shapes - 1:
            ball_speed = start_ball_speed + level
            possible_shape_number_maximum += new_ball(ball_speed)
        else:
            square_speed = start_square_speed + level / 2
            possible_shape_number_maximum += new_square(square_speed)

    time += 1
    move_shapes()
    pygame.display.update()

pygame.quit()
