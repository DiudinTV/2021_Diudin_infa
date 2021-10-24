import math
import random as rnd
import pygame
import pygame.draw as dr

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [BLACK, BLUE, YELLOW, MAGENTA, CYAN]

WIDTH = 1500
HEIGHT = 750


def score(screen, points):
    font = pygame.font.Font(None, 100)
    score_counter = font.render(str(points), True, BLACK)
    score_place = score_counter.get_rect(topleft=(20, 20))
    screen.blit(score_counter, score_place)


class Ball:
    def __init__(self, screen: pygame.Surface, x, y, r, power):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
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
    def __init__(self, screen):
        self.r = 25
        self.x = 3 * self.r
        self.y = HEIGHT - 3 * self.r
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
            self.vx = self.v
        elif self.x - 1.5 * self.r + self.vx < 0:
            self.x = 1.5 * self.r
            self.vx = -self.v
        else:
            self.x += self.vx

    def movey(self):
        if self.y + 1.5 * self.r + self.vy > HEIGHT:
            self.y = HEIGHT - 1.5 * self.r
            self.vy = self.v
        elif self.y - 1.5 * self.r + self.vy < 0:
            self.y = 1.5 * self.r
            self.vy = -self.v
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
        dr.circle(self.screen, self.power, (self.x, self.y), 1.5 * self.r)

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
        """ Меняет уничтоженную цель на новую. """
        self.r = rnd.randint(20, 40)
        self.x = rnd.randint(self.r, WIDTH - self.r)
        self.y = rnd.randint(100 + self.r, HEIGHT - self.r)
        self.color = rnd.choice(GAME_COLORS)
        self.live = 1
        self.speed = 5
        direction_x = rnd.random() - 0.5
        direction_y = rnd.random() - 0.5
        if direction_x != 0:
            direction_x *= 1 / abs(direction_x)
        if direction_y != 0:
            direction_y *= 1 / abs(direction_y)
        self.vx = self.speed * rnd.random() * direction_x
        self.vy = (self.speed ** 2 - self.vx ** 2) ** (1 / 2) * direction_y

    def hit(self):
        """Попадание шарика в цель."""
        self.screen.fill(WHITE)
        gun.color = GREEN
        gun.draw()
        font = pygame.font.Font(None, 100)
        message = font.render("Вы уничтожили цель за " + str(bullet) + " выстрелов", True, BLACK)
        place = message.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.screen.blit(message, place)
        pygame.display.update()
        clock.tick(1)
        for event in pygame.event.get():
            pass
        gun.f2_on = 0
        gun.f2_power = 5
        return 0

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.x + self.r > WIDTH:
            self.x = WIDTH - self.r
            self.vx *= -1
        elif self.x - self.r < 0:
            self.x = self.r
            self.vx *= -1
        if self.y + self.r > HEIGHT:
            self.y = HEIGHT - self.r
            self.vy *= -1
        elif self.y - self.r < 0:
            self.y = self.r
            self.vy *= -1

    def draw(self):
        dr.circle(self.screen, self.color, (self.x, self.y), self.r)


pygame.init()
our_screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
our_points = 0
number_of_targets = 15
balls = []
targets = []

clock = pygame.time.Clock()
gun = Gun(our_screen)
for _ in range(number_of_targets):
    targets.append(Target(our_screen))
finished = False

while not finished:
    our_screen.fill(WHITE)
    gun.draw()
    for t in targets:
        t.move()
        t.draw()
    for b in balls:
        b.draw()
    score(our_screen, our_points)
    pygame.display.update()

    clock.tick(FPS)
    for our_event in pygame.event.get():
        if our_event.type == pygame.QUIT:
            finished = True
        elif our_event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(our_event)
        elif our_event.type == pygame.MOUSEBUTTONUP:
            bullet += 1
            balls.append(gun.fire2_end(our_event))
        elif our_event.type == pygame.MOUSEMOTION:
            gun.targeting(our_event)
        if our_event.type == pygame.KEYDOWN:
            if our_event.key == 1073741903:  # RIGHT
                gun.vx += gun.v
            if our_event.key == 1073741904:  # LEFT
                gun.vx -= gun.v
            if our_event.key == 1073741905:  # DOWN
                gun.vy += gun.v
            if our_event.key == 1073741906:  # UP
                gun.vy -= gun.v
            if our_event.key == 113:  # q
                if gun.r > 5:
                    gun.r -= 5
                    gun.start_length = 3 * gun.r
            if our_event.key == 101:  # e
                if gun.r < 45:
                    gun.r += 5
                    gun.start_length = 3 * gun.r
            if our_event.key == 49:  # 1
                gun.power = BLACK
            elif our_event.key == 50:  # 2
                gun.power = BLUE
            elif our_event.key == 51:  # 3
                gun.power = YELLOW
            elif our_event.key == 52:  # 4
                gun.power = MAGENTA
            elif our_event.key == 53:  # 5
                gun.power = CYAN
        elif our_event.type == pygame.KEYUP:
            if our_event.key == 1073741903:
                gun.vx -= gun.v
            if our_event.key == 1073741904:
                gun.vx += gun.v
            if our_event.key == 1073741905:
                gun.vy -= gun.v
            if our_event.key == 1073741906:
                gun.vy += gun.v

    gun.movex()
    gun.movey()
    for t in targets:
        if gun.hit_test(t) and t.live:
            our_points -= 5
            t.live = 0
            our_screen.fill(RED)
            t.new_target()
            pygame.display.update()
            clock.tick(FPS)
    for b in balls:
        b.move()
        if b.live == 0:
            balls.pop(balls.index(b))
        for t in targets:
            if b.hit_test(t) and t.live:
                if t.color == b.color:
                    balls = []
                    our_points += 10
                    t.live = 0
                    bullet = t.hit()
                    t.new_target()
                else:
                    our_points -= 1
                    t.live = 0
                    t.new_target()
    gun.power_up()

pygame.quit()