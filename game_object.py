"""
game_object.py
Dit is de abstracte basisklasse voor alle objecten in ons spel.
Elke klasse zoals speler, vijand, platform, ... erft hiervan.
"""

from abc import ABC, abstractmethod


class GameObject(ABC):
    """
    Abstracte basisklasse voor alle game-objecten.

    We gebruiken ABC zodat Python ons verplicht om draw() zelf
    te implementeren in elke subklasse. Alle objecten in ons spel
    hebben een positie en grootte, en die slaan we hier op
    zodat we dat niet in elke klasse apart moeten schrijven.
    """

    def __init__(self, x, y, width, height):
        """
        Sla de startpositie en grootte op van het object.
        Wordt opgeroepen via super().__init__() in elke subklasse.

        Args:
            x (float): Horizontale startpositie in pixels.
            y (float): Verticale startpositie in pixels.
            width (int): Breedte van het object in pixels.
            height (int): Hoogte van het object in pixels.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def collides_with(self, other):
        """
        Controleer of dit object een ander object raakt.

        We gebruiken AABB (Axis-Aligned Bounding Box): elk object heeft
        een onzichtbare rechthoek eromheen. Als die rechthoeken overlappen
        op zowel de x-as als de y-as, is er een botsing.

        Args:
            other (GameObject): Het andere object waarmee we vergelijken.

        Returns:
            bool: True als de objecten elkaar raken, anders False.
        """
        horizontaal = self.x < other.x + other.width and self.x + self.width > other.x
        verticaal = self.y < other.y + other.height and self.y + self.height > other.y
        return horizontaal and verticaal

    def check_x_collision(self, platforms):
        """
        Los horizontale botsingen op met platforms.
        We duwen het object terug zodat het niet door een platform beweegt.

        Args:
            platforms (list): Lijst van alle platforms in het level.
        """
        for platform in platforms:
            if self.collides_with(platform):
                # Beweging naar rechts: zet links van het platform
                if self.vx > 0:
                    self.x = platform.x - self.width
                # Beweging naar links: zet rechts van het platform
                elif self.vx < 0:
                    self.x = platform.x + platform.width

    def check_y_collision(self, platforms):
        """
        Dit lost de verticale botsingen op met platforms.
        Als het object landt op een platform, zetten we on_ground op True
        zodat het object weet dat het kan springen.

        Args:
            platforms (list): Lijst van alle platforms in het level.
        """
        for platform in platforms:
            if self.collides_with(platform):
                # Val naar beneden: land bovenop het platform
                if self.vy > 0:
                    self.y = platform.y - self.height
                    self.vy = 0
                    self.on_ground = True
                # Spring omhoog: stuit terug naar beneden
                elif self.vy < 0:
                    self.y = platform.y + platform.height
                    self.vy = 0

    @abstractmethod
    def draw(self, screen, cam_x):
        """
        Teken het object op het scherm.
        Elke subklasse implementeert dit zelf omdat elk object er anders uitziet.

        Args:
            screen (pygame.Surface): Het scherm waarop we tekenen.
            cam_x (float): De camerapositie voor horizontaal scrollen.
        """
        pass
