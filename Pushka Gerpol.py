import math
from math import sqrt
from random import choice, randint as rnd

import pygame


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
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600
waiting_for_sleep_to_over = False


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30
        self.gravity = 1
        self.birth = pygame.time.get_ticks()

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        if self.x >= WIDTH - self.r or self.x <= self.r:
            if self.x > WIDTH - self.r:
                self.x = WIDTH - self.r
            if self.x < self.r:
                self.x = self.r
            self.vx *= -0.5
            self.vy *= 0.9
        if self.y >= HEIGHT - self.r:
            if self.y > HEIGHT - self.r:
                self.y = HEIGHT - self.r
            self.vy *= -0.5
            self.vx *= 0.5
            if abs(self.vy) <= 1.6:
                self.vy = 0
                self.gravity = 0

    def expired(self):
        if pygame.time.get_ticks() - self.birth > 2500:
            return True
        return False

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        return sqrt((obj.x - self.x)**2 + (obj.y - self.y)**2) <= obj.r + self.r


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY


    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            d = event.pos[0]-20
            self.an = math.atan((event.pos[1]-450) / d if d != 0 else 1)
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.line(screen, self.color, [40, 450],
                         [40 + self.f2_power * math.cos(self.an),
                          450 + self.f2_power * math.sin(self.an)], 10)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self, screen):
        self.points = 0
        self.live = 1
        self.screen = screen
        self.x = rnd(600, 780)
        self.y = rnd(300, 550)
        self.r = rnd(10, 50)
        self.color = RED
        self.velocity = rnd(-10,10)

    def new_target(self):
        self.x = rnd(600, 780)
        self.y = rnd(300, 550)
        self.r = rnd(10, 50)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        if waiting_for_sleep_to_over is not True:
            pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def move(self):
        self.y += self.velocity
        if self.y >= HEIGHT - self.r or self.y <= self.r:
            self.velocity *= -1




pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target1 = Target(screen)
target2 = Target(screen)
finished = False
start_sleep = None

while not finished:
    screen.fill(WHITE)
    if start_sleep != None and pygame.time.get_ticks() - start_sleep < 1000 and bullet != 0:
        text = pygame.font.Font(None, 50).render('Вы попали в цель за ' + str(bullet) + " раз",
                                                 True, (0, 0, 0))
        screen.blit(text, (20, 500))
    elif start_sleep != None and pygame.time.get_ticks() - start_sleep >= 1000:
        waiting_for_sleep_to_over = False
        start_sleep = None
        bullet = 0
        target1.live = 1
        target2.live = 1
    gun.draw()
    if target1.live:
        target1.draw()
        target1.move()
    if target2.live:
        target2.draw()
        target2.move()
    text = pygame.font.Font(None, 50).render('Счёт:' + str(target1.points + target2.points),
                                              True, (0, 0, 0))
    screen.blit(text, (0, 0))

    expired = []
    for i in range(len(balls)):
        if balls[i].expired():
            expired.append(i)
    for i in expired:
        del balls[i]

    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN and waiting_for_sleep_to_over is not True:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP and waiting_for_sleep_to_over is not True and gun.f2_on!=0:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION and waiting_for_sleep_to_over is not True:
            gun.targetting(event)

    for b in balls:
        b.move()
        if b.hittest(target1) and target1.live:
            target1.live = 0
            target1.hit()
            target1.new_target()
        if b.hittest(target2) and target2.live:
            target2.live = 0
            target2.hit()
            target2.new_target()
        if target1.live==0  and target2.live==0:
            start_sleep = pygame.time.get_ticks()
            waiting_for_sleep_to_over = True
            gun.f2_on = 0

    gun.power_up()

pygame.quit()
