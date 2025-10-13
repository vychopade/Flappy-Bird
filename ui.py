import pygame
import os

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
        self.rect = self.rendered_text.get_rect(center=(surface.get_width() // 2, self.y))
        surface.blit(self.rendered_text, self.rect)

    def is_hovered(self, mouse_pos):
        return self.rect and self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered(event.pos)


class Slider:
    def __init__(self, x, y, width, min_value, max_value, value):
        self.x = x
        self.y = y
        self.width = width
        self.height = 10
        self.min_value = min_value
        self.max_value = max_value
        self.value = value
        self.dragging = False
        self.handle_radius = 12

        # compute handle position based on value
        self.handle_x = self.x + (self.value - self.min_value) / (self.max_value - self.min_value) * self.width

        # define rect for positioning convenience
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if abs(event.pos[0] - self.handle_x) < 15 and abs(event.pos[1] - (self.y + self.height // 2)) < 15:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            # update handle x within range
            self.handle_x = max(self.x, min(event.pos[0], self.x + self.width))
            ratio = (self.handle_x - self.x) / self.width
            self.value = self.min_value + ratio * (self.max_value - self.min_value)

    def draw(self, screen):
        # bar
        pygame.draw.rect(screen, (100, 100, 100), (self.x, self.y, self.width, self.height))
        # handle
        pygame.draw.circle(screen, (230, 230, 230), (int(self.handle_x), self.y + self.height // 2), self.handle_radius)
        # sync rect position
        self.rect.y = self.y

    def get_value(self):
        return self.value
    


class ToggleButton:
    def __init__(self, x, y, font, text_on="MUTE", text_off="UNMUTE"):
        self.x = x
        self.y = y
        self.font = font
        self.text_on = text_on
        self.text_off = text_off
        self.is_on = False
        self.rect = None

    def draw(self, surface):
        text = self.text_on if not self.is_on else self.text_off
        color = (200, 200, 200)
        rendered = self.font.render(text, True, color)
        self.rect = rendered.get_rect(center=(self.x, self.y))
        surface.blit(rendered, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect and self.rect.collidepoint(event.pos):
                self.is_on = not self.is_on
                return True
        return False


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
