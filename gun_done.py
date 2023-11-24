import math
import random
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
GAME_COLORS = [BLUE, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = random.choice(GAME_COLORS)
        self.live = 30

    def move(self):
        self.x += self.vx
        self.y -= self.vy
        self.vy -= 1
        if self.x >= WIDTH - self.r:
            self.x = WIDTH - self.r
            self.vx = -0.6*self.vx
        if self.x <= self.r:
            self.x = self.r
            self.vx = -0.6*self.vx
        if self.y >= HEIGHT - self.r:
            self.y = HEIGHT - self.r
            self.vy = -0.6*self.vy
        if self.y <= self.r:
            self.y = self.r
            self.vy = -0.6*self.vy
        if self.y == HEIGHT - self.r and abs(self.vy) < 3:
            self.vy = 0
        try: 
            self.vx = self.vx * self.vy / self.vy
        except ZeroDivisionError:
            self.vx -= 0.05*self.vx        

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        if int(self.x) in range(obj.x - obj.r - self.r, obj.x + obj.r + self.r) and int(self.y) in range(obj.y - obj.r - self.r, obj.y + obj.r + self.r):
            return True
        else:
            return False

class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = BLACK
        self.length = 40
        self.width = 10
        self.x = 40
        self.y = 450
        self.grow = 0
    
    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        if event:
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = YELLOW
        else:
            self.color = BLACK

    def draw(self):
        a = self.length
        b = self.width / 2
        x = self.x
        y = self.y
        cos = math.sin(self.an + 0.5*math.pi)
        sin = math.cos(self.an + 0.5*math.pi)
        pygame.draw.polygon(self.screen, self.color, [[x, y], [x - b*sin, y - b*cos], [x - b*sin + a*cos, y - b*cos - a*sin], [x + b*sin + a*cos, y + b*cos - a*sin], [x + b*sin, y + b*cos]])

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = YELLOW
        else:
            self.color = BLACK
        
    def lengthten(self):
        if self.grow == 1 and self.length < 70:
            self.length += 0.5
        elif self.grow == 1 and self.length == 70:
            self.length = self.length
        
    def shorten(self):
        if self.grow == 0 and self.length > 40:
            self.length -= 2
        else:
            self.length = self.length
            

class Target:
    def __init__(self):
        self.points = 0
        self.live = 1
        self.new_target()
        self.vx = random.randint(5, 15)
        self.vy = random.randint(5, 15)
        self.r = random.randint(10, 50)
        self.x = random.randint(400, 780)
        self.y = random.randint(200, 550)
        self.color = RED
        self.screen = screen

    def new_target(self):
        self.points = 0
        self.live = 1
        self.vx = random.randint(5, 15)
        self.vy = random.randint(5, 15)
        self.r = random.randint(10, 50)
        self.x = random.randint(400, 780)
        self.y = random.randint(200, 550)
        self.color = RED
        self.screen = screen

    def hit(self, points=1):
        self.points += points

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
    
    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.x >= WIDTH - self.r:
            self.x = WIDTH - self.r
            self.vx = -self.vx
        if self.x <= self.r:
            self.x = self.r
            self.vx = -self.vx
        if self.y >= HEIGHT - 2*self.r - 20:
            self.y = HEIGHT - 2*self.r - 20
            self.vy = -self.vy
        if self.y <= self.r:
            self.y = self.r
            self.vy = -self.vy
    


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target()
target2 = Target()
finished = False

while not finished:
    target.move()
    target2.move()
    gun.shorten()
    gun.lengthten()
    screen.fill(WHITE)
    gun.draw()
    target.draw()
    target2.draw()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
            gun.grow = 1
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)  
            gun.grow = 0      
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
        if b.hittest(target) and target.live:
            target.live = 0
            target.hit()
            target.new_target()
        if b.hittest(target2) and target2.live:
            target2.live = 0
            target2.hit()
            target2.new_target()
    gun.power_up()

pygame.quit()
