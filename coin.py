# coin.py
import pygame
import random
from utils import load_image

class Coin:
    def __init__(self, screen_width, screen_height):
        self.radius = 12
        self.image = load_image("asset/coin.png", fallback_shape="circle", fallback_color=(255, 215, 0))
        self.reset(screen_width, screen_height)

    def reset(self, screen_width, screen_height):
        self.x = random.randint(self.radius, screen_width - self.radius)
        self.y = random.randint(self.radius, screen_height - self.radius)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.collected = False

    def draw(self, screen):
        if not self.collected:
            screen.blit(self.image, self.rect)

    def check_collision(self, player_rect):
        if not self.collected and self.rect.colliderect(player_rect):
            self.collected = True
            return True
        return False

