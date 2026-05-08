"""
finish.py
Finishlijn-klasse: de winconditie van het spel.
"""

import pygame
from game_object import GameObject


class Finish(GameObject):
    """
    De finishlijn die de speler moet bereiken om het spel te winnen.
    Bestaat uit een paal en een gele vlag.
    Erft botsingsdetectie over van GameObject.
    """

    def __init__(self, x, y):
        """
        Initialiseert de finishlijn op de gegeven positie.

        Args:
            x (float): Horizontale positie van de paal.
            y (float): Verticale positie (bovenkant van de paal).
        """
        super().__init__(x, y, 40, 120)

    def draw(self, screen, cam_x):
        """
        Tekent de finishlijn: een witte paal met een gele vlag.

        Args:
            screen (pygame.Surface): Het schermoppervlak.
            cam_x (float): De camerapositie voor scrolling.
        """
        # Witte paal
        pygame.draw.rect(
            screen,
            (230, 230, 230),
            (self.x - cam_x, self.y, 5, self.height)
        )

        # Gele vlag bovenaan de paal
        pygame.draw.rect(
            screen,
            (255, 220, 0),
            (self.x - cam_x + 5, self.y, 35, 25)
        )
