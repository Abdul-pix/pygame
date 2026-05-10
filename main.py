"""
main.py
Het hoofdbestand van mijn spel RUN.EXE.
Hier staat de game loop en de logica voor de verschillende speltoestanden.

Besturing:
    Pijltje links / rechts : bewegen
    Pijltje omhoog / spatie: springen
    ENTER                  : starten of herstarten
    ESC                    : afsluiten
"""

import pygame
import sys

from player import Player
from enemy import Enemy
from level_generator import make_level
from score_manager import ScoreManager

# Instellingen voor het scherm
SCREEN_W = 900
SCREEN_H = 600
FPS = 60
GRAVITY = 0.45


class Game:
    """
    De hoofdklasse die het spel beheert.

    Het spel heeft 4 toestanden:
        'menu'   : Startscherm, wacht op ENTER om te beginnen.
        'playing': Het spel is bezig.
        'dead'   : De speler is gepakt of gevallen.
        'won'    : De speler heeft de finish bereikt.
    """

    def __init__(self):
        """Initialiseer pygame, het scherm en laad het eerste level."""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("RUN.EXE")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(None, 30)
        self.big_font = pygame.font.SysFont(None, 60)

        self.state = "menu"
        self.reset()

    def reset(self):
        """
        Reset het spel: genereer een nieuw level en maak alle objecten opnieuw aan.
        Wordt aangeroepen bij het starten en na game over.
        """
        self.platforms, self.finish, self.powerups = make_level(SCREEN_H)

        ground_y = SCREEN_H - 70
        self.player = Player(120, ground_y - 40)
        self.enemy = Enemy(30, ground_y - 40)

        self.score = ScoreManager()
        self.camera_x = 0
        self.final_score = 0

    def run(self):
        """
        Start de game loop. Dit blijft draaien totdat het programma wordt afgesloten.
        Elke frame worden events verwerkt, objecten geüpdatet en alles getekend.
        clock.tick(FPS) zorgt dat het spel niet sneller loopt dan 60 frames per seconde.
        """
        while True:
            self.handle_events()

            if self.state == "playing":
                self.update()

            self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        """
        Verwerk alle pygame-events zoals afsluiten en toetsaanslagen.
        ENTER start of herstart het spel, ESC sluit af.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                # ENTER om te starten of opnieuw te spelen
                if event.key == pygame.K_RETURN:
                    if self.state in ("menu", "dead", "won"):
                        self.reset()
                        self.state = "playing"

    def update(self):
        """
        Update alle objecten elke frame: speler, vijand, powerups en win/verlies check.
        Wordt alleen aangeroepen als de toestand 'playing' is.
        """
        t = self.score.get_time()

        self.player.update(self.platforms, GRAVITY)
        self.enemy.update(self.player, self.platforms, GRAVITY, t)

        # Camera volgt de speler (speler staat op 1/3 van het scherm)
        self.camera_x = self.player.x - 300
        if self.camera_x < 0:
            self.camera_x = 0

        # Controleer of de speler een powerup oppakt
        for powerup in self.powerups:
            if powerup.active and self.player.collides_with(powerup):
                self.player.shield = True
                powerup.active = False

        # Verlies: speler valt uit het level
        if self.player.y > SCREEN_H + 100:
            self.state = "dead"

        # Verlies: vijand raakt de speler (schild absorbeert één treffer)
        if self.player.collides_with(self.enemy):
            if not self.player.use_shield():
                self.state = "dead"

        # Verlies: laser raakt de speler (schild absorbeert één treffer)
        for laser in self.enemy.lasers[:]:
            if self.player.collides_with(laser):
                if self.player.use_shield():
                    self.enemy.lasers.remove(laser)
                else:
                    self.state = "dead"

        # Win: speler bereikt de finishlijn
        if self.player.collides_with(self.finish):
            self.final_score = self.score.get_score()
            self.state = "won"

    def draw(self):
        """
        Teken alles op het scherm op basis van de huidige speltoestand.
        Roept pygame.display.flip() aan om het scherm te verversen.
        """
        self.screen.fill((20, 20, 40))

        # Teken alle game-objecten via hun eigen draw() methode
        for platform in self.platforms:
            platform.draw(self.screen, self.camera_x)
        for powerup in self.powerups:
            powerup.draw(self.screen, self.camera_x)
        self.finish.draw(self.screen, self.camera_x)
        self.enemy.draw(self.screen, self.camera_x)
        self.player.draw(self.screen, self.camera_x)

        # Teken het juiste scherm op basis van de toestand
        if self.state == "playing":
            self.draw_hud()
        elif self.state == "menu":
            self.draw_msg("RUN.EXE", "Druk ENTER om te starten")
        elif self.state == "dead":
            self.draw_msg("GAME OVER", "ENTER om opnieuw te spelen")
        elif self.state == "won":
            self.draw_msg("GEWONNEN!", "Score: " + str(self.final_score))

        pygame.display.flip()

    def draw_hud(self):
        """
        Teken de score, tijd en schildstatus bovenaan het scherm tijdens het spelen.
        """
        score = self.score.get_score()
        tijd = int(self.score.get_time())

        schild_tekst = "   Schild: AAN" if self.player.shield else ""
        tekst = self.font.render(f"Score: {score}   Tijd: {tijd}{schild_tekst}", True, (255, 255, 255))
        self.screen.blit(tekst, (20, 20))

    def draw_msg(self, title, ondertitel):
        """
        Teken een groot bericht in het midden van het scherm.
        Wordt gebruikt voor het menu, game over en gewonnen scherm.

        Args:
            title (str): Grote tekst bovenaan.
            ondertitel (str): Kleinere tekst eronder.
        """
        grote_tekst = self.big_font.render(title, True, (0, 220, 180))
        kleine_tekst = self.font.render(ondertitel, True, (255, 255, 255))

        self.screen.blit(grote_tekst, (SCREEN_W // 2 - grote_tekst.get_width() // 2, 230))
        self.screen.blit(kleine_tekst, (SCREEN_W // 2 - kleine_tekst.get_width() // 2, 300))


# Start het spel
if __name__ == "__main__":
    Game().run()
