import math
import random
import pygame


FPS = 60
GREY = 0x7D7D7D


WIDTH = 1920
HEIGHT = 1080

class Gun:

	def __init__(self, screen: pygame.Surface, x=int(WIDTH/2), y=1000):
		self.screen = screen
		self.x = x
		self.y = y
		self.vx = 0
		self.color = GREY
		self.live = 1
		
	def go_right(self, event):
		if event:
			TODO 
	
	def go_left(self, event):
		if event:
			TODO
	
	def move(self):
		TODO
		
	def draw(self):
		TODO
		
	def shoot(self):
		global balls
		new_ball = Ball(self.screen)
		new_ball.vx = TODO
		new_ball.vy = TODO
		balls.append(new_ball)
		
class Ball:
	
	def __init__(self, pushka, screen):
		self.x = pushka.x
		self.y = pushka.y
		self.vy = const
		self.color = GREY
		self.r = r
		self.power = 1
		
	def draw(self):
		pygame.draw.circle(
			self.screen,
			self.color,
			(self.x, self.y)
			self.r
		)
		
	def move(self):
		self.y += self.vy
		
class Rock:
	
	def __init__(self, pushka, ball, screen):
		self.x = random.randint(self.r, WIDTH - self.r)
		self.y = 0
		self.vy = const TODO
		self.vx = const TODO
		self.color = GREY
		self.level = random.randint(1, 5)
		self.r = self.level * 10
		self.HP = self.level * 100
		
	def new_rock(self):
		self.level -= 1
		self.r = self.level * 10
		self.HP = self.level * 100
		TODO	
	
	def decay(self):
		TODO
		
	def move(self):
		self.y += self.vy
		self.x += self.vx
		if self.y => HEIGHT - self.r:
			self.y = HEIGHT - self.r
			self.vy = -self.vy
		if self.x => WIDTH - self.r:
			self.x = WIDTH - self.r
			self.vx = -self.vx
		if self.x <= self.r:
			self.x = self.r
			self.vx = -self.vx
			
	def draw(self):
		pygame.draw.circle(
			self.screen,
			self.color,
			(self.x, self.y)
			self.r
		)
		
	def hittest(self, obj, screen):
		if self.x in range(TODO, TODO) and self.y in range(TODO, TODO):
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
finished = False

while not finished:
	gun.draw()
	gun.move()
    	screen.fill(WHITE) TODO
    	for b in balls:
        		b.draw()
		b.move()
		if b.y < 0:
			#убрать с экрана и массива TODO
	for r in rocks:
		r.draw()
		if r.level >= 2:
			r.decay()
    	pygame.display.update()
	
clock.tick(FPS)
for event in pygame.event.get():
	if event.type == pygame.QUIT:
        		finished = True
	elif gun.live == 0:
		finished = True 
       	elif event.type == #нажали левую стрелочку:
        		gun.move_left()
	elif event.type == #нажали правую стрелочку:
		gun.move_right()
	        
        
for r in rocks:
	r.move()
        if r.hittest(gun):
		gun.live = 0
		#конец игры
        if r.hittest(ball):
        		r.hp -= ball.power
		if r.hp == 0:
			#убрать с экрана и массива TODO
			
pygame.quit()
		
			
		
	
		
		