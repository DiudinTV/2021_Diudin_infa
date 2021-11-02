import math
import random as rnd
import pygame
import pygame.draw as dr

FPS = 30

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
VIOLET = (101, 0, 170)
ORANGE = (252, 102, 0)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
GAME_COLORS = [BLACK, BLUE, YELLOW, MAGENTA, CYAN]
ARROWS = [1073741903, 1073741904, 1073741905, 1073741906]
WASD = [100, 97, 115, 119]
TAB = 9
LEFT_SHIFT = 1073742049
RIGHT_SHIFT = 1073742053
ZX = [122, 120]
Q, E = 113, 101
SQUARE_BRACKETS = [91, 93]
ONE_TO_FIVE = [49, 50, 51, 52, 53]
SIX_TO_ZERO = [54, 55, 56, 57, 48]

TEAM_COLORS = [VIOLET, ORANGE]

WIDTH = 1500
HEIGHT = 750


def score(screen, points):
    """
    Выводит на экран счётчик очков игроков/команд

    :param screen: экран
    :param points: список очков 2х команд
    """
    font = pygame.font.Font(None, 100)
    score_counter1 = font.render(str(points[0]), True, TEAM_COLORS[0])
    score_counter2 = font.render(str(points[1]), True, TEAM_COLORS[1])
    score_place1 = score_counter1.get_rect(topleft=(20, 20))
    screen.blit(score_counter1, score_place1)
    score_place2 = score_counter2.get_rect(bottomright=(WIDTH - 20, HEIGHT - 20))
    screen.blit(score_counter2, score_place2)


class Collidable:
    def __init__(self, screen: pygame.Surface):
        """ Конструктор класса Collidable """
        self.screen = screen
        self.live = 1
        self.x = rnd.randint(0, WIDTH - 100)
        self.y = rnd.randint(0, HEIGHT - 100)
        self.r = 100
        self.v = 10
        self.vx = 2 * self.v * (rnd.random() - 0.5)
        direction_y = rnd.random() - 0.5
        if direction_y != 0:
            direction_y /= abs(direction_y)
        self.vy = (self.v ** 2 - self.vx ** 2) ** (1 / 2) * direction_y

    def hit_test(self, obj):
        """
        Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения объектов. В противном случае возвращает False.
        """
        if self.r + obj.r >= ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) ** (1 / 2):
            return True
        return False


class Ball(Collidable):
    def __init__(self, screen, x, y, r, power):
        """
        Конструктор класса Ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        r - радиус мяча
        power - цвет мяча, отвечающий за то, какие цели тот может уничтожить
        """
        super().__init__(screen)
        self.number = 0
        self.x = x
        self.y = y
        self.r = r
        self.color = power
        if self.color != BLACK:
            self.live = 70  # продолжительность жизни шаров, меньше для прямолетящих
        else:
            self.live = 35

    def move(self):
        """
        Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, сил гравитации для цветных мячей
        и стен по краям окна (размер окна WIDTH х HEIGHT).
        """
        self.x += self.vx
        self.y -= self.vy
        if self.y - self.r < 0:
            self.y = self.r
            self.vy *= -0.9
        elif self.y + self.r > HEIGHT:
            self.y = HEIGHT - self.r
            self.vy *= -0.9
        else:
            if self.color == BLUE:
                self.vy -= 0.5
            elif self.color == YELLOW:
                self.vy += 0.5
        if self.x + self.r > WIDTH:
            self.x = WIDTH - self.r
            self.vx *= -0.9
        elif self.x - self.r < 0:
            self.x = self.r
            self.vx *= -0.9
        else:
            if self.color == MAGENTA:
                self.vx += 0.5
            elif self.color == CYAN:
                self.vx -= 0.5

    def draw(self):
        """ Рисует мяч. """
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)


class Gun(Collidable):
    def __init__(self, screen, x, y, direction_keys, full_stop, change_keys, size_keys, fire, number):
        """
        Конструктор класса Gun

        Args:
        x - Расположение пушки по оси x
        y - Расположение пушки по оси y
        direction_keys - Список кнопок, отвечающих за смену направления движения (в порядке вправо, влево, вниз, вверх)
        full_stop - Кнопка для полной остановки пушки на месте
        change_keys - 5 кнопок для переключения между режимами стрельбы
        size_keys - 2е кнопки для изменения размера пушки (меньше, больше)
        fire - способ стрельбы и прицеливания (мышью или с помощью пробела, Q и E)
        number - номер игрока/команды данной пушки
        """
        super().__init__(screen)
        self.number = number
        self.right = direction_keys[0]
        self.left = direction_keys[1]
        self.down = direction_keys[2]
        self.up = direction_keys[3]
        self.stop = full_stop
        self.black = change_keys[0]
        self.blue = change_keys[1]
        self.yellow = change_keys[2]
        self.magenta = change_keys[3]
        self.cyan = change_keys[4]
        self.smaller = size_keys[0]
        self.bigger = size_keys[1]
        self.fire_method = fire
        self.invincibility = 60  # число кадров неуязвимости
        self.r = 15 * 1.5
        self.x = x
        self.y = y
        self.v = 10
        self.vx = 0
        self.vy = 0
        self.rotate = 0  # направление вращения башни
        self.start_length = 2 * self.r  # длина дула
        self.screen = screen
        self.f2_power = 5  # минимальная, стартовая сила стрельбы
        self.f2_on = 0
        self.an = 0  # угол направления дула
        self.power = BLACK  # цвет снарядов
        self.color = GREY

    def fire2_start(self):
        """
        Начало подготовки выстрела мячом (после чего начинает увеличиваться сила вплоть до самого выстрела)
        """
        self.f2_on = 1

    def fire2_end(self, event):
        """
        Выстрел мячом.

        Происходит при отпускании кнопки мыши или пробела.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши или угла дула, выбранного Q и E.
        """
        new_ball = Ball(self.screen, self.x + (self.f2_power + self.start_length) * math.cos(self.an),
                        self.y + (self.f2_power + self.start_length) * math.sin(self.an), 2 * self.r / 3, self.power)
        if self.fire_method == "MOUSE":
            self.an = math.atan2((event.pos[1] - self.y), (event.pos[0] - self.x))
        new_ball.vx = self.f2_power * math.cos(self.an) / 2 + self.vx / 2
        new_ball.vy = - self.f2_power * math.sin(self.an) / 2 - self.vy / 2
        new_ball.number = self.number
        self.f2_on = 0
        self.f2_power = 5
        return new_ball

    def targeting(self, event):
        """ Прицеливание. Положение дула зависит от положения мыши или начинает вращаться при нажатии Q или E. """
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY
        if self.fire_method == "MOUSE":
            self.an = math.atan2((event.pos[1] - self.y), (event.pos[0] - self.x))
        elif self.fire_method == "SPACE" and event.type == pygame.KEYDOWN:
            if event.key == Q or event.key == E:
                self.rotate += (107 - event.key) / 48  # положительный для E, отрицательный для Q
        elif self.fire_method == "SPACE" and event.type == pygame.KEYUP:
            self.rotate -= (107 - event.key) / 48

    def move_x(self):
        """ Перемещение пушки вдоль оси x вплоть до столкновения со стеной. """
        if self.x + self.r + self.vx > WIDTH:
            self.x = WIDTH - self.r
            self.vx = 0
        elif self.x - self.r + self.vx < 0:
            self.x = self.r
            self.vx = 0
        else:
            self.x += self.vx

    def move_y(self):
        """ Перемещение пушки вдоль оси y вплоть до столкновения со стеной. """
        if self.y + self.r + self.vy > HEIGHT:
            self.y = HEIGHT - self.r
            self.vy = 0
        elif self.y - self.r + self.vy < 0:
            self.y = self.r
            self.vy = 0
        else:
            self.y += self.vy

    def draw(self):
        """ Рисует пушку. """
        self.r = 2 * self.r / 3
        dr.polygon(self.screen, self.color,
                   [(self.x + self.r * math.cos(self.an + math.pi / 2),
                     self.y + self.r * math.sin(self.an + math.pi / 2)),
                    (self.x - self.r * math.cos(self.an + math.pi / 2),
                     self.y - self.r * math.sin(self.an + math.pi / 2)),
                    (self.x - self.r * math.cos(self.an + math.pi / 2) + (self.f2_power + self.start_length) * math.cos(
                        self.an),
                     self.y - self.r * math.sin(self.an + math.pi / 2) + (self.f2_power + self.start_length) * math.sin(
                         self.an)),
                    (self.x + self.r * math.cos(self.an + math.pi / 2) + (self.f2_power + self.start_length) * math.cos(
                        self.an),
                     self.y + self.r * math.sin(self.an + math.pi / 2) + (self.f2_power + self.start_length) * math.sin(
                         self.an))])
        self.r = 1.5 * self.r
        dr.circle(self.screen, TEAM_COLORS[self.number - 1], (self.x, self.y), self.r)
        dr.circle(self.screen, self.power, (self.x, self.y), 2 * self.r / 3)

    def power_up(self):
        """ Отвечает за зарядку силы выстрела и вращение дула при нажатии соответствующих кнопок. """
        self.an += self.rotate
        if self.f2_on:
            if self.f2_power < 3 * self.start_length - 2 * self.r:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target(Collidable):
    def __init__(self, screen):
        """
        Конструктор класса Target

        Меняет уничтоженную цель на новую, случайного типа.
        Обычные цели 5и игровых цветов могут быть уничтожены соответствующими снарядами, двигаются
        по прямой до столкновения с препятствием.
        Красные цели двигаются по синусоидам и не могут быть уничтожены попаданием, но направление их движения
        меняется при попадании и они также снимают очки при столкновении с пушкой
        """
        super().__init__(screen)
        self.live = 1
        self.type = 0
        self.r = rnd.randint(20, 50)
        self.x = rnd.randint(self.r + 150, WIDTH - self.r - 150)
        self.y = rnd.randint(self.r + 75, HEIGHT - self.r - 75)
        self.color = rnd.choice(GAME_COLORS)

    def hit(self, number):
        """
        Попадание шарика в цель. Появление сообщения о попадании и изменение очков.
        Возвращает обнулённый счётчик выстрелов для обоих игроков/команд.
        """
        self.screen.fill(WHITE)
        guns[number - 1].color = GREEN
        guns[number - 1].draw()
        font = pygame.font.Font(None, 100)
        message = font.render("Вы уничтожили цель за " + str(bullet[number - 1]) + " выстрелов", True,
                              TEAM_COLORS[number - 1])
        place = message.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.screen.blit(message, place)
        pygame.display.update()
        clock.tick(1)
        for _ in pygame.event.get():
            pass
        for gunn in guns:
            gunn.f2_on = 0
            gunn.f2_power = 5
        return [0, 0]

    def move(self):
        """ Перемещение целей в соответствии с приписанными им законами движения и рамками движения. """
        self.x += self.vx
        self.y += self.vy
        if self.x + self.r > WIDTH - 150:
            self.x = WIDTH - self.r - 150
            self.vx *= -1
        elif self.x - self.r < 150:
            self.x = self.r + 150
            self.vx *= -1
        if self.y + self.r > HEIGHT - 75:
            self.y = HEIGHT - self.r - 75
            self.vy *= -1
        elif self.y - self.r < 75:
            self.y = self.r + 75
            self.vy *= -1

    def draw(self):
        """ Рисует кружок-цель/волну. """
        dr.circle(self.screen, self.color, (self.x, self.y), self.r)


class Wave(Target):
    def __init__(self, screen):
        """ Конструктор класса Wave """
        super().__init__(screen)
        self.r = 50
        self.x = rnd.randint(self.r + 150, WIDTH - self.r - 150)
        self.y = rnd.randint(self.r + 75, HEIGHT - self.r - 75)
        self.v = 20
        self.color = RED
        self.vx = self.v * self.vx / abs(self.vx)
        self.vy = self.v * self.vy / abs(self.vy)
        self.type = rnd.choice([1, 2])

    def move(self):
        """ Перемещение целей в соответствии с приписанными им законами движения и рамками движения. """
        if self.type == 1:
            self.y += self.vy * math.sin(self.x / 4)
            self.x += self.vx
        elif self.type == 2:
            self.x += self.vx * math.sin(self.y / 4)
            self.y += self.vy
        if self.x + self.r > WIDTH:
            self.x = WIDTH - self.r
            self.vx *= -1
            self.vy *= -1
        elif self.x - self.r < 0:
            self.x = self.r
            self.vx *= -1
            self.vy *= -1
        if self.y + self.r > HEIGHT:
            self.y = HEIGHT - self.r
            self.vx *= -1
            self.vy *= -1
        elif self.y - self.r < 0:
            self.y = self.r
            self.vx *= -1
            self.vy *= -1


class Bomb(Target):
    def __init__(self, screen):
        """ Конструктор класса Bomb """
        super().__init__(screen)
        self.type = 3

    def hit_test(self, obj):
        """
        Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения объектов. В противном случае возвращает False.
        """
        if obj.x > self.x + self.r and obj.y > self.y + self.r:
            if ((self.x + self.r - obj.x) ** 2 + (self.y + self.r - obj.y) ** 2) ** (1 / 2) <= obj.r:
                return True
        elif obj.x < self.x - self.r and obj.y > self.y + self.r:
            if ((self.x - self.r - obj.x) ** 2 + (self.y + self.r - obj.y) ** 2) ** (1 / 2) <= obj.r:
                return True
        elif obj.x > self.x + self.r and obj.y < self.y - self.r:
            if ((self.x + self.r - obj.x) ** 2 + (self.y - self.r - obj.y) ** 2) ** (1 / 2) <= obj.r:
                return True
        elif obj.x < self.x - self.r and obj.y < self.y - self.r:
            if ((self.x - self.r - obj.x) ** 2 + (self.y - self.r - obj.y) ** 2) ** (1 / 2) <= obj.r:
                return True
        elif self.x - self.r > obj.x and abs(obj.x - self.x) <= self.r + obj.r:
            return True
        elif self.x + self.r < obj.x and abs(obj.x - self.x) <= self.r + obj.r:
            return True
        elif self.y - self.r > obj.y and abs(obj.y - self.y) <= self.r + obj.r:
            return True
        elif self.y + self.r < obj.y and abs(obj.y - self.y) <= self.r + obj.r:
            return True
        return False

    def blow_up(self):
        """
        Если бомба касается танка или в неё попадает не тот цвет снаряда, она уничтожается и из неёвылетает 4 волны

        :return: список из 4х новых целей-волн
        """
        tts = []
        t_new = Wave(our_screen)
        t_new.type = 1
        t_new.x = self.x
        t_new.y = self.y
        t_new.vx = abs(t_new.vx)
        t_new.vy = abs(t_new.vy)
        tts.append(t_new)
        t_new = Wave(our_screen)
        t_new.type = 1
        t_new.x = self.x
        t_new.y = self.y
        t_new.vx = -abs(t_new.vx)
        t_new.vy = -abs(t_new.vy)
        tts.append(t_new)
        t_new = Wave(our_screen)
        t_new.type = 2
        t_new.x = self.x
        t_new.y = self.y
        t_new.vy = abs(t_new.vy)
        t_new.vx = abs(t_new.vx)
        tts.append(t_new)
        t_new = Wave(our_screen)
        t_new.type = 2
        t_new.x = self.x
        t_new.y = self.y
        t_new.vy = -abs(t_new.vy)
        t_new.vx = -abs(t_new.vx)
        tts.append(t_new)
        return tts

    def open_up(self):
        """
        Вскрывает бомбу, в которую попали*, и выбрасывает 4 новых цели отличных от бомбы цветов
        *Попадание снаряда засчитывается с большей вероятностью при меньшей скорости снаряда
        (регестрирует выстрелы только граница квадрата-бомбы)

        :return: список из 4х новых целей
        """
        tts = []
        k = 0
        for i in range(5):
            if GAME_COLORS[i] != self.color:
                k += 1
                t_new = Target(our_screen)
                t_new.r = 50
                t_new.color = GAME_COLORS[i]
                t_new.vx = 10 * (-1) ** k
                t_new.vy = -10 * (-1) ** (k // 2)
                t_new.x = t.x
                t_new.y = t.y
                tts.append(t_new)
        return tts

    def move(self):
        """ Вместо перемещения бомба разростается. """
        self.r += 1

    def draw(self):
        """ Рисует квадрат-бомбу. """
        dr.rect(self.screen, self.color, (self.x - self.r, self.y - self.r, 2 * self.r, 2 * self.r))


pygame.init()
our_screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = [0, 0]
our_points = [0, 0]
number_of_targets = 6
balls = []
targets = []

clock = pygame.time.Clock()
gun1 = Gun(our_screen, 30, 720, WASD, LEFT_SHIFT, ONE_TO_FIVE, ZX, "SPACE", 1)
gun2 = Gun(our_screen, 1470, 30, ARROWS, RIGHT_SHIFT, SIX_TO_ZERO, SQUARE_BRACKETS, "MOUSE", 2)
guns = [gun1, gun2]
for _ in range(number_of_targets):
    targets.append(Target(our_screen))
finished = False

while not finished:
    our_screen.fill(GREEN)
    dr.rect(our_screen, WHITE, (150, 75, WIDTH - 300, HEIGHT - 150))
    dr.rect(our_screen, BLUE, (10, HEIGHT - 10, WIDTH - 20, 10))
    dr.rect(our_screen, YELLOW, (10, 0, WIDTH - 20, 10))
    dr.rect(our_screen, MAGENTA, (WIDTH - 10, 10, 10, HEIGHT - 20))
    dr.rect(our_screen, CYAN, (0, 10, 10, HEIGHT - 20))
    gun1.draw()
    gun2.draw()
    for t in targets:
        t.move()
        t.draw()
    for b in balls:
        b.draw()
    score(our_screen, our_points)
    pygame.display.update()

    clock.tick(FPS)
    for our_event in pygame.event.get():
        for gun in guns:
            if our_event.type == pygame.QUIT:
                finished = True
            elif our_event.type == pygame.MOUSEBUTTONDOWN and gun.fire_method == "MOUSE":
                gun.fire2_start()
            elif our_event.type == pygame.MOUSEBUTTONUP and gun.fire_method == "MOUSE":
                bullet[gun.number - 1] += 1
                balls.append(gun.fire2_end(our_event))
            elif our_event.type == pygame.MOUSEMOTION and gun.fire_method == "MOUSE":
                gun.targeting(our_event)
            elif our_event.type == pygame.KEYDOWN and gun.fire_method == "SPACE":
                if our_event.key == 32:
                    gun.fire2_start()
                elif our_event.key == Q or our_event.key == E:
                    gun.targeting(our_event)
            elif our_event.type == pygame.KEYUP and gun.fire_method == "SPACE":
                if our_event.key == 32:
                    bullet[gun.number - 1] += 1
                    balls.append(gun.fire2_end(our_event))
                elif our_event.key == Q or our_event.key == E:
                    gun.targeting(our_event)
            if our_event.type == pygame.KEYDOWN:
                if our_event.key == gun.right:
                    if gun.vx != gun.v:
                        gun.vx = gun.v
                    else:
                        gun.vy = 0
                if our_event.key == gun.left:
                    if gun.vx != -gun.v:
                        gun.vx = -gun.v
                    else:
                        gun.vy = 0
                if our_event.key == gun.down:
                    if gun.vy != gun.v:
                        gun.vy = gun.v
                    else:
                        gun.vx = 0
                if our_event.key == gun.up:
                    if gun.vy != -gun.v:
                        gun.vy = -gun.v
                    else:
                        gun.vx = 0
                if our_event.key == gun.stop:
                    gun.vx = 0
                    gun.vy = 0
                if our_event.key == gun.smaller:
                    if gun.r > 7.5:
                        gun.r -= 7.5
                        gun.start_length = 2 * gun.r
                if our_event.key == gun.bigger:
                    if gun.r < 37.5:
                        gun.r += 7.5
                        gun.start_length = 2 * gun.r
                if our_event.key == gun.black:
                    gun.power = BLACK
                elif our_event.key == gun.blue:
                    gun.power = BLUE
                elif our_event.key == gun.yellow:
                    gun.power = YELLOW
                elif our_event.key == gun.magenta:
                    gun.power = MAGENTA
                elif our_event.key == gun.cyan:
                    gun.power = CYAN
    for gun in guns:
        gun.move_x()
        gun.move_y()
        gun.power_up()
        gun.invincibility = max(0, gun.invincibility - 1)
        for t in targets:
            if t.live == 0:
                if len(targets) <= number_of_targets:
                    new_target = rnd.choice([Target(our_screen)] * 9 + [Wave(our_screen)] * 2 + [Bomb(our_screen)])
                    targets[targets.index(t)] = new_target
                else:
                    targets.pop(targets.index(t))
            if t.hit_test(gun) and t.live:
                t.live = 0
                if t.type == 3:
                    our_points[gun.number - 1] -= 5
                    for elem in t.blow_up():
                        targets.append(elem)
                    our_screen.fill(RED)
                    gun.invincibility = 0
                if gun.invincibility == 0:
                    our_points[gun.number - 1] -= 5
                    our_screen.fill(RED)
                    if t.type != 3:
                        gun.invincibility = 30
                pygame.display.update()
                clock.tick(FPS)
        for b in balls:
            b.move()
            b.live -= 1
            if b.live <= 0:
                balls.pop(balls.index(b))
            if gun.hit_test(b):
                b.live = 0
                if gun.invincibility > 0:
                    pass
                elif gun.number != b.number:
                    our_screen.fill(RED)
                    pygame.display.update()
                    clock.tick(FPS)
                    our_points[gun.number - 1] -= 20
                    our_points[b.number - 1] += 20
                    gun.invincibility = 30
                else:
                    our_screen.fill(RED)
                    pygame.display.update()
                    clock.tick(FPS)
                    our_points[gun.number - 1] -= 10
                    gun.invincibility = 30
    for b in balls:
        for t in targets:
            if t.hit_test(b) and t.live:
                if t.color == b.color and t.type != 3:
                    balls = []
                    our_points[b.number - 1] += 10
                    t.live = 0
                    bullet = t.hit(b.number)
                elif t.type == 1:
                    t.type = 2
                    t.vy = t.v
                    t.vx = 2 * t.v
                    b.live = 0
                elif t.type == 2:
                    t.type = 1
                    t.vx = t.v
                    t.vy = 2 * t.v
                    b.live = 0
                elif t.type == 3:
                    t.live = 0
                    b.live = 0
                    if t.color == b.color:
                        our_points[b.number - 1] += 20
                        for elem in t.open_up():
                            targets.append(elem)
                    else:
                        our_points[b.number - 1] -= 5
                        for elem in t.blow_up():
                            targets.append(elem)
                else:
                    our_points[b.number - 1] -= 1
                    t.live = 0

pygame.quit()
