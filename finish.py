import pygame
from game_object import GameObject

class Finish(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 120)

    def draw(self, screen, cam_x):
        pygame.draw.rect(screen, (230, 230, 230),
                         (self.x - cam_x, self.y, 5, self.height))
        pygame.draw.rect(screen, (255, 220, 0),
                         (self.x - cam_x + 5, self.y, 35, 25))