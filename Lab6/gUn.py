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
QE = [113, 101]
SQUARE_BRACKETS = [91, 93]
ONE_TO_FIVE = [49, 50, 51, 52, 53]
SIX_TO_ZERO = [54, 55, 56, 57, 48]

TEAM_COLORS = [VIOLET, ORANGE]

WIDTH = 1500
HEIGHT = 750


def score(screen, points):
    font = pygame.font.Font(None, 100)
    score_counter1 = font.render(str(points[0]), True, TEAM_COLORS[0])
    score_counter2 = font.render(str(points[1]), True, TEAM_COLORS[1])
    score_place1 = score_counter1.get_rect(topleft=(20, 20))
    screen.blit(score_counter1, score_place1)
    score_place2 = score_counter2.get_rect(bottomright=(WIDTH - 20, HEIGHT - 20))
    screen.blit(score_counter2, score_place2)


class Ball:
    def __init__(self, screen: pygame.Surface, x, y, r, power):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.number = 0
        self.screen = screen
        self.x = x
        self.y = y
        self.r = r
        self.vx = 0
        self.vy = 0
        self.color = power
        self.live = 1

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.y -= self.vy
        self.vx *= 0.99
        self.vy *= 0.99
        if self.y <= HEIGHT - self.r - 1:
            self.vy -= 1
        if self.y + self.r >= HEIGHT:
            self.y = HEIGHT - self.r
            self.vx *= 0.8
            self.vy *= -0.8
        if self.x + self.r > WIDTH:
            self.x = WIDTH - self.r
            self.vx *= -1
        elif self.x - self.r < 0:
            self.x = self.r
            self.vx *= -1
        if self.vx <= 2 and self.vy <= 2 and self.y == HEIGHT - self.r:
            self.live = 0

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def hit_test(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if self.r + obj.r >= ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) ** (1 / 2):
            return True
        return False


class Gun:
    def __init__(self, screen, x, y, direction_keys, full_stop, change_keys, size_keys, number):
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
        self.r = 15
        self.x = x
        self.y = y
        self.v = 10
        self.vx = 0
        self.vy = 0
        self.start_length = 3 * self.r
        self.screen = screen
        self.f2_power = 5
        self.f2_on = 0
        self.an = 1
        self.power = BLACK
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        new_ball = Ball(self.screen, self.x + (self.f2_power + self.start_length) * math.cos(self.an),
                        self.y + (self.f2_power + self.start_length) * math.sin(self.an), self.r, self.power)
        self.an = math.atan2((event.pos[1] - self.y), (event.pos[0] - self.x))
        new_ball.vx = self.f2_power * math.cos(self.an) / 2 + self.vx
        new_ball.vy = - self.f2_power * math.sin(self.an) / 2 + self.vy
        new_ball.number = self.number
        self.f2_on = 0
        self.f2_power = 5
        return new_ball

    def targeting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan2((event.pos[1] - self.y), (event.pos[0] - self.x))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def movex(self):
        if self.x + 1.5 * self.r + self.vx > WIDTH:
            self.x = WIDTH - 1.5 * self.r
            self.vx = 0
        elif self.x - 1.5 * self.r + self.vx < 0:
            self.x = 1.5 * self.r
            self.vx = 0
        else:
            self.x += self.vx

    def movey(self):
        if self.y + 1.5 * self.r + self.vy > HEIGHT:
            self.y = HEIGHT - 1.5 * self.r
            self.vy = 0
        elif self.y - 1.5 * self.r + self.vy < 0:
            self.y = 1.5 * self.r
            self.vy = 0
        else:
            self.y += self.vy

    def draw(self):
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
        dr.circle(self.screen, TEAM_COLORS[self.number - 1], (self.x, self.y), 1.5 * self.r)
        dr.circle(self.screen, self.power, (self.x, self.y), self.r)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < (self.start_length - self.r) * 3:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY

    def hit_test(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if 1.5 * self.r + obj.r >= ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) ** (1 / 2):
            return True
        return False


class Target:
    def __init__(self, screen):
        """ Вызывает инициализацию при создании нового объекта класса Target. """
        self.screen = screen
        self.points = 0
        self.new_target()

    def new_target(self):
        """ Меняет уничтоженную цель на новую, случайную. """
        self.live = 1
        direction_x = rnd.random() - 0.5
        direction_y = rnd.random() - 0.5
        if direction_x != 0:
            direction_x *= 1 / abs(direction_x)
        if direction_y != 0:
            direction_y *= 1 / abs(direction_y)
        if rnd.random() >= 0.5:
            self.type = 0
            self.r = rnd.randint(20, 50)
            self.x = rnd.randint(self.r + 150, WIDTH - self.r - 150)
            self.y = rnd.randint(self.r + 75, HEIGHT - self.r - 75)
            self.speed = 7
            self.color = rnd.choice(GAME_COLORS)
            self.vx = self.speed * rnd.random() * direction_x
            self.vy = (self.speed ** 2 - self.vx ** 2) ** (1 / 2) * direction_y
        else:
            self.r = 50
            self.x = rnd.randint(self.r, WIDTH - self.r)
            self.y = rnd.randint(self.r, HEIGHT - self.r)
            self.speed = 20
            self.color = RED
            self.vx = self.speed
            self.vy = self.speed
            if rnd.random() >= 0.5:
                self.vx *= direction_x
                self.type = 1
            else:
                self.vy *= direction_y
                self.type = 2

    def hit(self, number):
        """Попадание шарика в цель."""
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
        for event in pygame.event.get():
            pass
        for gunn in guns:
            gunn.f2_on = 0
            gunn.f2_power = 5
        return [0, 0]

    def move(self):
        if self.type == 1:
            self.vy = 2 * self.speed * math.sin(self.x)
        elif self.type == 2:
            self.vx = 2 * self.speed * math.sin(self.y)
        self.x += self.vx
        self.y += self.vy
        mediator = 1 - (self.type + 1) // 2  # == 0 if type == 1 or 2, 1 if 0
        if self.x + self.r > WIDTH - 150 * mediator:
            self.x = WIDTH - self.r - 150 * mediator
            self.vx *= -1
        elif self.x - self.r < 150 * mediator:
            self.x = self.r + 150 * mediator
            self.vx *= -1
        if self.y + self.r > HEIGHT - 75 * mediator:
            self.y = HEIGHT - self.r - 75 * mediator
            self.vy *= -1
        elif self.y - self.r < 75 * mediator:
            self.y = self.r + 75 * mediator
            self.vy *= -1

    def draw(self):
        dr.circle(self.screen, self.color, (self.x, self.y), self.r)


pygame.init()
our_screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = [0, 0]
our_points = [0, 0]
number_of_targets = 4
balls = []
targets = []

clock = pygame.time.Clock()
gun1 = Gun(our_screen, 30, 720, WASD, LEFT_SHIFT, ONE_TO_FIVE, QE, 1)
gun2 = Gun(our_screen, 1470, 30, ARROWS, RIGHT_SHIFT, SIX_TO_ZERO, SQUARE_BRACKETS, 2)
guns = [gun1, gun2]
for _ in range(number_of_targets):
    targets.append(Target(our_screen))
finished = False

while not finished:
    our_screen.fill(GREEN)
    dr.rect(our_screen, WHITE, (150, 75, WIDTH - 300, HEIGHT - 150))
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
            elif our_event.type == pygame.MOUSEBUTTONDOWN:
                gun.fire2_start(our_event)
            elif our_event.type == pygame.MOUSEBUTTONUP:
                bullet[gun.number - 1] += 1
                balls.append(gun.fire2_end(our_event))
            elif our_event.type == pygame.MOUSEMOTION:
                gun.targeting(our_event)
            if our_event.type == pygame.KEYDOWN:
                print(our_event.key)
                if our_event.key == gun.right:
                    gun.vx = gun.v
                    gun.vy = 0
                if our_event.key == gun.left:
                    gun.vx = -gun.v
                    gun.vy = 0
                if our_event.key == gun.down:
                    gun.vy = gun.v
                    gun.vx = 0
                if our_event.key == gun.up:
                    gun.vy = -gun.v
                    gun.vx = 0
                if our_event.key == gun.stop:
                    gun.vx = 0
                    gun.vy = 0
                if our_event.key == gun.smaller:
                    if gun.r > 5:
                        gun.r -= 5
                        gun.start_length = 3 * gun.r
                if our_event.key == gun.bigger:
                    if gun.r < 25:
                        gun.r += 5
                        gun.start_length = 3 * gun.r
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
        gun.movex()
        gun.movey()
        gun.power_up()
        for t in targets:
            if gun.hit_test(t) and t.live:
                our_points[gun.number - 1] -= 5
                t.live = 0
                our_screen.fill(RED)
                t.new_target()
                pygame.display.update()
                clock.tick(FPS)
        for b in balls:
            b.move()
            if b.live == 0:
                balls.pop(balls.index(b))
            if gun.hit_test(b) and gun.number != b.number:
                b.live = 0
                our_points[gun.number - 1] -= 100
                our_points[2 - gun.number] += 10
    for b in balls:
        for t in targets:
            if b.hit_test(t) and t.live:
                if t.color == b.color:
                    balls = []
                    our_points[b.number - 1] += 10
                    t.live = 0
                    bullet = t.hit(b.number)
                    t.new_target()
                elif t.type == 1:
                    t.type = 2
                    t.vy = t.speed
                    t.vx = 2 * t.speed
                    b.live = 0
                elif t.type == 2:
                    t.type = 1
                    t.vx = t.speed
                    t.vy = 2 * t.speed
                    b.live = 0
                else:
                    our_points[b.number - 1] -= 1
                    t.live = 0
                    t.new_target()

pygame.quit()
