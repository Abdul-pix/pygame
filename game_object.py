from abc import ABC
import pygame

class GameObject(ABC):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def collides_with(self, other):
        return self.get_rect().colliderect(other.get_rect())
