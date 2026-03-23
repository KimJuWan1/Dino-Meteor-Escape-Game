# main.py
import pygame
import random
import time
from microbit_controller import get_microbit_tilt, is_button_a_pressed, is_button_b_pressed, start_microbit_thread, stop_microbit_thread
from player import Player
from meteor import Meteor
from coin import Coin
from effect_manager import EffectManager
from stage_manager import StageManager
from game_state import GameState
from utils import load_image, draw_text
from stage_manager import StageManager
from timer_manager import TimerManager

# 초기화
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 1000
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("UFO 회피 게임")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)
import pygame.mixer

#마이크로 비트 입력시작!
start_microbit_thread()

# 사운드 초기화
pygame.mixer.init()

# 배경음악 및 효과음 로드
opening_sound = pygame.mixer.Sound("assets/sound/opening_sound.mp3")
coin_sound = pygame.mixer.Sound("assets/sound/coin_sound.mp3")
barrier_sound = pygame.mixer.Sound("assets/sound/barrier_sound.mp3")
meteor_shock_sound = pygame.mixer.Sound("assets/sound/meteor_shock_sound.wav")
meteor_explosion = pygame.mixer.Sound("assets/sound/meteor_explosion.wav")
dead_sound = pygame.mixer.Sound("assets/sound/dead_sound.mp3")

# 이미지 로딩
background = pygame.transform.scale(load_image("background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
player_normal = load_image("player_normal.png")
player_normal = pygame.transform.scale(player_normal, (150, 150))
player_ultimate = pygame.transform.scale(load_image("player_ultimate.png"), player_normal.get_size())
player_barrier = pygame.transform.scale(load_image("player_barrier.png"), player_normal.get_size())
meteor_img = pygame.transform.scale(load_image("meteor.png"), (50, 50))
coin_img = load_image("coin.png")
explosion_img = pygame.transform.scale(load_image("explosion.png"), (50, 50))
heart_img = pygame.transform.scale(load_image("heart_icon.png"), (30, 30))
shield_img = pygame.transform.scale(load_image("shield_icon.png"), (30, 30))
gamestart_img = pygame.transform.scale(load_image("gamestart.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))

# 오브젝트 생성
player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
player.load_images(player_normal, player_ultimate)
player.barrier_image = player_barrier

effects = EffectManager(explosion_img)
stage_manager = StageManager(font)
game_state = GameState(heart_img, shield_img, coin_img)
timer = TimerManager()  # 생존 시간 타이머 생성


meteors = []
coins = []
hit_count = 0
spawn_timer = 0
coin_spawn_timer = 0

# 상태 변수
game_started = False
game_over = False

# 마이크로비트 시작
get_microbit_tilt()  # 초기화용

# 게임 루프
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if not game_started:
        if not pygame.mixer.get_busy():
            opening_sound.play(-1)  # 무한 반복

        screen.blit(gamestart_img, (0, 0))
        draw_text(screen, "Press A + B to Start", SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100, 36, center=True)
        if is_button_a_pressed() and is_button_b_pressed():
            game_started = True
            stage_manager.on_stage_changed()
            opening_sound.stop()  # 오프닝 음악 중지
            timer.start()
        pygame.display.flip()
        clock.tick(60)
        continue

    if game_over:
        draw_text(screen, "Game Over", SCREEN_WIDTH//2, SCREEN_HEIGHT//2-80, 64, center=True)
        draw_text(screen, "Press A + B to Restart", SCREEN_WIDTH//2, SCREEN_HEIGHT//2 , 36, center=True)
        final_time = timer.get_elapsed_time()
        draw_text(screen, f"Your Time: {final_time}s", SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 80, 36, center=True)


        if is_button_a_pressed() and is_button_b_pressed():
            game_over = False
            game_started = False
            meteors.clear()
            coins.clear()
            hit_count = 0
            player.reset()
            game_state.reset()
        pygame.display.flip()
        clock.tick(60)
        continue

    # 마이크로비트 기울기 값 읽기
    tilt_x, tilt_y = get_microbit_tilt()
    player.update(tilt_x * 2, tilt_y * 2, SCREEN_WIDTH, SCREEN_HEIGHT)  # 민감도 증가

    # 배리어 발동
    if is_button_a_pressed() and game_state.shield > 0 and not player.barrier_active:
        if game_state.use_shield():
            player.activate_barrier()
            barrier_sound.play()

    # 궁극기 사용
    if is_button_b_pressed() and game_state.ultimate_ready:
        if game_state.use_ultimate():
            player.activate_ultimate()
            for meteor in meteors:
                effects.trigger_explosion(meteor.x, meteor.y)
            meteor_explosion.play()
            hit_count += len(meteors)
            meteors.clear()

    # 운석 생성
    spawn_timer += 1
    if spawn_timer > 30:
        spawn_timer = 0
        speed = stage_manager.get_meteor_speed()
        meteors.append(Meteor(SCREEN_WIDTH, SCREEN_HEIGHT, speed, meteor_img))

    # 동전 생성
    coin_spawn_timer += 1
    if coin_spawn_timer > 200:
        coin_spawn_timer = 0
        coins.append(Coin(SCREEN_WIDTH, SCREEN_HEIGHT))

    # 오브젝트 업데이트
    for meteor in meteors[:]:
        meteor.update()
        if meteor.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
            meteors.remove(meteor)
            hit_count += 1
        elif meteor.collides_with(player):
            if player.barrier_active:
                pass
            else:
                game_state.take_damage()
                meteor_shock_sound.play()
            meteors.remove(meteor)
            if game_state.is_game_over():
                timer.stop()
                game_over = True
                dead_sound.play()

    for coin in coins[:]:
        if coin.collected:
            coins.remove(coin)
            continue
        if coin.check_collision(player.get_rect()):
            game_state.collect_coin()
            coin_sound.play()
            coins.remove(coin)

    # 스테이지 업데이
    stage_manager.update(hit_count)

    # 오브젝트 그리기
    player.draw(screen)
    for meteor in meteors:
        meteor.draw(screen)
    for coin in coins:
        coin.draw(screen)

    effects.update()
    effects.draw(screen)

    game_state.draw_ui(screen)
    stage_manager.draw(screen)

    timer.draw(screen, font, SCREEN_WIDTH)  # 생존 시간 상단 중앙 표시

    # 상태 해제 처리
    player.deactivate_barrier()
    if player.ultimate_active:
        player.deactivate_ultimate()

    pygame.display.flip()
    clock.tick(60)

# 종료
stop_microbit_thread()
pygame.quit()
