"""
level_generator.py
Genereert een willekeurig level met platforms, powerups en een finishlijn.

Smart Design: elk level is anders door gebruik van random, wat het spel
afwisselender maakt en de herhaalbaarheid vergroot.
"""

import random
from platforms import Platform
from finish import Finish
from powerups import PowerUp


def make_level(screen_h):
    """
    Maak een willekeurig level aan.

    Het level begint met een breed startplatform, gevolgd door 10 willekeurige
    platforms. Er zijn 3 soorten platforms:
        - Normaal: gemiddelde breedte en hoogte.
        - Smal: smaller en hoger, moeilijker om op te landen.
        - Laag: breed maar dicht bij de grond, makkelijk maar gevaarlijk
                omdat de vijand er ook snel op kan.
    Op platform 4 en 8 staat een powerup.
    Het level eindigt met een breed eindplatform en een finishlijn.

    Args:
        screen_h (int): Hoogte van het scherm in pixels,
                        wordt gebruikt om de grondpositie te berekenen.

    Returns:
        tuple:
            - platform_list (list): Lijst van alle Platform-objecten.
            - finish (Finish): De finishlijn die de speler moet bereiken.
            - powerup_list (list): Lijst van alle PowerUp-objecten.
    """
    platform_list = []
    powerup_list = []
    ground_y = screen_h - 70

    # Startplatform: breed zodat de speler gemakkelijk kan beginnen
    platform_list.append(Platform(0, ground_y, 600, 70))

    x = 600
    y = ground_y

    for i in range(10):
        gap = random.randint(40, 70)

        # Kies willekeurig een platformtype
        soort = random.choice(["normaal", "smal", "laag"])

        if soort == "smal":
            # Smal en hoog: uitdagend om op te springen
            width = random.randint(80, 120)
            y += random.randint(-60, -20)
        elif soort == "laag":
            # Breed maar dicht bij de grond
            width = random.randint(200, 280)
            y = ground_y
        else:
            # Normaal platform
            width = random.randint(160, 230)
            y += random.randint(-30, 30)

        # Zorg dat het platform niet te hoog of te laag is
        if y < ground_y - 150:
            y = ground_y - 150
        if y > ground_y:
            y = ground_y

        platform = Platform(x + gap, y, width, 40)
        platform_list.append(platform)

        # Powerup op platform 4 en 8 (index 3 en 7)
        if i == 3 or i == 7:
            powerup_list.append(PowerUp(platform.x + width // 2, platform.y - 35))

        x += gap + width

    # Eindplatform en finishlijn
    platform_list.append(Platform(x + 100, ground_y, 500, 70))
    finish = Finish(x + 350, ground_y - 120)

    return platform_list, finish, powerup_list
