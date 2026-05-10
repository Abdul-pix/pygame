"""
platforms.py
De klasse voor platforms waarop de speler en vijand kunnen staan.
"""

import pygame
from game_object import GameObject


class Platform(GameObject):
    """
    Een platform in het spel waarop de speler kan staan of tegenaan kan botsen.
    Platforms bewegen niet, ze staan gewoon stil in het level.
    Erft de botsingslogica over van GameObject.
    """

    def __init__(self, x, y, width, height):
        """
        Maak een nieuw platform aan op de gegeven positie.

        Args:
            x (float): Horizontale positie.
            y (float): Verticale positie.
            width (int): Breedte in pixels.
            height (int): Hoogte in pixels.
        """
        super().__init__(x, y, width, height)

    def draw(self, screen, cam_x):
        """
        Dit tekent het platform als een grijsblauwe rechthoek op het scherm.

        Args:
            screen (pygame.Surface): Het scherm waarop we tekenen.
            cam_x (float): De camerapositie voor horizontaal scrollen.
        """
        pygame.draw.rect(
            screen,
            (70, 70, 100),
            (self.x - cam_x, self.y, self.width, self.height)
        )
