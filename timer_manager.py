# timer_manager.py
import time
import pygame

class TimerManager:
    def __init__(self):
        self.start_time = None
        self.elapsed = 0
        self.running = False

    def start(self):
        self.start_time = time.time()
        self.running = True

    def stop(self):
        if self.running:
            self.elapsed = time.time() - self.start_time
            self.running = False

    def get_elapsed_time(self):
        if self.running:
            return int(time.time() - self.start_time)
        else:
            return int(self.elapsed)

    def draw(self, screen, font, screen_width):
        seconds = self.get_elapsed_time()
        text_surface = font.render(f"TIME: {seconds}s", True, (255, 255, 255))
        screen.blit(text_surface, (screen_width // 2 - text_surface.get_width() // 2, 10))
