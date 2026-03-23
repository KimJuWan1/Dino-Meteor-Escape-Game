# player.py
import pygame
import time

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.size = 150

        self.image = None
        self.normal_image = None
        self.ultimate_image = None
        self.barrier_image = None

        self.barrier_active = False
        self.barrier_timer = 0

        self.ultimate_active = False
        self.ultimate_timer = 0

    def load_images(self, normal, ultimate):
        self.normal_image = pygame.transform.scale(normal, (self.size, self.size))
        self.ultimate_image = pygame.transform.scale(ultimate, (self.size, self.size))
        self.image = self.normal_image

    def update(self, tilt_x, tilt_y, screen_width, screen_height):
        self.x += tilt_x*0.03
        self.y += tilt_y*0.03
        self.x = max(0, min(screen_width - self.size, self.x))
        self.y = max(0, min(screen_height - self.size, self.y))


    def draw(self, screen):
        img = self.image
        if self.barrier_active and self.barrier_image:
            screen.blit(pygame.transform.scale(self.barrier_image, (self.size, self.size)), (self.x, self.y))
        else:
            screen.blit(img, (self.x, self.y))

    def get_rect(self):
        if self.image:
            return self.image.get_rect(topleft=(self.x, self.y))
        else:
            return pygame.Rect(self.x, self.y, self.size, self.size)


    def activate_barrier(self):
        self.barrier_active = True
        self.barrier_timer = time.time()
        self.image = pygame.transform.scale(self.barrier_image, (self.size, self.size))

    def deactivate_barrier(self):
        if self.barrier_active and time.time() - self.barrier_timer > 1.0:
            self.barrier_active = False
            self.image = self.normal_image

    def activate_ultimate(self):
        self.ultimate_active = True
        self.ultimate_timer = time.time()
        self.image = self.ultimate_image

    def deactivate_ultimate(self):
        if time.time() - self.ultimate_timer > 1.0:
            self.ultimate_active = False
            self.image = self.normal_image

    def reset(self):
        self.x = 400
        self.y = 500
        self.image = self.normal_image
        self.barrier_active = False
        self.ultimate_active = False
