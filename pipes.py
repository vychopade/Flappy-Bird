import pygame, random

class Pipe:
    def __init__(self, index, spacing, total_pipes, screen_width, screen_height,
                 gap_size=220, speed=5):
        """
        index: index of the pipe (0, 1, 2, ...)
        spacing: horizontal distance between pipes
        total_pipes: total number of pipes in the loop
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.gap_size = gap_size
        self.speed = speed
        self.spacing = spacing
        self.total_pipes = total_pipes
        self.index = index

        # Visual settings
        self.pipe_width = 90
        self.cap_height = 40
        self.cap_extension = 20

        # Random vertical gap
        self.gap_y = self.random_gap_y()

        # Start position: off-screen to the right
        self.x = screen_width + 400 + index * spacing

        self.calculate_pipe_positions()
        self.top_rect = None
        self.bottom_rect = None
        self.passed = False

    def random_gap_y(self):
        """Return a random Y position for the gap center."""
        margin = 200  # keep gaps away from top/bottom edges
        return random.randint(margin, self.screen_height - margin)

    def calculate_pipe_positions(self):
        """Calculate rect positions for top/bottom pipes"""
        self.top_height = self.gap_y - self.gap_size // 2
        self.bottom_y = self.gap_y + self.gap_size // 2
        self.bottom_height = self.screen_height - self.bottom_y

    def update(self):
        """Move pipes left and recycle smoothly off-screen"""
        self.x -= self.speed
        if self.x + self.pipe_width < 0:
            # Move behind the last pipe (off-screen to the right)
            self.x += self.spacing * self.total_pipes
            self.gap_y = self.random_gap_y()
            self.calculate_pipe_positions()
            self.passed = False

    def draw(self, screen):
        """Draw black pipes with slightly larger caps"""
        color = (0, 0, 0)

        # Top pipe
        self.top_rect = pygame.Rect(self.x, 0, self.pipe_width, self.top_height)
        cap_top = pygame.Rect(
            self.x - self.cap_extension // 2,
            self.top_height - self.cap_height,
            self.pipe_width + self.cap_extension,
            self.cap_height,
        )

        # Bottom pipe
        self.bottom_rect = pygame.Rect(self.x, self.bottom_y, self.pipe_width, self.bottom_height)
        cap_bottom = pygame.Rect(
            self.x - self.cap_extension // 2,
            self.bottom_y,
            self.pipe_width + self.cap_extension,
            self.cap_height,
        )

        pygame.draw.rect(screen, color, self.top_rect)
        pygame.draw.rect(screen, color, cap_top)
        pygame.draw.rect(screen, color, self.bottom_rect)
        pygame.draw.rect(screen, color, cap_bottom)

    def collides_with(self, player_rect):
        if self.top_rect and self.bottom_rect:
            return self.top_rect.colliderect(player_rect) or self.bottom_rect.colliderect(player_rect)
        return False
