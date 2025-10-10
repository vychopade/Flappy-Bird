import pygame
from player import Player
from pipes import Pipe
import math
import os

pygame.init()

WIDTH, HEIGHT = 1280, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

background = pygame.image.load("images/background.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

font_path = "images/Bellerose.ttf"
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

HIGHSCORE_FILE = "highscore.txt"

def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, "r") as f:
                return int(f.read().strip())
        except:
            return 0
    else:
        return 0

def save_highscore(value):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(value))

highscore = load_highscore()

class TextButton:
    def __init__(self, text, y, font, base_color, hover_color):
        self.text = text
        self.y = y
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.rendered_text = None
        self.rect = None

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.is_hovered(mouse_pos) else self.base_color
        self.rendered_text = self.font.render(self.text, True, color)
        self.rect = self.rendered_text.get_rect(center=(WIDTH // 2, self.y))
        surface.blit(self.rendered_text, self.rect)

    def is_hovered(self, mouse_pos):
        return self.rect and self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered(event.pos)


button_gap = 95 
base_y = HEIGHT // 2 + 70 

start_button = TextButton("START", base_y, font_medium, (180, 180, 180), (230, 230, 230))
options_button = TextButton("OPTIONS", base_y + button_gap, font_medium, (180, 180, 180), (230, 230, 230))
quit_button = TextButton("QUIT", base_y + button_gap * 2, font_medium, (180, 180, 180), (230, 230, 230))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_started and not game_over:
            if start_button.is_clicked(event):
                game_started = True
            elif options_button.is_clicked(event):
                print("Options menu not implemented yet.")
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

    if not game_started and not game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(210)
        overlay.fill((10, 10, 10))
        screen.blit(overlay, (0, 0))

        title_y = HEIGHT // 2 - 360  
        title_shadow = font_big.render("FLAPPY BIRD", True, (5, 5, 5))
        title_text = font_big.render("FLAPPY BIRD", True, (200, 200, 200))
        screen.blit(title_shadow, (WIDTH//2 - title_shadow.get_width()//2 + 5, title_y + 5))
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, title_y))

        hs_y = title_y + 150
        hs_text = font_small.render(f"High Score: {highscore}", True, (180, 180, 180))
        screen.blit(hs_text, (WIDTH//2 - hs_text.get_width()//2, hs_y))

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


    if not game_over:
        bird.update()
        for pipe in pipes:
            pipe.update()
            if pipe.collides_with(bird.rect):
                game_over = True
                if score > highscore:
                    highscore = score
                    save_highscore(highscore)
            if not pipe.passed and pipe.x + pipe.pipe_width < bird.x:
                score += 1
                pipe.passed = True

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
        screen.blit(lose_shadow, (WIDTH//2 - lose_shadow.get_width()//2 + 4, HEIGHT//2 - 120 + 4))
        screen.blit(lose_text, (WIDTH//2 - lose_text.get_width()//2, HEIGHT//2 - 120))

        restart_text = font_medium.render("Press R to Restart", True, (180, 180, 180))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 60))

        hs_text = font_small.render(f"High Score: {highscore}", True, (200, 200, 200))
        screen.blit(hs_text, (WIDTH//2 - hs_text.get_width()//2, HEIGHT//2 + 150))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
