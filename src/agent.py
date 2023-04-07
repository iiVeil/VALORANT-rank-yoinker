from .TermUI.src.TermUI.region import Region
from .TermUI.src.TermUI.position import Position


class Agent(Region):

    def __init__(self, data: dict):
        super().__init__(title, position, size)
        self.framed = False

    def draw(self):

        super().draw(self)
