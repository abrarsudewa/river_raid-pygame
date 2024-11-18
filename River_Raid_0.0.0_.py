import pygame
import random
pygame.init()

# Display setup
screen = pygame.display.set_mode([800, 500])
pygame.display.set_caption("River Raid")

# Fps setup
FPS = 120
clock = pygame.time.Clock()

# Player plane setup
x_plane_player = 400
y_plane_player = 450
speed_plane_player = 5
def plane_player(x, y, color):
    # Drawing the main body
    pygame.draw.rect(screen, color, pygame.Rect(x, y+20, 5, 20))
    # Drawing the right wing
    pygame.draw.rect(screen, color, pygame.Rect(x+5, y+30, 5, 5))
    pygame.draw.rect(screen, color, pygame.Rect(x+10, y+35, 5, 5))
    # Drawing the left wing
    pygame.draw.rect(screen, color, pygame.Rect(x-5, y+30, 5, 5))
    pygame.draw.rect(screen, color, pygame.Rect(x-10, y+35, 5, 5))

# Enemy plane setup
last_enemy_spawn = 0
plane_enemy_list = []
def plane_enemy(color, enemy_spawn_position, enemy_deleted_position, speed_plane_enemy, delay_plane_enemy):
    global last_enemy_spawn
    global plane_enemies
    # Moving and drawing each enemy
    for plane_enemies in plane_enemy_list:
        plane_enemies[1] += speed_plane_enemy  # Move down
        # Drawing the main body
        pygame.draw.rect(screen, color, pygame.Rect(plane_enemies[0], plane_enemies[1]+20, 5, 20))
        # Drawing the right wing
        pygame.draw.rect(screen, color, pygame.Rect(plane_enemies[0]+5, plane_enemies[1]+25, 5, 5))
        pygame.draw.rect(screen, color, pygame.Rect(plane_enemies[0]+10, plane_enemies[1]+20, 5, 5))
        # Drawing the left wing
        pygame.draw.rect(screen, color, pygame.Rect(plane_enemies[0]-5, plane_enemies[1]+25, 5, 5))
        pygame.draw.rect(screen, color, pygame.Rect(plane_enemies[0]-10, plane_enemies[1]+20, 5, 5))
        # Delete the enemies if get out of screen
        if plane_enemies[1] >= enemy_deleted_position:
            plane_enemy_list.remove(plane_enemies)

    # Spawn a new enemy if enough time has passed
    if current_time - last_enemy_spawn > delay_plane_enemy:
        plane_enemy_list.append([random.randint(10, 790), enemy_spawn_position])  # Spawn at random x position, y=0
        last_enemy_spawn = current_time

# Bullet setup
bullet_list = []
def bullet(color, speed_bullet, radius_bullet):
    global bullets
    # Drawing the bullet
    for bullets in bullet_list:
        bullets[1] -= speed_bullet
        pygame.draw.circle(screen, color, (bullets[0], bullets[1]), radius_bullet)
        if bullets[1] <= -10:
            bullet_list.remove(bullets)

# Making a fungtion shoot bullet
last_shot_bullet = 0
def shoot_bullet(delay_bullet):
    global last_shot_bullet
    if current_time - last_shot_bullet > delay_bullet:
            bullet_list.append([x_plane_player+2.7, y_plane_player+25])
            last_shot_bullet = current_time

# Collision setup
def collision():
    for plane_enemy in plane_enemy_list:
        enemy_rect = pygame.Rect(plane_enemy[0]-30, plane_enemy[1], 60, 20)  # Hitbox plane_enemy
        for bullet in bullet_list:
            bullet_rect = pygame.Rect(bullet[0] - 2, bullet[1] - 2, 4, 4)  # Hitbox bullet
            if enemy_rect.colliderect(bullet_rect):
                plane_enemy_list.remove(plane_enemy)
                bullet_list.remove(bullet)

running = True
while running:

    clock.tick(FPS)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    # plane_player movement
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        x_plane_player -= speed_plane_player
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        x_plane_player += speed_plane_player
    # if the player pressed space then called fungtion shoot_bullet() with delay 100 miliseconds
    if keys[pygame.K_SPACE]:
        shoot_bullet(250)

    screen.fill((0, 0, 255)) # Fill the background with white

    # Drawing the plane_player
    plane_player(x_plane_player, y_plane_player, (255, 255, 0))
    # Drawing the plane_enemy
    plane_enemy((0, 255, 255), -40, 550, 0.5, 700)
    # Drawing the bullet
    bullet((255, 255, 0), 5, 4)

    collision()

    pygame.display.flip()

pygame.quit()