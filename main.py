import pygame
import sys

from player import Player
from enemy import Enemy
from level_generator import make_level
from score_manager import ScoreManager

SCREEN_W = 900
SCREEN_H = 600
FPS = 60
GRAVITY = 0.45

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("RUN.EXE")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(None, 30)
        self.big_font = pygame.font.SysFont(None, 60)

        self.state = "menu"
        self.reset()

    def reset(self):
        self.platforms, self.finish = make_level(SCREEN_H)
        ground_y = SCREEN_H - 70

        self.player = Player(120, ground_y - 40)
        self.enemy = Enemy(30, ground_y - 40)

        self.score = ScoreManager()
        self.camera_x = 0
        self.final_score = 0

    def run(self):
        while True:
            self.handle_events()

            if self.state == "playing":
                self.update()

            self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if e.key == pygame.K_RETURN:
                    if self.state in ("menu", "dead", "won"):
                        self.reset()
                        self.state = "playing"

    def update(self):
        t = self.score.get_time()

        self.player.update(self.platforms, GRAVITY)
        self.enemy.update(self.player, self.platforms, GRAVITY, t)

        self.camera_x = self.player.x - 300
        if self.camera_x < 0:
            self.camera_x = 0

        if self.player.y > SCREEN_H + 100:
            self.state = "dead"

        if self.player.collides_with(self.enemy):
            self.state = "dead"

        if self.player.collides_with(self.finish):
            self.final_score = self.score.get_score()
            self.state = "won"

    def draw(self):
        self.screen.fill((20, 20, 40))

        for p in self.platforms:
            p.draw(self.screen, self.camera_x)

        self.finish.draw(self.screen, self.camera_x)
        self.enemy.draw(self.screen, self.camera_x)
        self.player.draw(self.screen, self.camera_x)

        if self.state == "playing":
            self.draw_hud()

        if self.state == "menu":
            self.draw_msg("RUN.EXE", "Druk ENTER om te starten")
        elif self.state == "dead":
            self.draw_msg("GAME OVER", "ENTER om opnieuw te spelen")
        elif self.state == "won":
            self.draw_msg("GEWONNEN", "Score: " + str(self.final_score))

        pygame.display.flip()

    def draw_hud(self):
        s = self.score.get_score()
        t = int(self.score.get_time())
        txt = self.font.render(f"Score: {s}   Tijd: {t}", True, (255, 255, 255))
        self.screen.blit(txt, (20, 20))

    def draw_msg(self, title, sub):
        t = self.big_font.render(title, True, (0, 220, 180))
        s = self.font.render(sub, True, (255, 255, 255))

        self.screen.blit(t, (SCREEN_W//2 - t.get_width()//2, 230))
        self.screen.blit(s, (SCREEN_W//2 - s.get_width()//2, 300))


if __name__ == "__main__":
    Game().run()