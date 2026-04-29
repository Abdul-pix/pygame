import random
from platform import Platform
from finish import Finish

def make_level(screen_h):
    platforms = []
    ground_y = screen_h - 70

    platforms.append(Platform(0, ground_y, 600, 70))

    x = 600
    y = ground_y

    for i in range(10):
        gap = random.randint(40, 70)
        w = random.randint(160, 230)
        y += random.randint(-30, 30)

        if y < ground_y - 90:
            y = ground_y - 90
        if y > ground_y:
            y = ground_y

        platforms.append(Platform(x + gap, y, w, 40))
        x += gap + w

    platforms.append(Platform(x + 100, ground_y, 500, 70))
    finish = Finish(x + 350, ground_y - 120)

    return platforms, finish