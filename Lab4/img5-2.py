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
NEWMNT = (48, 16, 38)
TOPGR = (254, 213, 148)
BOTGR = (179, 134, 148)
birdColor = (66, 33, 11)

CorsFirstpointBackMountains = (5, 280)

birdsParametrs = [(600, 120, 1.5), (450, 90, 2.0), (400, 180, 1.5), (500, 132, 1.0),  # Параметры,
                  (550, 450, 3.5), (500, 350, 4.0), (480, 500, 3.5), (700, 500, 3.0)]  # описывающие каждую из птиц

birdNormalScale = 60  # int


def y_bird_up(_x, scale):
    """
    Расчитывает и возвращает _y - значение вертикальной координаты точки верхней границы птицы с учетом коэффициента
        пропорциональности размера в зависимости от _x - горизонтальной координаты
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


def draw_bird(xBird, yBird, birdScale):
    """
    Рисует птицу, размер которой пропорционален Scale, а координаты левой верхней точки равны xBird, yBird
    :param xBird: координата левой верхней точки птицы по горизонтальной оси
    :param yBird: координата левой верхней точки птицы птицы по вертикальной оси
    :param birdScale: коэффициент пропорциональности размера птицы
    """
    birdRelativeCords = bird_cor(birdScale)
    birdCords = []
    for cordsPair in birdRelativeCords:
        cordsPair = (cordsPair[0] + xBird, cordsPair[1] + yBird)
        birdCords.append(cordsPair)
    dr.polygon(screen, birdColor, birdCords)






def cor_firstpoint_back_mountains():
    """
    Возвращает пару координат начальной точки задних гор
    """
    return CorsFirstpointBackMountains

def cor_left_slide_segment():
    """
    Возвращает массив координат первого слева сглаженного сегмента задних гор
    """

def cor_left_angular_segment():
    """
    Возвращает массив координат первого угловатого сегмента задних гор
    """

def cor_center_slide_segment():
    """
    Возвращает массив координат второго слева сглаженного сегмента задних гор
    """

def cor_center_angular_segment():
    """
    Возвращает массив координат второго угловатого сегмента задних гор
    """

def cor_right_slide_segment():
    """
    Возвращает массив координат третьего слева сглаженного сегмента задних гор
    """

def cor_right_angular_segment():
    """
    Возвращает массив координат третьего угловатого сегмента задних гор
    """

def draw_back_mountain():
    backMountainsCors = []
    backMountainsCors.append(cor_firstpoint_back_mountains())
    backMountainsCors.append(cor_left_slide_segment())
    backMountainsCors.append(cor_left_angular_segment())
    backMountainsCors.append(cor_center_slide_segment())
    backMountainsCors.append(cor_center_angular_segment())
    backMountainsCors.append(cor_right_slide_segment())
    backMountainsCors.append(cor_right_angular_segment())


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

dr.polygon(screen, TOPSKY, [(0, 0), (1000, 0), (1000, 133), (0, 133)])
dr.polygon(screen, BOTSKY, [(0, 133), (1000, 133), (1000, 266), (0, 266)])
dr.polygon(screen, TOPGR, [(0, 266), (1000, 266), (1000, 399), (0, 399)])
dr.circle(screen, SUN, (450, 125), 45)
dr.polygon(screen, BACKMNT, xy1)
dr.ellipse(screen, FOREMNT, (10, 225, 175, 480))
dr.polygon(screen, FOREMNT, xy2)
dr.polygon(screen, BOTGR, [(0, 409), (1000, 409), (1000, 667), (0, 667)])
dr.polygon(screen, NEWMNT, xy3)


def draw_birds(birdsParametrs):
    for birdParametrs in birdsParametrs:
        xBird = birdParametrs[0]
        yBird = birdParametrs[1]
        scale = birdParametrs[2]
        draw_bird(xBird, yBird, scale)


draw_birds(birdsParametrs)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
