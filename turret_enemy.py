"""
turret_enemy.py

Een stationaire vijand die een gebied bewaakt.
De turret gebruikt een eenvoudige state machine:
IDLE -> speler buiten detectiegebied
ATTACK -> speler binnen detectiegebied
"""

import pygame

from game_object import GameObject
from enemy import Laser


class TurretEnemy(GameObject):
    """
    Stationaire enemy met twee toestanden:
    idle en attack.
    """

    def __init__(self, x, y):
        super().__init__(x, y, 35, 40)

        self.state = "idle"

        self.detection_range = 450
        self.vertical_range = 100

        self.shoot_timer = 0
        self.shoot_delay = 50

        self.lasers = []

    def update(self, player):
        """
        Bepaal de toestand van de turret en update lasers.
        """

        dx = player.x - self.x
        dy = player.y - self.y

        # Speler moet dichtbij én ongeveer op dezelfde hoogte staan.
        if abs(dx) <= self.detection_range and abs(dy) <= self.vertical_range:
            self.state = "attack"
        else:
            self.state = "idle"

        if self.state == "attack":
            self.shoot_timer += 1

            if self.shoot_timer >= self.shoot_delay:
                self.shoot_at_player(player)
                self.shoot_timer = 0
        else:
            self.shoot_timer = 0

        for laser in self.lasers:
            laser.update()

        # Oude lasers verwijderen.
        self.lasers = [
            laser
            for laser in self.lasers
            if -500 < laser.x < 5000
        ]

    def shoot_at_player(self, player):
        """
        Schiet horizontaal naar links of rechts,
        afhankelijk van de positie van de speler.
        """

        laser_x = self.x + self.width // 2
        laser_y = self.y + self.height // 2

        if player.x > self.x:
            richting = 7
        else:
            richting = -7

        self.lasers.append(
            Laser(laser_x, laser_y, richting)
        )

    def draw(self, screen, cam_x):
        """
        Teken turret en zijn lasers.
        """

        if self.state == "attack":
            color = (255, 120, 40)
        else:
            color = (170, 90, 40)

        pygame.draw.rect(
            screen,
            color,
            (
                self.x - cam_x,
                self.y,
                self.width,
                self.height
            )
        )

        for laser in self.lasers:
            laser.draw(screen, cam_x)
