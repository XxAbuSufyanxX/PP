import pygame
import sys
import random
import math
import time
# Pygame entry
pygame.init()
# Constants
WIDTH, HEIGHT = 800, 600
# Screen
instructions = [
    "WASD to move",
    "Left Click to shoot",
    "Survive 15 rounds"
]
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PP")
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont("Comic Sans MS", 30)
# Variables
screen_center_x = screen.get_width() // 2
screen_center_y = screen.get_height() // 2
line_spacing = 40
total_height = len(instructions) * line_spacing
player_x = WIDTH / 2
player_y = HEIGHT / 2
player_radius = 20
player_speed = 175
player_health = 5
enemies = []
enemy_chaser_size = 20
enemy_chaser_speed = 60
enemy_chaser_health = 2
enemy_shooter_size = 60
enemy_shooter_speed = 100
enemy_shooter_health = 4
enemy_shooter_cooldown = 1.5
enemy_bullet_speed = 300
enemy_bullet_damage = 1
enemy_bullets = []
bullets = []
bullet_speed = 500
bullet_radius = 5
bullet_damage = 1
time_shot = 0
sht_cooldown = 0.4
dmg_cooldown = 90
current_round = 0
first_round_delay = 10000
restart_delay = 3000
round_delay = 2000
round_max = 15
round_time = None
wave_start = False
game_over = False
first_round_started = False
game_won = False
first_round_timer = pygame.time.get_ticks()
spawn_queue = []
spawn_timer = 0
base_spawn_interval = 1500
min_spawn_interval = 300
# Function of chaser
def spawn_chaser():
    side = random.choice(["top", "bottom", "left", "right"])

    if side == "top":
        x = random.randint(0, screen.get_width())
        y = -enemy_chaser_size
    elif side == "bottom":
        x = random.randint(0, screen.get_width())
        y = screen.get_height() + enemy_chaser_size
    elif side == "left":
        x = -enemy_chaser_size
        y = random.randint(0, screen.get_height())
    else:
        x = screen.get_width() + enemy_chaser_size
        y = random.randint(0, screen.get_height())

    enemies.append([x, y, 0, 0, "chaser", 0, enemy_chaser_health])
# Function of an octagon
def draw_octagon(surface, x, y, size, color):
    points = []
    for a in range(8):
        angle = a * (360 / 8)
        rad = math.radians(angle)
        px = x + size * math.cos(rad)
        py = y + size * math.sin(rad)
        points.append((px, py))
    pygame.draw.polygon(surface, color, points)
# Function of shooter
def spawn_shooter():
    side = random.choice(['l', 'r', "t", "b"])
    if side == 'l':
        x = - enemy_shooter_size / 2
        y = random.randint(0, HEIGHT)
        dx, dy = 0, 1
    elif side == 'r':
        x = WIDTH - enemy_shooter_size / 2
        y = random.randint(0, HEIGHT)
        dx, dy = 0, -1
    elif side == "t":
        x = random.randint(0, WIDTH)
        y = - enemy_shooter_size / 2
        dx, dy = 1, 0
    else:
        x = random.randint(0, WIDTH )
        y = HEIGHT - enemy_shooter_size / 2
        dx, dy = -1, 0
    enemies.append([x, y, dx, dy, "shooter", 0, enemy_shooter_health])
# Function of waves
def start_round(round_num):
    enemies.clear()
    spawn_queue.clear()
    num_chasers = 1 + round_num
    num_shooters = round_num // 3
    for _ in range(num_chasers):
        spawn_queue.append(spawn_chaser)
    for _ in range(num_shooters):
        spawn_queue.append(spawn_shooter)
# Function of intervals
def get_spawn_interval(round_num):
    interval = base_spawn_interval - (base_spawn_interval - min_spawn_interval) * ((round_num - 1)/(round_max - 1))
    return int(interval)
# Main loop
running = True
while running :
    screen.fill((0, 0, 0))
    dt = clock.tick(60) / 1000
    time_shot += dt
    # Quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Player drawing
    pygame.draw.circle(screen, (255, 255, 255), (player_x, player_y), player_radius)
    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_y -= player_speed * dt
    if keys[pygame.K_s]:
        player_y += player_speed * dt
    if keys[pygame.K_a]:
        player_x -= player_speed * dt
    if keys[pygame.K_d]:
        player_x += player_speed * dt
    # Boundaries
    if player_x < player_radius:
        player_x = player_radius
    if player_x > WIDTH - player_radius:
        player_x = WIDTH - player_radius
    if player_y < player_radius:
        player_y = player_radius
    if player_y > HEIGHT - player_radius:
        player_y = HEIGHT - player_radius
    # Shooting (event)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and time_shot >= sht_cooldown:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - player_x
            dy = mouse_y - player_y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            vx = dx / distance * bullet_speed
            vy = dy / distance * bullet_speed
            if event.button == 1 and time_shot >= sht_cooldown:
                bullets.append([player_x, player_y, vx, vy])
                time_shot = 0
    # Shooting (state)
    mouse_held = pygame.mouse.get_pressed()[0]
    if mouse_held and time_shot >= sht_cooldown:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - player_x
        dy = mouse_y - player_y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        vx = dx / distance * bullet_speed
        vy = dy / distance * bullet_speed
        bullets.append([player_x, player_y, vx, vy])
        time_shot = 0
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x - player_x
    dy = mouse_y - player_y
    distance = (dx ** 2 + dy ** 2) ** 0.5
    vx = dx / distance * bullet_speed
    vy = dy / distance * bullet_speed
    for bullet in bullets:
        bullet[0] += bullet[2] * dt
        bullet[1] += bullet[3] * dt
    # Bullet drawing
    for bullet in bullets:
        pygame.draw.circle(screen, (255, 255, 255),(bullet[0], bullet[1]), bullet_radius)
    # Bullet boundaries
    bullets = [bullet for bullet in bullets if 0 <= bullet[0] <= WIDTH and 0 <= bullet[1] <= HEIGHT]
    # Shooter movement
    for enemy in enemies:
        if enemy[4] == "shooter":
            enemy[0] += enemy[2] * enemy_shooter_speed * dt
            enemy[1] += enemy[3] * enemy_shooter_speed * dt
            if enemy[0] <= 0 or enemy[0] >= WIDTH - enemy_shooter_size:
                enemy[2] *= -1
            if enemy[1] <= 0 or enemy[1] >= HEIGHT - enemy_shooter_size:
                enemy[3] *= -1
    # Shooter drawing
            draw_octagon(screen, enemy[0] + enemy_shooter_size/2, enemy[1] + enemy_shooter_size/2, enemy_shooter_size/2, (255,0,0))
    # Shooter shooting
    for enemy in enemies:
        if enemy[4] == "shooter":
            enemy[5] += dt

            if enemy[5] >= enemy_shooter_cooldown:
                dx = player_x - enemy[0]
                dy = player_y - enemy[1]

                distance = (dx * dx + dy * dy) ** 0.5
                if distance != 0:
                    dx /= distance
                    dy /= distance

                enemy_bullets.append([
                    enemy[0],
                    enemy[1],
                    dx,
                    dy
                ])
                enemy[5] = 0
    for bullet in enemy_bullets:
        bullet[0] += bullet[2] * enemy_bullet_speed * dt
        bullet[1] += bullet[3] * enemy_bullet_speed * dt
    for bullet in enemy_bullets:
        pygame.draw.circle(
            screen,
            (255, 0, 0),
            (int(bullet[0]), int(bullet[1])),
            bullet_radius
        )
    enemy_bullets = [
        b for b in enemy_bullets
        if 0 <= b[0] <= WIDTH and 0 <= b[1] <= HEIGHT
    ]
    # Chaser movement
    for enemy in enemies:
        if enemy[4] == "chaser":
            dx = player_x - enemy[0]
            dy = player_y - enemy[1]
            distance = (dx * dx + dy * dy) ** 0.5
            if distance != 0:
                dx /= distance
                dy /= distance
            enemy[0] += dx * enemy_chaser_speed * dt
            enemy[1] += dy * enemy_chaser_speed * dt
            if distance > 5:
                enemy[0] += dx * enemy_chaser_speed * dt
                enemy[1] += dy * enemy_chaser_speed * dt

            # Chaser drawing
            points = [
                (enemy[0], enemy[1] - enemy_chaser_size),
                (enemy[0] - enemy_chaser_size, enemy[1] + enemy_chaser_size),
                (enemy[0] + enemy_chaser_size, enemy[1] + enemy_chaser_size)
            ]
            pygame.draw.polygon(screen, (255, 255, 0), points)
        if enemy[4] == "bouncer":
            print("timer:", enemy[5])
    # Collision
    if dmg_cooldown > 0:
        dmg_cooldown -= 1
    player_rect = pygame.Rect(
        player_x - player_radius,
        player_y - player_radius,
        player_radius * 2,
        player_radius * 2
    )
    if dmg_cooldown == 0:
        for bullet in enemy_bullets[:]:
            bullet_rect = pygame.Rect(
                bullet[0] - bullet_radius,
                bullet[1] - bullet_radius,
                bullet_radius * 2,
                bullet_radius * 2
            )
            if player_rect.colliderect(bullet_rect):
                player_health -= bullet_damage
                dmg_cooldown = 90
                enemy_bullets.remove(bullet)
                break
        if dmg_cooldown == 0:
            for enemy in enemies:
                size = enemy_chaser_size if enemy[4] == "chaser" else enemy_shooter_size
                enemy_rect = pygame.Rect(enemy[0], enemy[1], size, size)
                if player_rect.colliderect(enemy_rect):
                    player_health -= 1
                    dmg_cooldown = 90
                    break
    for enemy in enemies[:]:
        if enemy[4] == "chaser":
            enemy_rect = pygame.Rect(
                enemy[0] - enemy_chaser_size,
                enemy[1] - enemy_chaser_size,
                enemy_chaser_size * 2,
                enemy_chaser_size * 2
            )
        elif enemy[4] == "shooter":
            enemy_rect = pygame.Rect(
                enemy[0] - enemy_shooter_size,
                enemy[1] - enemy_shooter_size,
                enemy_shooter_size * 2,
                enemy_shooter_size * 2
            )

        for enemy in enemies[:]:
            if enemy[4] == "chaser":
                enemy_rect = pygame.Rect(enemy[0] - enemy_chaser_size,
                                         enemy[1] - enemy_chaser_size,
                                         enemy_chaser_size * 2,
                                         enemy_chaser_size * 2)
            elif enemy[4] == "shooter":
                enemy_rect = pygame.Rect(enemy[0] - enemy_shooter_size,
                                         enemy[1] - enemy_shooter_size,
                                         enemy_shooter_size * 2,
                                         enemy_shooter_size * 2)
            for bullet in bullets[:]:
                bullet_rect = pygame.Rect(bullet[0] - bullet_radius,
                                          bullet[1] - bullet_radius,
                                          bullet_radius * 2,
                                          bullet_radius * 2)
                if enemy_rect.colliderect(bullet_rect):
                    enemy[6] -= bullet_damage
                    bullets.remove(bullet)
                    if enemy[6] <= 0:
                        enemies.remove(enemy)
                    break
    # Health display
    if player_health > 3:
        color = (255, 255, 255)
    elif player_health > 2:
        color = (255, 165, 0)
    else:
        color = (255, 0, 0)
    health_text = font.render(f"HP: {player_health}/5", True, color)
    text_width = health_text.get_width()
    screen_width = screen.get_width()
    screen.blit(health_text, (screen_width - text_width - 10, 10))
    # Round display
    round_font = pygame.font.SysFont("Comic Sans MS", 30)
    round_text = round_font.render(f"Round: {current_round}/15", True, (255, 255, 255))
    round_rect = round_text.get_rect(topleft=(10, 10))
    screen.blit(round_text, round_rect)
    # Game over
    if player_health <= 0:
        game_over = True
    if game_over:
        screen.fill((0, 0, 0))
        game_over_font = pygame.font.SysFont("Comic Sans MS", 50)
        text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(2)
        prompt_font = pygame.font.SysFont("Comic Sans MS", 30)
        prompt_text = prompt_font.render("Try again? Press R", True, (255, 255, 255))
        prompt_rect = prompt_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 40))
        screen.blit(prompt_text, prompt_rect)
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                waiting = False
                player_health = 5
                enemies.clear()
                enemy_bullets.clear()
                damage_cooldown = 0
                current_round = 0
                game_over = False
    # Round progression
    if not first_round_started:
        font = pygame.font.SysFont("Comic Sans MS", 30)

        instructions = [
            "WASD to move",
            "Left Click to shoot",
            "Survive 15 rounds"
        ]
        for i, line in enumerate(instructions):
            text = font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.centerx = screen_center_x
            text_rect.centery = screen_center_y - total_height // 2 + i * line_spacing
            screen.blit(text, text_rect)
        if pygame.time.get_ticks() - first_round_timer >= first_round_delay:
            current_round = 15
            start_round(current_round)
            first_round_started = True
    if first_round_started and not enemies:
        if round_time is None:
            round_time = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - round_time >= round_delay:
            current_round += 1
            start_round(current_round)
            round_time = None
    current_time = pygame.time.get_ticks()
    interval = get_spawn_interval(current_round)

    if spawn_queue and current_time - spawn_timer >= interval:
        spawn_func = spawn_queue.pop(0)
        spawn_func()
        spawn_timer = current_time
    if current_round > round_max:
        time.sleep(3)
        game_won = True
    if game_won:
        screen.fill((0, 0, 0))
        font0 = pygame.font.SysFont("Comic Sans MS", 50)
        text = font0.render("YOU WON!", True, (0, 255, 0))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(2)
        prompt_font = pygame.font.SysFont("Comic Sans MS", 30)
        prompt_text = prompt_font.render("Try again? Press R", True, (255, 255, 255))
        prompt_rect = prompt_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 40))
        screen.blit(prompt_text, prompt_rect)
        pygame.display.flip()
        waiting0 = True
        while waiting0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                waiting0 = False
                player_health = 5
                enemies.clear()
                enemy_bullets.clear()
                damage_cooldown = 0
                current_round = 0
                game_won = False
    # Screen update
    pygame.display.flip()
# Pygame exit
pygame.quit()
sys.exit()