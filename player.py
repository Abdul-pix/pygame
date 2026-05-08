import pygame
from game_object import GameObject


class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 30, 40)
        self.vx = 0
        self.vy = 0
        self.speed = 4
        self.jump_force = -10
        self.on_ground = False
        self.shield = False

    def update(self, platforms, gravity):
        keys = pygame.key.get_pressed()

        self.vx = 0
        if keys[pygame.K_LEFT]:
            self.vx = -self.speed
        if keys[pygame.K_RIGHT]:
            self.vx = self.speed

        if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.on_ground:
            self.vy = self.jump_force
            self.on_ground = False

        self.vy += gravity
        if self.vy > 12:
            self.vy = 12

        self.x += self.vx
        self.check_x_collision(platforms)

        self.y += self.vy
        self.on_ground = False
        self.check_y_collision(platforms)

    def use_shield(self):
        if self.shield:
            self.shield = False
            return True
        return False

    def check_x_collision(self, platforms):
        for p in platforms:
            if self.collides_with(p):
                if self.vx > 0:
                    self.x = p.x - self.width
                elif self.vx < 0:
                    self.x = p.x + p.width

    def check_y_collision(self, platforms):
        for p in platforms:
            if self.collides_with(p):
                if self.vy > 0:
                    self.y = p.y - self.height
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.y = p.y + p.height
                    self.vy = 0

    def draw(self, screen, cam_x):
        if self.shield:
            color = (0, 150, 255)
        else:
            color = (0, 200, 180)

        pygame.draw.rect(
            screen,
            color,
            (self.x - cam_x, self.y, self.width, self.height)
        )
