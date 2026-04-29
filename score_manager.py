import time

class ScoreManager:
    def __init__(self):
        self.start = time.time()

    def get_time(self):
        return time.time() - self.start

    def get_score(self):
        s = 1000 - int(self.get_time() * 10)
        if s < 0:
            s = 0
        return s