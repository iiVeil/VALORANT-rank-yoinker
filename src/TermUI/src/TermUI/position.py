
import math


class Position:
    """Uses a tuple to create a better positioning object
    """

    def __init__(self, x: int = 0, y: int = 0, xypair: tuple = None):
        if xypair:
            self.x, self.y = xypair
        else:
            self.x = x
            self.y = y

    def __add__(self, other):
        if isinstance(other, Position):
            return Position(self.x+other.x, self.y+other.y)
        return self

    def __sub__(self, other):
        if isinstance(other, Position):
            return Position(self.x-other.x, self.y-other.y)
        return self

    def half(self):
        """Returns a position equal to half of the current, on both y and x

        Returns:
            Position: The calculated position, rounded down
        """
        return Position(math.floor(self.x/2), math.floor(self.y/2))
