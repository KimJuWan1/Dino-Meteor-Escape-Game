import pygame
import random
import math

class Meteor:
    def __init__(self, screen_width, screen_height, speed, image=None):
        self.size = 70
        self.speed = speed
        self.image = pygame.transform.scale(image, (self.size, self.size)) if image else None

        # 시작 위치: 상/하/좌/우 중 랜덤 선택
        side = random.choice(['top', 'bottom', 'left', 'right'])
        if side == 'top':
            self.x = random.randint(0, screen_width)
            self.y = -self.size
        elif side == 'bottom':
            self.x = random.randint(0, screen_width)
            self.y = screen_height + self.size
        elif side == 'left':
            self.x = -self.size
            self.y = random.randint(0, screen_height)
        else:  # right
            self.x = screen_width + self.size
            self.y = random.randint(0, screen_height)

        # 중앙 방향으로 향하는 속도 벡터
        center_x = screen_width // 2
        center_y = screen_height // 2
        angle = math.atan2(center_y - self.y, center_x - self.x)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed

        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.circle(screen, (200, 0, 0), self.rect.center, self.size // 2)

    def is_off_screen(self, screen_width, screen_height):
        return (self.x < -self.size or self.x > screen_width + self.size or
                self.y < -self.size or self.y > screen_height + self.size)

    def collides_with(self, player):
        # 이미지 중심 기반 원형 충돌 판정
        meteor_center = self.rect.center
        player_center = player.get_rect().center

        dx = meteor_center[0] - player_center[0]
        dy = meteor_center[1] - player_center[1]
        distance = math.hypot(dx, dy)

        # 원형 충돌 반경 (축소된 크기)
        meteor_radius = self.size * 0.4
        player_radius = player.get_rect().width * 0.4

        return distance < (meteor_radius + player_radius)

