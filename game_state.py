import pygame

class GameState:
    def __init__(self, heart_image, shield_image, coin_image, max_health=5, max_shield=4):
        self.max_health = max_health
        self.health = max_health

        self.max_shield = max_shield
        self.shield = max_shield
        self.shield_active = False

        self.coin_count = 0
        self.ultimate_ready = False

        self.heart_image = pygame.transform.scale(heart_image, (100, 100))
        self.shield_image = pygame.transform.scale(shield_image, (100, 100))
        self.coin_image = pygame.transform.scale(coin_image, (100, 100))

        self.state = "start"  # start, stage, play, gameover
        self.stage = 1
        self.meteors_avoided = 0
        self.score = 0

        self.font = pygame.font.SysFont(None, 40)

    def draw_ui(self, screen):
        spacing = 10
        start_x = 10
        top_y = 40

        # HP 텍스트
        hp_text = self.font.render("HP", True, (255, 255, 255))
        screen.blit(hp_text, (start_x, top_y-10))

        for i in range(self.health):
            screen.blit(self.heart_image, (start_x + 40 + i * (40 + spacing), top_y-50))

        # Shield 텍스트
        shield_y = top_y + 40 + 5
        shield_text = self.font.render("Shield", True, (255, 255, 255))
        screen.blit(shield_text, (start_x, shield_y-10))

        for i in range(self.shield):
            screen.blit(self.shield_image, (start_x + 70 + i * (40 + spacing), shield_y-50))

        # Coin UI
        coin_y = shield_y +45
        screen.blit(self.coin_image, (start_x-28, coin_y-40))
        coin_text = self.font.render(f"x {self.coin_count}", True, (255, 255, 255))
        screen.blit(coin_text, (start_x + 60, coin_y))

        # 궁극기 준비 알림
        if self.ultimate_ready:
            ult_text = self.font.render("ULTIMATE READY! (Press B)", True, (255, 255, 0))
            screen.blit(ult_text, (start_x+250, shield_y + 30))

    def take_damage(self):
        if self.shield_active:
            self.shield_active = False
            return
        if self.health > 0:
            self.health -= 1

    def use_shield(self):
        if self.shield > 0:
            self.shield -= 1
            self.shield_active = True
            return True
        return False

    def collect_coin(self):
        self.coin_count += 1
        if self.coin_count >= 5:
            self.ultimate_ready = True

    def use_ultimate(self):
        if self.ultimate_ready:
            self.coin_count -= 5
            self.ultimate_ready = False
            return True
        return False

    def is_game_over(self):
        return self.health <= 0

    def reset(self):
        self.health = self.max_health
        self.shield = self.max_shield
        self.shield_active = False
        self.coin_count = 0
        self.ultimate_ready = False
        self.stage = 1
        self.state = "start"
        self.meteors_avoided = 0
        self.score = 0

    def next_stage(self):
        self.stage += 1
        self.meteors_avoided = 0
