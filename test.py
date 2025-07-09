import pygame
from background import create_rain

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Create rain
rain = create_rain(100, WIDTH, HEIGHT)

running = True
while running:
    screen.fill((0, 0, 0))  # Clear background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Animate rain
    for drop in rain:
        drop.fall()
        drop.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
