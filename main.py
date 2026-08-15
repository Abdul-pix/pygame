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

        self.screen = pygame.display.set_mode(
            (SCREEN_W, SCREEN_H)
        )

        pygame.display.set_caption("RUN.EXE")

        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(None, 30)
        self.big_font = pygame.font.SysFont(None, 60)

        self.state = "menu"

        self.reset()

    def reset(self):
        """
        Reset het spel:
        genereer een nieuw level en maak alle objecten opnieuw aan.
        """

        (
            self.platforms,
            self.finish,
            self.powerups,
            self.turrets
        ) = make_level(SCREEN_H)

        ground_y = SCREEN_H - 70

        self.player = Player(
            120,
            ground_y - 40
        )

        self.enemy = Enemy(
            30,
            ground_y - 40
        )

        self.score = ScoreManager()

        self.camera_x = 0
        self.final_score = 0

    def run(self):
        """
        Start de game loop.
        """

        while True:
            self.handle_events()

            if self.state == "playing":
                self.update()

            self.draw()

            self.clock.tick(FPS)

    def handle_events(self):
        """
        Verwerk pygame-events zoals
        afsluiten, starten en herstarten.
        """

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_RETURN:

                    if self.state in (
                        "menu",
                        "dead",
                        "won"
                    ):
                        self.reset()
                        self.state = "playing"

    def update(self):
        """
        Update alle objecten
        en controleer win/verlies.
        """

        t = self.score.get_time()

        # -------------------------
        # PLAYER
        # -------------------------

        self.player.update(
            self.platforms,
            GRAVITY
        )

        # -------------------------
        # MOVING ENEMY
        # -------------------------

        self.enemy.update(
            self.player,
            self.platforms,
            GRAVITY,
            t
        )

        # -------------------------
        # TURRETS
        # -------------------------

        for turret in self.turrets:
            turret.update(self.player)

        # -------------------------
        # CAMERA
        # -------------------------

        self.camera_x = self.player.x - 300

        if self.camera_x < 0:
            self.camera_x = 0

        # -------------------------
        # POWERUPS
        # -------------------------

        for powerup in self.powerups:

            if (
                powerup.active
                and self.player.collides_with(powerup)
            ):
                self.player.shield = True
                powerup.active = False

        # -------------------------
        # SPELER VALT
        # -------------------------

        if self.player.y > SCREEN_H + 100:
            self.state = "dead"
            return

        # -------------------------
        # MOVING ENEMY COLLISION
        # -------------------------

        if self.player.collides_with(self.enemy):

            if not self.player.use_shield():
                self.state = "dead"
                return

        # -------------------------
        # TURRET COLLISION
        # -------------------------

        for turret in self.turrets:

            if self.player.collides_with(turret):

                if not self.player.use_shield():
                    self.state = "dead"
                    return

        # -------------------------
        # LASERS VAN MOVING ENEMY
        # -------------------------

        for laser in self.enemy.lasers[:]:

            if self.player.collides_with(laser):

                if self.player.use_shield():
                    self.enemy.lasers.remove(laser)

                else:
                    self.state = "dead"
                    return

        # -------------------------
        # LASERS VAN TURRETS
        # -------------------------

        for turret in self.turrets:

            for laser in turret.lasers[:]:

                if self.player.collides_with(laser):

                    if self.player.use_shield():
                        turret.lasers.remove(laser)

                    else:
                        self.state = "dead"
                        return

        # -------------------------
        # FINISH
        # -------------------------

        if self.player.collides_with(self.finish):

            self.final_score = self.score.get_score()
            self.state = "won"

    def draw(self):
        """
        Teken alle objecten en
        daarna HUD/menu/win-verliesscherm.
        """

        self.screen.fill((20, 20, 40))

        # Platforms
        for platform in self.platforms:

            platform.draw(
                self.screen,
                self.camera_x
            )

        # Powerups
        for powerup in self.powerups:

            powerup.draw(
                self.screen,
                self.camera_x
            )

        # Finish
        self.finish.draw(
            self.screen,
            self.camera_x
        )

        # Bewegende enemy + lasers
        self.enemy.draw(
            self.screen,
            self.camera_x
        )

        # Turrets + lasers
        for turret in self.turrets:

            turret.draw(
                self.screen,
                self.camera_x
            )

        # Player
        self.player.draw(
            self.screen,
            self.camera_x
        )

        # HUD / menu / game-over / win
        if self.state == "playing":

            self.draw_hud()

        elif self.state == "menu":

            self.draw_msg(
                "RUN.EXE",
                "Druk ENTER om te starten"
            )

        elif self.state == "dead":

            self.draw_msg(
                "GAME OVER",
                "ENTER om opnieuw te spelen"
            )

        elif self.state == "won":

            self.draw_msg(
                "GEWONNEN!",
                "Score: " + str(self.final_score)
            )

        pygame.display.flip()

    def draw_hud(self):
        """
        Teken score, tijd en schildstatus.
        """

        score = self.score.get_score()
        tijd = int(self.score.get_time())

        schild_tekst = (
            "   Schild: AAN"
            if self.player.shield
            else ""
        )

        tekst = self.font.render(
            f"Score: {score}   Tijd: {tijd}{schild_tekst}",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            tekst,
            (20, 20)
        )

    def draw_msg(self, title, ondertitel):
        """
        Teken menu-, game-over-
        of wintekst.
        """

        grote_tekst = self.big_font.render(
            title,
            True,
            (0, 220, 180)
        )

        kleine_tekst = self.font.render(
            ondertitel,
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            grote_tekst,
            (
                SCREEN_W // 2
                - grote_tekst.get_width() // 2,
                230
            )
        )

        self.screen.blit(
            kleine_tekst,
            (
                SCREEN_W // 2
                - kleine_tekst.get_width() // 2,
                300
            )
        )


# Start het spel
if __name__ == "__main__":
    Game().run()
