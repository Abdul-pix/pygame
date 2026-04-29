import pygame
from game_object import GameObject

class Platform(GameObject):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)

    def draw(self, screen, cam_x):
        pygame.draw.rect(screen, (70, 70, 100),
                         (self.x - cam_x, self.y, self.width, self.height))
