# Захар здарова
# Перед запуском нужно зайти в консоли в папку Project, чтобы программа могла считывать файлы из этой папки.
# Нужно вписать туда cd [путь к папке] без квадратных скобок
import random
import pygame
from pygame.locals import *

FPS = 60

GREY = 0x7D7D7D
RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 500
HEIGHT = 700
gravity = 0.5
spawn_k = 1.5
after_decay_speed_x = 2
after_decay_speed_y = -5


class Gun:
    def __init__(self, screen: pygame.Surface, x=int(WIDTH / 2)):
        self.r = 15
        self.x, self.y = x, HEIGHT - self.r
        self.live = 1
        self.speed = 5
        self.bullets, self.bullets_max = [], 1
        self.delta_time = 50

    def move(self):
        bt = pygame.key.get_pressed()
        if bt[pygame.K_LEFT]:
            self.x -= self.speed
            if self.x < self.r:
                self.x = self.r
        if bt[pygame.K_RIGHT]:
            self.x += self.speed
            if self.x > WIDTH - self.r:
                self.x = WIDTH - self.r


class Ball:
    def __init__(self, screen, pushka):
        self.x = pushka.x
        self.maxx = pushka.x
        self.y = pushka.y
        self.vx, self.vy = 0, 0
        self.screen = screen
        self.color = random.choice(GAME_COLORS)
        self.r = 5
        self.power = 100

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def move(self):
        self.y += self.vy
        self.x += self.vx
        if abs(self.x) >= abs(self.maxx):
            self.x = self.maxx
            self.vx = 0


class Rock:
    def __init__(self, screen, parent_level):
        self.screen = screen
        self.level = self.leveling(parent_level)
        self.r = round((self.level * 900) ** 0.5)
        self.x = random.randint(self.r, WIDTH - self.r)
        self.y = spawn_k * self.r
        self.vx, self.vy = 0, 0
        self.color = GREY
        self.HP = self.level * 1000
        self.delta_time = 1000
        self.touch_bottom = 0
        self.bonus_id = 0

    def move(self):
        self.y += self.vy
        self.x += self.vx
        self.vy += gravity
        if self.y >= HEIGHT - self.r:
            self.y = HEIGHT - self.r
            self.vy -= gravity
            self.vy = -((2 * gravity * (HEIGHT - self.r * (1 + spawn_k))) ** 0.5)
        if self.x <= self.r:
            self.x = self.r
            self.vx = -self.vx
        if self.x >= WIDTH - self.r:
            self.x = WIDTH - self.r
            self.vx = -self.vx

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def hittest(self, obj):
        if (obj.x - obj.r - self.r <= self.x <= obj.x + obj.r + self.r) and (
            obj.y - obj.r - self.r <= self.y <= obj.y + obj.r + self.r
        ):
            return True
        else:
            return False
        
    def leveling(self, parent_level):
        if parent_level == None:
            return random.randint(1, 5)
        else:
            return parent_level - 1

class Button:
    def __init__(self, screen, x, y, text, active_color, inactive_color):
        self.screen = screen
        self.x, self.y = x, y
        self.text = text
        self.width, self.height = (
            self.parameters(self.text)[0],
            self.parameters(self.text)[1],
        )
        self.inactive_color = inactive_color
        self.active_color = active_color

    def parameters(
        self,
        text,
        font="Palatino.ttc",
        font_size=25,
        font_color=(0, 0, 0),
    ):
        font = pygame.font.Font(font, font_size)
        message = font.render(text, True, font_color)
        messageRect = message.get_rect()
        return [messageRect.width, messageRect.height]

    def draw(self, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if (self.x - self.width // 2 < mouse[0] < self.x + self.width // 2) and (
            self.y - self.height // 2 < mouse[1] < self.y + self.height // 2
        ):
            pygame.draw.rect(
                screen,
                self.active_color,
                (
                    self.x - self.width // 2,
                    self.y - self.height // 2,
                    self.width,
                    self.height,
                ),
            )
            if action is not None and click[0] == 1:
                action()
        else:
            pygame.draw.rect(
                screen,
                self.inactive_color,
                (
                    self.x - self.width // 2,
                    self.y - self.height // 2,
                    self.width,
                    self.height,
                ),
            )
        print_text(self.text, self.x, self.y)


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пушка 2.0")
pygame.display.set_icon(pygame.image.load("Скала.bmp"))
font = pygame.font.Font("Palatino.ttc", 25)
gun_surf = pygame.image.load("gun.png").convert_alpha()
gun_surf.set_colorkey((255, 255, 255))
gun_surf = pygame.transform.scale(
    gun_surf, (gun_surf.get_width() // 10, gun_surf.get_height() // 10)
)
gun = Gun(gun_surf)


balls, rocks = [], []
max_rocks = 1
record = 0
score = 0

finished = False
direction = False

clock = pygame.time.Clock()
next_shoot_time, next_spawn_time = pygame.time.get_ticks(), pygame.time.get_ticks()


def print_text(
    text,
    x,
    y,
    font_color=(0, 0, 0),
    font="Palatino.ttc",
    font_size=25,
):
    font = pygame.font.Font(font, font_size)
    message = font.render(text, True, font_color)
    messageRect = message.get_rect()
    messageRect.topleft = (x - messageRect.width // 2, y - messageRect.height // 2)
    screen.blit(message, messageRect)


def charge(pushka):
    if len(pushka.bullets) == 0 and pushka.bullets_max > 1:
        for b in range(pushka.bullets_max):
            b = Ball(screen, pushka)
            pushka.bullets.append(b)


# def position(pushka):
#     if pushka.bullets_max % 2 == 0:
#         delta = -2
#         for b in pushka.bullets:
#             if pushka.bullets.index(b) % 2 == 0:
#                 b.maxx = pushka.x + (pushka.bullets.index(b) * 2 - delta) * b.r
#                 b.vx = 1
#                 delta += 1
#             else:
#                 b.maxx = pushka.x - ((pushka.bullets.index(b) - 1) * 2 - delta) * b.r
#                 b.vx = -1


def shoot(pushka):
    global balls, next_shoot_time, current_time
    if current_time >= next_shoot_time:
        if pushka.bullets_max > 1:
            for b in pushka.bullets:
                b.y = pushka.y
                b.x = pushka.x
                b.vy = -10
            balls += pushka.bullets
            pushka.bullets.clear()
        else:
            new_ball = Ball(screen, pushka)
            new_ball.vy = -10
            balls.append(new_ball)
        next_shoot_time = current_time + pushka.delta_time


def spawn_rock():
    global rocks, next_spawn_time, current_time
    if current_time >= next_spawn_time and len(rocks) < max_rocks:
        new_rock = Rock(screen, None)
        rocks.append(new_rock)
        next_spawn_time = current_time + new_rock.delta_time


def collide():
    global rocks, balls
    for r in rocks:
        if r.hittest(gun):
            gun.live -= 1
        for b in balls:
            if r.hittest(b):
                r.HP -= b.power
                balls.remove(b)


def decay(rock):
    if rock.level > 1:
        new_rock1, new_rock2 = Rock(screen, rock.level), Rock(screen, rock.level)
        new_rock1.x, new_rock2.x = rock.x, rock.x
        new_rock1.y, new_rock2.y = rock.y, rock.y
        new_rock1.vx, new_rock2.vx = -after_decay_speed_x, after_decay_speed_x
        new_rock1.vy, new_rock2.vy = after_decay_speed_y, after_decay_speed_y
        rocks.append(new_rock1)
        rocks.append(new_rock2)


def bonuses(bonus_id, pushka, bullets):
    if bonus_id == 1:
        pushka.speed *= 1.5
    elif bonus_id == 2:
        for b in bullets:
            b.vy *= 1.5
    elif bonus_id == 3:
        pushka.bullets_max *= 2


def finish():
    global finished
    finished = True

def restart():
    global score
    score = 0
    main()

def main():
    global score, current_time
    gun.live = 1
    current_time = pygame.time.get_ticks()
    print_text(f"Score: {score}", 70, 20)
    spawn_rock(), gun.move(), charge(gun), shoot(gun), collide()

    for b in balls:
        b.draw()
        b.move()
        if b.y < 0:
            balls.remove(b)

    for r in rocks:
        r.draw()
        r.move()
        if r.HP <= 0:
            score += r.level * 10
            decay(r)
            rocks.remove(r)


while not finished:
    screen.fill(WHITE)
    if gun.live:
        main()
    else:
        rocks.clear()
        balls.clear()
        print_text("POTRACHENO", WIDTH // 2, 100, font_size=50)
        print_text(f"SCORE: {score}", WIDTH // 2, 250, font_size=40)
        if score >= record and score != 0:
            print_text("NEW RECORD!", WIDTH // 2, 200, font_size=40)
            record = score
        button_restart = Button(
            screen,
            WIDTH // 2,
            HEIGHT // 2 + 40,
            "RESTART",
            (226, 135, 67),
            (234, 182, 118),
        )
        button_exit = Button(
            screen,
            WIDTH // 2,
            HEIGHT // 2 + 80,
            "EXIT",
            (226, 135, 67),
            (234, 182, 118),
        )
        button_restart.draw(restart)
        button_exit.draw(finish)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == KEYDOWN:
            direction = event.key
        if event.type == KEYUP:
            direction = False

    screen.blit(gun_surf, gun_surf.get_rect(center=(gun.x, HEIGHT - 15)))
    pygame.display.update()
    clock.tick(FPS)


pygame.quit()