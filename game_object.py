from abc import ABC

class GameObject(ABC):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h

    def collides_with(self, other):
        left1 = self.x
        right1 = self.x + self.width
        top1 = self.y
        bottom1 = self.y + self.height

        left2 = other.x
        right2 = other.x + other.width
        top2 = other.y
        bottom2 = other.y + other.height

        if left1 < right2 and right1 > left2 and top1 < bottom2 and bottom1 > top2:
            return True
        else:
            return False
