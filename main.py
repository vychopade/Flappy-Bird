import pygame
from player import Player
from pipes import Pipe
from ui import TextButton, Slider, ToggleButton, load_highscore, save_highscore
import math
import os
import random

pygame.init()
pygame.mixer.init()

point_sound = pygame.mixer.Sound("data/point.mp3")
point_sound.set_volume(0.6)
pygame.mixer.music.load("data/main_song.ogg")
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(-1) 

WIDTH, HEIGHT = 1280, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

background = pygame.image.load("data/background.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

font_path = "data/Bellerose.ttf"
font_big = pygame.font.Font(font_path, 110)
font_medium = pygame.font.Font(font_path, 70)
font_small = pygame.font.Font(font_path, 45)

bird = Player(200, HEIGHT // 2, HEIGHT)
PIPE_COUNT = 4
PIPE_SPACING = 400
pipes = [Pipe(i, PIPE_SPACING, PIPE_COUNT, WIDTH, HEIGHT) for i in range(PIPE_COUNT)]

clock = pygame.time.Clock()
running = True
game_started = False
game_over = False
score = 0
frame_count = 0
options_menu = False
pipe_speed = 5
volume = 0.6
muted = False

highscore = load_highscore()

button_gap = 95
base_y = HEIGHT // 2 + 70

start_button = TextButton("START", base_y, font_medium, (180, 180, 180), (230, 230, 230))
options_button = TextButton("OPTIONS", base_y + button_gap, font_medium, (180, 180, 180), (230, 230, 230))
quit_button = TextButton("QUIT", base_y + button_gap * 2, font_medium, (180, 180, 180), (230, 230, 230))

options_y = HEIGHT // 2 - 200
option_spacing = 130  # vertical space 
pipe_speed_slider = Slider(WIDTH // 2 - 250, options_y + 60, 500, 2, 12, pipe_speed)
volume_slider = Slider(WIDTH // 2 - 250, options_y + option_spacing + 60, 500, 0.0, 1.0, volume)
mute_button = ToggleButton(WIDTH // 2, options_y + option_spacing * 2 + 30, font_small)
back_button = TextButton("BACK", options_y + option_spacing * 3 + 50, font_medium,
                         (180, 180, 180), (230, 230, 230))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if options_menu:

            pipe_speed_slider.handle_event(event)
            volume_slider.handle_event(event)
            volume = volume_slider.get_value()
            pygame.mixer.music.set_volume(0 if muted else volume)

            if mute_button.handle_event(event):
                muted = mute_button.is_on

            if back_button.is_clicked(event):
                options_menu = False
                pipe_speed = int(pipe_speed_slider.get_value())
                volume = volume_slider.get_value()
                point_sound.set_volume(0 if muted else volume*0.5)
            continue


        if not game_started and not game_over and not options_menu:
            if start_button.is_clicked(event):
                game_started = True
            elif options_button.is_clicked(event):
                options_menu = True
            elif quit_button.is_clicked(event):
                running = False

        elif not game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird.jump()

        elif game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            bird = Player(200, HEIGHT // 2, HEIGHT)
            pipes = [Pipe(i, PIPE_SPACING, PIPE_COUNT, WIDTH, HEIGHT) for i in range(PIPE_COUNT)]
            score = 0
            game_over = False
            game_started = False

    screen.blit(background, (0, 0))

    # OPTIONS MENU
    if options_menu:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(210)
        overlay.fill((10, 10, 10))
        screen.blit(overlay, (0, 0))

        # Title
        title_text = font_big.render("OPTIONS", True, (200, 200, 200))
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 300))
        screen.blit(title_text, title_rect)

        # Pipe Speed
        label_speed = font_small.render(f"Pipe Speed: {int(pipe_speed_slider.get_value())}", True, (180, 180, 180))
        label_speed_rect = label_speed.get_rect(center=(WIDTH // 2, pipe_speed_slider.rect.y - 40))
        screen.blit(label_speed, label_speed_rect)
        pipe_speed_slider.draw(screen)

        # Volume
        label_vol = font_small.render(f"Volume: {volume_slider.get_value():.2f}", True, (180, 180, 180))
        label_vol_rect = label_vol.get_rect(center=(WIDTH // 2, volume_slider.rect.y - 40))
        screen.blit(label_vol, label_vol_rect)
        volume_slider.draw(screen)

        mute_button.draw(screen)
        back_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)
        continue


    # MAIN MENU
    if not game_started and not game_over and not options_menu:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(210)
        overlay.fill((10, 10, 10))
        screen.blit(overlay, (0, 0))

        title_y = HEIGHT // 2 - 360
        title_shadow = font_big.render("FLAPPY BIRD", True, (5, 5, 5))
        title_text = font_big.render("FLAPPY BIRD", True, (200, 200, 200))
        screen.blit(title_shadow, (WIDTH // 2 - title_shadow.get_width() // 2 + 5, title_y + 5))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, title_y))

        hs_y = title_y + 150
        hs_text = font_small.render(f"High Score: {highscore}", True, (180, 180, 180))
        screen.blit(hs_text, (WIDTH // 2 - hs_text.get_width() // 2, hs_y))

        mouse_pos = pygame.mouse.get_pos()
        hovered_button = None
        for button in [start_button, options_button, quit_button]:
            if button.is_hovered(mouse_pos):
                hovered_button = button
                break

        for button in [start_button, options_button, quit_button]:
            color = button.hover_color if button == hovered_button else button.base_color
            rendered = button.font.render(button.text, True, color)
            button.rect = rendered.get_rect(center=(WIDTH // 2, button.y))
            screen.blit(rendered, button.rect)

        bird.y = HEIGHT // 2 + int(math.sin(frame_count / 25) * 25)
        bird.rect.y = bird.y
        bird.draw(screen)
        frame_count += 1

        pygame.display.flip()
        clock.tick(60)
        continue

    # GAMEPLAY
    if not game_over:
        bird.update()
        for pipe in pipes:
            pipe.update(speed=pipe_speed)
            if pipe.collides_with(bird.rect):
                game_over = True
                if score > highscore:
                    highscore = score
                    save_highscore(highscore)
            if not pipe.passed and pipe.x + pipe.pipe_width < bird.x:
                score += 1
                pipe.passed = True
                if not muted:
                    point_sound.play()

    for pipe in pipes:
        pipe.draw(screen)
    bird.draw(screen)

    score_text = font_big.render(str(score), True, (230, 230, 230))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 40))

    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(220)
        overlay.fill((20, 20, 20))
        screen.blit(overlay, (0, 0))

        lose_shadow = font_big.render("YOU LOSE!", True, (10, 10, 10))
        lose_text = font_big.render("YOU LOSE!", True, (180, 50, 50))
        screen.blit(lose_shadow, (WIDTH // 2 - lose_shadow.get_width() // 2 + 4, HEIGHT // 2 - 120 + 4))
        screen.blit(lose_text, (WIDTH // 2 - lose_text.get_width() // 2, HEIGHT // 2 - 120))

        restart_text = font_medium.render("Press R to Restart", True, (180, 180, 180))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 60))

        hs_text = font_small.render(f"High Score: {highscore}", True, (200, 200, 200))
        screen.blit(hs_text, (WIDTH // 2 - hs_text.get_width() // 2, HEIGHT // 2 + 150))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
