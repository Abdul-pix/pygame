import pygame
from game_object import GameObject


class Laser:
    def __init__(self, x, y, vx):
        self.x = x
        self.y = y
        self.width = 35
        self.height = 6
        self.vx = vx

    def update(self):
        self.x += self.vx

    def draw(self, screen, cam_x):
        pygame.draw.rect(
            screen,
            (255, 50, 50),
            (self.x - cam_x, self.y, self.width, self.height)
        )


class Enemy(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 30, 40)

        self.vx = 0
        self.vy = 0

        self.speed = 2
        self.jump_force = -10
        self.on_ground = False
        self.jump_wait = 0

        self.lasers = []
        self.shoot_timer = 0

    def update(self, player, platforms, gravity, time_passed):
        self.set_speed(time_passed)
        self.follow_player(player)
        self.try_jump_over_gap(platforms)

        self.vy += gravity
        if self.vy > 12:
            self.vy = 12

        self.x += self.vx
        self.check_x_collision(platforms)

        self.y += self.vy
        self.on_ground = False
        self.check_y_collision(platforms)

        if self.y > 800:
            self.respawn(player)

        self.update_lasers(player)

    def set_speed(self, time_passed):
        self.speed = 2 + time_passed * 0.08
        if self.speed > 5:
            self.speed = 5

    def follow_player(self, player):
        if player.x > self.x:
            self.vx = self.speed
        else:
            self.vx = -self.speed

    def try_jump_over_gap(self, platforms):
        if self.jump_wait > 0:
            self.jump_wait -= 1

        if self.on_ground and self.jump_wait == 0:
            if not self.ground_in_front(platforms):
                self.vy = self.jump_force
                self.jump_wait = 30

    def ground_in_front(self, platforms):
        if self.vx > 0:
            test_x = self.x + self.width + 10
        else:
            test_x = self.x - 10

        test_y = self.y + self.height + 8

        for p in platforms:
            if p.x < test_x < p.x + p.width and p.y < test_y < p.y + p.height:
                return True

        return False

    def update_lasers(self, player):
        self.shoot_timer += 1

        if self.shoot_timer > 100:
            self.shoot_at_player(player)
            self.shoot_timer = 0

        for laser in self.lasers:
            laser.update()

        self.lasers = [laser for laser in self.lasers if -500 < laser.x < 5000]

    def shoot_at_player(self, player):
        laser_x = self.x + self.width // 2
        laser_y = self.y + self.height // 2

        if player.x > self.x:
            self.lasers.append(Laser(laser_x, laser_y, 7))
        else:
            self.lasers.append(Laser(laser_x, laser_y, -7))

    def respawn(self, player):
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

                if self.on_ground and self.jump_wait == 0:
                    self.vy = self.jump_force
                    self.jump_wait = 30

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
        pygame.draw.rect(
            screen,
            (220, 40, 70),
            (self.x - cam_x, self.y, self.width, self.height)
        )

        for laser in self.lasers:
            laser.draw(screen, cam_x)
