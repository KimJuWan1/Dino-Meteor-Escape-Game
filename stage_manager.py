# stage_manager.py
class StageManager:
    def __init__(self, font):
        self.font = font
        self.stage = 1

    def update(self, score):
        self.stage = 1 + score // 10

    def get_meteor_speed(self):
        return 3 + self.stage  # stage가 높아질수록 속도 증가

    def draw(self, screen):
        text = self.font.render(f"Stage {self.stage}", True, (255, 255, 255))
        text_rect = text.get_rect(topright=(screen.get_width() - 20, 20))  # 오른쪽 상단
        screen.blit(text, text_rect)
    def on_stage_changed(self):
        # 필요한 초기화 작업이 있다면 여기에 작성
        pass