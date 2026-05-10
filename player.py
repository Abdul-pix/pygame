"""
player.py
De speler die de gebruiker bestuurt met het toetsenbord.
"""

import pygame
from game_object import GameObject


class Player(GameObject):
    """
    De speler die via het toetsenbord beweegt en kan springen.
    Erft de botsingslogica over van GameObject.
    """

    def __init__(self, x, y):
        """
        Dit maakt de speler aan op de gegeven startpositie.

        Args:
            x (float): Horizontale startpositie.
            y (float): Verticale startpositie.
        """
        super().__init__(x, y, 30, 40)
        self.vx = 0          # horizontale snelheid
        self.vy = 0          # verticale snelheid
        self.speed = 4       # loopsnelheid
        self.jump_force = -10  # hoe hard de speler springt (negatief = omhoog)
        self.on_ground = False
        self.shield = False  # True als de speler een schild heeft opgepakt

    def update(self, platforms, gravity):
        """
        Verwerk toetsenbordinput, pas zwaartekracht toe en los botsingen op.
        Dit wordt elke frame aangeroepen vanuit de game loop.

        Args:
            platforms (list): Lijst van alle platforms in het level.
            gravity (float): Zwaartekracht die elke frame bij vy wordt opgeteld.
        """
        keys = pygame.key.get_pressed()

        # Links en rechts bewegen
        self.vx = 0
        if keys[pygame.K_LEFT]:
            self.vx = -self.speed
        if keys[pygame.K_RIGHT]:
            self.vx = self.speed

        # Springen (alleen als de speler op de grond staat)
        if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.on_ground:
            self.vy = self.jump_force
            self.on_ground = False

        # Zwaartekracht toepassen, maximale valsnelheid is 12
        self.vy += gravity
        if self.vy > 12:
            self.vy = 12

        # Horizontale beweging + botsingen oplossen
        self.x += self.vx
        self.check_x_collision(platforms)

        # Verticale beweging + botsingen oplossen
        self.y += self.vy
        self.on_ground = False
        self.check_y_collision(platforms)

    def use_shield(self):
        """
        Gebruik het schild als de speler er één heeft.
        Na gebruik verdwijnt het schild.

        Returns:
            bool: True als het schild gebruikt werd, False als er geen schild was.
        """
        if self.shield:
            self.shield = False
            return True
        return False

    def draw(self, screen, cam_x):
        """
        Teken de speler op het scherm.
        Blauw = schild actief, cyaan = normaal.

        Args:
            screen (pygame.Surface): Het scherm waarop we tekenen.
            cam_x (float): De camerapositie voor horizontaal scrollen.
        """
        if self.shield:
            color = (0, 150, 255)   # blauw als schild actief
        else:
            color = (0, 200, 180)   # cyaan normaal

        pygame.draw.rect(screen, color, (self.x - cam_x, self.y, self.width, self.height))
