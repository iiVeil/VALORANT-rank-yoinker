from .TermUI.src.TermUI.region import Region
from .TermUI.src.TermUI.position import Position


class Agent(Region):

    def __init__(self, title: str, position: Position, size: Position, data: dict):
        super().__init__(title, position, size)
