import curses
from enum import Enum
from .position import Position
from .element import Element


class Button(Element):
    def __init__(self, text: str, position: Position, callback):
        super().__init__(position)
        self.text = text
        self.framed = True
        self.clicked = False
        self.highlight = "><"
        self.size = Position(len(self.text)+2, 1) + Position(1, 1)
        self.pack = {
            "right": Position(
                self.size.x+position.x+1, position.y),
            "down": Position(position.x, position.y+self.size.y+1),
            "up": Position(position.x, position.y-1)
        }
        self.occupies = None
        self.callback = callback

    def set_text(self, text: str):
        """Set the text of the button and resize it, this will not redraw the button.

        This will do nothing if you do not add it to a region using Region().add_element()..

        Args:
            text (str): the buttons new text
        """
        if self.region is None:
            return
        self.text = text
        self.size = Position(len(self.text)+2, 1) + Position(1, 1)
        self.end = self.start + self.size

    def draw(self) -> None:
        """Draw the button to the screen

        This will do nothing if you do not add it to a region using Region().add_element()..
        """
        if self.region is None or self.hidden:
            return
        # * Initialize the corners of the button
        self.addstr(self.start.y, self.start.x,
                    ButtonCharacters.TOPLEFT.value, curses.color_pair(self.color))
        self.addstr(self.start.y, self.end.x,
                    ButtonCharacters.TOPRIGHT.value, curses.color_pair(self.color))
        self.addstr(self.end.y, self.start.x,
                    ButtonCharacters.BOTTOMLEFT.value, curses.color_pair(self.color))
        self.addstr(self.end.y, self.end.x,
                    ButtonCharacters.BOTTOMRIGHT.value, curses.color_pair(self.color))

        # * Vertical lines
        for iy in range(self.end.y-self.start.y):
            if 0 < iy < self.end.y:
                self.addstr(iy+self.start.y, self.start.x,
                            ButtonCharacters.VERTICAL.value, curses.color_pair(self.color))
                self.addstr(
                    iy+self.start.y, self.end.x,
                    ButtonCharacters.VERTICAL.value, curses.color_pair(self.color))

        # * Horizontal lines
        for ix in range(self.end.x-self.start.x):
            if 0 < ix < self.end.x:
                char = ButtonCharacters.HORIZONTAL.value
                self.addstr(self.start.y, ix+self.start.x,
                            char, curses.color_pair(self.color))
                self.addstr(
                    self.end.y, ix+self.start.x,
                    ButtonCharacters.HORIZONTAL.value, curses.color_pair(self.color))

        if self.text is not "":
            # * Draw button text
            self.addstr(
                self.start.y+1, self.start.x+2, self.text, curses.color_pair(self.color) + curses.A_UNDERLINE)

            # * Make it look clickable?
            self.addstr(self.start.y+1,
                        self.start.x+1, self.highlight[0], curses.color_pair(self.color))
            self.addstr(self.start.y+1,
                        self.end.x-1, self.highlight[1], curses.color_pair(self.color))

    def click(self):
        """What to do when a button is clicked

        This will do nothing if you do not add it to a region using Region().add_element()..
        """
        if self.region is None:
            return
        self.clicked = not self.clicked
        self.callback(self)


class ButtonCharacters(Enum):
    TOPLEFT = "┌"
    TOPRIGHT = "┐"
    BOTTOMLEFT = "└"
    BOTTOMRIGHT = "┘"
    HORIZONTAL = "─"
    VERTICAL = "│"
