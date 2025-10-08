import pygame
from player import Player
from pipes import Pipe
import math

pygame.init()

WIDTH, HEIGHT = 1280, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

background = pygame.image.load("images/background.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

font_big = pygame.font.SysFont("Arial", 100, bold=True)
font_medium = pygame.font.SysFont("Arial", 60)
font_small = pygame.font.SysFont("Arial", 40)

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

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_started and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_started = True

        elif not game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird.jump()

        elif game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            bird = Player(200, HEIGHT // 2, HEIGHT)
            pipes = [Pipe(i, PIPE_SPACING, PIPE_COUNT, WIDTH, HEIGHT) for i in range(PIPE_COUNT)]
            score = 0
            game_over = False
            game_started = False

    screen.blit(background, (0, 0))

    if not game_started:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)  # darker
        overlay.fill((20, 20, 20))
        screen.blit(overlay, (0, 0))

        title_shadow = font_big.render("FLAPPY BIRD", True, (10, 10, 10))
        title_text = font_big.render("FLAPPY BIRD", True, (180, 180, 180))
        screen.blit(title_shadow, (WIDTH//2 - title_shadow.get_width()//2 + 5, HEIGHT//2 - 120 + 5))
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 120))

        msg = font_medium.render("Press SPACE to Start", True, (150, 150, 150))
        screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 + 50))

        bird.y = HEIGHT // 2 + int(math.sin(frame_count / 25) * 25)
        bird.rect.y = bird.y
        bird.draw(screen)
        frame_count += 1

        pygame.display.flip()
        clock.tick(60)
        continue

    if not game_over:
        bird.update()
        for pipe in pipes:
            pipe.update()
            if pipe.collides_with(bird.rect):
                game_over = True
            if not pipe.passed and pipe.x + pipe.pipe_width < bird.x:
                score += 1
                pipe.passed = True

    for pipe in pipes:
        pipe.draw(screen)
    bird.draw(screen)

    # Score
    score_text = font_big.render(str(score), True, (230, 230, 230))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 40))

    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(220)
        overlay.fill((30, 30, 30))
        screen.blit(overlay, (0, 0))

        lose_shadow = font_big.render("YOU LOSE!", True, (10, 10, 10))
        lose_text = font_big.render("YOU LOSE!", True, (180, 50, 50))
        screen.blit(lose_shadow, (WIDTH//2 - lose_shadow.get_width()//2 + 4, HEIGHT//2 - 120 + 4))
        screen.blit(lose_text, (WIDTH//2 - lose_text.get_width()//2, HEIGHT//2 - 120))

        restart_text = font_medium.render("Press R to Restart", True, (180, 180, 180))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
