# effect_manager.py
import pygame
import time

class EffectManager:
    def __init__(self, explosion_image, size=50):
        self.explosions = []  # 각 폭발 효과의 위치와 시작 시간 저장
        self.explosion_image = pygame.transform.scale(explosion_image, (size, size))
        self.size = size

    def trigger_explosion(self, x, y):
        """운석이 제거될 때 폭발 효과 트리거"""
        self.explosions.append({
            "pos": (x, y),
            "start_time": time.time()
        })

    def update(self):
        """폭발 효과 지속시간 관리 (0.3초 유지)"""
        now = time.time()
        self.explosions = [
            e for e in self.explosions
            if now - e["start_time"] < 0.3
        ]

    def draw(self, screen):
        """폭발 이미지 출력"""
        for e in self.explosions:
            x, y = e["pos"]
            screen.blit(self.explosion_image, (x, y))
