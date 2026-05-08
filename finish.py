"""
finish.py
De finishlijn die de speler moet bereiken om het level te winnen.
"""

import pygame
from game_object import GameObject


class Finish(GameObject):
    """
    De finishlijn aan het einde van het level.
    Als de speler hiermee botst, wint hij het spel.
    Bestaat uit een witte paal met een gele vlag bovenaan.
    Erft de botsingsdetectie over van GameObject.
    """

    def __init__(self, x, y):
        """
        Maak de finishlijn aan op de gegeven positie.

        Args:
            x (float): Horizontale positie van de paal.
            y (float): Verticale positie (bovenkant van de paal).
        """
        super().__init__(x, y, 40, 120)

    def draw(self, screen, cam_x):
        """
        Teken de finishlijn: een witte paal met een gele vlag erboven.

        Args:
            screen (pygame.Surface): Het scherm waarop we tekenen.
            cam_x (float): De camerapositie voor horizontaal scrollen.
        """
        # Witte paal
        pygame.draw.rect(screen, (230, 230, 230), (self.x - cam_x, self.y, 5, self.height))

        # Gele vlag bovenaan de paal
        pygame.draw.rect(screen, (255, 220, 0), (self.x - cam_x + 5, self.y, 35, 25))
