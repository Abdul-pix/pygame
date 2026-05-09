"""
score_manager.py
Houdt de score bij tijdens het spel.
Hoe sneller de speler de finish bereikt, hoe meer punten hij krijgt.
"""

import time


class ScoreManager:
    """
    Dit beheert de score van de speler.
    De score begint op 1000 en daalt met 10 punten per seconde.
    Snel finishen = hoge score.
    """

    def __init__(self):
        """Sla het starttijdstip op zodat we de verstreken tijd kunnen berekenen."""
        self.start_tijd = time.time()

    def get_time(self):
        """
        Dit geeft terug hoeveel seconden er al gespeeld is.

        Returns:
            float: Verstreken tijd in seconden.
        """
        return time.time() - self.start_tijd

    def get_score(self):
        """
        Dit berekent de huidige score op basis van de verstreken tijd.
        De score kan niet onder 0 gaan.

        Returns:
            int: Huidige score tussen 0 en 1000.
        """
        score = 1000 - int(self.get_time() * 10)
        if score < 0:
            score = 0
        return score
