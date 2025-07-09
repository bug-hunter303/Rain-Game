import pygame
import random

class Raindrop:
    def __init__(self, width, height):
        self.x = random.randint(0, width)
        self.y = random.randint(-height, 0)
        self.length = random.randint(10, 20)
        self.speed = random.randint(5, 15)
        self.screen_height = height
        self.screen_width = width

    def fall(self):
        self.y += self.speed
        if self.y > self.screen_height:
            self.y = random.randint(-self.screen_height, 0)
            self.x = random.randint(0, self.screen_width)

    def draw(self, screen):
        pygame.draw.line(screen, (0, 0, 255), (self.x, self.y), (self.x, self.y + self.length), 1)

def create_rain(drop_count, width, height):
    return [Raindrop(width, height) for _ in range(drop_count)]
