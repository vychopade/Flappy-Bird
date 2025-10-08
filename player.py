import pygame

class Player:
    def __init__(self, x, y, screen_height):
        self.x = x
        self.y = y
        self.velocity = 0
        self.gravity = 0.5
        self.lift = -9
        self.screen_height = screen_height

        self.bird_up = pygame.image.load("images/bird2.png").convert_alpha()  #wings up
        self.bird_down = pygame.image.load("images/bird3.png").convert_alpha() #wings down

        self.bird_up = pygame.transform.scale(self.bird_up, (60, 60))
        self.bird_down = pygame.transform.scale(self.bird_down, (60, 60))

        self.image = self.bird_up

        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

        bottom_limit = self.screen_height - self.rect.height // 2
        if self.y > bottom_limit:
            self.y = bottom_limit
            self.velocity = 0

        if self.velocity < 0:          # going up
            self.image = self.bird_up
        else:                          # going down or still
            self.image = self.bird_down

        self.rect.center = (self.x, self.y)

    def jump(self):
        self.velocity = self.lift

    def draw(self, screen):
        screen.blit(self.image, self.rect)
