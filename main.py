import pygame
import player

pygame.init()

WIDTH, HEIGHT = 1280, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

background = pygame.image.load("images/background.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

bird = player.Player(200, HEIGHT // 2, HEIGHT)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird.jump()

    bird.update()

    screen.blit(background, (0, 0))
    bird.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
