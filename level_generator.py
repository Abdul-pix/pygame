"""
level_generator.py

Genereert een willekeurig level met platforms,
powerups, een turret en een finishlijn.

Smart Design:
Het level wordt willekeurig opgebouwd binnen vaste grenzen,
zodat er variatie is zonder dat het level onredelijk wordt.
"""

import random

from platforms import Platform
from finish import Finish
from powerups import PowerUp
from turret_enemy import TurretEnemy


def make_level(screen_h):
    """
    Maak een willekeurig level aan.

    Returns:
        tuple:
            - platform_list
            - finish
            - powerup_list
            - turret_list
    """

    platform_list = []
    powerup_list = []
    turret_list = []

    ground_y = screen_h - 70

    # Breed startplatform.
    platform_list.append(
        Platform(0, ground_y, 600, 70)
    )

    x = 600
    y = ground_y

    # Maak 10 willekeurige platforms.
    for i in range(10):

        gap = random.randint(40, 70)

        soort = random.choice(
            ["normaal", "smal", "laag"]
        )

        if soort == "smal":
            width = random.randint(80, 120)
            y += random.randint(-60, -20)

        elif soort == "laag":
            width = random.randint(200, 280)
            y = ground_y

        else:
            width = random.randint(160, 230)
            y += random.randint(-30, 30)

        # Hoogte begrenzen zodat het level speelbaar blijft.
        if y < ground_y - 150:
            y = ground_y - 150

        if y > ground_y:
            y = ground_y

        # Het platform met de turret moet breed genoeg zijn.
        if i == 5 and width < 180:
            width = 180

        platform = Platform(
            x + gap,
            y,
            width,
            40
        )

        platform_list.append(platform)

        # Powerups op platform 4 en 8.
        if i == 3 or i == 7:
            powerup_list.append(
                PowerUp(
                    platform.x + width // 2,
                    platform.y - 35
                )
            )

        # Eén turret op platform 6.
        if i == 5:

            turret_x = (
                platform.x
                + platform.width
                - 45
            )

            turret_y = (
                platform.y
                - 40
            )

            turret_list.append(
                TurretEnemy(
                    turret_x,
                    turret_y
                )
            )

        x += gap + width

    # Eindplatform.
    platform_list.append(
        Platform(
            x + 100,
            ground_y,
            500,
            70
        )
    )

    # Finish.
    finish = Finish(
        x + 350,
        ground_y - 120
    )

    return (
        platform_list,
        finish,
        powerup_list,
        turret_list
    )
