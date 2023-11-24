import math
import random
import pygame
from pygame.locals import *


FPS = 60
GREY = 0x7D7D7D
WHITE = 0xFFFFFF
RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

direction = False


class Gun:
    def __init__(self, screen: pygame.Surface, x=int(WIDTH/2)):
        self.screen = screen
        self.x = x
        self.r = 10
        self.y = HEIGHT - self.r
        self.color = GREY
        self.live = 1
			
    def move(self, direction):
        if direction:
            if direction == K_RIGHT:
                self.x += 5
            elif direction == K_LEFT:
                self.x -= 5
            
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
		self.y = pushka.y
		self.screen = screen
		self.vy = -10
		self.color = random.choice(GAME_COLORS)
		self.r = 10
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
		
class Rock:
	def __init__(self, screen):
		self.screen = screen
		self.level = random.randint(1, 5)
		self.r = self.level * 10
		self.x = random.randint(self.r, WIDTH - self.r)
		self.y = 20
		self.vy = 0
		self.color = GREY
		self.HP = self.level * 50
		self.flag = 0
		self.max_vy = 0
            
	def move(self):
		self.y += self.vy
		if self.y >= HEIGHT - self.r:
			self.y = HEIGHT - self.r
			self.vy = -self.vy
			if self.y >= HEIGHT - self.r - 2 and not self.flag:
				self.max_vy = abs(self.vy)
			self.flag = 1
		if not self.flag:
			self.vy += 1
		
            
               
			
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
gun = Gun(screen)
finished = False

clock = pygame.time.Clock()
next_shoot_time = pygame.time.get_ticks()
next_spawn_time = pygame.time.get_ticks()

def shoot(pushka):
    global balls, next_shoot_time, current_time
    delta_shoot_time = 500
    if current_time >= next_shoot_time:
        new_ball = Ball(screen, pushka)
        balls.append(new_ball)
        next_shoot_time = current_time + delta_shoot_time
    
def spawn_rock():
    global rocks, next_spawn_time, current_time
    delta_spawn_time = 5000
    if current_time >= next_spawn_time:
        new_rock = Rock(screen)
        rocks.append(new_rock)
        next_spawn_time = current_time + delta_spawn_time
            
while not finished:
    current_time = pygame.time.get_ticks()
    screen.fill(WHITE)
    spawn_rock()
    shoot(gun)
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
            rocks.remove(r)
            
    for b in balls:
        b.draw()
        b.move()
        if b.y < 0:
            balls.remove(b)
    
    gun.draw()
    gun.move(direction)
    pygame.display.update()
    clock.tick(FPS)
	        	
pygame.quit()