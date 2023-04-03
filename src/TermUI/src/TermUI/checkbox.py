import curses
from enum import Enum
from .position import Position
from .element import Element
from .button import ButtonCharacters


class Checkbox(Element):

    def __init__(self, checked: bool, position: Position):
        super().__init__(position)
        self.checked = checked
        self.colors = [161, 156]
        self.size = Position(2, 1)
        self.pack = {
            "right": Position(
                self.size.x+position.x+1, position.y),
            "down": Position(position.x, position.y+self.size.y+1),
            "up": Position(position.x, position.y-1)
        }

    def draw(self):

        if self.region is None or self.hidden:
            return
        self.color = self.colors[self.checked]
        # * Initialize the corners of the checkbox
        self.addstr(self.start.y, self.start.x,
                    ButtonCharacters.TOPLEFT.value if not self.checked else FilledBox.TOP_LEFT.value, curses.color_pair(self.color))
        self.addstr(self.start.y, self.end.x,
                    ButtonCharacters.TOPRIGHT.value if not self.checked else FilledBox.TOP_RIGHT.value, curses.color_pair(self.color))
        self.addstr(self.end.y, self.start.x,
                    ButtonCharacters.BOTTOMLEFT.value if not self.checked else FilledBox.BOTTOM_LEFT.value, curses.color_pair(self.color))
        self.addstr(self.end.y, self.end.x,
                    ButtonCharacters.BOTTOMRIGHT.value if not self.checked else FilledBox.BOTTOM_RIGHT.value, curses.color_pair(self.color))

        # * Vertical lines
        for iy in range(self.end.y-self.start.y):
            if 0 < iy < self.end.y:
                self.addstr(iy+self.start.y, self.start.x,
                            ButtonCharacters.VERTICAL.value if not self.checked else FilledBox.VERTICAL_LEFT.value, curses.color_pair(self.color))
                self.addstr(
                    iy+self.start.y, self.end.x,
                    ButtonCharacters.VERTICAL.value if not self.checked else FilledBox.VERTICAL_RIGHT.value, curses.color_pair(self.color))

        # * Horizontal lines
        for ix in range(self.end.x-self.start.x):
            if 0 < ix < self.end.x:
                self.addstr(self.start.y, ix+self.start.x,
                            ButtonCharacters.HORIZONTAL.value if not self.checked else FilledBox.HORIZONTAL_TOP.value, curses.color_pair(self.color))
                self.addstr(
                    self.end.y, ix+self.start.x,
                    ButtonCharacters.HORIZONTAL.value if not self.checked else FilledBox.HORIZONTAL_BOTTOM.value, curses.color_pair(self.color))

    def click(self):
        if self.region is None or self.hidden:
            return
        self.checked = not self.checked
        if self.callback is not None:
            self.callback(self)
        self.region.ui.draw()


class FilledBox(Enum):
    BOTTOM_RIGHT = "▘"
    BOTTOM_LEFT = "▝"
    TOP_LEFT = "▗"
    TOP_RIGHT = "▖"
    VERTICAL_LEFT = "▐"
    VERTICAL_RIGHT = "▌"
    HORIZONTAL_TOP = "▄"
    HORIZONTAL_BOTTOM = "▀"
