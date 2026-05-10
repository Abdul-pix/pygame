"""
powerups.py
De klasse voor powerups die de speler kan oppakken.
"""

import pygame
from game_object import GameObject


class PowerUp(GameObject):
    """
    Een powerup die de speler een schild geeft als hij erop loopt.
    Verdwijnt nadat de speler hem oppakt.
    Erft de botsingsdetectie over van GameObject.
    """

    def __init__(self, x, y):
        """
        Maak een powerup aan op de gegeven positie.

        Args:
            x (float): Horizontale positie.
            y (float): Verticale positie.
        """
        super().__init__(x, y, 24, 24)
        # active = False betekent dat de speler hem al opgepakt heeft
        self.active = True

    def draw(self, screen, cam_x):
        """
        Teken de powerup als een blauw blokje, maar alleen als hij nog niet opgepakt is.

        Args:
            screen (pygame.Surface): Het scherm waarop we tekenen.
            cam_x (float): De camerapositie voor horizontaal scrollen.
        """
        if self.active:
            pygame.draw.rect(
                screen,
                (50, 150, 255),
                (self.x - cam_x, self.y, self.width, self.height)
            )
