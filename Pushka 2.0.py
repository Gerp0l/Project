import random
import pygame
from pygame.locals import *

FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


WIDTH = 1000
HEIGHT = 700


pygame.init()
pygame.mixer.init()


screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Pushka 2.0")
pygame.display.set_icon(pygame.image.load("images/pushka_icon.png"))

floor = 120


class Gun:
    def __init__(
        self, screen=pygame.image.load("images/gun.png").convert_alpha(), x=WIDTH // 2
    ):
        self.screen = screen
        self.w, self.h = self.screen.get_width() // 10, self.screen.get_height() // 10
        self.r = self.h // 4
        self.x, self.y = x, HEIGHT - floor - self.h // 4
        self.live = 3
        self.live_max = 3
        self.speed = 20
        self.bullets, self.bullets_max = [], 1
        self.delta_time = 35

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

    def draw(self):
        gun_surf = self.screen
        gun_surf = pygame.transform.scale(gun_surf, (self.w, self.h))
        screen.blit(
            gun_surf, gun_surf.get_rect(center=(self.x, HEIGHT - floor - self.h // 4))
        )


class Ball:
    def __init__(self, screen, gun):
        self.x = gun.x
        self.maxx = gun.x
        self.y = gun.y - 1.75 * gun.r
        self.vx, self.vy = 0, 0
        self.screen = screen
        self.color = BLACK
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
    def __init__(
        self, 
        parent_level=None,
        screen=pygame.image.load("images/rock.png").convert_alpha(),
        parent_luck=0,
    ):
        self.screen = screen
        self.level = self.leveling(parent_level)
        self.parent_luck = parent_luck
        # self.luck = int(-10 * random.random() + level + abs(self.parent_luck))
        self.bonus = None
        self.w, self.h = int(screen.get_width() * 1.5 ** (self.level) * 0.15), int(
            screen.get_height() * 1.5 ** (self.level) * 0.15
        )
        self.vx, self.vy = 0, 0
        self.HP = self.level * 1000
        self.delta_time = 1000
        self.phi, self.omega = random.randint(0, 359), random.randint(-3, 3)
        self.diag = int(((self.w // 2) ** 2 + (self.h // 2) ** 2) ** 0.5)
        self.spawn_side=random.randint(2,3)
        if self.spawn_side==3:
            self.x = WIDTH+self.diag   
        if self.spawn_side==2:
            self.x = -self.diag               
        self.y = spawn_k * self.diag

    def move(self):
        if not paused:
            self.x += self.vx
            if self.y >= HEIGHT - self.diag / 2 - floor:
                self.y = HEIGHT - self.diag / 2 - floor
                self.vy = -(
                    (2 * gravity * (HEIGHT - floor - 2*self.diag * spawn_k)) ** 0.5
                )
            if self.spawn_side==0:
                self.phi += self.omega
                self.y += self.vy
                self.vy += gravity
                if self.x <= self.diag / 2:
                    self.x = self.diag / 2
                    self.vx = -self.vx
                if self.x >= WIDTH - self.diag / 2:
                    self.x = WIDTH - self.diag / 2
                    self.vx = -self.vx
            if self.spawn_side==3 and self.x>WIDTH-self.diag:
                self.vx=-after_decay_speed_x
            if self.spawn_side==2 and self.x<self.diag:
                self.vx=after_decay_speed_x
            else:
                self.spawn_side=0


    def hittest(self, obj):
        return (
            obj.x - obj.r - self.diag // 2 <= self.x <= obj.x + obj.r + self.diag // 2
        ) and (
            obj.y - obj.r - self.diag // 2 <= self.y <= obj.y + obj.r + self.diag // 2
        )

    def leveling(self, parent_level):
        if parent_level == None:
            return random.randint(1, 3)
        else:
            return parent_level - 1

    def draw(self):
        rock_surf = self.screen
        rock_surf = pygame.transform.scale(
            rock_surf,
            (
                int(rock_surf.get_width() * 1.5 ** (self.level) * 0.15),
                int(rock_surf.get_height() * 1.5 ** (self.level) * 0.15),
            ),
        )
        rock_surf = pygame.transform.rotate(rock_surf, self.phi)
        screen.blit(rock_surf, rock_surf.get_rect(center=(self.x, self.y)))

        font = pygame.font.Font("fonts/Arcade.ttf", int(15 * 1.5**self.level))
        text = font.render(f"{self.HP // ball_power}", True, WHITE)
        text = pygame.transform.rotate(text, self.phi)
        screen.blit(text, (text.get_rect(center=(self.x, self.y))))


class Button:
    def __init__(
        self,
        screen,
        x,
        y,
        active_color=(19, 207, 22),
        inactive_color=BLACK,
        text="",
        image="",
        inactive_image="",
        font="fonts/Arcade.ttf",
        font_color=BLACK,
        font_size=45,
    ):
        self.screen = screen
        self.x, self.y = x, y
        self.text = text
        self.image = image
        self.inactive_image = inactive_image
        self.font = font
        self.font_size = font_size
        self.font_color = font_color
        self.w, self.h = (
            self.parameters()[0],
            self.parameters()[1],
        )
        self.inactive_color = inactive_color
        self.active_color = active_color

    def parameters(self):
        if self.text != "":
            font = pygame.font.Font(self.font, self.font_size)
            message = font.render(self.text, True, self.font_color)
            messageRect = message.get_rect()
            return [messageRect.w, messageRect.h]
        else:
            image = pygame.image.load(self.image).convert_alpha()
            return [image.get_width() // 8, image.get_height() // 8]

    def draw(self, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.text != "":
            if (self.x - self.w // 2 < mouse[0] < self.x + self.w // 2) and (
                self.y - self.h // 2 < mouse[1] < self.y + self.h // 2
            ):
                print_text(
                    self.text,
                    self.x,
                    self.y,
                    self.active_color,
                    font="fonts/Arcade.ttf",
                    font_size=40,
                )
                if action is not None and click[0] == 1:
                    action()
            else:
                print_text(
                    self.text,
                    self.x,
                    self.y,
                    self.inactive_color,
                    font="fonts/Arcade.ttf",
                    font_size=40,
                )
        else:
            if (self.x < mouse[0] < self.x + self.w) and (
                self.y < mouse[1] < self.y + self.h
            ):
                image = pygame.image.load(self.image).convert_alpha()
                image = pygame.transform.scale(image, (self.w, self.h))
                screen.blit(image, (self.x, self.y))
                if action is not None and click[0] == 1:
                    action()
            else:
                image = pygame.image.load(self.inactive_image).convert_alpha()
                image = pygame.transform.scale(image, (self.w, self.h))
                screen.blit(image, (self.x, self.y))


gun = Gun()

balls, rocks = [], []
ball_power = 0

active_bonuses, arr_bonuses = [], [
    "b_power_up",
    "b_max_up",
    "extra_live",
]

record, score = 0, 0
level, max_rocks = 1, 1

gravity, spawn_k = 2, 1
after_decay_speed_x, after_decay_speed_y = 5, -5
BallsSpeed=30

finished, started, paused, muted, direction = False, False, False, False, False

background = pygame.image.load("images/background.png")
music = pygame.mixer.music.load("sounds/music.mp3")
if not muted:
    pygame.mixer.music.play(-1)

clock = pygame.time.Clock()
next_shoot_time, next_spawn_time, next_bonus_time = (
    pygame.time.get_ticks(),
    pygame.time.get_ticks(),
    pygame.time.get_ticks(),
)

last_collide = pygame.time.get_ticks()
last_mute_click = 0


def print_text(
    text,
    x,
    y,
    font_color=BLACK,
    font="fonts/Arcade.ttf",
    font_size=20,
):
    font = pygame.font.Font(font, font_size)
    message = font.render(text, True, font_color)
    messageRect = message.get_rect()
    messageRect.topleft = (x - messageRect.w // 2, y - messageRect.h // 2)
    screen.blit(message, messageRect)


def charge(gun):
    if len(gun.bullets) == 0 and gun.bullets_max > 1:
        for b in range(gun.bullets_max):
            b = Ball(screen, gun)
            gun.bullets.append(b)


def position(gun):
    if gun.bullets_max % 2 == 0:
        delta = -2
        for b in gun.bullets:
            if gun.bullets.index(b) % 2 == 0:
                b.maxx = gun.x + (gun.bullets.index(b) * 2 - delta) * b.r
                b.vx = 1
                delta += 1
            else:
                b.maxx = gun.x - ((gun.bullets.index(b) - 1) * 2 - delta) * b.r
                b.vx = -1


def shoot(gun):
    global balls, next_shoot_time, current_time
    if current_time >= next_shoot_time:
        if gun.bullets_max > 1:
            for b in gun.bullets:
                b.y = gun.y
                b.x = gun.x
                b.vy = -BallsSpeed
            balls += gun.bullets
            gun.bullets.clear()
        else:
            new_ball = Ball(screen, gun)
            new_ball.vy = -BallsSpeed
            balls.append(new_ball)
        next_shoot_time = current_time + gun.delta_time


def spawn_rock():
    global rocks, next_spawn_time, current_time, max_rocks
    if current_time >= next_spawn_time and len(rocks) < max_rocks:
        new_rock = Rock(None)
        rocks.append(new_rock)
        next_spawn_time = current_time + new_rock.delta_time


def collide():
    global rocks, balls, current_time, last_collide
    cooldown = 300
    for r in rocks:
        if r.hittest(gun):
            if current_time - last_collide >= cooldown:
                gun.live -= 1
                last_collide = current_time
        for b in balls:
            if r.hittest(b):
                r.HP -= b.power
                balls.remove(b)

def decay(rock):
    if rock.level > 1:
        new_rock1, new_rock2 = Rock(rock.level), Rock(rock.level)
        new_rock1.spawn_side, new_rock2.spawn_side=0, 0
        new_rock1.x, new_rock2.x = rock.x, rock.x
        new_rock1.y, new_rock2.y = rock.y, rock.y
        new_rock1.vx, new_rock2.vx = -after_decay_speed_x, after_decay_speed_x
        new_rock1.vy, new_rock2.vy = after_decay_speed_y, after_decay_speed_y
        rocks.append(new_rock1)
        rocks.append(new_rock2)


def bonuses(bonus_id):
    global level, active_bonuses, next_bonus_time, current_time
    bonus_delta_time = 10000
    if (
        active_bonuses.count(bonus_id) < 3
        and bonus_id in arr_bonuses
        and current_time >= next_bonus_time
    ):
        if bonus_id == "b_max_up":
            gun.bullets_max *= 2
        elif bonus_id == "b_power_up":
            for b in gun.bullets:
                b.power *= 1.5
        elif bonus_id == "extra_live":
            if gun.live < gun.live_max:
                gun.live += 1
            else:
                gun.live += 1
                gun.live_max += 1
        active_bonuses.append(bonus_id)
        next_bonus_time = current_time + (bonus_delta_time / (level * 10))


def bonuses_clear():
    global active_bonuses
    for bonus_id in active_bonuses:
        if bonus_id == "gun_speed_up":
            gun.speed /= 1.5
        elif bonus_id == "b_max_up":
            gun.bullets_max //= 2
        elif bonus_id == "b_speed_up":
            for b in gun.bullets:
                b.speed /= 1.5
        elif bonus_id == "b_power_up":
            for b in gun.bullets:
                b.power /= 1.5
        elif bonus_id == "extra_live":
            if gun.live_max > 3:
                gun.live_max -= 1
            if gun.live > 3:
                gun.live -= 1

    active_bonuses.clear()


def hearts():
    for i in range(gun.live_max):
        empty_heart = pygame.image.load("images/empty_heart.png").convert_alpha()
        empty_heart = pygame.transform.scale(empty_heart, (30, 30))
        screen.blit(empty_heart, (20 + 30 * i, 40))
        for j in range(gun.live):
            full_heart = pygame.image.load("images/full_heart.png").convert_alpha()
            full_heart = pygame.transform.scale(full_heart, (30, 30))
            screen.blit(full_heart, (20 + 30 * j, 40))


def start():
    global started
    started = True


def finish():
    global finished
    finished = True


def restart():
    global score, active_bonuses, current_time
    gun.live = gun.live_max
    score = 0
    # bonuses_clear()
    main()


def start_menu():
    global record
    gun_logo = pygame.image.load("images/pushka_logo.png").convert_alpha()
    gun_logo = pygame.transform.scale(gun_logo, (400, 153))
    screen.blit(gun_logo, gun_logo.get_rect(center=(WIDTH/2, 100)))
    button_start = Button(
        screen, WIDTH // 2, HEIGHT // 2, WHITE, BLACK, "START"
    )
    button_start.draw(start)


def end_menu():
    global score, record
    rocks.clear(), balls.clear()
    game_over = pygame.image.load("images/game_over.png").convert_alpha()
    game_over = pygame.transform.scale(game_over, (300, 150))
    screen.blit(game_over, game_over.get_rect(center=(WIDTH/2, 100)))
    print_text(f"SCORE:{score}", WIDTH // 2, 300, font_size=30)
    if score >= record and score != 0:
        print_text("NEW RECORD!", WIDTH // 2, 250, font_size=30)
        record = score
    else:
        print_text(f"RECORD:{record}", WIDTH // 2, 250, font_size=30)
    button_restart = Button(
        screen, WIDTH // 2, HEIGHT // 2 + 100, WHITE, BLACK, "RESTART"
    )
    button_exit = Button(
        screen, WIDTH // 2, HEIGHT // 2 + 150, WHITE, BLACK, "EXIT"
    )
    button_restart.draw(restart)
    button_exit.draw(finish)


def pause():
    global paused, gun
    paused = not paused
    if paused == True:
        for r in rocks:
            r.vx = 0
            r.vy = 0
        for b in balls:
            b.vy = 0
    else:
        for b in balls:
            b.vy = -10


def mute():
    global muted, current_time, last_mute_click
    cooldown = 100
    if current_time >= last_mute_click + cooldown:
        muted = not muted
        if muted == True:
            pygame.mixer.music.pause()
            last_mute_click = pygame.time.get_ticks()
        else:
            pygame.mixer.music.unpause()
            last_mute_click = pygame.time.get_ticks()


def main():
    global score, current_time, max_rocks, level, ball_power, paused
    level = 1 + score // 150
    max_rocks = level
    current_time = pygame.time.get_ticks()

    for b in balls:
        ball_power = b.power
        b.draw()
        b.move()
        if b.y < 0:
            balls.remove(b)
            

    for rock in rocks:
        rock.draw()
        rock.move()
        if rock.HP <= 0:
            score += rock.level * 10
            decay(rock)
            # if rock.luck in range(1, 5):
            # bonuses(random.choice(arr_bonuses))
            rocks.remove(rock)

    font = pygame.font.Font("fonts/Arcade.ttf", 20)
    text = font.render(f"Score:{score}", True, WHITE)
    text_rect = text.get_rect(topleft=(20, 10))
    screen.blit(text, text_rect)

    gun.draw(), hearts()

    if not paused:
        spawn_rock(), gun.move(), collide(), shoot(gun), charge(gun)
        # print(rocks[0].x)
        # print(rocks[0].spawn_side)
        # print(WIDTH-rocks[0].diag)
        button_pause = Button(
            screen,
            WIDTH - 75,
            10,
            BLACK,
            BLACK,
            "",
            "images/pause_black.png",
            "images/pause_white.png",
        )
        button_pause.draw(pause)

    else:
        button_unpause = Button(
            screen,
            WIDTH // 2 - 80,
            HEIGHT // 2 - 32,
            BLACK,
            BLACK,
            "",
            "images/unpause_black.png",
            "images/unpause_white.png",
        )
        if not muted:
            button_mute = Button(
                screen,
                WIDTH // 2 + 48,
                HEIGHT // 2 - 32,
                BLACK,
                BLACK,
                "",
                "images/mute_black.png",
                "images/mute_white.png",
            )
            button_mute.draw(mute)
        else:
            button_unmute = Button(
                screen,
                WIDTH // 2 + 48,
                HEIGHT // 2 - 32,
                BLACK,
                BLACK,
                "",
                "images/unmute_black.png",
                "images/unmute_white.png",
            )
            button_unmute.draw(mute)
        button_unpause.draw(pause)


while not finished:
    screen.blit(background, (0, 0))
    if not started:
        start_menu()
    elif gun.live and started:
        main()
    else:
        end_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == KEYDOWN:
            direction = event.key
        if event.type == KEYUP:
            direction = False
    
    pygame.display.update()
    clock.tick(FPS)


pygame.quit()
