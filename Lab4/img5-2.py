import pygame
from pygame.draw import polygon, circle
import numpy as np
from math import cos, pi, sin

pygame.init()

FPS = 30
screen = pygame.display.set_mode((1000, 667))

TOPSKY = (254, 213, 162)
BOTSKY = (254, 213, 196)
SUN = (252, 238, 33)
backMountainColor = (252, 152, 49)
midMountainColor = (172, 67, 52)
NEWMNT = (48, 16, 38)
TOPGR = (254, 213, 148)
BOTGR = (179, 134, 148)
birdColor = (66, 33, 11)

# bird parameters
birdsParametrs = [(600, 120, 1.5), (450, 90, 2.0), (400, 180, 1.5), (500, 132, 1.0),  # Параметры,
                  (550, 450, 3.5), (500, 350, 4.0), (480, 500, 3.5), (700, 500, 3.0)]  # описывающие каждую из птиц
birdNormalScale = 60  # int

# backmountains parameters
xLeftSlideCorBackMount = np.arange(10, 210, 1)
xCenterSlideCorBackMount = np.arange(600, 750, 1)
xRightSlideCorBackMount = np.arange(830, 900, 1)
cordsFirstpointBackMountains = [(5, 280)]
cordsBackLeftAngularSegment = [(250, 115), (265, 140), (380, 230), (437, 223),
                               (470, 240), (510, 190), (560, 200), (590, 175)]
cordsBackRightAngularSegment = [(780, 155)]
cordsEndpointsBackMountains = [(940, 160), (1000, 198)]

# midmountains parameters
cordsFirstpointsMidMountains = [(0, 400)]
xLeftSlideCorMidMount = np.arange(0, 180, 1)
xRightSlideCorMidMount = np.arange(540, 770, 1)
cordsMidAngularSegment = [(180, 380), (220, 330), (270, 360), (300, 285),
                          (380, 300), (450, 350), (540, 335)]
cordsEndpointsMidMountains = [(845, 290), (885, 325), (915, 290), (955, 300),
                              (1000, 240), (1000, 400)]


def y_bird_up(_x, scale):
    """
    Расчитывает и возвращает _y - значение вертикальной координаты точки верхней границы птицы с учетом коэффициента
        пропорциональности размера в зависимости от _x - горизонтальной координаты
    :param _x: горизонтальная координата
    :param scale: коэффициент пропорциональности размера птицы.
    :return: _y
    """
    if _x <= birdNormalScale / 2:
        _y = round(_x ** 2 / 90 * scale)
    else:
        _y = round((birdNormalScale - _x) ** 2 / 90 * scale)
    return _y


def y_bird_down(_x, scale):
    """
        Расчитывает и возвращает _y - значение вертикальной координаты точки нижней границы птицы с учетом коэффициента
            пропорциональности размера в зависимости от _x - горизонтальной координаты
        :param _x: горизонтальная координата
        :param scale: коэффициент пропорциональности размера птицы.
        :return: _y
        """
    if _x <= birdNormalScale / 2:
        _y = round(_x / 2 * scale)
    else:
        _y = round((birdNormalScale - _x) / 2 * scale)
    return _y


def bird_cor(scale):
    """
    Возвращает координаты границ рисунка птицы, привязанные к прямоугольной системе координат
        с центром в верхней левой точке птицы, в соответствии сразмерами, пропорциональными birdNormalScale
        с коэффициентом Scale
    :param scale: коэффициент пропорциональности размера птицы.
    :return: массив пар координат птицы в системе координат, связанной с ее левой верхней точкой
    """
    global birdNormalScale
    birdRelativeCords = []
    for _x in range(birdNormalScale):
        xUpBird = round(_x * scale)
        yUpBird = y_bird_up(_x, scale)
        birdRelativeCords.append((xUpBird, yUpBird))
    for _x in range(birdNormalScale, -1, -1):
        xUpBird = round(_x * scale)
        yUpBird = y_bird_down(_x, scale)
        birdRelativeCords.append((xUpBird, yUpBird))
    return birdRelativeCords


def draw_bird(xbird, ybird, birdscale):
    """
    Рисует птицу, размер которой пропорционален Scale, а координаты левой верхней точки равны xBird, yBird
    :param xbird: координата левой верхней точки птицы по горизонтальной оси
    :param ybird: координата левой верхней точки птицы птицы по вертикальной оси
    :param birdscale: коэффициент пропорциональности размера птицы
    """
    birdRelativeCords = bird_cor(birdscale)
    birdCords = []
    for cordsPair in birdRelativeCords:
        cordsPair = (cordsPair[0] + xbird, cordsPair[1] + ybird)
        birdCords.append(cordsPair)
    polygon(screen, birdColor, birdCords)


def draw_birds(birdsparametrs):
    for birdParametrs in birdsparametrs:
        xBird = birdParametrs[0]
        yBird = birdParametrs[1]
        scale = birdParametrs[2]
        draw_bird(xBird, yBird, scale)


def cor_firstpoint_back_mountains():
    """
    Возвращает пару координат начальной точки задних гор
    """
    return cordsFirstpointBackMountains


def cor_left_slide_back_segment():
    """
    Рассчитывает вертикальные координаты первого слева сглаженного сегмента задних гор и
    возвращает массив координат(x, y) первого слева сглаженного сегмента задних гор
    """
    cords = []
    for _x in xLeftSlideCorBackMount:
        _y = 220 - ((_x - 10) ** 2 // 340)
        cords.append((round(_x), round(_y)))
    return cords


def cor_left_angular_back_segment():
    """
    Возвращает массив координат первого угловатого сегмента задних гор
    """
    return cordsBackLeftAngularSegment


def cor_center_slide_back_segment():
    """
    Рассчитывает вертикальные координаты второго слева сглаженного сегмента задних гор и
    возвращает массив координат(x, y) второго слева сглаженного сегмента задних гор
    """
    cords = []
    for _x in xCenterSlideCorBackMount:
        _y = 3 * cos((_x - 550) * 1.2 / 180 * pi) * (_x - 600) / 4 + 175
        cords.append((round(_x), round(_y)))
    return cords


def cor_right_angular_back_segment():
    """
    Возвращает массив координат второго угловатого сегмента задних гор
    """
    return cordsBackRightAngularSegment


def cor_right_slide_back_segment():
    """
    Рассчитывает вертикальные координаты третьего слева сглаженного сегмента задних гор и
    возвращает массив координат(x, y) третьего слева сглаженного сегмента задних гор
    """
    cords = []
    for _x in xRightSlideCorBackMount:
        _y = 145 + ((_x - 820) / 1.5) ** 2 / 100
        cords.append((round(_x), round(_y)))
    return cords


def cor_endpoints_back_mountains():
    """
    Возвращает две пары координат конечных точек задних гор
    """
    return cordsEndpointsBackMountains


def draw_back_mountains():
    """
    Рисует задние горы по полученным из используемых функций координатам
    """
    backMountainsCords = cor_firstpoint_back_mountains() + \
                         cor_left_slide_back_segment() + \
                         cor_left_angular_back_segment() + \
                         cor_center_slide_back_segment() + \
                         cor_right_angular_back_segment() + \
                         cor_right_slide_back_segment() + \
                         cor_endpoints_back_mountains()

    polygon(screen, backMountainColor, backMountainsCords)


def cor_firstpoints_mid_mountains():
    """
    Возвращает пару координат начальной точки средних гор
    """
    return cordsFirstpointsMidMountains


def cor_left_slide_mid_segment():
    """
    Рассчитывает вертикальные координаты первого слева сглаженного сегмента средних гор и
    возвращает массив координат(x, y) первого слева сглаженного сегмента средних гор
    """
    cords = []
    for _x in xLeftSlideCorMidMount:
        _y = (_x - 90) ** 2 / 50 + 220
        cords.append((round(_x), round(_y)))
    return cords


def cor_angular_mid_segment():
    """
    Возвращает массив координат угловатого сегмента средних гор
    """
    return cordsMidAngularSegment


def cor_right_slide_mid_segment():
    """
    Рассчитывает вертикальные координаты второго слева сглаженного сегмента средних гор и
    возвращает массив координат(x, y) второго слева сглаженного сегмента средних гор
    """
    cords = []
    for _x in xRightSlideCorMidMount:
        _y = 335 - 60 * sin((_x - 540) / 200 * pi)
        cords.append((round(_x), round(_y)))
    return cords


def cor_endpoints_mid_mountains():
    """
    Возвращает массив пар координат конечных точек средних гор
    """
    return cordsEndpointsMidMountains


def draw_mid_mountains():
    """
    Рисует горы среднего плана по полученным из используемых функций координатам
    """
    midMountainsCords = cor_firstpoints_mid_mountains() + \
                        cor_left_slide_mid_segment() + \
                        cor_angular_mid_segment() + \
                        cor_right_slide_mid_segment() + \
                        cor_endpoints_mid_mountains()

    polygon(screen, midMountainColor, midMountainsCords)


def draw_front_mountains():
    """
    Рисует горы переднего плана по полученным из используемых функций координатам
    """
    midMountainsCords = cor_firstpoints_mid_mountains() + \
                        cor_left_slide_mid_segment() + \
                        cor_angular_mid_segment() + \
                        cor_right_slide_mid_segment() + \
                        cor_endpoints_mid_mountains()

    polygon(screen, midMountainColor, midMountainsCords)


# new mountains:
x3 = x2 = np.arange(200, 0, -1)
xy3 = [(0, 320), (120, 340), (230, 520)]

# prelast slide:
for el in x3:
    T = 430 - el, (-el ** 2 / 400) + 620
    xy3.append(T)

xy3.append((500, 640))
xy3.append((650, 540))
xy3.append((710, 570))

# last slide:
for el in x3:
    T = 910 - el, (-(el - 160) ** 2 / 200) + 578
    xy3.append(T)
for el in x3:
    if el >= 110:
        T = 1110 - el, 450 - (np.sin(el / 200 * np.pi) * 82)
        xy3.append(T)

xy3.append((1000, 667))
xy3.append((0, 667))

polygon(screen, TOPSKY, [(0, 0), (1000, 0), (1000, 133), (0, 133)])
polygon(screen, BOTSKY, [(0, 133), (1000, 133), (1000, 266), (0, 266)])
polygon(screen, TOPGR, [(0, 266), (1000, 266), (1000, 399), (0, 399)])
circle(screen, SUN, (450, 125), 45)
# polygon(screen, backMountainColor, xy1)
# polygon(screen, FOREMNT, xy2)
polygon(screen, BOTGR, [(0, 409), (1000, 409), (1000, 667), (0, 667)])
polygon(screen, NEWMNT, xy3)


def draw_picture():
    
    draw_back_mountains()
    draw_mid_mountains()
    draw_front_mountains()

    draw_birds(birdsParametrs)


draw_picture()

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
