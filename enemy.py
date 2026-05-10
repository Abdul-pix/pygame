"""
enemy.py
De vijand die de speler achtervolgt en lasers schiet.
De vijand wordt sneller naarmate het spel langer duurt.
"""

import pygame
import math
from game_object import GameObject


class Laser(GameObject):
    """
    Een laser die de vijand afschiet richting de speler.
    Erft van GameObject zodat we botsingen kunnen detecteren met de speler.
    """

    def __init__(self, x, y, vx):
        """
        Maak een laser aan op de gegeven positie met een horizontale snelheid.

        Args:
            x (float): Startpositie horizontaal.
            y (float): Startpositie verticaal.
            vx (float): Snelheid: positief = rechts, negatief = links.
        """
        super().__init__(x, y, 35, 6)
        self.vx = vx

    def update(self):
        """Beweeg de laser elke frame horizontaal."""
        self.x += self.vx

    def draw(self, screen, cam_x):
        """
        Teken de laser als een rode rechthoek.

        Args:
            screen (pygame.Surface): Het scherm waarop we tekenen.
            cam_x (float): De camerapositie voor horizontaal scrollen.
        """
        pygame.draw.rect(screen, (255, 50, 50), (self.x - cam_x, self.y, self.width, self.height))


class Enemy(GameObject):
    """
    De vijand met AI die de speler achtervolgt.

    Smart Design:
    - Gebruikt vectorberekening om altijd even snel naar de speler te bewegen,
      ongeacht de richting of afstand.
    - Springt automatisch over gaten en muren.
    - Schiet elke 100 frames een laser af richting de speler.
    - Wordt sneller naarmate de tijd vordert, maximaal snelheid 5.
    """

    def __init__(self, x, y):
        """
        Maak de vijand aan op de gegeven startpositie.

        Args:
            x (float): Horizontale startpositie.
            y (float): Verticale startpositie.
        """
        super().__init__(x, y, 30, 40)
        self.vx = 0
        self.vy = 0
        self.speed = 2
        self.jump_force = -10    # negatief = omhoog springen
        self.on_ground = False
        self.jump_wait = 0       # wacht een aantal frames voor de volgende sprong
        self.lasers = []
        self.shoot_timer = 0

    def update(self, player, platforms, gravity, time_passed):
        """
        Update de vijand elke frame: AI, zwaartekracht en botsingen.

        Args:
            player (Player): De speler die achtervolgd wordt.
            platforms (list): Lijst van alle platforms.
            gravity (float): Zwaartekracht per frame.
            time_passed (float): Verstreken speeltijd in seconden.
        """
        self.set_speed(time_passed)
        self.follow_player(player)
        self.try_jump_over_gap(platforms)

        # Zwaartekracht toepassen, maximale valsnelheid is 12
        self.vy += gravity
        if self.vy > 12:
            self.vy = 12

        # Horizontale beweging + botsingen (overschreven versie springt over muren)
        self.x += self.vx
        self.check_x_collision(platforms)

        # Verticale beweging + botsingen
        self.y += self.vy
        self.on_ground = False
        self.check_y_collision(platforms)

        # Herspawn als de vijand uit het level valt
        if self.y > 800:
            self.respawn(player)

        self.update_lasers(player)

    def set_speed(self, time_passed):
        """
        Verhoog de snelheid van de vijand op basis van de verstreken tijd.
        Maximale snelheid is 5 zodat het spel speelbaar blijft.

        Args:
            time_passed (float): Verstreken tijd in seconden.
        """
        self.speed = 2 + time_passed * 0.08
        if self.speed > 5:
            self.speed = 5

    def follow_player(self, player):
        """
        Beweeg de vijand richting de speler via vectorberekening.

        We berekenen de richtingsvector van de vijand naar de speler,
        normaliseren die (lengte = 1) en schalen hem met self.speed.
        Zo beweegt de vijand altijd even snel, ongeacht de afstand.

        Args:
            player (Player): De speler om naartoe te bewegen.
        """
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance > 0:
            self.vx = (dx / distance) * self.speed
        else:
            self.vx = 0

    def try_jump_over_gap(self, platforms):
        """
        Laat de vijand springen als er een gat voor hem is.
        Zo valt hij niet in gaten terwijl hij de speler achtervolgt.

        Args:
            platforms (list): Lijst van alle platforms.
        """
        if self.jump_wait > 0:
            self.jump_wait -= 1

        if self.on_ground and self.jump_wait == 0:
            if not self.ground_in_front(platforms):
                self.vy = self.jump_force
                self.jump_wait = 30

    def ground_in_front(self, platforms):
        """
        Controleer of er een platform is voor de vijand in zijn bewegingsrichting.
        We kijken iets voor en iets onder de vijand.

        Args:
            platforms (list): Lijst van alle platforms.

        Returns:
            bool: True als er grond is, False als er een gat is.
        """
        if self.vx > 0:
            test_x = self.x + self.width + 10
        else:
            test_x = self.x - 10
        test_y = self.y + self.height + 8

        for platform in platforms:
            x_klopt = platform.x < test_x < platform.x + platform.width
            y_klopt = platform.y < test_y < platform.y + platform.height
            if x_klopt and y_klopt:
                return True
        return False

    def check_x_collision(self, platforms):
        """
        Overschrijft check_x_collision van GameObject.
        Lost horizontale botsingen op en laat de vijand ook over muren springen
        zodat hij de speler kan blijven achtervolgen.

        Args:
            platforms (list): Lijst van alle platforms.
        """
        for platform in platforms:
            if self.collides_with(platform):
                if self.vx > 0:
                    self.x = platform.x - self.width
                else:
                    self.x = platform.x + platform.width

                # Spring over de muur
                if self.on_ground and self.jump_wait == 0:
                    self.vy = self.jump_force
                    self.jump_wait = 30

    def update_lasers(self, player):
        """
        Update alle lasers en schiet elke 100 frames een nieuwe laser af.
        Verwijder lasers die te ver weg zijn.

        Args:
            player (Player): De speler om op te schieten.
        """
        self.shoot_timer += 1
        if self.shoot_timer > 100:
            self.shoot_at_player(player)
            self.shoot_timer = 0

        for laser in self.lasers:
            laser.update()

        # Verwijder lasers buiten het speelveld
        self.lasers = [laser for laser in self.lasers if -500 < laser.x < 5000]

    def shoot_at_player(self, player):
        """
        Schiet een laser af in de richting van de speler.

        Args:
            player (Player): De speler om op te richten.
        """
        laser_x = self.x + self.width // 2
        laser_y = self.y + self.height // 2

        # Schiet naar rechts of links afhankelijk van waar de speler is
        if player.x > self.x:
            richting = 7
        else:
            richting = -7

        self.lasers.append(Laser(laser_x, laser_y, richting))

    def respawn(self, player):
        """
        Zet de vijand terug in het spel als hij uit het level gevallen is.
        Spawnt iets achter de speler zodat de achtervolging doorgaat.

        Args:
            player (Player): De speler om achter te spawnen.
        """
        self.x = player.x - 200
        self.y = 100
        self.vy = 0

    def draw(self, screen, cam_x):
        """
        Teken de vijand en alle actieve lasers op het scherm.

        Args:
            screen (pygame.Surface): Het scherm waarop we tekenen.
            cam_x (float): De camerapositie voor horizontaal scrollen.
        """
        pygame.draw.rect(screen, (220, 40, 70), (self.x - cam_x, self.y, self.width, self.height))

        for laser in self.lasers:
            laser.draw(screen, cam_x)
