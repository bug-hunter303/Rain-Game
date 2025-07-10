import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Raindodge")

# Load GIF background frames
bg_frames = []
bg_folder = "assets/gif_frames"
for file in sorted(os.listdir(bg_folder)):
    if file.endswith(".png"):
        frame = pygame.image.load(os.path.join(bg_folder, file)).convert()
        frame = pygame.transform.scale(frame, (WIDTH, HEIGHT))
        bg_frames.append(frame)

bg_frame_index = 0
bg_timer = 0

# Raindrop properties
raindrop_width, raindrop_height = 20, 40
raindrop_speed = 5
raindrops = []

# Load images
original_image = pygame.image.load("assets/raindrop.png").convert_alpha()
raindrop_image = pygame.transform.scale(original_image, (raindrop_width, raindrop_height))
sprite_sheet = pygame.image.load("assets/Dino.png").convert_alpha()

# Sprite properties
frame_width, frame_height = 24, 24
scaled_width, scaled_height = 64, 48
num_frames = 24
frames = [
    pygame.transform.scale(
        sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height)),
        (scaled_width, scaled_height)
    )
    for i in range(num_frames)
]

# Animation variables
current_frame = 0
frame_timer = 0
facing_left = False

# Colors
TEXT_COLOR = (255, 255, 255)

# Player properties
player_width, player_height = scaled_width, scaled_height
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 7

# Font
font = pygame.font.SysFont("ithaca", 36)

# Clock
clock = pygame.time.Clock()

# Timer event for raindrops
ADDRAINDROPEVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ADDRAINDROPEVENT, 600)

# Score timer
start_ticks = pygame.time.get_ticks()

def draw_player(x, y):
    frame = frames[current_frame]
    if facing_left:
        frame = pygame.transform.flip(frame, True, False)
    screen.blit(frame, (x, y))

def draw_raindrop(raindrop):
    screen.blit(raindrop_image, (raindrop.x, raindrop.y))

def display_text(text, x, y):
    img = font.render(text, True, TEXT_COLOR)
    screen.blit(img, (x, y))

def game_over_screen(score):
    screen.fill((0, 0, 0))
    display_text("Game Over!", WIDTH // 2 - 80, HEIGHT // 2 - 50)
    display_text(f"Score: {int(score)} seconds", WIDTH // 2 - 110, HEIGHT // 2)
    display_text("Press R to Restart or Q to Quit", WIDTH // 2 - 170, HEIGHT // 2 + 50)
    pygame.display.flip()

def main():
    global player_x, current_frame, facing_left, raindrops, raindrop_speed, start_ticks

    last_level = 0
    frame_timer = 0
    running = True
    game_over = False
    final_score = 0
    bg_frame_index = 0
    bg_timer = 0

    while running:
        dt = clock.tick(60)

        # Time and difficulty scaling
        seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
        raindrop_speed = 7 + seconds_passed * 0.2

        # Raindrop chaos mode
        if seconds_passed > 30 and last_level < 4:
            spawn_count = 5
            pygame.time.set_timer(ADDRAINDROPEVENT, 200)
            last_level = 4
        elif seconds_passed > 20 and last_level < 3:
            spawn_count = 4
            pygame.time.set_timer(ADDRAINDROPEVENT, 300)
            last_level = 3
        elif seconds_passed > 10 and last_level < 2:
            spawn_count = 3
            pygame.time.set_timer(ADDRAINDROPEVENT, 400)
            last_level = 2
        elif seconds_passed > 5 and last_level < 1:
            spawn_count = 2
            pygame.time.set_timer(ADDRAINDROPEVENT, 500)
            last_level = 1
        else:
            spawn_count = 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == ADDRAINDROPEVENT and not game_over:
                for _ in range(spawn_count):
                    drop_x = random.randint(0, WIDTH - raindrop_width)
                    drop = pygame.Rect(drop_x, 0, raindrop_width, raindrop_height)
                    raindrops.append(drop)

            if game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        raindrops.clear()
                        player_x = WIDTH // 2 - player_width // 2
                        raindrop_speed = 5
                        start_ticks = pygame.time.get_ticks()
                        game_over = False
                        last_level = 0
                    elif event.key == pygame.K_q:
                        running = False

        keys = pygame.key.get_pressed()

        if not game_over:
            # Player movement
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player_x -= player_speed
                facing_left = True
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player_x += player_speed
                facing_left = False

            player_x = max(0, min(WIDTH - player_width, player_x))

            # Animate player
            frame_timer += dt
            if frame_timer >= 100:
                current_frame = (current_frame + 1) % len(frames)
                frame_timer = 0

            # Animate background
            bg_timer += dt
            if bg_timer >= 100:
                bg_frame_index = (bg_frame_index + 1) % len(bg_frames)
                bg_timer = 0

            # Move raindrops
            for drop in raindrops:
                drop.y += raindrop_speed

            # Remove off-screen raindrops
            raindrops = [drop for drop in raindrops if drop.y < HEIGHT]

            # Check for collision
            player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
            for drop in raindrops:
                if player_rect.colliderect(drop):
                    game_over = True
                    final_score = seconds_passed
                    break

            # Draw everything
            screen.blit(bg_frames[bg_frame_index], (0, 0))  # ✅ draw animated background
            draw_player(player_x, player_y)
            for drop in raindrops:
                draw_raindrop(drop)
            display_text(f"Time: {int(seconds_passed)}s", 10, 10)
            pygame.display.flip()
        else:
            game_over_screen(final_score)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
