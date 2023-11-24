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
    def __init__(self, screen: pygame.Surface, x=int(WIDTH/2), y=400):
        self.screen = screen
        self.x = x
        self.y = y
        self.color = GREY
        self.live = 1
        self.r = 10
			
    def move(self, direction):
        if direction:
            if direction == K_RIGHT:
                self.x += 3
            elif direction == K_LEFT:
                self.x -= 3
            
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
		self.vy = -1
		self.color = random.choice(GAME_COLORS)
		self.r = 10
		self.power = 1

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
		self.y = 0
		self.vy = 10
		self.vx = 0
		self.color = GREY
		self.HP = self.level * 100
		
	def new_rock(self):
		self.level -= 1
		self.r = self.level * 10
		self.HP = self.level * 100

	def move(self):
		self.y += self.vy
		self.x += self.vx
		if self.y >= HEIGHT - self.r:
			self.y = HEIGHT - self.r
			self.vy = -self.vy
		if self.x >= WIDTH - self.r:
			self.x = WIDTH - self.r
			self.vx = -self.vx
		if self.x <= self.r:
			self.x = self.r
			self.vx = -self.vx
			
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


clock = pygame.time.Clock()
gun = Gun(screen)
rock = Rock(screen)
rocks.append(rock)
finished = False

def shoot(pushka):
    global balls
    delta_shoot_time = 10000
    current_time = pygame.time.get_ticks()
    next_shoot_time = current_time
    if current_time >= next_shoot_time:
        new_ball = Ball(screen, pushka)
        balls.append(new_ball)
        next_shoot_time = current_time + delta_shoot_time
    print(current_time, next_shoot_time)
      

while not finished:
    screen.fill(WHITE)
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
        if r.HP == 0:
            rocks.pop(r)
            
    for b in balls:
        b.draw()
        b.move()
    
    gun.draw()
    gun.move(direction)
              
    pygame.display.update()
    clock.tick(FPS)
    
	        	
pygame.quit()