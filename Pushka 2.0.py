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

WIDTH = 400
HEIGHT = 600

class Gun:
    def __init__(self, screen: pygame.Surface, x=int(WIDTH/2)):
        self.screen = screen
        self.x = x
        self.r = 15
        self.y = HEIGHT - self.r
        self.color = GREY
        self.live = 1
        self.speed = 5
        self.bullets = []
        self.bullets_max = 1
        self.delta_time = 500

    def move(self, direction):
        if direction:
            if direction == K_RIGHT:
                self.x += self.speed
            elif direction == K_LEFT:
                self.x -= self.speed
        if self.x <= self.r:
            self.x = self.r
        elif self.x >= WIDTH - self.r:
            self.x = WIDTH - self.r
            
    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
            
class Ball:
    def __init__(self, screen, pushka):
        self.x = pushka.x
        self.maxx = pushka.x
        self.y = pushka.y
        self.vx = 0
        self.vy = 0
        self.screen = screen
        self.color = random.choice(GAME_COLORS)
        self.r = 5
        self.power = 10

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        
    def move(self):
        self.y += self.vy
        self.x += self.vx
        if abs(self.x) >= abs(self.maxx):
            self.x = self.maxx
            self.vx = 0 

class Rock:
    def __init__(self, screen):
        self.screen = screen
        self.level = random.randint(1, 5)
        self.r = self.level * 10
        self.x = random.randint(self.r, WIDTH - self.r)
        self.y = - 1.5 * self.r
        self.vy = 0
        self.color = GREY
        self.HP = self.level * 50

    def move(self):
        self.y += self.vy
        self.vy += 0.5
        if self.y >= HEIGHT - self.r:
            self.y = HEIGHT - self.r
            self.vy -= 0.5
            self.vy = -self.vy
            self.flag = 1

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r)
        
    def hittest(self, obj):
        if self.x in range(obj.x - obj.r - self.r, obj.x + obj.r + self.r) and self.y in range(obj.y - obj.r - self.r, obj.y + obj.r + self.r):
            return True
        else:
            return False
    
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

balls = []
rocks = []
max_rocks = 3
gun = Gun(screen)
score = 0

finished = False
direction = False

clock = pygame.time.Clock()
next_shoot_time = pygame.time.get_ticks()
next_spawn_time = pygame.time.get_ticks()

def charge(pushka):
    if len(pushka.bullets) == 0:
        for b in range(pushka.bullets_max):
            b = Ball(screen, pushka)
            pushka.bullets.append(b)

def position(pushka):
    if pushka.bullets_max % 2 == 0:
        delta = -2
        for b in pushka.bullets:
            if pushka.bullets.index(b) % 2 == 0:
                b.maxx = pushka.x + (pushka.bullets.index(b) * 2 - delta) * b.r
                b.vx = 1
                delta += 1
            else:
                b.maxx = pushka.x - ((pushka.bullets.index(b) - 1) * 2 - delta) * b.r
                b.vx = -1

def shoot(pushka):
    global balls, next_shoot_time, current_time
    if current_time >= next_shoot_time:
        delta_shoot_time = pushka.delta_time
        for b in pushka.bullets:
            b.y = pushka.y
            b.x = pushka.x
            b.vy = -10
        balls += pushka.bullets
        pushka.bullets.clear()
        next_shoot_time = current_time + delta_shoot_time

def spawn_ball(pushka):
    global balls, next_shoot_time, current_time
    if current_time >= next_shoot_time:
        delta_shoot_time = pushka.delta_time
        new_ball = Ball(screen, pushka)
        new_ball.vy = -10
        balls.append(new_ball)
        next_shoot_time = current_time + delta_shoot_time
    
def spawn_rock():
    global rocks, next_spawn_time, current_time
    delta_spawn_time = 5000
    if current_time >= next_spawn_time and len(rocks) < max_rocks:
        new_rock = Rock(screen)
        rocks.append(new_rock)
        next_spawn_time = current_time + delta_spawn_time

def bonuses(bonus_id, pushka, bullets):
    if bonus_id == 1:
        pushka.speed *= 1.5
    elif bonus_id == 2:
        for b in bullets:
            b.vy *= 1.5
    elif bonus_id == 3:
        pushka.bullets_max *= 2

while not finished:
    current_time = pygame.time.get_ticks()
    
    screen.fill(WHITE)
    
    spawn_rock()
    gun.draw()
    gun.move(direction)
    
    if gun.bullets_max > 1:
        charge(gun)
        position(gun)
        shoot(gun)
    else:
        spawn_ball(gun)

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if gun.live == 0:
            finished = True    
        if event.type == KEYDOWN: 
            direction = event.key
        if event.type == KEYUP:  
            direction = False

    for r in rocks:
        r.draw()
        r.move()
        if r.hittest(gun):
            gun.live = 0
        for b in balls:
            if r.hittest(b):
                r.HP -= b.power
                balls.remove(b)
        if r.HP == 0:
            score += r.level * 10
            rocks.remove(r)
            
    for b in balls:
        b.draw()
        b.move()
        if b.y < 0:
            balls.remove(b)

    font = pygame.font.Font('/Users/zakhararonovich/Desktop/MIPT/GitHub/Project/Palatino.ttc', 25)
    score_text = font.render(f'Score: {score}', True, (0, 0, 0))
    screen.blit(score_text, (15, 5))
    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()