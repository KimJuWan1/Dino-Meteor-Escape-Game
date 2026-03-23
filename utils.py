# utils.py
import pygame
import os

def draw_text(screen, text, x, y, font_size=32, color=(255, 255, 255), center=False):
    font = pygame.font.SysFont(None, font_size)
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(rendered, rect)

def load_image(path, fallback_shape=None, fallback_color=(255, 255, 255), radius=20):
    try:
        full_path = os.path.join("assets", path)
        return pygame.image.load(full_path).convert_alpha()
    except:
        # 이미지 없을 때 대체 도형 그리기
        if fallback_shape == 'circle':
            surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, fallback_color, (radius, radius), radius)
            return surf
        # 플레이스홀더 이미지로 대체
        try:
            return pygame.image.load(os.path.join("assets", "placeholder.png")).convert_alpha()
        except:
            print(f"[load_image] 이미지 로딩 실패: {path}")
            return pygame.Surface((50, 50))  # 최소한의 빈 Surface 반환
