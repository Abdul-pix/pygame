import pygame
from game_object import GameObject

class Enemy(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 30, 40)
        self.vx = 0
        self.vy = 0
        self.speed = 2
        self.jump_force = -10
        self.on_ground = False
        self.jump_wait = 0

    def update(self, player, platforms, gravity, t):
        self.speed = 2 + t * 0.1
        if self.speed > 6:
            self.speed = 6

        if self.jump_wait > 0:
            self.jump_wait -= 1

        if player.x > self.x:
            self.vx = self.speed
        else:
            self.vx = -self.speed

        if self.on_ground and player.y < self.y - 40 and self.jump_wait == 0:
            self.vy = self.jump_force
            self.jump_wait = 30

        self.vy += gravity
        if self.vy > 12:
            self.vy = 12

        self.x += self.vx
        self.check_x_collision(platforms)

        self.y += self.vy
        self.on_ground = False
        self.check_y_collision(platforms)

        if self.y > 800:
            self.x = player.x - 200
            self.y = 100
            self.vy = 0

    def check_x_collision(self, platforms):
        for p in platforms:
            if self.collides_with(p):
                if self.vx > 0:
                    self.x = p.x - self.width
                else:
                    self.x = p.x + p.width

    def check_y_collision(self, platforms):
        for p in platforms:
            if self.collides_with(p):
                if self.vy > 0:
                    self.y = p.y - self.height
                    self.vy = 0
                    self.on_ground = True
                else:
                    self.y = p.y + p.height
                    self.vy = 0

    def draw(self, screen, cam_x):
        pygame.draw.rect(screen, (220, 40, 70),
                         (self.x - cam_x, self.y, self.width, self.height))